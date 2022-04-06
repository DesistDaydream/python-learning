#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 解析命令行参数
import argparse

# 实例化解析器
parser = argparse.ArgumentParser(description="Python CLI tools")
parser.add_argument("-a", "--args-one", default="HelloWorld", help="参数一")

# 解析命令行参数功能
class cli_flags:
    def __init__(self) -> None:
        # 解析命令行参数
        cliArgs = parser.parse_args()

        self.ArgsOne = cliArgs.args_one


if __name__ == "__main__":
    # 实例化命令行参数
    args = cli_flags()

    # 获取参数
    print(args.args_one)
