from enum import Enum
from varname import varname
from luxor.core.context import Context
from luxor.utils.threads import thread_id


class Ref(Enum):
    lvalue = 1
    rvalue = 2


class Var:
    def __init__(self, **kwargs):
        self.ctx: Context = kwargs['context']
        self.ref: Ref = kwargs.get('ref', Ref.lvalue)
        self.name: str = kwargs.get('name')
        if self.ref == Ref.lvalue and self.name is None:
            self.name = varname(2)  # variable declared 2 frames above
        self.tid = thread_id()
        self.callstack: str = \
            self.ctx[str(self.tid) + '.callstack'].format()
        self.name = str(self.tid) + '.' + \
            self.callstack + '.' + self.name
        self.autotrigger: bool = kwargs.get('autotrigger', True)

    def trigger(self, name: str, *args) -> None:
        if self.autotrigger:
            event = getattr(self, 'trigger_' + name)(*args)
            self.ctx.push_event(event)
