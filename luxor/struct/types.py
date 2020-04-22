from __future__ import annotations
from copy import copy
from typing import Union
from luxor.core.objects import Object
from luxor.core.events import Event
from luxor.core.context import Context
from varname import varname


class Var:
    pass


class Int:
    def __init__(self, value: int = 0, **kwargs) -> None:
        if 'name' in kwargs:
            self.name: str = kwargs['name']
        else:
            self.name: str = varname()
        self.ctx: Context = kwargs['context']
        self.obj = self.ctx.request_object()
        self.obj.value = copy(value)
        self.__value = copy(value)
        self.event_prefix = 'Int.' + self.name + '.'

    def set(self, value: Union[int, Int]) -> None:
        if type(value) == Int:
            value = value.value

        def set_value(event: Event):
            self.obj.value = copy(value)

        self.ctx.push_event(Event([self.event_prefix + 'set'],
                            set_value, self.obj, {
            'set.value.old': copy(self.__value),
            'set.value.new': copy(value)
        }))
        self.__value = copy(value)

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value: Union[int, Int]) -> None:
        self.set(value)

    @value.getter
    def value(self) -> int:
        self.ctx.push_event(Event([self.event_prefix + 'get'],
                            None, self.obj, {'get.value': copy(self.__value)}))
        return self.__value
