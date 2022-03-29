# 格式化输出
# 使用 % 符号
formatString = "World"
formatInt = 3
formatFloat = 3.1415926
print("Hello%s%s" % (",", formatString))
print("%.2f" % (formatFloat))
# 使用 format 函数
print("Hello{}{}".format(",", formatString))
print("Hello{1}{1}".format(",", formatString))
print("{:.3f}".format(formatFloat))
