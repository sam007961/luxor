from typing import List
from copy import copy
from .events import Event, EventHandler, EventInterceptor
from .objects import Object


class Context:
    def __init__(self) -> None:
        self.__events: List[Event] = []
        self.__event_handlers: List = []
        self.__event_interceptors: List = []

        self.__objects: List[Object] = []

    def push_event(self, event: Event) -> None:
        event = self.__run_interceptors(copy(event))
        if event is None:
            return
        event.ctx = self
        self.__events.append(event)
        self.__run_handlers(copy(event))

    def pop_event(self) -> Event:
        event = self.__events.pop(0)
        if event.action is not None:
            event.action(self)
        return event

    def add_object(self, obj: Object) -> None:
        obj.ctx = self
        self.__objects.append(obj)

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
