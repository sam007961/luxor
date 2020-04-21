from __future__ import annotations
from typing import List, Dict, Any, Callable, NewType, TYPE_CHECKING
from luxor.core.objects import Object
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


class EventHandler:
    @staticmethod
    def handle(input: Event) -> List[Event]:
        pass


class EventInterceptor:
    @staticmethod
    def intercept(input: Event) -> Event:
        pass
