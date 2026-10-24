https://vimhelp.org/usr_01.txt.html

`usr_01.txt`  适用于 `Vim version 9.2`。最后修改：2026 Feb 14

**VIM 用户手册**，作者 Bram Moolenaar

# 关于手册

本章介绍 Vim 随附的手册。阅读本章可了解解释命令时所依据的条件。

- 01.1 两本手册
- 01.2 已安装 Vim
- 01.3 使用 Vim 教程
- 01.4 版权

下一章：[`usr_02.txt`] Vim 的第一步  
目录：[`usr_toc.txt`]

---

## 01.1 两本手册

Vim 文档由两部分组成：

1. [用户]手册  
   面向任务的解释，从简单到复杂。像一本书一样从头读到[末尾]。

2. 参考手册  
   精确描述 Vim 中一切工作方式。

这些手册中使用的记法在此解释：[`notation`]

### 跳来跳去

文本在两本手册之间包含超链接，使你可以在编辑任务的描述与所用命令和选项的精确解释之间快速跳转。使用以下两个命令：

- 按 `CTRL-]` 跳转到光标下的主题。
- 按 `CTRL-O` 跳回（重复按可继续向前回溯）。

许多链接位于竖线中，像这样：[`bars`]。竖线本身可能被隐藏或不可见；见下文。选项名（如 `'number'`）、双引号中的命令（如 `":write"`）以及任何其他单词也可以用作链接。试试看：将光标移到 `CTRL-]` 上，并在其上按 `CTRL-]`。

其他主题可以用 `:help` 命令找到；参见 [`help.txt`]。

竖线和星号通常通过 `conceal` 特性隐藏。它们也使用 `hl-Ignore`，使文本颜色与背景相同。你可以用以下命令使它们可见：

```vim
:set conceallevel=0
:hi link HelpBar Normal
:hi link HelpStar Normal
```

---

## 01.2 已安装 Vim

大多数手册假定 Vim 已正确安装。如果你还没有安装，或者 Vim 无法正常运行（例如找不到文件，或在 GUI 中菜单不显示），请先阅读安装章节：[`usr_90.txt`]。

这些手册通常假定你使用的 Vim 已关闭 Vi 兼容性。对大多数命令来说这无关紧要，但有时很重要，例如多级撤销。确保你使用良好配置的一个简单方法是复制示例 `vimrc` 文件。在 Vim 内执行此操作，你不必检查它位于何处。如何执行取决于你使用的系统：

**Unix：**

```vim
:!cp -i $VIMRUNTIME/vimrc_example.vim ~/.vimrc
```

**MS-Windows：**

```vim
:!copy $VIMRUNTIME/vimrc_example.vim $VIM/_vimrc
```

**Amiga：**

```vim
:!copy $VIMRUNTIME/vimrc_example.vim $VIM/.vimrc
```

如果文件已存在，你可能想保留它。

如果你现在启动 Vim，`'compatible'` 选项应处于关闭状态。你可以用以下命令检查：

```vim
:set compatible?
```

如果它响应 `"nocompatible"`，说明你做对了。如果响应 `"compatible"`，那就有麻烦了。你必须查明该选项为什么仍被设置。也许找不到你在上面写入的文件。用以下命令查明：

```vim
:scriptnames
```

如果你的文件不在列表中，请检查其位置和名称。如果它在列表中，那么一定有其他位置重新打开了 `'compatible'` 选项。

更多信息参见 [`vimrc`] 和 [`compatible-default`]。

> **注意：**
> 本手册介绍以常规方式使用 Vim。还有一种称为 `evim`（easy Vim）的替代方式。它仍然是 Vim，但使用方式类似于 Notepad 这样的点击输入编辑器。它始终停留在 `Insert` 模式，因此感觉非常不同。用户手册不解释它，因为它应该基本上是自解释的。详情参见 [`evim-keys`]。

---

## 01.3 使用 Vim 教程

关于交互式教程，参见 [`vim-tutor-mode`]。

与其阅读文本（很无聊！），你可以使用 `vimtutor` 学习最初的 Vim 命令。这是一个分为 2 章的 30 分钟教程，手把手教授最基本的 Vim 功能。

在 Unix 上，如果 Vim 已正确安装，你可以从 shell 启动它：

```sh
vimtutor
```

在 MS-Windows 上，你可以在 `"Program/Vim 9.1"` 菜单中找到它。或者从安装目录执行 `vimtutor.bat`（你可以在 Vim 内使用 `:echo $VIMRUNTIME` 找到此目录）。

这会复制第 1 章的教程文件，以便你可以编辑它而不会损坏原始文件。要继续第 2 章，可以使用以下命令：

```sh
vimtutor -c 2
```

教程有几个翻译版本。要了解你的语言版本是否可用，请使用双字母语言代码。例如法语：

```sh
vimtutor fr
```

在 Unix 上，如果你更喜欢使用 Vim 的 GUI 版本，请使用 `gvimtutor` 或 `vimtutor -g`，而不是 `vimtutor`。

对于 OpenVMS，如果 Vim 已正确安装，你可以在 VMS 提示符下用以下命令启动 `vimtutor`：

```text
@VIM:vimtutor
```

可选择像上面一样添加双字母语言代码。

在其他系统上，你需要做一点工作：

1. 复制教程文件。你可以用 Vim 完成（它知道在哪里找到它）：  

    ```sh
    vim --clean -c 'e $VIMRUNTIME/tutor/tutor1' -c 'w! TUTORCOPY' -c 'q'
    ```

   这会将文件 `"TUTORCOPY"` 写入当前目录。要使用教程的翻译版本，请在文件名后附加双字母语言代码。例如法语：

    ```sh
    vim --clean -c 'e $VIMRUNTIME/tutor/tutor1.fr' -c 'w! TUTORCOPY' -c 'q'
    ```

2. 用 Vim 编辑复制出的文件：  

    ```sh
    vim --clean TUTORCOPY
    ```

   `--clean` 参数确保 Vim 以良好的默认值启动。

3. 使用完毕后删除复制出的文件：  

    ```bat
    del TUTORCOPY
    ```

---

## 01.4 版权

Vim 用户手册和参考手册的版权归 Bram Moolenaar 所有（Copyright (c) 1988）。本材料只能根据 Open Publication License v1.0 或更高版本中规定的条款和条件分发。最新版本目前可在以下地址获取：
<https://opencontent.org/openpub/>

为手册做出贡献的人必须同意上述版权声明。

用户手册的部分内容来自 Steve Oualline 所著的《Vi IMproved - Vim》一书（New Riders Publishing 出版，ISBN：0735710015）。Open Publication License 适用于本书。只收录了选定的部分，并且这些部分已被修改（例如删除图片、为 Vim 6.0 及更高版本更新文本、修正错误）。省略 `frombook` 标签并不意味着文本不来自本书。

非常感谢 Steve Oualline 和 New Riders 创作本书并在 OPL 下发布它！在编写用户手册时，它提供了极大的帮助。不仅提供了字面文本，还确定了语气和风格。

如果你通过销售手册赚钱，强烈鼓励你将部分利润捐赠给乌干达的艾滋病受害者。参见 [`Kuwasha`]。

---

下一章：[`usr_02.txt`] Vim 的第一步

版权：参见 [`manual-copyright`]  `vim:tw=78:ts=8:noet:ft=help:norl:`