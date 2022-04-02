#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from urllib import request
import tarfile

parser = argparse.ArgumentParser(description="CDN curl tools")
parser.add_argument("-c", "--containerd-version", default="1.6.2", help="containerd 版本")
parser.add_argument("-n", "--nerdctl-version", default="0.18.0", help="nerdctl 版本")


class cli_flags:
    def __init__(self) -> None:
        # 解析命令行参数
        args = parser.parse_args()

        self.ContainerdVersion = args.containerd_version
        self.NerdctlVersion = args.nerdctl_version


def extract(tar_path, target_path):
    try:
        tar = tarfile.open(tar_path, "r:gz")
        file_names = tar.getnames()
        for file_name in file_names:
            tar.extract(file_name, target_path)
        tar.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    flags = cli_flags()

    containerdURL = (
        "https://github.com/containerd/containerd/releases/download/v{0}/cri-containerd-{0}-linux-amd64.tar.gz".format(
            flags.ContainerdVersion
        )
    )
    nerdctlURL = "https://github.com/containerd/nerdctl/releases/download/v{0}/nerdctl-{0}-linux-arm64.tar.gz".format(
        flags.NerdctlVersion
    )
    print(containerdURL)
    print(nerdctlURL)

    containerdFile = "cri-containerd-{0}-linux-amd64.tar.gz".format(flags.ContainerdVersion)
    nerdctlFile = "nerdctl-{0}-linux-arm64.tar.gz".format(flags.NerdctlVersion)

    # request.urlretrieve(containerdURL, containerdFile)
    # request.urlretrieve(nerdctlURL, nerdctlFile)

    extract(containerdFile, "/mnt/e/Projects/DesistDaydream/python-learning")
    extract(nerdctlFile, "/mnt/e/Projects/DesistDaydream/python-learning")
