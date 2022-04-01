import unittest
import type


class TestType(unittest.TestCase):
    # 必须以 test 开头的方法才是测试方法，在执行测试指令时才会被执行
    def testFormatOutput(self):
        type.formatOutput()


if __name__ == "__main__":
    unittest.main()
