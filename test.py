from algebra.algebra import Variable, Add

x = Variable('x')
y = Variable('y', Add(x, 3))
print(y)  # 'x + 3'

# assign: 代入
y1 = y.assign({'x': 2})
print(y1)  # Add(Constant(2), Constant(3))

# operate: 計算
y2 = y1.operate()
print(y2)  # {'1': 5}

# evaluate: 代入，計算，表示
z = Variable('z', Add(y, x))
z.evaluate()