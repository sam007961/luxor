from typing import Callable
from luxor.core.events import EventWrapper, EventInterceptor


def interceptor(func: Callable[[EventWrapper], None]):
    class Interceptor(EventInterceptor):
        def intercept(self, wrapper: EventWrapper) -> None:
            func(wrapper)
    return Interceptor
