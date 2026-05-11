class a:
    def __init__(self):
        print('init')
        self.x = 0
    def pt(self):
        print(self.x)
    def __del__(self):
        print('del')

b = a()
b = 1
b = a()
del(b)