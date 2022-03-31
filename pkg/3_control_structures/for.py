from collections.abc import Iterable

listType = ["List", "DataType", 1, 3.1415926]

for l in listType:
    print(l)

for i, v in enumerate(listType):
    print("元素号: ", i)
    print("值: ", v)

# 判断一个对象是否是可迭代的
print(isinstance(listType, Iterable))
