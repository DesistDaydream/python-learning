#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from ast import For, Try
import shutil
from urllib import request
import os, sys, stat
import tarfile
import logging

parser = argparse.ArgumentParser(description="Containerd 安装包生成工具")
parser.add_argument("-d", "--download-dir", default="/tmp/downloads", help="下载目录")
parser.add_argument("-w", "--work-dir", default="/tmp/downloads/work", help="工作目录")
parser.add_argument("-z", "--docker-version", default="20.10.23", help="docker 版本")
parser.add_argument("-x", "--docker-compose-version", default="2.16.0", help="docker compose 版本")
parser.add_argument("-c", "--containerd-version", default="1.6.6", help="containerd 版本")
parser.add_argument("-r", "--runc-version", default="1.1.2", help="Runc 版本")
parser.add_argument("-p", "--cni-plugin-version", default="1.1.1", help="CNI 插件版本")
parser.add_argument("-n", "--nerdctl-version", default="0.20.0", help="nerdctl 版本")
parser.add_argument("-a", "--arch", default="amd64", help="工具架构")
parser.add_argument("-l", "--log-level", default="info", help="日志级别.可用的值有: info,warn,debug")


class cli_flags:
    def __init__(self) -> None:
        # 解析命令行参数
        args = parser.parse_args()

        self.DownloadDir = args.download_dir
        self.WorkDir = args.work_dir
        self.DockerVersion = args.docker_version
        self.DockerComposeVersion = args.docker_compose_version
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
class files_handler:
    def __init__(self):
        # 文件名
        self.DockerFileName = "docker-{}.tgz".format(flags.DockerVersion)
        self.DockerServiceFileName = "docker.service"
        self.DockerCompletionFileName = "docker"
        self.DockerComposeFileName = "docker-compose"
        # 文件保存路径
        self.DockerFilePath = "{}/{}".format(flags.DownloadDir, self.DockerFileName)
        self.DockerServiceFilePath = "{}/{}".format(flags.DownloadDir, self.DockerServiceFileName)
        self.DockerCompletionFilePath = "{}/{}".format(flags.DownloadDir, self.DockerCompletionFileName)
        self.DockerComposeFilePath = "{}/{}".format(flags.DownloadDir, self.DockerComposeFileName)
        # 下载文件的 URL
        self.DockerURL = "https://download.docker.com/linux/static/stable/x86_64/{}".format(self.DockerFileName)
        self.DockerServiceURL = "https://raw.githubusercontent.com/moby/moby/v{}/contrib/init/systemd/{}".format(
            flags.DockerVersion, self.DockerServiceFileName
        )
        self.DockerCompletionURL = (
            "https://raw.githubusercontent.com/docker/cli/v{}/contrib/completion/bash/docker".format(
                flags.DockerVersion
            )
        )
        self.DockerComposeURL = (
            "https://github.com/docker/compose/releases/download/v{}/docker-compose-linux-x86_64".format(
                flags.DockerComposeVersion
            )
        )

    def downloadFiles(self):
        logging.debug("Docker Service 下载 URL: {}".format(self.DockerServiceURL))
        logging.debug("Docker Completion 文件 下载 URL: {}".format(self.DockerCompletionURL))
        logging.debug("Docker 下载 URL: {}".format(self.DockerURL))
        logging.debug("Docker Compose 下载 URL: {}".format(self.DockerComposeURL))

        # 创建下载目录
        if not os.path.exists(flags.DownloadDir):
            os.makedirs(flags.DownloadDir)

        # 下载 tar 包
        # TODO: 验证下载结果
        if not os.path.exists(self.DockerServiceFilePath):
            request.urlretrieve(self.DockerServiceURL, self.DockerServiceFilePath)
        if not os.path.exists(self.DockerCompletionFilePath):
            request.urlretrieve(self.DockerCompletionURL, self.DockerCompletionFilePath)
        if not os.path.exists(self.DockerFilePath):
            request.urlretrieve(self.DockerURL, self.DockerFilePath)
        if not os.path.exists(self.DockerComposeFilePath):
            request.urlretrieve(self.DockerComposeURL, self.DockerComposeFilePath)

    # 提取文件
    def extractingFiles(self):
        # 创建目录
        os.makedirs(flags.WorkDir + "/etc/systemd/system", exist_ok=True)
        os.makedirs(flags.WorkDir + "/usr/share/bash-completion/completions", exist_ok=True)
        os.makedirs(flags.WorkDir + "/usr/local/bin", exist_ok=True)

        # 提取 Docker
        extracting(self.DockerFilePath, flags.WorkDir + "/usr/bin/")

        # 将 Docker 的 Service 文件拷贝到指定目录
        if not os.path.exists(flags.WorkDir + "/etc/systemd/system/" + self.DockerServiceFileName):
            shutil.copy2(self.DockerServiceFilePath, flags.WorkDir + "/etc/systemd/system/")

        # 将 Docker 的命令行补全文件拷贝到指定目录
        if not os.path.exists(
            flags.WorkDir + "/usr/share/bash-completion/completions/" + self.DockerCompletionFileName
        ):
            shutil.copy2(self.DockerCompletionFilePath, flags.WorkDir + "/usr/share/bash-completion/completions/")

        # 将 docker-compose 文件拷贝到指定目录，并赋予权限
        if not os.path.exists(flags.WorkDir + "/usr/local/bin/" + self.DockerComposeFileName):
            shutil.copy2(self.DockerComposeFilePath, flags.WorkDir + "/usr/local/bin/")
            os.chmod(
                flags.WorkDir + "/usr/local/bin/" + self.DockerComposeFileName,
                stat.S_IRWXU + stat.S_IRGRP + stat.S_IXGRP + stat.S_IROTH,
            )

        # # 提取 CNI Plugins
        # extracting(self.CNIpluginFilePath, flags.WorkDir + "/opt/cni/bin/")

        # # 提取 Nerdctl
        # extracting(self.NerdctlFilePath, flags.WorkDir + "/usr/local/bin/")


def handleFiles(flags: cli_flags):
    # 生成 nerdctl 的命令行补全
    if not os.path.exists(flags.WorkDir + "/usr/share/bash-completion/completions"):
        os.makedirs(flags.WorkDir + "/usr/share/bash-completion/completions")
    nedctlCMD = "{0}/usr/local/bin/nerdctl completion bash > {0}/usr/share/bash-completion/completions/nerdctl".format(
        flags.WorkDir
    )
    # 非 root 环境执行这个命令会有一些 WARN，忽略即可
    os.system(nedctlCMD)

    # 生成 crictl 配置文件
    # TODO: 有必要做嘛？


if __name__ == "__main__":
    flags = cli_flags()
    initLogging()

    # 实例化文件处理器
    files = files_handler()

    # 下载文件
    files.downloadFiles()
    # 提取文件
    files.extractingFiles()
    # 提取文件后，处理归档目录以满足归档条件
    # handleFiles(flags)
    # 归档，生成归档文件
    archiving(flags.WorkDir, flags.DownloadDir + "/docker-ehualu-{}.tar.gz".format(flags.DockerVersion))
