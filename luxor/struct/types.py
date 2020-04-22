from copy import copy
from typing import Union
from luxor.core.objects import Object
from luxor.core.events import Event
from luxor.core.context import Context


class Var:
    pass


class Int:
    def __init__(self, value: int, name: str, ctx: Context) -> None:
        self.event_prefix = 'Int.' + name + '.'
        self.name = name
        self.ctx = ctx
        self.obj = ctx.request_object()
        self.obj.value = value
        self.__value = value

    def set(self, value: int) -> None:
        def set_value(ctx: Context):
            self.obj.value = copy(value)

        self.ctx.push_event(Event([self.event_prefix + 'set'],
                            set_value, self, {
            'set.value.old': copy(self.__value),
            'set.value.new': copy(value)
        }))
        self.__value = value
