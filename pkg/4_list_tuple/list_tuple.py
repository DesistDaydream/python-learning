# Python 中没有 Array 数据类型，而是 list 数据类型
# list 中元素的数据类型不必保持一致
listType = ["List", "DataType", 1, 3.1415926]

print("数组长度: %s" % len(listType))
print("第一个元素: %s\n最后一个元素: %f" % (listType[0], listType[-1]))

# 追加元素
listType.append("DesistDaydream")
# 插入元素。将 inserted 插入到 List 中的 1 号元素位置
listType.insert(1, "inserted")
# 删除末尾元素
listType.pop()
# 删除指定位置的元素
listType.pop(1)


# Python 中的 tuple 类型是一个不可变的 list
