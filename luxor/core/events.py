from __future__ import annotations
from typing import List, Tuple, Dict, Any, Union, Callable, TYPE_CHECKING
import re
if TYPE_CHECKING:
    from .context import context
    from .objects import Object


class Event:
    def __init__(self, classes: Union[str, List[str]], **kwargs) -> None:
        self.classes = classes if type(classes) == list else [classes]
        self.source: Object = kwargs.get('source')
        self.meta: Dict[str, Any] = kwargs.get('meta', {})
        self.action: Callable[Context, None] = kwargs.get('action')
        self.stack: Tuple[str, ...] = None
        self.ctx: Context = None

    def __str__(self):
        return str(self.source) + ' -> ( ' + \
            str(self.classes) + ', ' + str(self.meta) + ' )'


class EventInterceptor:
    @staticmethod
    def intercept(event: Event) -> Event:
        pass


def match(event: Event, pattern: str) -> bool:
    pattern.replace('.', '\\.')
    for cls in event.classes:
        if re.compile(pattern).match(cls) is not None:
            return True
    return False
