from __future__ import annotations
from typing import Union
from luxor.core.events import Event
from luxor.controllers.expressions import Var


class Int(Var):
    def __init__(self, value: Number = 0, **kwargs) -> None:
        super(Int, self).__init__(**kwargs)
        self.event_prefix = self.name + '.int.'
        self.__obj = self.ctx.request_object()
        self.__obj['class'] = frozenset({'int', self.callstack + '.int'})
        self.__obj['label'] = self.name
        self.sset(value)
        self.trigger('new', value)

    def sget(self) -> int:
        return self.__obj.sget('value')

    def sset(self, value: Number) -> (int, int):
        if type(value) == Int:
            new = value.get()
        else:
            new = int(value)
        old = self.sget()
        self.__obj['value'] = new
        return old, new

    def get(self) -> int:
        value = self.__obj['value']
        self.trigger('get', value)
        return value

    def set(self, value: Number) -> None:
        old, new = self.sset(value)
        if type(value) == float:
            self.trigger('cast_literal', value, new)
        self.trigger('set', old, new)

    @property
    def value(self) -> int:
        pass

    @value.getter
    def value(self) -> int:
        return self.get()

    @value.setter
    def value(self, value: Number) -> None:
        self.set(value)

    def trigger_new(self, value) -> None:
        return Event(self.event_prefix + 'new',
                     source=self.__obj, meta={
                         'new.value': value
                     })

    def trigger_get(self, value) -> Event:
        return Event(self.event_prefix + 'get',
                     source=self.__obj, meta={
                         'get.value': value
                     })

    def trigger_set(self, old: int, new: int) -> None:
        return Event(self.event_prefix + 'set',
                     source=self.__obj, meta={
                         'set.value.old': old,
                         'set.value.new': new
                     })

    def trigger_cast_literal(self, old: float, new: int) -> None:
        return Event(self.event_prefix + 'literal.cast',
                     source=self.__obj, meta={
                         'cast.value.type': type(old),
                         'cast.value.old': old,
                         'cast.value.new': new
                     })


Number = Union[int, float, Int]
