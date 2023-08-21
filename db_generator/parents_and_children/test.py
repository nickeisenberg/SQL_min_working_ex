class Test:
    def __init__(self):
        self.x = 'hello'
    @staticmethod
    def foo(x, y):
        return print(x + y)

test = Test()

test.foo(1, 2)
