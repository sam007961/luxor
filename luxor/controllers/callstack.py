from typing import List, Tuple


class CallStack:
    def __init__(self) -> None:
        self.__stack: List[Tuple[str, int]] = []

    def push(self, name: str, idx: int = 0) -> None:
        stack = self.__stack
        if len(stack) > 0 and stack[-1][0] == name:
            top_name, top_count = stack[-1]
            stack[-1] = (top_name, top_count + 1)
        else:
            stack.append((name, 0))

    def pop(self, idx: int = 0) -> None:
        if len(self.__stack) == 0:
            return
        stack = self.__stack
        top_name, top_count = stack[-1]
        if top_count > 0:
            stack[-1] = (top_name, top_count - 1)
        else:
            stack.pop()

    @property
    def depth(self) -> int:
        return sum(count + 1 for _, count in self.__stack)

    def format(self) -> str:
        return '.'.join(s[0] + '[{}]'.format(s[1]) for s in self.__stack)
