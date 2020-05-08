from __future__ import annotations
from typing import Union
from luxor.core.objects import Object
from luxor.core.events import Event
from luxor.controllers.expressions import Var


class Int(Var):
    def __init__(self, value: Numeric = 0, **kwargs) -> None:
        super(Int, self).__init__(**kwargs)
        self.event_prefix = self.name + '.int.'
        self.obj = self.ctx.request_object()
        self.obj['class'] = ('int')
        self.sset(value)
        self.auto_trigger('new', value)

    def sget(self) -> int:
        return self.obj.sget('value')

    def sset(self, value: Numeric) -> (int, int):
        if type(value) == Int:
            new = value.get()
        else:
            new = int(value)
        old = self.sget()
        self.obj['value'] = new
        return old, new

    def get(self) -> int:
        value = self.obj['value']
        self.auto_trigger('get', value)
        return value

    def set(self, value: Numeric) -> None:
        old, new = self.sset(value)
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
