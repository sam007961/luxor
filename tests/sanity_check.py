import pathmagic  # noqa
from luxor.core import Context
from luxor.struct.types import Int

ctx = Context()
x = Int(0, context=ctx)
x.set(5)
x.set(7)
x.set(2)
x.value = 3

y = Int(0, context=ctx)
y.set(x)
y.value = x

ctx.log()

for _ in range(11):
    ctx.pop_event()

print(ctx.get_object(0).peek('value'))
