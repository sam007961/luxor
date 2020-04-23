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
        self.name: str = kwargs.get('name', varname())
        self.ctx: Context = kwargs['context']
        self.obj = self.ctx.request_object()
        self.obj['value'] = value
        self.event_prefix = 'int.' + self.name + '.'
        self._trigger_new(value)

    def set(self, value: Union[int, Int]) -> None:
        if type(value) == Int:
            value = value.value

        old = self.obj.peek('value')
        self.obj['value'] = value
        self._trigger_set(old, value)

    def get(self) -> int:
        value = copy(self.obj['value'])
        self._trigger_get(value)
        return value

    @property
    def value(self) -> int:
        pass

    @value.setter
    def value(self, value: Union[int, Int]) -> None:
        self.set(value)

    @value.getter
    def value(self) -> int:
        return self.get()

    def _trigger_new(self, value) -> None:
        self.ctx.push_event(Event(self.event_prefix + 'new',
                            self.obj, {
                                'new.value': copy(value)
                            }))

    def _trigger_set(self, old: int, new: int) -> None:
        self.ctx.push_event(Event(self.event_prefix + 'set',
                            self.obj, {
                                'set.value.old': copy(old),
                                'set.value.new': copy(new)
                            }))

    def _trigger_get(self, value) -> None:
        self.ctx.push_event(Event(self.event_prefix + 'get',
                            self.obj, {
                                'get.value': copy(value)
                            }))
