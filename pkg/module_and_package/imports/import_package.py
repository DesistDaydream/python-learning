import sys

# 当直接执行本代码时，想要导入其他目录的模块，可以通过相对路径导入
# 运行方式：
# python3 -m pkg.module_and_package.imports.import_package
# 原因：https://stackoverflow.com/questions/68960171/python-error-importerror-attempted-relative-import-with-no-known-parent-packa
# from ..packages import def_module

# 当上层目录的 Python 代码调用该模块时，不用使用相对路径
from packages import def_module

print(sys.path)
print(def_module.fib(1000))


def PrintSomething():
    print("hahaha")
