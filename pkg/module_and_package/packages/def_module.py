#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"Module Demo"

__author__ = "DesistDaydream"


def fib(n):  # 输出最大到 n 的斐波那契级数
    a, b = 0, 1
    while a < n:
        print(a, end=" ")
        a, b = b, a + b
    print()


def fib2(n):  # 返回最大到 n 的斐波那契级数
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result


# 当我们在命令行直接使用 python3 def_module.py 运行模块文件时，Python 解释器把 __name__ 这个特殊变量的值设为 __main__
# 如果在其他地方导入 def_module 模块时 __name__ 变量的值则是本模块的名称(i.e.def_module)
# 因此，这种 if 测试可以让一个模块通过命令行运行时执行一些额外的代码，最常见的就是运行单元测试。
if __name__ == "__main__":
    import sys

    fib(int(sys.argv[1]))
