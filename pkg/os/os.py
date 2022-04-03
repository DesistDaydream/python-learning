#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

# 获取当前目录
CurrentDir = os.getcwd()
print("当前目录为: ", CurrentDir)

# 列出目录下的所有文件，若省略参数，则默认列出当前目录下的文件
print(os.listdir())
