import os
import shutil
import sysconfig
import fnmatch

# 要保留的文件和目录列表
keep_files_dirs = [
    "README.txt",
    # PIP 包
    "pip",
    # setuptools 包
    "_distutils_hack",
    "pkg_resources",
    "setuptools",
    "distutils-precedence.pth",
]

# 使用通配符匹配的文件和目录模式
keep_pattern = [
    "pip-*.dist-info",
    "setuptools-*.dist-info",
]

# 获取 site-packages 目录路径
site_packages_path = sysconfig.get_paths()["purelib"]

# 遍历 site-packages 目录下的所有文件和目录
for item in os.listdir(site_packages_path):
    item_path = os.path.join(site_packages_path, item)

    # 检查当前项是否在保留列表或匹配的通配符模式中
    if item not in keep_files_dirs and not any(fnmatch.fnmatch(item, pattern) for pattern in keep_pattern):
        if os.path.isdir(item_path):
            print(f"Deleting directory: {item_path}")
            shutil.rmtree(item_path)  # 删除目录
        else:
            print(f"Deleting file: {item_path}")
            os.remove(item_path)  # 删除文件
