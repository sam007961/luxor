import pathmagic  # noqa
from luxor.core import Context
from luxor.controllers.types import Int
from luxor.core.treedict import TreeDict

ctx = Context()
ctx.push_stack('test')
x = Int(0, context=ctx)
x.set(5)
x.set(7.0)
x.set(2)
x.value = 3

ctx.push_stack('deep')
y = Int(0, context=ctx)
y.set(x)
y.value = x

x.obj.insert_child(0, y.obj)
y.obj.set_parent(x.obj)

ctx.log()
# ctx.log(show_operations=True)

# for _ in range(7):
#     ctx.pop_event()

while ctx.has_events:
    ctx.pop_event()

print(ctx.peek_object(0).sget('value'))

d = TreeDict()
d['int.background-color'] = '#123123'

print(d.extract())
print(d['int.background-color'])
