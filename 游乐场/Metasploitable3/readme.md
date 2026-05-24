# Metasploitable3

Metasploitable3 是一个从头开始构建、包含大量安全漏洞的虚拟机。它旨在用作使用 [metasploit](https://github.com/rapid7/metasploit-framework) 测试漏洞利用的目标。

Metasploitable3 以 BSD 风格许可证发布。详情请参见 COPYING 文件。

## 快速开始

要使用 https://app.vagrantup.com/rapid7/ 上提供的预构建镜像，请创建一个新的本地 metasploitable 工作区：

Linux 用户：
```
mkdir metasploitable3-workspace
cd metasploitable3-workspace
curl -O https://raw.githubusercontent.com/rapid7/metasploitable3/master/Vagrantfile && vagrant up
```

Windows 用户：
```
mkdir metasploitable3-workspace
cd metasploitable3-workspace
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/rapid7/metasploitable3/master/Vagrantfile" -OutFile "Vagrantfile"
vagrant up
```

或者克隆此仓库并自行构建您的 box。

## 构建 Metasploitable 3

系统要求：
* 能够运行下面列出的所有必需应用程序的操作系统
* 推荐支持 VT-x/AMD-V 的处理器
* 驱动器上有 65 GB 可用空间
* 4.5 GB 内存

必需软件：

* [Packer](https://www.packer.io/intro/getting-started/install.html)
* [Vagrant](https://www.vagrantup.com/docs/installation/)
* [Vagrant Reload 插件](https://github.com/aidanns/vagrant-reload#installation)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)、libvirt/qemu-kvm、vmware（需要付费许可证）或 parallels（需要付费许可证）
* 互联网连接

### 自动构建：

1. - 在 **Linux/OSX** 上，运行 `./build.sh windows2008` 构建 Windows box，或运行 `./build.sh ubuntu1404` 构建 Linux box。如果 /tmp 空间较小，请使用 `TMPDIR=/var/tmp ./build.sh ...` 将临时 packer 磁盘映像存储在 /var/tmp 下。
   - 在 **Windows** 上，打开 powershell 终端，运行 `.\build.ps1 windows2008` 构建 Windows box，或运行 `.\build.ps1 ubuntu1404` 构建 Linux box。如果没有向脚本传递选项（即 `.\build.ps1`），则同时构建两个 box。
2. 如果两个 box 都成功构建，运行 `vagrant up` 启动两者。要启动任意一个 VM，可以使用：
    - `vagrant up ub1404`：启动 Linux box
    - `vagrant up win2k8`：启动 Windows box
3. 此过程完成后，您应该可以在 VirtualBox 中打开 VM 并登录。默认凭据为用户名：`vagrant`，密码：`vagrant`。

### 手动构建：

1. 克隆此仓库并导航到主目录。
2. 运行 `packer build --only=<provider> ./packer/templates/windows_2008_r2.json` 构建基础 VM 镜像，其中 `<provider>` 是您首选的可视化平台。目前支持 `virtualbox-iso`、`qemu` 和 `vmware-iso` 提供程序。第一次运行时需要下载操作系统安装 ISO，因此需要一段时间。
3. 创建基础 Vagrant box 后，需要将其添加到您的 Vagrant 环境中。可以使用命令 `vagrant box add packer/builds/windows_2008_r2_*_0.1.0.box --name=rapid7/metasploitable3-win2k8` 完成。
4. 如果尚未安装，请使用 `vagrant plugin install vagrant-reload` 安装 reload vagrant 供应程序。
5. 要启动 VM，运行命令 `vagrant up win2k8`。这将启动 VM 并运行所有必要的安装和配置脚本以完成所有设置。大约需要 10 分钟。
6. 此过程完成后，您可以在 VirtualBox 中打开 VM 并登录。默认凭据为：
    - 用户名：`vagrant`
    - 密码：`vagrant`

### ub1404 开发与修改

使用 Vagrant 和轻量级 Ubuntu 14.04 vagrant cloud box 镜像，您可以快速设置和定制 ub1404 Metasploitable3 以进行开发或定制。为此，请安装 Vagrant 和一个虚拟机管理程序，如 VirtualBox、VMWare 或 libvirt。

安装相关的提供程序插件：

    # virtualbox
    vagrant plugin install vagrant-vbguest

    # libvirt
    vagrant plugin install vagrant-libvirt

然后，导航到此仓库中的 [chef/dev/ub1404](chef/dev/ub1404) 目录。检查那里的 Vagrantfile。选择一个支持您提供程序的基础 box。

Metasploitable ub1404 使用 vagrant `chef-solo` 供应程序。在 Vagrantfile 中配置 chef_solo 块，使用您想要的 metasploitable chef 配方——您可以在 [chef/cookbooks/metasploitable](chef/cookbooks/metasploitable) 文件夹中浏览它们。或者，在那里添加或编辑您自己的 cookbook 和/或配方。

从 [chef/dev/ub1404](chef/dev/ub1404) 目录，您可以运行 `vagrant up` 获取一个开发虚拟 ub1404 实例。在初始的 `up` 构建和供应之后，当您编辑 chef runlist 或编辑 chef 配方时，请从同一目录运行 `vagrant rsync && vagrant provision`。为了更快的开发，您可以注释掉不需要重新运行的配方——但即使全部启用，vagrant 重新供应也不应超过一两分钟。Chef 旨在具有幂等性，因此您可以经常重新运行此命令。

考虑在修改配方之前拍摄快照（例如 `vagrant snapshot save fresh`），以便您可以始终恢复到初始状态（`vagrant restore fresh`）。如果您想要一个*完全*全新的快照，您可以使用 `vagrant up --no-provision` 进行初始化，然后拍摄快照，接着执行 `vagrant provision`。

## 漏洞列表
* [请参见 wiki 页面](https://github.com/rapid7/metasploitable3/wiki/Vulnerabilities)

## 更多信息
Wiki 包含更多详细信息，是文档的主要来源。请[查阅它](https://github.com/rapid7/metasploitable3/wiki/)。

## 致谢
此项目的 Windows 部分基于 GitHub 用户 [joefitzgerald](https://github.com/joefitzgerald) 的 [packer-windows](https://github.com/joefitzgerald/packer-windows) 项目。Packer 模板、原始 Vagrantfile 和安装应答文件被用作基础模板，并针对此项目的需求进行了构建。
