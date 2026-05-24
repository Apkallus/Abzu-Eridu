下载二进制工具后移动到其中一个命令 PATH `/usr/local/bin`

VMware Workstation linux 安装
- 安装依赖项 `sudo apt install build-essential linux-headers-$(uname -r)`

安装 packer 插件
```sh
# 安装 vmware 插件
packer plugins install github.com/vmware/vmware

# 安装 post-processor vagrant 插件
# 复制配置文件到 metasploitable3 构建目录下新建的 .pkr.hcl 配置文件 https://github.com/hashicorp/packer-plugin-vagrant/blob/main/README.md
# 设置模板插件
packer init .
```

模板文件中设置网络适配参数
`./packer/templates/windows_2008_r2.json` 的 vmware 中设置 "network_adapter_type": "vmxnet3"

自动下载的 CA 异常，手动下载后
`./packer/templates/windows_2008_r2.json` 设置原 url 为手动下载后的文件路径
```sh
# "variables": {
#     "iso_url": "https://download.microsoft.com/download/4/1/D/41DEA7E0-B30D-4012-A1E3-F24DC03BA1BB/7601.17514.101119-1850_x64fre_server_eval_en-us-GRMSXEVAL_EN_DVD.iso",
"iso_url": "file:///home/apkallus/metasploitable3-master/iso/7601.17514.101119-1850_x64fre_server_eval_en-us-GRMSXEVAL_EN_DVD.iso",
```

继续构建 VM 基础镜像，但缺乏 libaio，然而 libaio 已经更名
```sh
# 查看包位置
dpkg -L libaio1t64
# 创建库链接，设置旧名到新库
sudo ln -sf /usr/lib/x86_64-linux-gnu/libaio.so.1t64.0.2 /usr/lib/libaio.so.1
```

vm 内开启嵌套虚拟
systeminfo 查看物理机信息，发现 Virtualization-based security 启用
下载 Device Guard and Credential Guard hardware readiness tool 工具 https://www.microsoft.com/en-us/download/details.aspx?id=53337
允许脚本执行 Set-ExecutionPolicy Unrestricted -Scope Process -Force
执行脚本 .\DG_Readiness_Tool_v3.6.ps1 -Disable -AutoReboot 并重启

atips 转为使用预构建 box：
- 核心故障为多个虚拟化不兼容，于是关闭物理机中的虚拟化后开启嵌套虚拟化
    - 然而 Virtualization-based security 似乎无法手动关闭，于是下载 windows 工具以关闭
    - 文章
        https://community.broadcom.com/vmware-cloud-foundation/discussion/disabling-hyper-v-hypervisor-on-windows-11-pro-host-to-get-vmware-17s-cpl0-vs-ulm-monitor-mode
- 使用预构建 box
    - 预构建 box 链接失效，迁移到
        https://portal.cloud.hashicorp.com/vagrant/discover/rapid7/metasploitable3-win2k8
    - 下载 vagrant 的二进制文件，运行 `vagrant --appimage-extract` 生成目录
        - 创建 `squashfs-root/AppRun` 到 `vagrant` 的软链接到 PATH 路径
    - 按照 readme 添加 box 到 vagrant 环境 
        ```sh
        vagrant box add ./windows --name=rapid7/metasploitable3-win2k8
        vagrant box add ./linux --name=rapid7/metasploitable3-ubuntu1404
        ```
    - 安装依赖项
        `sudo apt install net-tools`
    - 安装 vagrant vmware 插件 
        `vagrant plugin install vagrant-vmware-desktop`
    - 安装 vagrant 环境 Vagrant VMware Utility
        https://developer.hashicorp.com/vagrant/install/vmware
    - snapshot 克隆报错，修改配置文件为完整克隆
        ```sh
        config.vm.provider "vmware_desktop" do |vm|
            vm.linked_clone = false
        end
        ```
    
    - 安装 RDP，vmware 的鼠标无法移动
        `sudo apt install remmina remmina-plugin-rdp`
        - 设置安全级别为 0