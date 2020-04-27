from __future__ import annotations
from typing import Union
from luxor.core.objects import Object
from luxor.core.events import Event
from luxor.core.context import Context
from varname import varname


class Var:
    pass


class Int:
    def __init__(self, value: int = 0, **kwargs) -> None:
        self.name: str = kwargs.get('name')
        if self.name is None:
            self.name = varname()
        self.ctx: Context = kwargs['context']
        self.autoevent: bool = kwargs.get('autoevent', True)
        self.autokey: bool = kwargs.get('autokey', True)
        self.obj = self.ctx.request_object()
        self.event_prefix = 'int.' + self.name + '.'
        self.place(value)
        if self.autoevent:
            self.trigger_new(value)

    def peek(self) -> int:
        return self.obj.peek('value')

    def place(self, value: Numeric) -> (int, int):
        if type(value) == Int:
            new = value.get()
        else:
            new = int(value)
        old = self.peek()
        self.obj['value'] = new
        return old, new

    def get(self) -> int:
        value = self.obj['value']
        self.trigger_get(value)
        return value

    def set(self, value: Numeric) -> None:
        old, new = self.place(value)
        if self.autoevent:
            if type(value) == float:
                self.trigger_cast_other(value, new)
            self.trigger_set(old, new)

    @property
    def value(self) -> int:
        pass

    @value.getter
    def value(self) -> int:
        return self.get()

    @value.setter
    def value(self, value: Numeric) -> None:
        self.set(value)

    def trigger_new(self, value) -> None:
        self.ctx.push_event(Event(self.event_prefix + 'new',
                            source=self.obj, meta={
                                'new.value': value
                            }))

    def trigger_get(self, value) -> None:
        self.ctx.push_event(Event(self.event_prefix + 'get',
                            source=self.obj, meta={
                                'get.value': value
                            }))

    def trigger_set(self, old: int, new: int) -> None:
        self.ctx.push_event(Event(self.event_prefix + 'set',
                            source=self.obj, meta={
                                'set.value.old': old,
                                'set.value.new': new
                            }))

    def trigger_cast_other(self, old: float, new: int) -> None:
        self.ctx.push_event(Event(self.event_prefix + 'other.cast',
                            source=self.obj, meta={
                                'cast.value.type': type(old),
                                'cast.value.old': old,
                                'cast.value.new': new
                            }))


Numeric = Union[int, float, Int]
