def log(func):
    def wrapper(*args, **kw):
        print("call %s():" % func.__name__)
        return func(*args, **kw)

    return wrapper


@log
# 装饰器引用的下一行必须是注释或者函数定义、类定义。这是标准语法
# 若不按照标准语法写，则会报错: Expected function or class declaration after decorator
# 在这个示例中，@log 相当于 now = log(now)
def now():
    print("2015-3-25")


f = now
f()
