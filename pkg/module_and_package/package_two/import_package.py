import os
import sys


def useSysPath():
    # 添加搜索模块的路径以导入其他包中的模块
    sys.path.append(os.getcwd() + "/module_and_package")

    import package_one.def_module as def_module

    print(def_module.fib(1000))


def notUseSysPath():
    # 当可以通过相对路径导入其他包的模块
    # 但是如果想要直接执行本文件，需要通过如下方式运行：
    # python3 -m pkg.module_and_package.imports.import_package
    # 原因：https://stackoverflow.com/questions/68960171/python-error-importerror-attempted-relative-import-with-no-known-parent-packa
    from ..package_one import def_module

    print(def_module.fib(1000))


def PrintSomething() -> str:
    return "hahaha"


if __name__ == "__main__":
    useSysPath()
    notUseSysPath()
    PrintSomething()
