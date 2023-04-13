#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 导入模块的两种方式
# 第一种：通过 PackageName.ModuelName 的方式导入。即：包名.模块名。as 关键字用以指定模块的别名。
import package_two.import_package as direct_import

# 第二种：使用 from 关键是指定包名，然后使用 import 关键字指定该包中的模块名
from package_two import import_package as indirect_import

# import_package.useSysPath()
# import_package.notUseSysPath()
print("通过 import 关键字直接导入包中的模块:", direct_import.PrintSomething())
print("通过 from 关键字间接导入包中的模块:", indirect_import.PrintSomething())
