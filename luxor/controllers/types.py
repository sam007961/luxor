from __future__ import annotations
from typing import Union
from luxor.core.objects import Object
from luxor.core.events import Event
from luxor.core.context import Context
from varname import varname


class Var:
    def __init__(self, **kwargs):
        self.name: str = kwargs.get('name')
        if self.name is None:
            self.name = varname(2)
        self.ctx: Context = kwargs['context']
        self.autotrigger: bool = kwargs.get('autotrigger', True)

    def auto_trigger(self, name: str, *args) -> None:
        if self.auto_trigger:
            getattr(self, 'trigger_' + name)(*args)


class Int(Var):
    def __init__(self, value: Numeric = 0, **kwargs) -> None:
        super(Int, self).__init__(**kwargs)
        self.event_prefix = self.name + '.int.'
        self.obj = self.ctx.request_object()
        self.obj['class'] = ('int')
        self.place(value)
        self.auto_trigger('new', value)

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
        self.auto_trigger('get', value)
        return value

    def set(self, value: Numeric) -> None:
        old, new = self.place(value)
        if type(value) == float:
            self.auto_trigger('cast_literal', value, new)
        self.auto_trigger('set', old, new)

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

    def trigger_cast_literal(self, old: float, new: int) -> None:
        self.ctx.push_event(Event(self.event_prefix + 'literal.cast',
                            source=self.obj, meta={
                                'cast.value.type': type(old),
                                'cast.value.old': old,
                                'cast.value.new': new
                            }))


Numeric = Union[int, float, Int]
