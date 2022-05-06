#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from ast import For, Try
import shutil
from urllib import request
import os, sys, stat
import tarfile
import logging


parser = argparse.ArgumentParser(description="CDN curl tools")
parser.add_argument("-d", "--download-dir", default="/tmp/downloads", help="下载目录")
parser.add_argument("-w", "--work-dir", default="/tmp/downloads/work", help="工作目录")
parser.add_argument("-c", "--containerd-version", default="1.6.4", help="containerd 版本")
parser.add_argument("-r", "--runc-version", default="1.1.1", help="Runc 版本")
parser.add_argument("-p", "--cni-plugin-version", default="1.1.1", help="CNI 插件版本")
parser.add_argument("-n", "--nerdctl-version", default="0.19.0", help="nerdctl 版本")
parser.add_argument("-a", "--arch", default="amd64", help="工具架构")
parser.add_argument("-l", "--log-level", default="info", help="日志级别.可用的值有: info,warn,debug")


class cli_flags:
    def __init__(self) -> None:
        # 解析命令行参数
        args = parser.parse_args()

        self.DownloadDir = args.download_dir
        self.WorkDir = args.work_dir
        self.ContainerdVersion = args.containerd_version
        self.RuncVersion = args.runc_version
        self.CNIPluginVersion = args.cni_plugin_version
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


def archiving(src: str, dest: str):
    # 改变工作路径以去掉所有待归档文件的前缀
    os.chdir(src)
    logging.debug("当前工作路径: {}".format(os.getcwd()))

    # 创建归档文件
    tar = tarfile.open(dest, "w:gz")

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


def extracting(tar_path: str, target_path: str):
    try:
        tar = tarfile.open(tar_path, "r:gz")
        file_names = tar.getnames()
        for file_name in file_names:
            tar.extract(file_name, target_path)
        tar.close()
    except Exception as e:
        print(e)


# 文件处理器。下载、解压、处理。继承了命令行标志
class files_handler(cli_flags):
    def __init__(self):
        # containerdFileName = "cri-containerd-cni-{}-linux-{}.tar.gz".format(flags.ContainerdVersion, flags.Arch)
        self.containerdFileName = "containerd-{}-linux-{}.tar.gz".format(flags.ContainerdVersion, flags.Arch)
        self.containerdServiceFileName = "containerd.service"
        self.runcFileName = "runc.{}".format(flags.Arch)
        self.cnipluginFileName = "cni-plugins-linux-{}-v{}.tgz".format(flags.Arch, flags.CNIPluginVersion)
        self.nerdctlFileName = "nerdctl-{}-linux-{}.tar.gz".format(flags.NerdctlVersion, flags.Arch)
        self.containerdFile = ""
        self.containerdServiceFile = ""
        self.runcFile = ""
        self.cnipluginFile = ""
        self.nerdctlFile = ""

    def downloadFiles(self):
        containerdURL = "https://github.com/containerd/containerd/releases/download/v{}/{}".format(
            flags.ContainerdVersion, self.containerdFileName
        )
        containerdServiceURL = "https://raw.githubusercontent.com/containerd/containerd/main/{}".format(
            self.containerdServiceFileName
        )
        runcURL = "https://github.com/opencontainers/runc/releases/download/v{}/{}".format(
            flags.RuncVersion, self.runcFileName
        )
        cnipluginURL = "https://github.com/containernetworking/plugins/releases/download/v{}/{}".format(
            flags.CNIPluginVersion, self.cnipluginFileName
        )
        nerdctlURL = "https://github.com/containerd/nerdctl/releases/download/v{}/{}".format(
            flags.NerdctlVersion, self.nerdctlFileName
        )
        logging.debug("Containerd 下载 URL: {}".format(containerdURL))
        logging.debug("Containerd Service 下载 URL: {}".format(containerdServiceURL))
        logging.debug("Runc 下载 URL: {}".format(runcURL))
        logging.debug("CNI Plugin 下载 URL: {}".format(cnipluginURL))
        logging.debug("Nerdctl 下载 URL: {}".format(nerdctlURL))

        self.containerdFile = "{}/{}".format(flags.DownloadDir, self.containerdFileName)
        self.containerdServiceFile = "{}/{}".format(flags.DownloadDir, self.containerdServiceFileName)
        self.runcFile = "{}/{}".format(flags.DownloadDir, self.runcFileName)
        self.cnipluginFile = "{}/{}".format(flags.DownloadDir, self.cnipluginFileName)
        self.nerdctlFile = "{}/{}".format(flags.DownloadDir, self.nerdctlFileName)

        # 下载 tar 包
        # TODO: 验证下载结果
        if not os.path.exists(self.containerdFile):
            request.urlretrieve(containerdURL, self.containerdFile)
        if not os.path.exists(self.containerdServiceFile):
            request.urlretrieve(containerdServiceURL, self.containerdServiceFile)
        if not os.path.exists(self.runcFile):
            request.urlretrieve(runcURL, self.runcFile)
        if not os.path.exists(self.cnipluginFile):
            request.urlretrieve(cnipluginURL, self.cnipluginFile)
        if not os.path.exists(self.nerdctlFile):
            request.urlretrieve(nerdctlURL, self.nerdctlFile)

    # 提取文件
    def extractingFiles(self):
        # 提取 Containerd
        extracting(self.containerdFile, flags.WorkDir + "/usr/local/")

        # 提取 Containerd 的 Service
        if not os.path.exists(flags.WorkDir + "/etc/systemd/system"):
            os.makedirs(flags.WorkDir + "/etc/systemd/system")
        if not os.path.exists(flags.WorkDir + "/etc/systemd/system/" + self.containerdServiceFileName):
            shutil.move(self.containerdServiceFile, flags.WorkDir + "/etc/systemd/system/")

        # 提取 runc
        if not os.path.exists(flags.WorkDir + "/usr/local/sbin"):
            os.makedirs(flags.WorkDir + "/usr/local/sbin")
        shutil.move(self.runcFile, flags.WorkDir + "/usr/local/sbin/runc")
        os.chmod(flags.WorkDir + "/usr/local/sbin/runc", stat.S_IRWXU + stat.S_IRGRP + stat.S_IXGRP + stat.S_IROTH)

        # 提取 CNI Plugins
        extracting(self.cnipluginFile, flags.WorkDir + "/opt/cni/bin/")

        # 提取 Nerdctl
        extracting(self.nerdctlFile, flags.WorkDir + "/usr/local/bin/")


def handleFiles():
    # 生成 nerdctl 的命令行补全
    if not os.path.exists(flags.WorkDir + "/usr/share/bash-completion/completions"):
        os.makedirs(flags.WorkDir + "/usr/share/bash-completion/completions")

    # 删除 nerdctl 的一些没用的文件
    needDeleteFiles = ["containerd-rootless-setuptool.sh", "containerd-rootless.sh"]
    for file in needDeleteFiles:
        filePath = flags.WorkDir + "/usr/local/bin/" + file
        if os.path.exists(filePath):
            os.remove(filePath)

    # 将 nerdctl 移动到 /usr/local/bin 下
    nedctlCMD = "{0}/usr/local/bin/nerdctl completion bash > {0}/usr/share/bash-completion/completions/nerdctl".format(
        flags.WorkDir
    )
    os.system(nedctlCMD)

    # 生成 crictl 配置文件
    # TODO: 有必要做嘛？


if __name__ == "__main__":
    flags = cli_flags()
    initLogging()

    # # 实例化文件处理器
    # files = files_handler()

    # # 下载文件
    # files.downloadFiles()
    # # 提取文件
    # files.extractingFiles()
    # # 提取文件后，处理归档目录以满足归档条件
    # handleFiles()
    # 归档，生成归档文件
    archiving(flags.WorkDir, flags.DownloadDir + "/ehualu-containerd-{}.tar.gz".format(flags.ContainerdVersion))
