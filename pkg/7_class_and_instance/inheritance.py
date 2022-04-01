#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# object 表示该类从哪个类继承下来。如果没有合适的继承，就是 object，这是所有类最终都会继承的类。
class Animal(object):
    def run(self):
        print("Animal is running...")


# Dog 类继承了 Animal
class Dog(Animal):
    pass


# Cat 类继承了 Animal
class Cat(Animal):
    pass


dog = Dog()
dog.run()

cat = Cat()
cat.run()
