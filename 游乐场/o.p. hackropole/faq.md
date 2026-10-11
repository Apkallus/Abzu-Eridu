# 常见问题解答

## 目录

- [概述](#generalities)
- [挑战](#challenges)
- [分类](#categories)
- [解题报告](#write-ups)
- [Docker 安装](#docker-installation)
- [为 Hackropole 做贡献](#contribute-to-hackropole)
- [没有找到答案？](#you-did-not-find-your-answer)

## 概述

**什么是 Hackropole？**

Hackropole 是一个归档法国网络安全挑战赛（[FCSC](https://fcsc.fr/)）挑战的平台。任何人都可以重新挑战这些题目，无论是否拥有账户。希望使用账户（Discord、GitHub 或 GitLab）登录的参与者将解锁额外功能，例如进度跟踪、提交挑战解决方案的能力，以及获得挑战和解决方案的书签系统。

**如果我在平台上发现错误或漏洞，该怎么办？**

如果您在挑战或平台上发现错误或漏洞，可以通过电子邮件地址 `hackropole[at]ssi.gouv.fr` 将此信息分享给 ANSSI 组织团队。

## 挑战

**我是初学者，应该从哪里开始？**

每年，FCSC 都会尝试为网络安全和 CTF 初学者提供挑战。Hackropole 将这些挑战收集在 `intro` 标签下，您可以点击[挑战](https://hackropole.fr/en/challenges/)并按难度排序来找到它们。

**如何解决一个挑战？**

要解决一个挑战，您应该首先阅读相关页面上提供的描述。在大多数情况下，挑战页面上会列出需要下载的文件。这些文件可能有各种格式，例如 Python 脚本、文本文件、网络捕获、图像等。

对于某些挑战，需要下载的特殊文件是 `docker-compose.yml`，它允许您在本地机器上运行挑战。这可能是一个要分析的网站、一个要利用的二进制文件、一个包含要提取秘密的密码学预言机等。为此，您需要安装 Docker（参见后续说明）。

**挑战的难度是如何估计的？**

在 Hackropole 和 FCSC 期间，挑战分为四个难度级别：

- 入门挑战 `[intro]`，
- 简单挑战 ⭐，
- 中等挑战 ⭐⭐，
- 困难挑战 ⭐⭐⭐。

难度由组织团队估计，并可能在 FCSC 结束时根据玩家实际感知的难度重新评估。

**我可以使用自动化暴力破解工具吗？**

像 `dirbuster`、`dirb`、`wfuzz`、`sqlmap`、`nmap`、`nikto`、`hydra` 等自动化暴力破解工具**没有用**。如果您使用它们，说明您没有走在正确的道路上。

## 分类

**“Crypto”类别中的挑战是什么？**

[Crypto](https://hackropole.fr/en/crypto/) 类别的挑战涉及密码学领域，需要分析或发现密码算法或协议中的弱点。这可能涉及分析哈希函数、椭圆曲线、基于 RSA 的密码系统、分组密码算法等。

如果您是该类别的初学者，我们建议您从以下入门挑战开始：

- `[intro]` [Clair connu](https://hackropole.fr/en/challenges/crypto/fcsc2021-crypto-clair-connu/)
- `[intro]` [ROT13](https://hackropole.fr/en/challenges/crypto/fcsc2023-crypto-rot13/)
- `[intro]` [SMIC 1](https://hackropole.fr/en/challenges/crypto/fcsc2020-crypto-smic-1/)
- `[intro]` [SMIC 2](https://hackropole.fr/en/challenges/crypto/fcsc2020-crypto-smic-2/)

**“Forensics”类别中的挑战是什么？**

[Forensics](https://hackropole.fr/en/forensics/) 类别的挑战涉及数字调查，即分析各种数字媒体（内存转储、硬盘、智能手机等）以找到入侵迹象。

如果您是该类别的初学者，我们建议您从以下入门挑战开始：

- `[intro]` [Cap ou Pcap](https://hackropole.fr/en/challenges/forensics/fcsc2020-forensics-cap-ou-pcap/)
- `[intro]` [Rituel en chaine](https://hackropole.fr/en/challenges/forensics/fcsc2021-forensics-rituel-en-chaine/)
- `[intro]` [Échec OP 0/3](https://hackropole.fr/en/challenges/forensics/fcsc2022-forensics-echec-op-1/)

**“Hardware”类别中的挑战是什么？**

[Hardware](https://hackropole.fr/en/hardware/) 类别的挑战涵盖与网络安全最低层相关的各种概念，包括电子电路分析、无线电信号研究、侧信道攻击、故障攻击等。

如果您是该类别的初学者，我们建议您从以下入门挑战开始：

- `[intro]` [Ne pas jeter l’éponge](https://hackropole.fr/en/challenges/hardware/fcsc2022-hardware-ne-pas-jeter-leponge/)
- `[intro]` [Waterfall](https://hackropole.fr/en/challenges/hardware/fcsc2021-hardware-waterfall/)
- `[intro]` [Dystylosaurus](https://hackropole.fr/en/challenges/hardware/fcsc2023-hardware-dystylosaurus/)
- `[intro]` [Seven Sins](https://hackropole.fr/en/challenges/hardware/fcsc2022-hardware-seven-sins/)

**“Misc”类别中的挑战是什么？**

[Misc](https://hackropole.fr/en/misc/) 类别的挑战涵盖广泛的不直接属于其他类别、但仍具有有趣技术方面的挑战。这些可能包括编程挑战、算法问题、系统管理挑战、工业系统安全等。

如果您是该类别的初学者，我们建议您从以下入门挑战开始：

- `[intro]` [A l’envers](https://hackropole.fr/en/challenges/misc/fcsc2022-misc-a-l-envers/)
- `[intro]` [Tri Sélectif](https://hackropole.fr/en/challenges/misc/fcsc2023-misc-tri-selectif/)
- `[intro]` [QRCode](https://hackropole.fr/en/challenges/misc/fcsc2022-misc-qrcode/)

**“Pwn”类别中的挑战是什么？**

[Pwn](https://hackropole.fr/en/pwn/) 类别的挑战涉及利用二进制程序中的漏洞，主要是在 GNU/Linux 上。挑战以编译后的二进制文件形式提供，有时附带其依赖项或源代码，以及一个用于模拟在其环境中访问该二进制文件的 Docker 镜像。这些挑战的目标通常是读取远程系统上的文件或获取该机器的 shell。

如果您是该类别的初学者，我们建议您从以下入门挑战开始：

- `[intro]` [bofbof](https://hackropole.fr/en/challenges/pwn/fcsc2021-pwn-bofbof/)
- `[intro]` [Shellcode](https://hackropole.fr/en/challenges/pwn/fcsc2022-pwn-shellcode/)
- `[intro]` [uid](https://hackropole.fr/en/challenges/pwn/fcsc2023-pwn-uid/)
- `[intro]` [Poney](https://hackropole.fr/en/challenges/pwn/fcsc2020-pwn-poney/)

**“Reverse”类别中的挑战是什么？**

[Reverse](https://hackropole.fr/en/reverse/) 类别的挑战要求仅以编译后的二进制文件形式理解所提供程序的操作。目标架构可能各不相同，从适用于 GNU/Linux 或 Windows 的标准 64 位 ELF 或 PE 二进制文件，到 ARM 或 MIPS 处理器，甚至更奇特的架构（如视频游戏机）。

如果您是该类别的初学者，我们建议您从以下入门挑战开始：

- `[intro]` [Tarte Tatin](https://hackropole.fr/en/challenges/reverse/fcsc2020-reverse-tarte-tatin/)
- `[intro]` [ybab](https://hackropole.fr/en/challenges/reverse/fcsc2019-reverse-ybab/)
- `[intro]` [Guessy](https://hackropole.fr/en/challenges/reverse/fcsc2021-reverse-guessy/)

**“Web”类别中的挑战是什么？**

[Web](https://hackropole.fr/en/web/) 类别的挑战涉及分析 Web 应用程序（无论是否提供源代码），以找到可利用的漏洞，从而允许读取远程系统上的文件、访问数据库、冒充高权限用户等。该类别的挑战也以 Docker 容器形式提供。

如果您是该类别的初学者，我们建议您从以下入门挑战开始：

- `[intro]` [NES Forever](https://hackropole.fr/en/challenges/web/fcsc2020-web-nes-forever/)
- `[intro]` [Header](https://hackropole.fr/en/challenges/web/fcsc2022-web-header/)
- `[intro]` [Babel Web](https://hackropole.fr/en/challenges/web/fcsc2020-web-babel-web/)
- `[intro]` [Scully 1](https://hackropole.fr/en/challenges/web/fcsc2019-web-scully-1/)

## 解题报告

**我如何阅读解题报告？**

要查看解题报告，您必须首先通过输入有效的 flag 来验证挑战。一旦您找到并在专用字段中输入该 flag，该挑战的可用解决方案列表将出现在页面上。

**解题报告包含什么？**

Hackropole 上发布的解题报告包含解决挑战的步骤。

**谁编写解题报告？**

Hackropole 上发布的解题报告主要由社区编写。在某些情况下，Hackropole 团队或某些挑战的作者也可能提供解题报告。

## Docker 安装

**如何在 Microsoft Windows 上安装 Docker？**

我们建议阅读 [Docker 官方文档](https://docs.docker.com/desktop/install/windows-install/)。您可以通过解决以下挑战来测试您的设置：`[intro]` [Welcome Docker](https://hackropole.fr/en/challenges/misc/fcsc2024-misc-welcome-docker/)。

**如何在 GNU/Linux 上安装 Docker？**

我们建议阅读 [Docker 官方文档](https://docs.docker.com/engine/install/ubuntu)。您可以通过解决以下挑战来测试您的设置：`[intro]` [Welcome Docker](https://hackropole.fr/en/challenges/misc/fcsc2024-misc-welcome-docker/)。

如果您的机器上不存在 `docker compose` 命令（2020 年引入），我们建议按照官方说明更新 Docker。

如果您愿意，并且您的发行版允许，您可以按照[这些说明](https://docs.docker.com/engine/security/rootless/)以“rootless”模式使用 Docker。

**如何在 Apple Mac 上安装 Docker？**

我们建议阅读 [Docker 官方文档](https://docs.docker.com/desktop/install/mac-install/)。您可以通过解决以下挑战来测试您的设置：`[intro]` [Welcome Docker](https://hackropole.fr/en/challenges/misc/fcsc2024-misc-welcome-docker/)。

如果您遇到与使用 Apple Silicon 处理器的 Mac 相关的问题，请在 Discord 上联系我们，或发送邮件至 `hackropole[at]ssi.gouv.fr`。

**如何使用 Docker 启动挑战？**

要启动 Docker 挑战，只需从相应页面下载 `docker-compose.yml` 文件，然后在同一位置的终端中执行以下命令：`docker compose up`。然后，只需按照挑战页面上的说明访问服务。

**某些 pwn 挑战无法在我的 Linux 发行版上运行。我该怎么办？**

某些 Linux 发行版（如 Fedora）提供了一种称为 SELinux 的默认安全机制。此机制可能会阻止某些挑战的二进制文件禁用某些内存区域的保护。我们强烈建议您不要禁用 SELinux，因为这会降低您机器的整体安全性。如果出现问题，您可以创建新的 SELinux 策略并使用 Docker 加载它。

## 为 Hackropole 做贡献

**Hackropole 网站是如何生成的？**

挑战和解题报告以 Markdown 格式编写。然后我们使用 [Hugo 静态站点生成器](https://gohugo.io/)生成此站点的 HTML、CSS 和 JavaScript 内容。

**我在哪里可以找到 Hackropole 网站的源代码？**

用于生成静态站点的 Hugo 主题在 MIT 许可证下发布在 [github.com/ANSSI-FR/hackropole-hugo](https://github.com/FCSC-FR/hackropole-hugo)。提供了一个包含一些挑战和解题报告的示例站点，用于在本地测试主题。我们邀请您重用此主题并提出修改建议。

## 没有找到答案？

对于本页未涵盖的任何其他问题，请联系我们，最好使用专用的 [Discord 服务器](https://discord.gg/P8rpVNZ)，或者使用常规电子邮件 `hackropole[at]ssi.gouv.fr`。