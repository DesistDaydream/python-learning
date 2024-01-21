import sys
import site

print(sys.prefix, sys.exec_prefix)

print(site.getsitepackages())
