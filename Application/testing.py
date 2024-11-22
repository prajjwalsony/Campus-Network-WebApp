a = [1]
b = [2]
def func1(a=a, b=b):
    print(a[0], b[0])

a.clear()
b.clear()
a.append(6)
b.append(3)

func1()