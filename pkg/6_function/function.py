import math

#  定义函数
def myFunction():
    return "Hello World"


# 调用函数
returnValue = myFunction()
print(returnValue)

# 空函数
def noneFunction():
    pass


# 函数的参数
# Python 函数的返回值本质是一个 tuple 类型的数据
def move(x, y, step, angle):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny


print("函数的返回值: {}".format(move(100, 100, 60, math.pi / 6)))

# 默认参数
def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s


print("函数的参数使用默认值: ", power(5))

# 可变参数
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum


print("可变参数的函数调用: ", calc(1, 2), calc())
