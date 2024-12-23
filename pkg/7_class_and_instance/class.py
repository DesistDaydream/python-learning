#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# 使用 class 关键字定义一个名为 Student 的类
# 从 3.7 版本开始，可以使用 dataclass 装饰器来简化类的定义，不用再定义 __init__() 方法了，具体可以看 pkg\runtime_services\dataclasses.py  # noqa: E501
class Student:
    # 初始化属性。总是要带一个 self 参数，用来表示这个类自身，当实例化后，可以通过实例化后的变量直接调用自身的属性
    def __init__(self, name):
        self.name = name
        self.score = ""

    # https://docs.python.org/3.12/reference/datamodel.html#emulating-callable-objects
    # 把实例化后的 Student 当作函数调用时，会自动调用 __call__ 方法
    def __call__(self):
        print("call")

    # 方法，获取实例化后的 name 属性的值。即获取学生的名字
    def getName(self):
        return self.name

    # 方法，根据 数学 与 计算机 的成绩计算总成绩
    def sum(self, math, computer):
        self.score = math + computer

    # 方法，输出某个学生的总成绩
    def printScore(self):
        print("%s 的分数为: %s" % (self.name, self.score))

    # 方法，根据成绩得出等级
    def getGrade(self):
        if self.score >= 90:
            return "A"
        elif self.score >= 60:
            return "B"
        else:
            return "C"


# 实例化
bart = Student("Bart Simpson")
# 这里由于上面有 self，所以 self.name 就表示这个类自身的 name 属性，当实例化后，可以直接使用实例化的变量调用 name 属性
print(bart.name)

bart.sum(100, 99)
bart.printScore()
print("%s 的评级: %s" % (bart.getName(), bart.getGrade()))

# 调用实例化后的对象，把对象当成函数一样使用，相当于调用 __call__() 方法
bart()