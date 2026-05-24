# ⚠️ PwnTillDawn 战场测试环境

要在 PwnTillDawn 网络中测试你的技能，搭建一个渗透测试环境至关重要。因此，我们将向你展示如何在 Windows 系统上搭建一个 Kali Linux 虚拟机，该虚拟机已预装了各种渗透测试所需的实用工具。

首先，我们需要安装 VMware Workstation Player，我们将用它来在系统上启动 Kali Linux 虚拟机。VMware Workstation Player 对于非商业用途是免费的。  
请从 [VMware 官方网站](https://www.vmware.com/products/workstation-player/workstation-player-evaluation.html) 下载最新版本的 VMware Workstation 并进行安装。

接下来，你需要从 [官方 Kali Linux 下载页面](https://www.offensive-security.com/kali-linux-vm-vmware-virtualbox-image-download/) 下载 VMware 版的 Kali Linux 镜像。该镜像本身就是一个已安装并配置好 Kali Linux 操作系统的虚拟机，可以节省我们一些设置时间。我们只需将镜像从 ZIP 文件中解压出来，然后在 VMware Workstation Player 中打开它即可。

要在 Workstation Player 中打开镜像，只需点击 "Player" 按钮，然后前往 "文件 > 打开"。这将打开一个目录浏览器，你需要浏览到包含 "Kali-linux*.vmx" 文件的文件夹。

![打开虚拟机](https://online.pwntilldawn.com/Content/img/test_environment_1.png)

打开虚拟机后，它会出现在左侧面板中。要启动该虚拟机，请选中它，然后点击 "播放虚拟机" 或绿色三角形按钮：

![播放虚拟机](https://online.pwntilldawn.com/Content/img/test_environment_2.png)

Kali Linux 启动完成后，使用下载页面提供的用户凭据登录。在撰写本教程时，默认凭据为 "kali/kali"。

![登录](https://online.pwntilldawn.com/Content/img/test_environment_3.png)

我们快要完成了。点击顶部菜单中的黑色方块打开一个终端窗口，然后在终端中使用 "passwd" 命令更改用户密码。

![更改密码](https://online.pwntilldawn.com/Content/img/test_environment_4.png)

现在你可以下载连接包，它将使你能够连接到 PwnTillDawn 网络。

[Connection Pack](https://online.pwntilldawn.com/Home/DownloadConnectionPackage)

最后一步是连接到 PwnTillDawn VPN。为此，请执行命令 `sudo openvpn PwnTillDawn.ovpn`（如下图所示）以启动连接。

![连接VPN](https://online.pwntilldawn.com/Content/img/test_environment_5.png)

![连接成功](https://online.pwntilldawn.com/Content/img/test_environment_6.png)

现在，你已经连接到 PwnTillDawn 战场网络了！