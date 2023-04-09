from dataclasses import dataclass


# dataclasses 模块提供了一个装饰器和一些函数，用于自动为用户定义的 class 添加一些特殊方法，从而简化数据类的定义。
# 例如 __init__()、__repr__()、__eq__()、__lt__() 等方法。
# 比如这里声明了一个 dataclass_demo 类，如果是以前的话，需要自己定义 `def __init__():`，就像下面这样
# class dataclass_demo:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
# 现在使用 dataclass 装饰器，就可以省去这一步了
@dataclass
class Student:
    name: str
    score: int

    def getName(self):
        return self.name

    def sum(self, math, computer):
        self.score = math + computer

    def printScore(self):
        print("%s 的分数为: %s" % (self.name, self.score))

    def getGrade(self):
        if self.score >= 90:
            return "A"
        elif self.score >= 60:
            return "B"
        else:
            return "C"


# 实例化
bart = Student("Bart Simpson", 0)
# 这里由于上面有 self，所以 self.name 就表示这个类自身的 name 属性，当实例化后，可以直接使用实例化的变量调用 name 属性
print(bart.name)

bart.sum(100, 99)
bart.printScore()
print("%s 的评级: %s" % (bart.getName(), bart.getGrade()))
