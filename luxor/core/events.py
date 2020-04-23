from __future__ import annotations
from typing import List, Dict, Any, Union, Callable, NewType, TYPE_CHECKING
if TYPE_CHECKING:
    from .context import context
    from .objects import Object


class Event:
    def __init__(self, classes: Union[str, List[str]],
                 source: Object = None, meta: Dict[str, Any] = {},
                 **kwargs) -> None:
        self.classes = classes if type(classes) == list else [classes]
        self.source = source
        self.meta = meta
        self.action: Callable[Context, None] = kwargs.get('action')
        self.stack: List[str] = None
        self.ctx: Context = None

    def __str__(self):
        return 'uid: ' + str(self.source.uid) + ' -> ( ' + \
            str(self.classes) + ', ' + str(self.meta) + ' )'


class EventHandler:
    @staticmethod
    def handle(input: Event) -> List[Event]:
        pass


class EventInterceptor:
    @staticmethod
    def intercept(input: Event) -> Event:
        pass
