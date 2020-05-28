from typing import List, Any, Union, Type, Iterator
from threading import RLock
from luxor.core.events import Event, match, EventWrapper, EventInterceptor
from luxor.core.objects import Object
from luxor.core.treedict import TreeDict


class Context:
    def __init__(self) -> None:
        self.__lock: RLock = RLock()
        self.__events: List[Event] = []
        self.__interceptors: List[EventInterceptor] = []
        self.__closed = False

        self.__objects: List[Object] = []
        self.__n_obj: int = 0
        self.__n_inter: int = 0

        self.__properties: TreeDict = TreeDict()

    def push_event(self, event: Event) -> None:
        if self.closed:
            return
        self.__lock.acquire()
        wrapper = self.__intercept(event)
        if not wrapper.canceled:
            for e in wrapper.prev_chain:
                self.push_event(e)
            if wrapper.event.action is not None:
                wrapper.event.action()
            self.__events.append(wrapper.event)
            for e in wrapper.next_chain:
                self.push_event(e)
        self.__lock.release()

    def pop_event(self) -> Event:
        if not self.closed:
            raise Exception('cannot pop events from open context.')
        event = self.__events.pop(0)
        if event.action is not None:
            event.action()
        return event

    @property
    def closed(self) -> bool:
        return self.__closed

    def close(self) -> None:
        self.__closed = True

    @property
    def events_count(self) -> int:
        return len(self.__events)

    @property
    def has_events(self) -> bool:
        return self.events_count > 0

    def event(self, idx: int) -> Event:
        return self.__events[idx] if idx < self.events_count else None

    @property
    def events(self) -> Iterator[Event]:
        for e in self.__events:
            yield e

    def add_object(self, obj: Object) -> None:
        self.__lock.acquire()
        obj.ctx = self
        obj.uid = self.__n_obj
        self.__objects.append(obj)
        self.__n_obj += 1
        obj._trigger_new()
        self.__lock.release()

    def peek_object(self, uid: int) -> Object:
        return next((obj for obj in self.__objects
                    if obj.uid == uid), None)

    def request_object(self, **kwargs) -> Object:
        obj = Object(kwargs.get('parent'))
        self.add_object(obj)
        return obj

    def reset_objects(self) -> None:
        for obj in self.__objects:
            obj.snew()

    def add_interceptor(self, inter: Union[EventInterceptor, Type]):
        self.__lock.acquire()
        if not isinstance(inter, EventInterceptor):
            inter = inter()
        inter.uid = self.__n_inter
        self.__n_inter += 1
        self.__interceptors.append(inter)
        self.__lock.release()

    def remove_interceptor(self, inter: EventInterceptor) -> None:
        self.__interceptors.remove(inter)

    def __getitem__(self, name: str) -> Any:
        return self.get(name)

    def __setitem__(self, name: str, value: Any):
        self.set(name, value)

    def get(self, name: str) -> Any:
        self.__lock.acquire()
        return self.__properties[name]
        self.__lock.release()

    def set(self, name: str, value: Any) -> None:
        self.__lock.acquire()
        self.__properties[name] = value
        self.__lock.release()

    def log(self, **kwargs):
        print(*[str(e) for e in self.__events
              if kwargs.get('show_operations', False)
              or not match(e, 'operation.*')], sep='\n')

    def __intercept(self, event: Event) -> EventWrapper:
        wrapper = EventWrapper(self, event)
        for i in self.__interceptors:
            i.intercept(wrapper)
            if wrapper.canceled:
                break
        return wrapper
