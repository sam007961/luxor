from __future__ import annotations
from copy import copy
from typing import List, Dict, Any, NewType, TYPE_CHECKING
from .events import Event
if TYPE_CHECKING:
    from .context import context


class Object:
    def __init__(self, parent: Object = None,
                 uid: int = None, ctx: Context = None) -> None:
        self.uid = uid
        self.__parent = None
        self.__attributes: Dict[str, Any] = {}
        self.__children: List[Object] = []
        self.ctx = ctx
        # if parent is not None:
        #     self.parent = parent

    def peek(self, name: str) -> Any:
        return self.__attributes[name]

    def __getitem__(self, name: str) -> Any:
        self._trigger_getattr(name)
        return self.__attributes[name]

    def __setitem__(self, name: str, value: Any) -> None:
        old = copy(self.__attributes.get(name))
        self.__attributes[name] = value
        self._trigger_setattr(name, old, value)

    def __eq__(self, value: Object):
        return self.uid == value.uid

    def _trigger_new(self) -> None:
        def do_new(event: Event) -> None:
            self.__parent = None
            self.__attributes.clear()
            self.__children.clear()

        self.ctx.push_event(Event('operation.new', self, {
            'new.uid': copy(self.uid)
        }, action=do_new))

    def _trigger_setattr(self, name: str, old: Any, new: Any) -> None:
        def do_set(event: Event) -> None:
            self.__attributes[name] = new

        self.ctx.push_event(Event('operation.attribute.set', self, {
            'set.name': copy(name),
            'set.value.old': copy(old),
            'set.value.new': copy(new)
        }, action=do_set))

    def _trigger_getattr(self, name: str) -> None:
        self.ctx.push_event(Event('operation.attribute.get', self, {
            'get.name': copy(name),
            'get.value': copy(self.__attributes[name])
        }))
