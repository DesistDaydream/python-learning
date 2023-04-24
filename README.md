# python-learning

更新 pip
`pip install --upgrade pip`

对于 Python 开发用户来讲，PIP 安装软件包是家常便饭。但国外的源下载速度实在太慢，浪费时间。而且经常出现下载后安装出错问题。所以把 PIP 安装源替换成国内镜像，可以大幅提升下载速度，还可以提高安装成功率。

国内源：
新版 ubuntu 要求使用 https 源，要注意。

- 清华：https://pypi.tuna.tsinghua.edu.cn/simple
- 阿里云：http://mirrors.aliyun.com/pypi/simple/
- 中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/
- 华中理工大学：http://pypi.hustunique.com/
- 山东理工大学：http://pypi.sdutlinux.org/
- 豆瓣：http://pypi.douban.com/simple/

临时使用：
可以在使用 pip 的时候加参数 `-i https://pypi.tuna.tsinghua.edu.cn/simple`

例如：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyspider`，这样就会从清华这边的镜像去安装 pyspider 库。

永久修改，一劳永逸：
Linux 下，修改 ~/.pip/pip.conf (没有就创建一个文件夹及文件。文件夹要加“.”，表示是隐藏文件夹)

内容如下：

[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host=mirrors.aliyun.com
windows 下，直接在 user 目录中创建一个 pip 目录，如：C:\Users\xx\pip，新建文件 pip.ini。内容同上。

# practice

https://www.bilibili.com/video/BV1T34y1o73U

# 虚拟环境

最小化的虚拟化境依赖包

```
├── _distutils_hack
├── distutils-precedence.pth
├── pip
├── pip-23.1.1.dist-info
├── pkg_resources
├── setuptools
└── setuptools-65.5.0.dist-info
```
