from __future__ import annotations
from typing import Dict, Any
from copy import deepcopy


class TreeDict:
    def __init__(self, data: Dict[str, Any] = {}) -> None:
        self.__data: Dict[str, Any] = data

    def __getitem__(self, key: str) -> Any:
        item = self.__fetch(key)
        if type(item) == dict:
            return TreeDict(item)
        else:
            return item

    def __setitem__(self, key: str, value: Any) -> None:
        self.__place(key, value)

    def extract(self) -> Dict[str, Any]:
        return deepcopy(self.__data)

    def __fetch(self, _key: str) -> Any:
        keys = _key.split('.')
        result = self.__data
        for key in keys:
            result = result.get(key, {})
        return result

    def __place(self, _key: str, value: Any):
        keys = _key.split('.')
        target = self.__data
        for key in keys[:-1]:
            if key not in target: 
                target[key] = {}
            target = target[key]
        target[keys[-1]] = value
