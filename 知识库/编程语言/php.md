## 配置

https://www.php.net/manual/en/ini.core.php

- `cgi.fix_pathinfo` `bool`

    为 CGI 提供真正的 `PATH_INFO`/`PATH_TRANSLATED` 支持。PHP 之前的行为是将 `PATH_TRANSLATED` 设置为 `SCRIPT_FILENAME`，并且不解析 `PATH_INFO` 是什么。关于 `PATH_INFO` 的更多信息，请参阅 CGI 规范。将此选项设置为 1 将使 PHP CGI 修复其路径以符合规范。设置为 0 将使 PHP 恢复之前的行为。此选项默认开启。您应修改您的脚本以使用 `SCRIPT_FILENAME` 而非 `PATH_TRANSLATED`。

    > 即，此处默认设置：当路径文件不存在时的向前回溯的文件查找行为

## 语法

### 文件系统

#### move_uploaded_file()

```php
function move_uploaded_file(string $from, string $to): bool
```

当 from 文件有效时，上传到 to 路径


#### unlink() - 删除文件

```php
function unlink(string $filename, ?resource $context = null): bool
```

删除 filename 文件，如果文件是符号链接，将会删除符号链接。

#### symlink() - 创建符号链接

```php
function symlink(string $target, string $link): bool
```

symlink() creates a symbolic link to the existing target with the specified name link. 

#### readlink() - 读取符号链接指向的路径

```php
function readlink(string $path): string|false
```

Returns the contents of the symbolic link path or false on error. 

# PHP 手册

https://www.php.net/manual/zh/index.php

## 语言参考 
### 流程控制

#### include 表达式包含并运行指定文件

```php
// 本地
include 'vars.php';

// URL
include 'http://www.example.com/file.php?foo=1&bar=2';
```

被包含文件先按参数给出的路径寻找，如果没有给出目录（只有文件名）时则按照 `include_path` 指定的目录寻找。如果在 `include_path` 下没找到该文件则 `include` 最后才在调用脚本文件所在的目录和当前工作目录下寻找。如果最后仍未找到文件则 `include` 结构会发出一条 `E_WARNING` ；这一点和 `require` 不同，后者会发出一个 `E_ERROR` 。

## 函数参考 

### 文件系统相关扩展 
#### 文件系统 
##### 文件系统函数

###### file_get_contents — 将整个文件读入一个字符串

```php
function file_get_contents(
    string $filename,
    bool $use_include_path = false,
    ?resource $context = null,
    int $offset = 0,
    ?int $length = null
): string|false
```

参数
- `filename`
    要读取的文件的名称。（唯一必选参数）

### 文本处理 
#### 字符串 
##### 字符串 函数
###### echo — 输出一个或多个字符串

```php
function echo(string ...$expressions): void
```

输出一个或多个表达式，没有额外的换行符或者空格。

echo 不是函数，而是语言结构。它的参数是表达式列表，跟在 echo 关键字后面，用逗号分隔，不用括号分隔。与其它的返回结构不同，echo 没有返回值

快捷语法，可以在开始标记后直接跟等号

```php
<?=$foo?>
```

示例
```php
<?php
echo "echo does not require parentheses.";

// 参数是可以产生字符串的任意表达式
$foo = "example";
echo "foo is $foo"; // "foo is example"
?>
```

### 影响 PHP 行为的扩展 
#### 错误处理 
##### 安装/配置

- `display_errors string`
    该选项设置是否将错误信息作为输出的一部分打印到屏幕，或者对用户隐藏。 
    - > 这是辅助开发的功能，不应在生产系统中使用 (例如连接到互联网的系统)。 

#### PHP 选项/信息 
##### PHP 选项/信息 函数

- `set_include_path` — 设置 `include_path` 配置选项

### 文件系统相关扩展 
#### 文件系统 
##### 安装/配置

- `allow_url_fopen bool`
    启用可感知 URL 的 `fopen` 封装协议，从而可以像访问文件一样访问 URL 对象。默认封装协议支持通过 `ftp` 或 `http` 协议访问 远程文件，某些扩展（例如 `zlib`）可能会注册其他封装协议。 

- `allow_url_include bool`
    此选项允许以下函数使用可感知 URL 的 `fopen` 封装协议： `include`、`include_once`、 `require`、`require_once`。 
    - > 此设置要求启用 `allow_url_fopen`。 

## 附录 

https://www.php.net/manual/zh/appendices.php

### php.ini 配置

https://www.php.net/manual/zh/ini.core.php

语言选项
- `disable_functions string`
    -  此指令允许禁用某些函数。它接受逗号分隔的函数名列表作为参数。 从 PHP 8.0.0 开始，禁用函数会删除其定义，允许用户重新定义它。 在 PHP 8.0.0 之前，禁用函数只是阻止函数被调用。
    - 此指令仅能禁用 内置函数。不能影响用户自定义函数。 

- `expose_php bool`
    - 确定是否向外界公开服务器上安装了 PHP，在 HTTP 标头中包含 PHP 版本号（例如：`X-Powered-By: PHP/5.3.7`）。

路径和目录
- `include_path string`

    - 指定 `require`、`include`、`fopen()`、`file()`、`readfile()` 和 `file_get_contents()` 函数在其中查找文件的目录列表，格式类似于系统的 PATH `环境变量:目录列表`，在 Unix 中使用冒号分隔，在 Windows 中使用分号分隔。 
    - 示例 
        ```ini
        # Unix include_path
        include_path=".:/php/includes"

        # Windows include_path
        include_path=".;c:\php\includes"
        ```

- `open_basedir string`
    - 将 PHP 可以访问的文件限制在指定的目录树中，包括文件本身。 
    - 默认设置是允许打开所有文件。 