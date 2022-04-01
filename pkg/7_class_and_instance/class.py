#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 使用 class 关键字定义一个名为 Student 的类
class Student(object):
    # 初始化属性
    def __init__(self, name):
        self.name = name
        self.score = ""

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

bart.sum(100, 99)
bart.printScore()
print("%s 的评级: %s" % (bart.getName(), bart.getGrade()))
