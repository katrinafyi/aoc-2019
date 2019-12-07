def a():
    print('got', (yield 1))
    print('passed 1')
    yield 2 
    print('passed 2')

x = a()
print('after a()')
print(next(x))
print(x.send('asdf'))
print(next(x))