# PwnTillDawn 在线战场

PwnTillDawn 在线战场是一个渗透测试实验平台。目标很简单：利用一连串的弱点和漏洞，攻入尽可能多的机器，并收集旗标文件来证明你成功完成了利用。每台可被攻破的目标机器至少包含一个"FLAG"（通常是一个文件，一般位于用户的桌面或用户的根目录下），你需要找到它并在应用程序中提交。旗标多数情况下为 SHA1 格式，但也并非绝对。

## 接入 PwnTillDawn 网络

1. 仔细阅读[规则](https://online.pwntilldawn.com/Home/Rules)。
   **注意**：如果这是你初次接触攻击性安全，并且不知道如何搭建测试环境，请阅读我们的 [PwnTillDawn 测试环境指南](https://online.pwntilldawn.com/Home/TestingEnvironment)。

2. 下载下方的连接包

   - [Connection Pack](https://online.pwntilldawn.com/Home/DownloadConnectionPackage)

3. 打开你的终端，运行 `openpwn PwnTillDawn.ovpn`

4. 扫描 `10.150.150.10` 到 `10.150.150.254` 范围内的网络，寻找有漏洞的目标！

5. 选择一台机器，并将其 IP 地址填入目标（target）区域。这能让你获取关于该目标的信息，例如操作系统、难度以及工作负载（即当前正在攻陷该机器的 PwnTillDawn 用户数量）。如果你想专门攻陷某一台机器，你需要点击它，然后点击“签到”（check-in）按钮。签到目标至关重要，因为它是提供负载指示的依据。此外，只有在签到一台机器后，你才能收到即将到来活动的通知、请求恢复机器，以及提交旗标。完成对一台机器的攻击后，请不要忘记“签退”（check out）。