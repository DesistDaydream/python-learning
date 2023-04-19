def dict_demo():
    # Python 中 dict 就是 map
    d = {"Michael": 95, "Bob": 75, "Tracy": 85}
    print(d)
    print(d["Bob"])

    d["Adam"] = 67
    print(d["Adam"])

    # 判断 map 中的 key 是否存在
    print("DesistDaydream" in d)
    # 通过 get() 方法判断 key 是否在 dict 中，如果存在则返回 key 对应的 value，不存在则返回第二个参数定义的内容
    print(d.get("DesistDaydream", "若 key 不存在则返回这一段字符串"))

    print("Adam" in d)

    # 删除 dict 中的 key，key 删除后，对应的 value 也会一并删除
    d.pop("Adam")


def dict_dict_demo():
    # dict 中的 value 也可以是 dict
    d = {
        "Michael": {"Math": 95, "English": 85},
        "Bob": {"Math": 75, "English": 75},
        "Tracy": {"Math": 85, "English": 75},
    }

    print(d)


if __name__ == "__main__":
    # dict_demo()
    dict_dict_demo()
