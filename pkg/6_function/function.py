import math

#  定义函数
def myFunction(myArg):
    return myArg


# 调用函数
returnValue = myFunction("Hello World")
print(returnValue)

# 空函数
def noneFunction():
    pass


# Python 函数的返回值本质是一个 tuple 类型的数据
def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny


print("函数的返回值: {}".format(move(100, 100, 60, math.pi / 6)))
