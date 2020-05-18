from __future__ import annotations
from typing import List, Set, Dict, Any, Union, Callable, TYPE_CHECKING
from luxor.core.match import build_pattern, match
if TYPE_CHECKING:
    from luxor.core.objects import Object
    from luxor.core.context import Context


class Event:
    def __init__(self, classes: Union[str, Set[str]], **kwargs) -> None:
        self.classes = classes if type(classes) == set \
            else {classes} if type(classes) == str else set(classes)
        self.source: Object = kwargs.get('source')
        self.meta: Dict[str, Any] = kwargs.get('meta', {})
        self.action: Callable[[Event], None] = kwargs.get('action')

    def __str__(self):
        return str(self.source) + ' -> ( ' + \
            str(self.classes) + ', ' + str(self.meta) + ' )'


@match.register
def match_event(event: Event, pattern: str) -> bool:
    pat = build_pattern(pattern)
    for cls in event.classes:
        if pat.search(cls) is not None:
            return True
    return False


class EventWrapper:
    def __init__(self, ctx: Context, event: Event) -> None:
        self.ctx = ctx
        self.event = event
        self.prev_chain: List[Event] = []
        self.next_chain: List[Event] = []

    def match(self, pattern: str) -> bool:
        return match(self.event, pattern)

    def prepend(self, event: Event) -> None:
        self.prev_chain.append(event)

    def append(self, event: Event) -> None:
        self.next_chain.append(event)

    def extend(self, **kwargs) -> None:
        self.event.classes.update(kwargs.get('classes', {}))
        self.event.meta.update(kwargs.get('meta', {}))

        ext = kwargs.get('action')
        if ext is not None:
            action = self.event.action

            def extended_action(event: Event):
                action(event)
                ext(event)
            self.event.action = extended_action

    def override(self, **kwargs) -> None:
        self.event.classes = kwargs.get('classes', self.event.classes)
        self.event.meta = kwargs.get('meta', self.event.meta)
        self.event.action = kwargs.get('action', self.event.action)

    def cancel(self) -> None:
        self.event = None

    @property
    def canceled(self) -> bool:
        return self.event is None

    @property
    def source(self) -> Object:
        return self.event.source


class EventInterceptor:
    def __init__(self):
        self.uid = None

    def __eq__(self, value: EventInterceptor) -> bool:
        return self.uid == value.uid

    def intercept(self, wrapper: EventWrapper) -> None:
        pass
