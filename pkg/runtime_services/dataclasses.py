from dataclasses import dataclass

# dataclasses 模块提供了一个装饰器和一些函数，用于为用户定义的类自动添加一些特殊方法，从而简化数据类的定义。
# 例如 __init__()、__repr__()、__eq__()、__lt__() 等方法。


@dataclass
class dataclass_demo:
    name: str
    age: int
