# 示例数据
envs = [
    {"name": "JD_COOKIE", "remarks": "remark=user1", "value": "cookie1"},
    {"name": "JD_COOKIE", "remarks": "remark=user2", "value": "cookie2"},
    {"name": "JD_COOKIE", "remarks": "remark=user3", "value": "cookie3"},
    {"name": "OTHER_COOKIE", "remarks": "remark=user4", "value": "cookie4"},
]

# 指定 pt_pin
pt_pin = "user2"

# 使用 lambda 表达式筛选满足条件的字典。
# 利用 lamdba 将 envs 当做 x，若 x 中的 name、remarks 都满足条件。则匹配上。
jd_cookies = list(filter(lambda x: x["name"] == "JD_COOKIE" and x["remarks"] == f"remark={pt_pin}", envs))

# 打印结果
print(jd_cookies)
