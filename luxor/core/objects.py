from __future__ import annotations
from typing import List, Dict, Any, NewType, TYPE_CHECKING
if TYPE_CHECKING:
    from .context import context


class Object:
    def __init__(self, parent: Object = None,
                 ctx: Context = None) -> None:
        self.parent = parent
        self.ctx = ctx
        self.properties: Dict[str, Any] = {}
        self.children: List[Object] = []
