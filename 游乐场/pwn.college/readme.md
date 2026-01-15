在 CTF 中获取 flag 从而证明安全模型（flag不应当被读取）的无效。

模块中，文本块右上角的链接对应 Github 仓库的md文件

> 注意：pwn.college 道场会记住你上次使用的最后一个工作空间界面（终端、VSCode 等），并默认为此界面，因此你运行的下个挑战将默认启动 VSCode，直到你切换为止。
> 
> 包含挑战的实际文件位于 `/challenge` 目录中。
>
> 旗帜实际上存在于 `/flag` 文件中。在任何挑战中，你的真正目标都是通过任何必要手段获取这个文件的内容，即使挑战程序本身并没有特意这样做。
> 
> 你 dojo 中的主目录（`/home/hacker`）在各个挑战之间是持久的。

flag 格式为 `pwn.college{xx.xx}`

使用 vscode UI 模式，可设置 vscode 的各种字体大小以及终端的配色，启动缓慢但响应迅速。

md文本的编辑链接
```html
<a href="https://github.com/pwncollege/linux-luminarium/edit/master/processes/kill/DESCRIPTION.md#L1" target="_blank" class="github-edit-link" title="Edit on GitHub">
    <i class="fas fa-edit"></i>
</a>
```
选择所有编辑链接，将跳转替换为复制链接地址到粘贴板，并阻止跳转。见 JavaScript.md 的浏览器脚本

B站公开课视频似乎与道场的模块视频不同。

<https://pwn.college/cse365-f2025>
CSE 365 2025 秋 
课程模块 - 道场 映射：
模块1 - 道场 Linux Luminarium - 全部
模块2 - 道场 Playing With Programs - 除“程序滥用”模块外
模块3 - 橙带 Web Security - Web安全
模块4 - 道场 Computing 101 - 全部
模块5 - 橙带 Web Security - 逆向工程
模块6 - 橙带 Web Security - 二进制漏洞利用
模块7 - 橙带 Web Security - 通信拦截
模块8 - 橙带 Web Security - 密码学

即，CSE 365 不包括基础道场的：  
Playing With Programs - 程序滥用
橙带 Web Security - 密码学
橙带 Web Security - 访问控制
橙带 Web Security - 集成安全

按照 CSE 365 课程模块顺序，最后再返回基础道场

CSE 466 2025 秋 
对应程序安全与系统安全这两个道场的全部模块

CSE 598 - Spring 2025
对应软件利用道场的全部模块+两个额外模块

其他 CSE 似乎拥有独特内容