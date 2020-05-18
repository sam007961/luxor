import threading
from luxor.core.events import EventWrapper
from luxor.utils.decorators import interceptor


def thread_id() -> str:
    return threading.currentThread().name


@interceptor
def add_thread_info(wrapper: EventWrapper) -> None:
    tid = thread_id()
    stack = wrapper.ctx[tid + '.callstack']
    wrapper.extend(meta={
        'thread.id': tid,
        'thread.callstack': stack.format(),
        'thread.callstack.depth': stack.depth
    })
