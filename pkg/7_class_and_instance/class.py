#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 使用 class 关键字定义一个名为 Student 的类
class Student(object):
    # 初始化属性
    def __init__(self, name):
        self.name = name
        self.score = ""

    # 方法，根据 数学 与 计算机 的成绩计算总成绩
    def sum(self, math, computer):
        self.score = math + computer

    # 方法，输出某个学生的总成绩
    def print_score(self):
        print("%s 的分数为: %s" % (self.name, self.score))


# 实例化
bart = Student("Bart Simpson")

bart.sum(100, 99)
bart.print_score()
