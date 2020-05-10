from typing import Union
from enum import Enum


class Unit(Enum):
    Px = 1


class Color:
    def __init__(self, r: int, g: int, b: int, a: int) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a


class Length:
    def __init__(self, value: Union[int, float], unit: Unit) -> None:
        self.value = value
        self.unit = unit


PropertyValue = Union[str, Color, Length]
