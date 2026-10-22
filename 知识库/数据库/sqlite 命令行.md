#  Command Line Shell For SQLite 

https://www.sqlite.org/cli.html

## 1. 入门

SQLite 项目提供一个名为 `sqlite3`（在 Windows 上为 `sqlite3.exe`）的命令行程序，允许用户针对 SQLite 数据库交互式运行 SQL 语句。本文简要介绍如何使用 `sqlite3` 程序。

### 1.1. SQLite 命令行程序与 SQLite 库

SQLite 库是实现 SQL 数据库引擎的代码。`sqlite3` 命令行程序或 `CLI` 是一个应用程序，它接受用户输入并将其传给 SQLite 库进行求值。要理解这是两个不同的东西。当有人说“SQLite”或“sqlite3”时，可能指 SQLite 库本身，也可能指为库提供人机界面的 `CLI`。你通常需要结合上下文判断说话者到底指哪一个。

本文讲的是 `CLI`，不是底层 SQLite 库。

### 1.2. CLI 的 GUI 替代方案

`sqlite3` 程序由 SQLite 核心开发者编写并面向他们使用，是官方支持的交互式访问 SQLite 数据库文件的方式。不过，有些用户可能更喜欢图形用户界面（`GUI`）。第三方提供了若干此类程序。

### 1.3. 启动 CLI

在命令提示符下输入 `sqlite3` 启动 `sqlite3` 程序，后面可选地跟上存放 SQLite 数据库（或 ZIP 归档）的文件名。如果指定的文件不存在，将自动创建具有该名称的新数据库文件。如果命令行上没有指定数据库文件，则使用临时内存数据库。该内存数据库在程序退出时删除。

启动时，`sqlite3` 程序会显示简短横幅消息，然后提示你输入 SQL。输入 SQL 语句（以分号结尾），按“Enter”，SQL 就会执行。

例如，要创建一个名为 `ex1.db` 的新 SQLite 数据库，其中只有一个名为 `tbl1` 的表，可以这样做：

```console
# 加载数据库
user@host:~$ sqlite3 ex1.db
SQLite version 3.54.0 2026-10-15 18:36:39
Enter ".help" for usage hints.
# 执行 SQL 查询
SQLite-3.54 ex1.db-> create table tbl1(one text, two int);
SQLite-3.54 ex1.db-> insert into tbl1 values('hello!',10),('goodbye',20);
SQLite-3.54 ex1.db-> select * from tbl1;
╭─────────┬─────╮
│   one   │ two │
╞═════════╪═════╡
│ hello!  │  10 │
│ goodbye │  20 │
╰─────────┴─────╯
SQLite-3.54 ex1.db->
```

输入系统的文件结束字符（通常是 `Control-D`）终止 `sqlite3` 程序。使用中断字符（通常是 `Control-C`）停止长时间运行的 SQL 语句。

请确保在每条 SQL 命令末尾输入分号！`sqlite3` 程序会寻找分号来判断 SQL 命令是否完整。如果省略分号，`sqlite3` 会给出续行提示符，并等待你输入更多文本以完成 SQL 命令。此功能允许你输入跨多行的 SQL 命令。例如：

```console
SQLite-3.54 ex1.db-> CREATE TABLE tbl2 (
                );->   f1 varchar(30) primary key,
                );->   f2 text,
                );->   f3 real
                );-> );
SQLite-3.54 ex1.db->
```

### 1.4. 在 Windows 上双击启动

Windows 用户可以双击 `sqlite3.exe` 图标，让命令行 shell 弹出一个运行 SQLite 的终端窗口。不过，由于双击启动 `sqlite3.exe` 时没有命令行参数，因此不会指定数据库文件，所以 SQLite 会使用一个临时内存数据库，该数据库在会话退出时删除。要将持久磁盘文件用作数据库，请在终端窗口启动后立即输入 `.open` 命令：

```console
SQLite version 3.54.0 2026-10-15 18:36:39
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
SQLite-3.54 memory-> .open ex1.db
SQLite-3.54 ex1.db->
```

上面的示例会打开并使用名为 `ex1.db` 的数据库文件。如果 `ex1.db` 文件先前不存在，则会创建它。你可能想使用完整路径名，以确保文件位于你认为它所在的目录中。使用正斜杠作为目录分隔符。换句话说，使用 `c:/work/ex1.db`，而不是 `c:\work\ex1.db`。

或者，你可以使用默认临时存储创建新数据库，然后使用 `.save` 命令将该数据库保存到磁盘文件：

```console
SQLite version 3.54.0 2026-10-15 18:36:39
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
SQLite-3.54 memory-> ... many SQL commands omitted ...
SQLite-3.54 memory-> .save ex1.db
SQLite-3.54 memory->
```

使用 `.save` 命令时要小心，因为它会覆盖任何同名的已有数据库文件，而不会提示确认。与 `.open` 命令一样，你可能想使用带正斜杠目录分隔符的完整路径名，以避免歧义。

### 1.5. 自定义提示符

有关如何自定义 `CLI` 生成的提示符字符串的信息，请参阅配套的 `[CLI 提示符]` 文档。要禁用着色，请将环境变量设置为 [`NO_COLOR=1`](https://no-color.org)，或运行命令：`.prompt --no-color`。

### 1.6. 在 Web 浏览器中运行 CLI

可以使用 [Emscripten](https://en.wikipedia.org/wiki/Emscripten) 编译 `CLI`，使其在 Web 浏览器内运行。你可以在 [https://sqlite.org/fiddle](https://sqlite.org/fiddle) 试用较新版本的 `CLI`。Web 浏览器标签页不是通用计算机，因此 `CLI` 的所有功能并非都在 `fiddle` 中可用。但你可以把 `fiddle` 用作试用 SQL 命令的沙盒。