#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections.abc import Iterable

listType = ["List", "DataType", 1, 3.1415926]

for value in listType:
    print(value)

# 通过 enumerate() 函数可以获取元素的索引
for index, value in enumerate(listType):
    print("元素号: ", index)
    print("值: ", value)

# 判断一个对象是否是可迭代的
print(isinstance(listType, Iterable))
