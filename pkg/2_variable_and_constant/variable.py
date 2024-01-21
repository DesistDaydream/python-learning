#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 声明变量
s = "Hello, World!"
name = "John"
varialbeScope: str = "scope"  # 变量的作用域

# 引用变量
print(s)
print(name)

# 变量的本质是对象的引用
# 在 Python 中有一个与 ESMAScript 中类似的 object(对象) 概念。
# 在 Python 中，所有的数据都是对象，每一个对象都有唯一的标识符、类型和值。与 JavaScript 不同的是，在 Python 中，变量本身并不拥有内存空间，它只是指向一个对象的引用。因此，我们在 Python 中声明变量时，并不需要显式地指定它的类型。  # noqa: E501
print("对象标识符: ", id(s))
print("对象的类型: ", type(s))
print("对象的值: ", s)
# Python 中不同类型的对象具有各自的属性和方法。因此，此时如果将变量作为一个对象，那么这个就可以调用这个对象的属性和方法。例如：  # noqa: E501
print(s.upper())  # 输出 "HELLO, WORLD!"
print(s.lower())  # 输出 "hello, world!"
print(s.capitalize())  # 输出 "Hello, world!"

# 调用字符串对象的方法
print(s.split(","))  # 输出 ['Hello', ' World!']
print(s.replace("World", "Python"))  # 输出 "Hello, Python!"

# 在这个例子中，我们首先创建了一个字符串类型的变量 s，然后使用 . 运算符来调用字符串对象的属性和方法。
# 例如，我们调用 upper() 方法将字符串中的所有字母转换为大写，调用 lower() 方法将字符串中的所有字母转换为小写，调用 capitalize() 方法将字符串的第一个字母转换为大写。  # noqa: E501
# 另外，我们还调用了 split() 方法将字符串按照给定的分隔符拆分成一个列表，调用 replace() 方法将字符串中的某个子串替换为另一个字符串。  # noqa: E501

# 除了字符串类型的变量，其他类型的变量也可以具有属性和方法。例如，我们可以创建一个列表类型的变量 lst，然后使用 . 运算符来调用列表对象的属性和方法，例如：  # noqa: E501
lst = [1, 2, 3, 4, 5]

# 调用列表对象的属性
print(len(lst))  # 输出 5

# 调用列表对象的方法
lst.append(6)
print(lst)  # 输出 [1, 2, 3, 4, 5, 6]
lst.reverse()
print(lst)  # 输出 [6, 5, 4, 3, 2, 1]

# 在这个例子中，我们首先创建了一个列表类型的变量 lst，然后使用 . 运算符来调用列表对象的属性和方法。例如，我们调用 len() 函数来获取列表的长度，调用 append() 方法向列表中添加一个元素，调用 reverse() 方法将列表中的元素倒序排列。  # noqa: E501


# 变量的作用域
def VariableScopeDemo():
    # 若在函数中不使用 global 关键字，那么就算与全局变量同名，函数内的该变量也是仅作用域函数内部。
    # 注意：这里注释的原因是：在使用 global 关键字全局声明之前分配了“varialbeScope”
    # varialbeScope = "Local Variable"
    # print(varialbeScope) # 若直接输出，则输出的是全局变量的值

    # 若想在函数中改变全局变量，需要使用 global 关键字
    global varialbeScope
    varialbeScope = "Global Variable"


VariableScopeDemo()
print(varialbeScope)
