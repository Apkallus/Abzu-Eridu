<https://www.root-me.org/?page=faq&lang=en>

# ![FAQ](https://www.root-me.org/squelettes/img/faq.svg?1566640918) 常见问题解答

## 本页将解答你最常遇到的问题

## 什么是“flag”或“验证密码”？

它是在每个挑战中需要找到的字符串。在挑战页面输入该密码，即可证明你已通过该挑战。

## 我的 IP 地址似乎被封禁了，怎样才能重新访问网站？

防火墙会保护我们免受拒绝服务攻击，并封禁符合以下任一条件的 IP 地址：

- 每秒发起超过 25 个连接
- 同时保持超过 25 个 TCP 连接

该封禁是临时的，仅持续 5 分钟。封禁期间请勿尝试连接我们的服务，否则封禁时间将会延长。

## 我无法连接到挑战

要访问挑战机器，你必须先登录门户 [www.root-me.org](https://www.root-me.org)。登录后，你的 IP 地址将被防火墙放行。登录和访问挑战必须使用同一个 IP 地址。

别忘了，Root-Me 的 SSH 服务并不在 22 端口上运行。连接时必须指定正确的端口。

请使用[服务状态](https://www.root-me.org/?page=structure&inc=inclusions%2Fservices&lang=en)页面查看各服务状态，以及你的 IP 地址是否被允许访问。

## 我宝贵的分数去哪儿了？！

每周以及每次验证 flag 时，玩家分数都会重新计算。因此，如果某个挑战的分值发生变化，你的分数也会随之变化。

## 访问 Web 挑战时需要发送会话 cookie 吗？

不需要。访问 Web 挑战从来都不需要发送门户 cookie（例如 `spip_session`）。系统只进行 IP 地址过滤。

## 为什么有些已发布的解法不再有效？

一些较旧的解法无法再照搬使用。挑战及其托管系统有时会更新，因此解法也必须相应调整。

这些改动通常涉及 App-System 挑战，因为其中的某些防护会随时间变化。例如，`dash`（由 `/bin/sh` 使用，因此也被 `system(3)` 使用）默认不再保留有效权限（与 `bash` 行为相同），在编写某些漏洞利用时必须考虑这一点。

## 我是初学者，有点迷茫……应该从哪里开始？

Root-Me 的某些板块相当困难，例如 **Realistic** 挑战，需要你对 Web 应用漏洞等有扎实的了解。

正因为有太多初学者感到迷茫，我们觉得需要提供一个**学习路径**示例，来告诉你应该先从哪里入手：

1. [![Programming](https://www.root-me.org/IMG/logo/rubon17.svg) Programming](https://www.root-me.org/en/Challenges/Programming/)
  
  自动化任务并构建 shellcode。
  
  **相关资源**
  - [Python 学习](https://repository.root-me.org/Programmation/Python/EN%20-%20Learning%20with%20Python.pdf)
  - [学习 Ruby.tar](https://repository.root-me.org/Programmation/Ruby/EN%20-%20Learning%20ruby.tar.gz)
  - [学习 Ruby.tar（法语）](https://repository.root-me.org/Programmation/Ruby/FR%20-%20Apprenez%20ruby.tar.gz)


2. [![Network](https://www.root-me.org/IMG/logo/rubon182.svg) Network](https://www.root-me.org/en/Challenges/Network/)
  
  分析捕获的流量、网络服务，并进行数据包分析。
  
  **相关资源**
  - [Scapy 实战](https://repository.root-me.org/R%C3%A9seau/FR%20-%20Scapy%20en%20pratique.pdf)
  - [实用数据包分析 - Wireshark](https://repository.root-me.org/R%C3%A9seau/EN%20-%20Practical%20packet%20analysis%20-%20Wireshark.pdf)
  - [网络](https://repository.root-me.org/R%C3%A9seau/)



3. [![Web - Server](https://www.root-me.org/IMG/logo/rubon68.svg) Web - Server](https://www.root-me.org/en/Challenges/Web-Server/)
  
  探索互联网中使用的机制、协议和技术，并学习如何滥用它们！
  
  [![Web - Client](https://www.root-me.org/IMG/logo/rubon16.svg) Web - Client](https://www.root-me.org/en/Challenges/Web-Client/)
  
  浏览器中实现的客户端技术。
  
  **相关资源**
  - [OWASP 测试指南 v4](https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20OWASP%20testing%20guide%20v4.pdf)
  - [Web 应用程序代码安全](https://repository.root-me.org/Exploitation%20-%20Web/FR%20-%20S%C3%A9curit%C3%A9%20du%20Code%20des%20Applications%20Web.pdf)
  - [Web 利用](https://repository.root-me.org/Exploitation%20-%20Web/)



4. [![Cryptanalysis](https://www.root-me.org/IMG/logo/rubon18.svg) Cryptanalysis](https://www.root-me.org/en/Challenges/Cryptanalysis/)
  
  破解加密算法。
  
  [![Steganography](https://www.root-me.org/IMG/logo/rubon67.svg) Steganography](https://www.root-me.org/en/Challenges/Steganography/)
  
  将信息隐藏于文档中的艺术。
  
  **相关资源**
  - [隐写术](https://repository.root-me.org/St%C3%A9ganographie/)
  - [密码学](https://repository.root-me.org/Cryptographie/)

5. [![Forensic](https://www.root-me.org/IMG/logo/rubon208.svg) Forensic](https://www.root-me.org/en/Challenges/Forensic/)
  
  通过分析内存转储、日志文件、网络捕获等，训练数字调查技能。
  
  **相关资源**
  - [取证](https://repository.root-me.org/Forensic/)

6. [![App - Script](https://www.root-me.org/IMG/logo/rubon189.svg) App - Script](https://www.root-me.org/en/Challenges/App-Script/)
  
  利用脚本和系统中的环境弱点、配置错误和漏洞模式。
  
  [![App - System](https://www.root-me.org/IMG/logo/rubon203.svg) App - System](https://www.root-me.org/en/Challenges/App-System/)
  
  这些挑战将帮助你理解应用层漏洞。
  
  [![Cracking](https://www.root-me.org/IMG/logo/rubon69.svg) Cracking](https://www.root-me.org/en/Challenges/Cracking/)
  
  逆向二进制文件并破解可执行程序。

7. [![Realist](https://www.root-me.org/IMG/logo/rubon70.svg?1637496509) Realist](https://www.root-me.org/en/Challenges/Realist/)
  
  真实场景挑战。
  
  [![CTF all the day](https://www.root-me.org/IMG/logo/rubon196.svg?1637496499) CTF all the day](https://www.root-me.org/en/Capture-The-Flag/CTF-all-the-day/)
  
  在真实环境中提升你的黑客技能，目标是完全攻陷并“root”主机！