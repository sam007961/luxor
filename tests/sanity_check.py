import pathmagic  # noqa
from luxor.core import Context
from luxor.struct.types import Int

ctx = Context()
x = Int(0, 'x', ctx)
x.set(5)
x.set(7)
x.set(2)

ctx.log()
