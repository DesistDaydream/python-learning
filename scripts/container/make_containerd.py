#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from ast import For, Try
import shutil
from urllib import request
import os
import tarfile
import logging


parser = argparse.ArgumentParser(description="CDN curl tools")
parser.add_argument("-d", "--download-dir", default="/root/downloads", help="下载目录")
parser.add_argument("-w", "--work-dir", default="/root/downloads/work", help="工作目录")
parser.add_argument("-c", "--containerd-version", default="1.6.2", help="containerd 版本")
parser.add_argument("-n", "--nerdctl-version", default="0.18.0", help="nerdctl 版本")
parser.add_argument("-a", "--arch", default="amd64", help="工具架构")
parser.add_argument("-l", "--log-level", default="info", help="工具架构")


class cli_flags:
    def __init__(self) -> None:
        # 解析命令行参数
        args = parser.parse_args()

        self.DownloadDir = args.download_dir
        self.WorkDir = args.work_dir
        self.ContainerdVersion = args.containerd_version
        self.NerdctlVersion = args.nerdctl_version
        self.Arch = args.arch

        self.LogLevel = args.log_level


def initLogging():
    loglevel = {"info": logging.INFO, "warn": logging.WARN, "debug": logging.DEBUG}

    logging.basicConfig(
        level=loglevel[flags.LogLevel],
        format="[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %a %H:%M:%S",
        # filename="test.log",
        # filemode="w",
    )


def archiving():
    # 改变工作路径以去掉所有待归档文件的前缀
    os.chdir(flags.WorkDir)
    logging.debug("当前工作路径: {}".format(os.getcwd()))

    # 创建归档文件
    tar = tarfile.open(flags.DownloadDir + "/ehualu-containerd-{}.tar.gz".format(flags.ContainerdVersion), "w:gz")

    # 开始归档
    for root, dir, files in os.walk("."):
        for file in files:
            fullpath = os.path.join(root, file)
            tar.add(fullpath)
    tar.close()

    # os.system(
    #     "cd {};tar -zcvf {}/ehualu-containerd-{}.tar.gz *".format(
    #         flags.WorkDir, flags.DownloadDir, flags.ContainerdVersion
    #     )
    # )


def extracting(tar_path, target_path):
    try:
        tar = tarfile.open(tar_path, "r:gz")
        file_names = tar.getnames()
        for file_name in file_names:
            tar.extract(file_name, target_path)
        tar.close()
    except Exception as e:
        print(e)


def downloadFiles(flags: cli_flags):
    containerdFileName = "cri-containerd-cni-{}-linux-{}.tar.gz".format(flags.ContainerdVersion, flags.Arch)
    nerdctlFileName = "nerdctl-{}-linux-{}.tar.gz".format(flags.NerdctlVersion, flags.Arch)

    containerdURL = "https://github.com/containerd/containerd/releases/download/v{}/{}".format(
        flags.ContainerdVersion, containerdFileName
    )
    nerdctlURL = "https://github.com/containerd/nerdctl/releases/download/v{}/{}".format(
        flags.NerdctlVersion, nerdctlFileName
    )
    logging.debug("Containerd 下载 URL: {}".format(containerdURL))
    logging.debug("Nerdctl 下载 URL: {}".format(nerdctlURL))

    containerdFile = "{}/{}".format(flags.DownloadDir, containerdFileName)
    nerdctlFile = "{}/{}".format(flags.DownloadDir, nerdctlFileName)

    # 下载 tar 包
    # TODO: 验证下载结果
    if not os.path.exists(containerdFile):
        request.urlretrieve(containerdURL, containerdFile)
    if not os.path.exists(nerdctlFile):
        request.urlretrieve(nerdctlURL, nerdctlFile)

    # 提取文件
    extracting(containerdFile, flags.WorkDir)
    extracting(nerdctlFile, flags.WorkDir)


def handleFiles():
    # 生成 nerdctl 的命令行补全
    if not os.path.exists(flags.WorkDir + "/usr/share/bash-completion/completions"):
        os.makedirs(flags.WorkDir + "/usr/share/bash-completion/completions")

    # 删除一些没用的文件
    needDeleteFiles = ["containerd-rootless-setuptool.sh", "containerd-rootless.sh"]
    for file in needDeleteFiles:
        filePath = flags.WorkDir + "/" + file
        if os.path.exists(filePath):
            os.remove(filePath)

    # 将 nerdctl 移动到 /usr/local/bin 下
    if not os.path.exists(flags.WorkDir + "/usr/local/bin/nerdctl"):
        shutil.move(flags.WorkDir + "/nerdctl", flags.WorkDir + "/usr/local/bin")
        os.system(
            "/root/downloads/work/usr/local/bin/nerdctl completion bash > /root/downloads/work/usr/share/bash-completion/completions/nerdctl"
        )


if __name__ == "__main__":
    flags = cli_flags()
    initLogging()

    # 下载文件
    downloadFiles(flags)
    # 提取文件后，处理归档目录以满足归档条件
    handleFiles()
    # 归档，生成归档文件
    archiving()
