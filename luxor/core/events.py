from __future__ import annotations
from typing import List, Dict, Any, Callable, NewType, TYPE_CHECKING
from .objects import Object
if TYPE_CHECKING:
    from .context import context


class Event:
    def __init__(self, classes: List[str], action: Callable[Context, None],
                 source: Object = None, meta: Dict[str, Any] = {},
                 ctx: Context = None) -> None:
        self.classes = classes
        self.action = action
        self.source = source
        self.meta = meta
        self.ctx = ctx

    def __str__(self):
        return '( ' + str(self.classes) + ', ' + str(self.meta) + ' )'


class EventHandler:
    @staticmethod
    def handle(input: Event) -> List[Event]:
        pass


class EventInterceptor:
    @staticmethod
    def intercept(input: Event) -> Event:
        pass
