try:
    print("try...")
    r = 10 / 0
    print("result:", r)
except ZeroDivisionError as err:
    print("except:", err)
finally:
    print("finally...")
print("END")
