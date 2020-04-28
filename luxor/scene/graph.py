from __future__ import annotations
from typing import List, Union

NodeData = Union[str]


class Node:
    def __init__(self):
        self.children: List[Node] = []
        self.data: NodeData = None
