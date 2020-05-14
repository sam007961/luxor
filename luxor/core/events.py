from typing import List, Set, Tuple, Dict, Any, Union, Callable, TYPE_CHECKING
from luxor.core.match import build_pattern, match
if TYPE_CHECKING:
    from .context import Context
    from .objects import Object


class Event:
    def __init__(self, classes: Union[str, Set[str]], **kwargs) -> None:
        self.classes = classes if type(classes) == set \
            else {classes} if type(classes) == str else set(classes)
        self.source: Object = kwargs.get('source')
        self.meta: Dict[str, Any] = kwargs.get('meta', {})
        self.action: Callable[Context, None] = kwargs.get('action')
        self.stack: Tuple[str, ...] = None
        self.ctx: Context = None

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
    def __init__(self, event: Event) -> None:
        self.__event = event
        self.prev_chain: List[Event] = []
        self.next_chain: List[Event] = []

    def match(self, pattern: str) -> bool:
        return match(self.__event, pattern)

    def prepend(self, event: Event) -> None:
        self.prev_chain.append(event)

    def append(self, event: Event) -> None:
        self.next_chain.append(event)

    def extend(self, **kwargs) -> None:
        self.__event.classes.update(kwargs.get('classes', {}))
        self.__event.meta.update(kwargs.get('meta', {}))

        ext = kwargs.get('action')
        if ext is not None:
            action = self.__event.action

            def extended_action(event: Event):
                action(event)
                ext(event)
            self.__event.action = extended_action

    def override(self, **kwargs) -> None:
        self.__event.classes = kwargs.get('classes', self.__event.classes)
        self.__event.meta = kwargs.get('meta', self.__event.meta)
        self.__event.action = kwargs.get('action', self.__event.action)

    def cancel(self) -> None:
        self.__event = None

    @property
    def canceled(self) -> bool:
        return self.__event is None

    @property
    def event(self) -> Event:
        return self.__event


class EventInterceptor:
    def intercept(self, wrapper: EventWrapper) -> None:
        pass
