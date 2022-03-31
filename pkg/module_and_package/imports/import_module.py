import sys

sys.path.append("/mnt/e/Projects/DesistDaydream/python-learning/pkg/module_and_package")

import packages.def_module as def_module

print(sys.path)
print(def_module.fib(1000))
