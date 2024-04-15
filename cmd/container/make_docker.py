#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from ast import For, Try
import shutil
from urllib import request
import os, sys, stat
import tarfile
import logging
import json
import fileinput


parser = argparse.ArgumentParser(description="Docker 部署包生成工具")
parser.add_argument("-d", "--download-dir", default="/tmp/downloads", help="下载目录")
parser.add_argument("-w", "--work-dir", default="/tmp/downloads/work", help="工作目录")
# runc、containerd 版本都是多少？这里涉及到使用的 containerd.service，如何通过代码确定当前版本的 docker 所使用的 containerd 版本呢？
parser.add_argument("-z", "--docker-version", default="24.0.6", help="docker 版本")
parser.add_argument("-x", "--docker-compose-version", default="2.24.2", help="docker compose 版本")
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
        self.ContainerdServiceFileName = "containerd.service"
        self.DockerFileName = "docker-{}.tgz".format(flags.DockerVersion)
        self.DockerServiceFileName = "docker.service"
        self.DockerSocketFileName = "docker.socket"
        self.DockerCompletionFileName = "docker"
        self.DockerComposeFileName = "docker-compose"
        # 文件保存路径
        self.ContainerdServiceFilePath = "{}/{}".format(flags.DownloadDir, self.ContainerdServiceFileName)
        self.DockerFilePath = "{}/{}".format(flags.DownloadDir, self.DockerFileName)
        self.DockerServiceFilePath = "{}/{}".format(flags.DownloadDir, self.DockerServiceFileName)
        self.DockerSocketFilePath = "{}/{}".format(flags.DownloadDir, self.DockerSocketFileName)
        self.DockerCompletionFilePath = "{}/{}".format(flags.DownloadDir, self.DockerCompletionFileName)
        self.DockerComposeFilePath = "{}/{}".format(flags.DownloadDir, self.DockerComposeFileName)
        # 下载文件的 URL
        self.ContainerdServiceURL = "https://raw.githubusercontent.com/containerd/containerd/main/{}".format(
            self.ContainerdServiceFileName
        )
        # https://download.docker.com/linux/static/stable/x86_64/docker-24.0.6.tgz
        self.DockerURL = "https://download.docker.com/linux/static/stable/x86_64/{}".format(self.DockerFileName)
        self.DockerServiceURL = "https://raw.githubusercontent.com/moby/moby/v{}/contrib/init/systemd/{}".format(
            flags.DockerVersion, self.DockerServiceFileName
        )
        self.DockerSocketURL = "https://raw.githubusercontent.com/moby/moby/v{}/contrib/init/systemd/{}".format(
            flags.DockerVersion, self.DockerSocketFileName
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
        logging.debug("Containerd Service 下载 URL: {}".format(self.ContainerdServiceURL))
        logging.debug("Docker Service 下载 URL: {}".format(self.DockerServiceURL))
        logging.debug("Docker Socket 下载 URL: {}".format(self.DockerSocketURL))
        logging.debug("Docker Completion 文件 下载 URL: {}".format(self.DockerCompletionURL))
        logging.debug("Docker 下载 URL: {}".format(self.DockerURL))
        logging.debug("Docker Compose 下载 URL: {}".format(self.DockerComposeURL))

        # 创建下载目录
        if not os.path.exists(flags.DownloadDir):
            os.makedirs(flags.DownloadDir)

        # 下载 tar 包
        # TODO: 验证下载结果
        if not os.path.exists(self.ContainerdServiceFilePath):
            request.urlretrieve(self.ContainerdServiceURL, self.ContainerdServiceFilePath)
        if not os.path.exists(self.DockerServiceFilePath):
            request.urlretrieve(self.DockerServiceURL, self.DockerServiceFilePath)
        if not os.path.exists(self.DockerSocketFilePath):
            request.urlretrieve(self.DockerSocketURL, self.DockerSocketFilePath)
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
        os.makedirs(flags.WorkDir + "/usr/bin", exist_ok=True)
        os.makedirs(flags.WorkDir + "/etc/docker", exist_ok=True)

        # 拷贝 containerd.service 文件到工作目录
        if not os.path.exists(flags.WorkDir + "/etc/systemd/system/" + self.ContainerdServiceFileName):
            shutil.copy2(self.ContainerdServiceFilePath, flags.WorkDir + "/etc/systemd/system/")

        # 提取 Docker
        extracting(self.DockerFilePath, flags.WorkDir)
        docker_files = os.listdir(flags.WorkDir + "/docker/")
        for file in docker_files:
            shutil.move(flags.WorkDir + "/docker/" + file, flags.WorkDir + "/usr/bin/" + file)

        # 将 Docker 的 Service 文件拷贝到工作目录
        if not os.path.exists(flags.WorkDir + "/etc/systemd/system/" + self.DockerServiceFileName):
            shutil.copy2(self.DockerServiceFilePath, flags.WorkDir + "/etc/systemd/system/")
        if not os.path.exists(flags.WorkDir + "/etc/systemd/system/" + self.DockerSocketFileName):
            shutil.copy2(self.DockerSocketFilePath, flags.WorkDir + "/etc/systemd/system/")

        # 将 Docker 的命令行补全文件拷贝到工作目录
        if not os.path.exists(
            flags.WorkDir + "/usr/share/bash-completion/completions/" + self.DockerCompletionFileName
        ):
            shutil.copy2(self.DockerCompletionFilePath, flags.WorkDir + "/usr/share/bash-completion/completions/")

        # 将 docker-compose 文件拷贝到工作目录，并赋予权限
        # binDir = "/usr/local/bin/" # 独立形式
        binDir = "/root/.docker/cli-plugins/" # 插件形式
        os.makedirs(flags.WorkDir + binDir, exist_ok=True)
        if not os.path.exists(flags.WorkDir + binDir + self.DockerComposeFileName):
            shutil.copy2(self.DockerComposeFilePath, flags.WorkDir + binDir)
            os.chmod(
                flags.WorkDir + binDir + self.DockerComposeFileName,
                stat.S_IRWXU + stat.S_IRGRP + stat.S_IXGRP + stat.S_IROTH,
            )


def handleFiles(flags: cli_flags):
    config = {
        "experimental": True,
        "registry-mirrors": ["https://ac1rmo5p.mirror.aliyuncs.com"],
        "exec-opts": ["native.cgroupdriver=systemd"],
        "default-address-pools": [{"base": "10.38.0.0/16", "size": 24}],
        "live-restore": True,
        "log-driver": "json-file",
        "log-opts": {"max-size": "10m", "max-file": "10"},
        "storage-driver": "overlay2",
        # "storage-opts": ["overlay2.override_kernel_check=true"],
    }

    json_str = json.dumps(config, indent=2)
    with open(flags.WorkDir + "/etc/docker/daemon.json", "w") as f:
        f.write(json_str)

    # 修改 containerd.service 文件
    for line in fileinput.input(flags.WorkDir + "/etc/systemd/system/containerd.service" , inplace=True):
        line = line.replace("ExecStart=/usr/local/bin/containerd", "ExecStart=/usr/bin/containerd")
        print(line, end="")

    # 修改 docker.socket 文件
    for line in fileinput.input(flags.WorkDir + "/etc/systemd/system/docker.socket", inplace=True):
        line = line.replace("ListenStream=/run/docker.sock", "ListenStream=/var/run/docker.sock")
        line = line.replace("SocketGroup=docker", "SocketGroup=root")
        print(line, end="")

    # 在 docker.service 文件中判断 ExecStartPost=/usr/sbin/iptables -P FORWARD ACCEPT 字符串是否存在，如果不存在，则在将其插入到以 ExecStart 开头的串字符串所在行的上一行
    file_path = flags.WorkDir + "/etc/systemd/system/docker.service"

    for line in fileinput.input(file_path, inplace=True):
        if line.strip().startswith("ExecStartPost=/usr/sbin/iptables -P FORWARD ACCEPT"):
            continue
        elif line.strip().startswith("ExecStart"):
            print("ExecStartPost=/usr/sbin/iptables -P FORWARD ACCEPT\n" + line, end="")
        else:
            print(line, end="")


if __name__ == "__main__":
    flags = cli_flags()
    initLogging()

    # 实例化文件处理器
    files = files_handler()

    logging.debug("当前工作路径: {}".format(os.getcwd()))

    # 下载文件
    files.downloadFiles()
    # 提取文件
    files.extractingFiles()
    # 提取文件后，处理归档目录以满足归档条件
    handleFiles(flags)
    # 归档，生成归档文件
    archiving(flags.WorkDir, flags.DownloadDir + "/docker-dd-{}.tar.gz".format(flags.DockerVersion))
