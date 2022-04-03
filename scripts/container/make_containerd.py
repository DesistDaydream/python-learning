#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from ast import For
import shutil
from urllib import request
import os
import tarfile


parser = argparse.ArgumentParser(description="CDN curl tools")
parser.add_argument("-d", "--download-dir", default="/root/downloads", help="下载目录")
parser.add_argument("-w", "--work-dir", default="/root/downloads/work", help="工作目录")
parser.add_argument("-c", "--containerd-version", default="1.6.2", help="containerd 版本")
parser.add_argument("-n", "--nerdctl-version", default="0.18.0", help="nerdctl 版本")
parser.add_argument("-a", "--arch", default="amd64", help="工具架构")


class cli_flags:
    def __init__(self) -> None:
        # 解析命令行参数
        args = parser.parse_args()

        self.DownloadDir = args.download_dir
        self.WorkDir = args.work_dir
        self.ContainerdVersion = args.containerd_version
        self.NerdctlVersion = args.nerdctl_version
        self.Arch = args.arch


def extract(tar_path, target_path):
    try:
        tar = tarfile.open(tar_path, "r:gz")
        file_names = tar.getnames()
        for file_name in file_names:
            tar.extract(file_name, target_path)
        tar.close()
    except Exception as e:
        print(e)


def downloadFiles(flags: cli_flags):
    containerdName = "cri-containerd-cni-{}-linux-{}.tar.gz".format(flags.ContainerdVersion, flags.Arch)
    nerdctalName = "nerdctl-{}-linux-{}.tar.gz".format(flags.NerdctlVersion, flags.Arch)

    containerdURL = "https://github.com/containerd/containerd/releases/download/v{}/{}".format(
        flags.ContainerdVersion, containerdName
    )
    nerdctlURL = "https://github.com/containerd/nerdctl/releases/download/v{}/{}".format(
        flags.NerdctlVersion, nerdctalName
    )
    print(containerdURL)
    print(nerdctlURL)

    containerdFile = "{}/{}".format(flags.DownloadDir, containerdName)
    nerdctlFile = "{}/{}".format(flags.DownloadDir, nerdctalName)

    # 下载 tar 包
    if not os.path.exists(containerdFile):
        request.urlretrieve(containerdURL, containerdFile)
    if not os.path.exists(nerdctlFile):
        request.urlretrieve(nerdctlURL, nerdctlFile)

    # 解包
    extract(containerdFile, flags.WorkDir)
    extract(nerdctlFile, flags.WorkDir)


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

    # tar = tarfile.open(flags.WorkDir + "/ehualu-containerd.tar.gz","r:gz")
    # tar.
    os.system(
        "cd {};tar -zcvf {}/ehualu-containerd-{}.tar.gz *".format(
            flags.WorkDir, flags.DownloadDir, flags.ContainerdVersion
        )
    )


if __name__ == "__main__":
    flags = cli_flags()

    downloadFiles(flags)
    handleFiles()
