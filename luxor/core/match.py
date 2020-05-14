from functools import singledispatch
import re


def build_pattern(pattern: str) -> re.Pattern:
    pattern = pattern.replace('.', '\\.')
    pattern = pattern.replace('*', '.*')
    return re.compile(pattern)


@singledispatch
def match(arg, pattern: str) -> bool:
    pass


@match.register
def match_string(arg: str, pattern: str) -> bool:
    pat = build_pattern(pattern)
    return pat.search(arg) is not None
