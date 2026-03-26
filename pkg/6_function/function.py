import math


# 定义函数
# 其中 -> str 用以指定函数返回值的类型，可以省略。
def myFunction() -> str:
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


# 注意：默认参数必须放在参数列表的最后面。
# 下面这种写法将会报错: SyntaxError: non-default argument follows default argument(非默认参数遵循默认参数)
# def power(x=2, n):

print("函数的参数使用默认值: ", power(5))


# 可变参数
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum


print("可变参数的函数调用: ", calc(1, 2), calc())


# 关键字参数
# 通过这种写法特性，可以在函数调用时填写的参数顺序与声明时不一致，甚至可以省略某个参数。
# 所谓的关键字参数，就是在调用时，除了指定参数的值，还需要指定参数的名称。如果不指定名称，解释器也没法识别传入的到底是哪个参数
def calc(a, b=None, c=None):
    if b is None:
        b = 0
    if c is None:
        c = 0
    return a + b + c


# 这里的参数第一个是 a，可以省略参数名称。后面的 b 如果不写，那么就要写 c 参数名称。否则 calc(1,20) 就相当于 calc(a=1, b=20)
print("关键字参数的函数的返回值: {}".format(calc(1, c=20)))


# 不定长参数
# 定义函数时，参数前面加个 * ，表示这个参数可以接收任意数量的参数。传入的参数以 tuple 的形式导入
# 注意：args 不是关键字，只是约定俗成的名称
def calc(*args):
    # 传入的参数是 (1, 2, 3)
    print(args)
    sum = 0
    for n in args:
        sum = sum + n * n
    return sum


print("不定长参数的函数调用: ", calc(1, 2, 3))


# 定义函数时，参数前面加个 ** ，表示这个参数可以接收任意数量的关键字参数。传入的参数以 dict 的形式导入
# 注意：kwargs 不是关键字，只是约定俗成的名称
def calc(**kwargs):
    # 传入的参数是 {'a': 1, 'b': 2, 'c': 3}
    print(kwargs)
    sum = 0
    for n in kwargs.values():
        sum = sum + n * n
    return sum


print("不定长参数的函数调用: ", calc(a=1, b=2, c=3))
