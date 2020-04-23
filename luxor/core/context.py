from typing import List
from copy import copy
from .events import Event, EventHandler, EventInterceptor
from .objects import Object


class Context:
    def __init__(self) -> None:
        # TODO: TreeDict
        self.__stack = List[str]
        self.__events: List[Event] = []
        self.__event_handlers: List = []
        self.__event_interceptors: List = []

        self.__objects: List[Object] = []
        self.__uid_counter = 0

    def push_event(self, event: Event) -> None:
        event.ctx = self
        event.stack = copy(self.__stack)
        event = self.__run_interceptors(event)
        if event is None:
            return
        self.__events.append(event)
        self.__run_handlers(copy(event))

    def pop_event(self) -> Event:
        event = self.__events.pop(0)
        if event.action is not None:
            event.action(event)
        return event

    def has_events(self) -> bool:
        return len(self.__events) > 0

    def add_object(self, obj: Object) -> None:
        obj.ctx = self
        obj.uid = self.__uid_counter
        obj._trigger_new()
        self.__objects.append(obj)
        self.__uid_counter += 1

    def get_object(self, uid: int) -> Object:
        return self.__objects[uid] if uid < len(self.__objects) else None

    def request_object(self) -> Object:
        obj = Object()
        self.add_object(obj)
        return obj

    def log(self):
        print(*[str(e) for e in self.__events], sep='\n')

    def __run_interceptors(self, event: Event) -> None:
        return event

    def __run_handlers(self, event: Event) -> None:
        pass
