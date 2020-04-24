from __future__ import annotations
from typing import List, Dict, Union, NewType, TYPE_CHECKING
from .events import Event
if TYPE_CHECKING:
    from .context import context

Immutable = Union[int, float, complex, str, tuple, frozenset, bytes]


class Object:
    def __init__(self, parent: Object = None,
                 uid: int = None, ctx: Context = None) -> None:
        self.uid = uid
        self.__parent = None
        self.__attributes: Dict[str, Immutable] = {}
        self.__children: List[Object] = []
        self.ctx = ctx
        # if parent is not None:
        #     self.parent = parent

    def peek(self, name: str) -> Immutable:
        return self.__attributes.get(name)

    def place(self, name: str, value: Immutable) -> None:
        self.__attributes[name] = value

    def __getitem__(self, name: str) -> Immutable:
        self._trigger_getattr(name)
        return self.peek(name)

    def __setitem__(self, name: str, value: Immutable) -> None:
        old = self.peek(name)
        self.place(name, value)
        self._trigger_setattr(name, old, value)

    def __eq__(self, value: Object):
        return self.uid == value.uid

    def _trigger_new(self) -> None:
        def do_new(event: Event) -> None:
            self.__parent = None
            self.__attributes.clear()
            self.__children.clear()

        self.ctx.push_event(Event('operation.new',
                            source=self, meta={
                                'new.uid': self.uid
                            }, action=do_new))

    def _trigger_getattr(self, name: str) -> None:
        self.ctx.push_event(Event('operation.attribute.get',
                            source=self, meta={
                                'get.name': name,
                                'get.value': self.__attributes[name]
                            }))

    def _trigger_setattr(self, name: str,
                         old: Immutable, new: Immutable) -> None:
        def do_set(event: Event) -> None:
            self.__attributes[name] = new

        self.ctx.push_event(Event('operation.attribute.set',
                            source=self, meta={
                                'set.name': name,
                                'set.value.old': old,
                                'set.value.new': new
                            }, action=do_set))
