from typing import List
from copy import copy
from .events import Event, EventInterceptor, match
from .objects import Object


class Context:
    def __init__(self) -> None:
        # TODO: TreeDict
        self.__stack: List[str] = []
        self.__events: List[Event] = []
        self.__interceptors: List[EventInterceptor] = []

        self.__objects: List[Object] = []
        self.__uid_counter = 0

    def push_event(self, event: Event) -> None:
        event.ctx = self
        event.stack = tuple(self.__stack)
        if event.action is not None:
            event.action(event)
        self.__events.append(event)

    def pop_event(self) -> Event:
        event = self.__events.pop(0)
        if event.action is not None and match(event, 'operation.*'):
            event.action(event)
        return event

    @property
    def events_count(self) -> int:
        return len(self.__events)

    @property
    def has_events(self) -> bool:
        return self.events_count > 0

    def peek_event(self, index: int) -> Event:
        return self.__events[index] if index < self.events_count else None

    def add_object(self, obj: Object) -> None:
        obj.ctx = self
        obj.uid = self.__uid_counter
        self.__objects.append(obj)
        self.__uid_counter += 1
        obj._trigger_new()

    def peek_object(self, uid: int) -> Object:
        return self.__objects[uid] if uid < len(self.__objects) else None

    def request_object(self, **kwargs) -> Object:
        obj = Object(kwargs.get('parent'))
        self.add_object(obj)
        return obj

    def log(self, **kwargs):
        print(*[str(e) for e in self.__events
              if kwargs.get('show_operations', False)
              or not match(e, 'operation.*')], sep='\n')

    def __run_pre_interceptors(self, event: Event) -> None:
        return event
