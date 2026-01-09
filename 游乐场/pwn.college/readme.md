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

使用 vscode UI 模式：
- 可设置 vscode 的各种字体大小以及终端的配色
- 响应迅速

md文本的编辑链接
```html
<a href="https://github.com/pwncollege/linux-luminarium/edit/master/processes/kill/DESCRIPTION.md#L1" target="_blank" class="github-edit-link" title="Edit on GitHub">
    <i class="fas fa-edit"></i>
</a>
```
选择所有编辑链接，将跳转替换为复制链接地址到粘贴板，并阻止跳转。见 JavaScript.md 的浏览器脚本