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
        self.place_parent(parent)

    def peek(self, name: str) -> EventSafe:
        return self.__attributes.get(name)

    def place(self, name: str, value: EventSafe) -> EventSafe:
        old = self.peek(name)
        self.__attributes[name] = value
        return old

    def peek_parent(self) -> Object:
        return self.__parent

    def place_parent(self, parent: Object) -> Object:
        old = self.peek_parent()
        self.__parent = parent
        return old

    def peek_child(self, index: int) -> Object:
        return self.__children[index]

    def place_child(self, index: int, child: Object) -> None:
        self.__children.insert(index, child)

    def pop_child(self, index: int) -> Object:
        return self.__children.pop(index)

    def __getitem__(self, name: str) -> EventSafe:
        value = self.peek(name)
        self._trigger_getattr(name, value)
        return value

    def __setitem__(self, name: str, value: EventSafe) -> None:
        old = self.place(name, value)
        self._trigger_setattr(name, old, value)

    def get_parent(self) -> Object:
        parent = self.peek_parent()
        self._trigger_getparent(parent)
        return parent

    def set_parent(self, parent: Object) -> None:
        old = self.place_parent(parent)
        self._trigger_setparent(old, parent)

    def get_child(self, index: int) -> Object:
        child = self.peek_child(index)
        self._trigger_getchild(index, child)
        return child

    def insert_child(self, index: int, child: Object) -> None:
        self.place_child(index, child)
        self._trigger_insertchild(index, child)

    def remove_child(self, index) -> Object:
        child = self.pop_child(index)
        self._trigger_removechild(index, child)
        return child

    def __eq__(self, value: Object):
        return self.uid == value.uid

    def _trigger_new(self) -> None:
        parent = self.peek_parent()

        def do_new(event: Event) -> None:
            self.parent = parent
            self.__attributes.clear()
            self.__children.clear()

        self.ctx.push_event(Event('operation.new',
                            source=self, meta={
                                'new.uid': self.uid,
                                'new.parent': parent
                            }, action=do_new))

    def _trigger_getattr(self, name: str, value: EventSafe) -> None:
        self.ctx.push_event(Event('operation.attribute.get',
                            source=self, meta={
                                'get.name': name,
                                'get.value': value
                            }))

    def _trigger_setattr(self, name: str,
                         old: EventSafe, new: EventSafe) -> None:
        self.ctx.push_event(Event('operation.attribute.set',
                            source=self, meta={
                                'set.name': name,
                                'set.value.old': old,
                                'set.value.new': new
                            }, action=lambda e: self.place(name, new)))

    def _trigger_getparent(self, parent: Object) -> None:
        self.ctx.push_event(Event('operation.parent.get',
                            source=self, meta={
                                'get.value': parent
                            }))

    def _trigger_setparent(self, old: Object, new: Object) -> None:
        self.ctx.push_event(Event('operation.parent.set',
                            source=self, meta={
                                'set.old': old,
                                'set.new': new
                            }, action=lambda e: self.place_parent(new)))

    def _trigger_getchild(self, index: int, child: Object) -> None:
        self.ctx.push_event(Event('operation.child.get',
                            source=self, meta={
                                'get.index': index,
                                'get.value': child
                            }))

    def _trigger_insertchild(self, index: int, child: Object) -> None:
        self.ctx.push_event(Event('operation.child.insert',
                            source=self, meta={
                                'insert.index': index,
                                'insert.value': child
                            },
                            action=lambda e: self.place_child(index, child)))

    def _trigger_removechild(self, index: int, child: Object) -> None:
        self.ctx.push_event(Event('operation.child.remove',
                            source=self, meta={
                                'remove.index': index,
                                'remove.value': child
                            }, action=lambda e: self.pop_child(index)))

    def __str__(self):
        return '{ uid: ' + str(self.uid) + ' }'


EventSafe = Union[int, float, complex, str, tuple, frozenset, bytes, Object]
