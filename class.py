class test:
    def __del__(self):
        print("destracted")
    def __init__(self) -> None:
        pass
    def a(self):
        del self
        return True
d = test()
print(d.a())