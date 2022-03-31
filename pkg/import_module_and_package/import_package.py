import sys

from ..module_and_package import hello

print(sys.path)
print(hello.test())

# 运行方式：
# python3 -m pkg.import.import_package
# 原因：https://stackoverflow.com/questions/68960171/python-error-importerror-attempted-relative-import-with-no-known-parent-packa


# def abcdfg():
#     print("hahaha")
