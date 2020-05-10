from __future__ import annotations
from typing import List, Union, Dict
from luxor.core.objects import Object
from luxor.core.events import Event
from luxor.scene.style import PropertyValue


class Node:
    def __init__(self) -> None:
        self.children: List[Node] = []
        self.data: NodeData = None
        self.properties: Dict[str, PropertyValue]


class Element:
    def __init__(self, tag: str, attributes: Dict[str, str]) -> None:
        self.tag = tag
        self.attributes = attributes


class Template:
    def __init__(self, src: str, obj: Object, event: Event) -> None:
        self.graph = None
        self.obj = obj
        self.event = event


NodeData = Union[str, Element, Template]
