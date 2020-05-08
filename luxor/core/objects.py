from __future__ import annotations
from typing import List, Dict, Union, NewType, TYPE_CHECKING
from .events import Event
if TYPE_CHECKING:
    from .context import context


class Object:
    def __init__(self, parent: Object = None,
                 uid: int = None, ctx: Context = None) -> None:
        self.uid = uid
        self.__parent = None
        self.__attributes: Dict[str, EventSafe] = {}
        self.__children: List[Object] = []
        self.ctx = ctx
        self.sset_parent(parent)

    def sget(self, name: str) -> EventSafe:
        return self.__attributes.get(name)

    def sset(self, name: str, value: EventSafe) -> None:
        self.__attributes[name] = value

    def sget_parent(self) -> Object:
        return self.__parent

    def sset_parent(self, parent: Object) -> None:
        self.__parent = parent

    def sget_child(self, index: int) -> Object:
        return self.__children[index]

    def sinsert_child(self, index: int, child: Object) -> None:
        self.__children.insert(index, child)

    def sremove_child(self, index: int) -> Object:
        return self.__children.pop(index)

    def __getitem__(self, name: str) -> EventSafe:
        value = self.sget(name)
        self._trigger_getattr()
        return value

    def __setitem__(self, name: str, value: EventSafe) -> None:
        self._trigger_setattr(name, value)

    def get(self, name: str) -> EventSafe:
        return self[name]

    def set(self, name: str, value: EventSafe) -> None:
        self[name] = value

    def get_parent(self) -> Object:
        parent = self.sget_parent()
        self._trigger_getparent()
        return parent

    def set_parent(self, parent: Object) -> None:
        self._trigger_setparent(parent)

    def get_child(self, index: int) -> Object:
        child = self.sget_child(index)
        self._trigger_getchild(index, child)
        return child

    def insert_child(self, index: int, child: Object) -> None:
        self._trigger_insertchild(index, child)

    def remove_child(self, index) -> Object:
        child = self.sget_child(index)
        self._trigger_removechild(index)
        return child

    def __eq__(self, value: Object):
        return self.uid == value.uid

    def _trigger_new(self) -> None:
        parent = self.sget_parent()

        def do_new(event: Event) -> None:
            self.parent = parent
            self.__attributes.clear()
            self.__children.clear()

        self.ctx.push_event(Event('operation.new', source=self, action=do_new))

    def _trigger_getattr(self) -> None:
        self.ctx.push_event(Event('operation.attribute.get', source=self))

    def _trigger_setattr(self, name: str, new: EventSafe) -> None:
        self.ctx.push_event(Event('operation.attribute.set', source=self,
                            action=lambda e: self.sset(name, new)))

    def _trigger_getparent(self) -> None:
        self.ctx.push_event(Event('operation.parent.get', source=self))

    def _trigger_setparent(self, new: Object) -> None:
        self.ctx.push_event(Event('operation.parent.set', source=self,
                            action=lambda e: self.sset_parent(new)))

    def _trigger_getchild(self, index: int, child: Object) -> None:
        self.ctx.push_event(Event('operation.child.get', source=self))

    def _trigger_insertchild(self, index: int, child: Object) -> None:
        self.ctx.push_event(Event('operation.child.insert', source=self,
                            action=lambda e: self.sinsert_child(index, child)))

    def _trigger_removechild(self, index: int) -> None:
        self.ctx.push_event(Event('operation.child.remove', source=self,
                            action=lambda e: self.sremove_child(index)))

    def __str__(self):
        return '{ uid: ' + str(self.uid) + ' }'


EventSafe = Union[int, float, complex, str, tuple, frozenset, bytes, Object]
