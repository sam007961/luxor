from enum import Enum
from varname import varname
from luxor.core.context import Context


class Ref(Enum):
    lvalue = 1
    rvalue = 2


class Var:
    def __init__(self, **kwargs):
        self.ctx: Context = kwargs['context']
        self.ref = kwargs.get('ref', Ref.lvalue)
        self.name: str = kwargs.get('name')
        if self.ref == Ref.lvalue and self.name is None:
            self.name = varname(2)  # variable declared 2 levels above
        self.name = '.'.join(self.ctx.stack + (self.name,))
        self.autotrigger: bool = kwargs.get('autotrigger', True)

    def auto_trigger(self, name: str, *args) -> None:
        if self.auto_trigger:
            getattr(self, 'trigger_' + name)(*args)
