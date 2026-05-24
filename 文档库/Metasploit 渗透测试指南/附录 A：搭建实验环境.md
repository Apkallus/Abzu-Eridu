A

## 配置你的实验环境

学习使用 Metasploit 框架的最佳方式就是实践。本附录将说明如何搭建一个测试环境，以便运行本书中的示例。我们将使用 Kali Linux 来攻击和渗透测试 Linux 及 Windows 系统。

本实验室的虚拟机配置在 x86 和 AMD64 架构的设备上效果最佳。Apple Silicon Mac（如 M1 和 M2）的虚拟机支持有限，但如果你使用此类设备，可以通过 Docker 容器来搭建一个简化版的实验环境。在撰写本文时，这意味着你将无法安装最新版本的易受攻击的 Linux 目标机，并且必须在在线环境中执行基于 Windows 的攻击。

请访问 https://nostarch.com/metasploit-2nd-edition 并点击页面上的链接加入我们的 Discord 社区，在那里你可以与其他读者交流。

## x86 和 AMD64

首先访问 https://github.com/rapid7/metasploitable3，按照 README.md 文件中的说明创建你的目标 Linux 和 Windows Metasploitable 3 虚拟机。

## 警告

这些系统存在漏洞且易于攻击。不要在这些机器上进行任何敏感活动；如果你能攻击它们，别人也能。

接下来，下载并安装 VMware、VirtualBox 或其他你选择的虚拟化软件。然后从 https://www.kali.org 下载 Kali。为你已安装的虚拟化软件选择适当的版本。

对于想要更高级配置的用户，可以考虑将这些机器放在 pfSense 防火墙后面。虽然本书的任何练习都不需要这样做，但它提供了另一层保护。你可以在 https://www.pfsense.org/download/ 找到 pfSense 的安装文件和说明。

你还需要设置一个 Windows Active Directory 服务器，并将 Windows 目标机器加入其中。微软有几个优秀的安装指南。例如，以下实验室使用名为 Vagrant 的工具来自动化设置环境：https://github.com/alebov/AD-lab。

如果你的 Linux 机器有 77GB 的可用空间，你可以安装 Orange-Cyberdefense 的 Active Directory 游戏实验室环境（https://github.com/Orange-Cyberdefense/GOAD）。下载 git 仓库后，只需几条命令即可设置 Active Directory 环境。

Metasploit 中的许多数据库模块都针对 Microsoft 的 SQL 服务器。要执行这些攻击，你需要在设置的易受攻击的 Windows 机器上安装 SQL Server Express。微软在 https://www.microsoft.com/en-us/sql-server/sql-server-downloads 免费提供 SQL Server Express。安装时，除身份验证模式外，所有选项均选择默认值。选择混合模式，设置 sa 登录密码为 password123，然后继续安装。

你还需要对 SQL 服务器进行一些额外更改，使其在你的网络上可访问。选择“开始”▸“所有程序”▸“Microsoft SQL Server”▸“配置工具”，然后选择“SQL Server 配置管理器”。配置管理器启动后，选择“SQL Server 服务”，右键单击“SQL Server”并选择“停止”。展开“SQL Server 网络配置管理器”，然后选择“MSSQLSERVER 的协议”。

双击“TCP/IP”。在“协议”选项卡中，将“已启用”设置为“是”，将“全部侦听”设置为“否”。接下来，仍在“TCP/IP 属性”对话框中，选择“IP 地址”选项卡，并删除“IPAll”下的所有条目。在“IP1”和“IP2”下，删除“TCP 动态端口”的值，并将它们的“活动”和“已启用”均设置为“是”。

将 IP1 的 IP 地址设置为匹配你的 IP 地址，IP2 的地址设置为 127.0.0.1，并将它们的 TCP 端口均设置为 1433。然后单击“确定”。

接下来，你需要启用 SQL Server Browser 服务。选择“SQL Server 服务”，双击“SQL Server Browser”。在“服务”选项卡中，将“启动模式”设置为“自动”。

默认情况下，SQL 服务器在低权限的网络服务账户下运行，这是一个很好的默认设置。然而，这与我们在实际部署中发现的并不完全一致，因为管理员经常更改此设置，而不是试图解决出现的权限问题。在某些目标系统上，我们发现 SQL Server Browser 服务以提升的 SYSTEM 账户运行。此外，许多系统将 SQL Server 服务登录为本地系统，这是旧版本 Microsoft SQL Server（2000 及更早版本）的默认设置。

因此，双击“SQL Server (SQLEXPRESS)”并设置“登录身份”为“本地系统”来更改账户。完成后单击“确定”。然后，右键单击“SQL Server (SQLEXPRESS)”并选择“启动”。对 SQL Server Browser 执行相同操作。

最后，关闭配置管理器，并通过打开命令提示符并运行以下两个 netstat 命令来验证一切是否正常工作：

```cmd
C:\Documents and Settings\Administrator>netstat -ano | find "1433"
  TCP 192.168.1.155:1433 0.0.0.0:0 LISTENING 512

C:\Documents and Settings\Administrator>netstat -ano | find "1434"
  UDP 0.0.0.0:1434 *:* 512
```

你之前配置的 IP 地址应正在侦听 TCP 端口 1433 和 UDP 端口 1434，如上面的代码所示。

## ARM 和 Apple Silicon

对 ARM 和 Apple Silicon 架构的虚拟机支持有限。虽然你可以通过使用 Docker 容器来运行你的机器来设置实验室的某个版本，但 Windows Server 和 Metasploitable 3 机器在 Apple Silicon 环境中不作为 Docker 容器提供。因此，你的实验室将包含两台 Linux 机器：Kali 攻击机（attacker）和 Metasploitable 2 Linux 目标机（target）。

Metasploitable 2 包含的示例漏洞集与 Metasploitable 3 略有不同，因此在学习本书时可能需要调整练习。如果将来有 Metasploitable 3 容器可用，请随意安装它来代替。

要自己测试 Windows 黑客示例，你可以使用在线实验室环境。我们推荐 Hack The Box 的在线 Active Directory 课程，该课程附带一个可用于此目的的关联实验室。请访问 https://academy.hackthebox.com/course/preview/active-directory-ldap。

首先从 https://www.docker.com/products/docker-desktop/ 下载并安装 Docker Desktop。在启动 Docker 容器之前，启动 Docker Desktop 应用程序，然后返回应用程序菜单并启动一个新的终端窗口。然后，运行以下命令下载 Kali 和 Metasploitable 2：

```bash
$ sudo docker pull kalilinux/kali-rolling
$ sudo docker pull tleemcjr/metasploitable2
```

现在你已经下载了容器，运行以下命令创建一个新的虚拟网络来容纳这些机器：

```bash
$ docker network create vnet
```

接下来，通过运行以下命令启动目标 Metasploitable 容器：

```bash
$ sudo docker run --network=vnet -h target -it --rm --name metasploitable2 tleemcjr/metasploitable2
```

这应该会在我们称为 vnet 的网络上启动 Metasploitable 机器。`-it` 标志以交互模式启动容器，`-h` 标志指定主机名（target）。

通过运行以下命令启动 Kali 机器：

```bash
$ sudo docker run --network=vnet -h attacker -it --rm --name kalibox kalilinux/kali-rolling
```

请注意，每次启动目标机和攻击机时都需要运行这些命令。

一旦 Kali 机器启动，运行以下命令以更新 Kali 机器并安装标准渗透测试工具集：

```bash
$ apt update
$ apt -y install sudo kali-linux-headless
```

要暂停机器，请运行 `docker pause` 命令：

```bash
$ docker pause metasploitable2
$ docker pause kalibox
```

接下来，安装你将在本书中使用的额外 Kali 包。

## 安装 Kali 元包

Kali 的默认安装并不包含我们需要的所有工具。Kali 团队将专业工具分组为称为元包（metapackages）的包。例如，他们为硬件黑客提供了一个元包 `kali-tools-hardware`，为密码学和隐写术提供了一个元包 `kali-tools-crypto-stego`。

他们甚至提供了一个包含所有其他元包的元包。让我们通过安装这个元包来增强 Kali。在 Kali 终端中运行以下命令。这需要一些时间，因为我们正在安装多个包：

```bash
kali@kali:~$ sudo apt-get install -y kali-linux-everything
```

安装完成后，通过运行以下命令检查 Metasploit 是否已安装：

```bash
kali@kali:~$ msfconsole
```
