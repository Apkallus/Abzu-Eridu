### getconf — 获取配置值

https://man7.org/linux/man-pages/man1/getconf.1p.html

```sh
getconf [-v specification] system_var

getconf [-v specification] path_var pathname
```

#### 描述

在第一种概要形式中，`getconf` 实用程序应将 `system_var` 操作数所指定变量的值写入标准输出。

在第二种概要形式中，`getconf` 实用程序应将 `path_var` 操作数所指定变量针对 `pathname` 操作数所指定路径的值写入标准输出。

每个配置变量的值应如同通过调用 POSIX.1‐2017 本卷或 POSIX.1‐2017 系统接口卷中定义其可用的函数所获得的那样确定（参见“操作数”节）。该值应反映当前运行环境中的条件。

#### 选项

`getconf` 实用程序应符合 POSIX.1‐2017 基础定义卷 *第 12.2 节*，*实用程序语法指南*。

应支持以下选项：

- `-v specification`
    
    指示要确定配置变量的特定规范和版本。如果未指定此选项，返回的值对应于实现默认的符合规范的编译环境。
    
    如果命令：
    
    ```sh
    getconf _POSIX_V7_ILP32_OFF32
    ```
    
    不会将 `"-1\n"` 或 `"undefined\n"` 写入标准输出，则形式如下的命令：
    
    ```sh
    getconf -v POSIX_V7_ILP32_OFF32 ...
    ```
    
    确定与 [c99(1p)] 扩展描述中指定的 POSIX_V7_ILP32_OFF32 编译环境相对应的配置变量值。
    
    如果命令：
    
    ```sh
    getconf _POSIX_V7_ILP32_OFFBIG
    ```
    
    不会将 `"-1\n"` 或 `"undefined\n"` 写入标准输出，则形式如下的命令：
    
    ```sh
    getconf -v POSIX_V7_ILP32_OFFBIG ...
    ```
    
    确定与 [c99(1p)] 扩展描述中指定的 POSIX_V7_ILP32_OFFBIG 编译环境相对应的配置变量值。
    
    如果命令：
    
    ```sh
    getconf _POSIX_V7_LP64_OFF64
    ```
    
    不会将 `"-1\n"` 或 `"undefined\n"` 写入标准输出，则形式如下的命令：
    
    ```sh
    getconf -v POSIX_V7_LP64_OFF64 ...
    ```
    
    确定与 [c99(1p)] 扩展描述中指定的 POSIX_V7_LP64_OFF64 编译环境相对应的配置变量值。
    
    如果命令：
    
    ```sh
    getconf _POSIX_V7_LPBIG_OFFBIG
    ```
    
    不会将 `"-1\n"` 或 `"undefined\n"` 写入标准输出，则形式如下的命令：
    
    ```sh
    getconf -v POSIX_V7_LPBIG_OFFBIG ...
    ```
    
    确定与 [c99(1p)] 扩展描述中指定的 POSIX_V7_LPBIG_OFFBIG 编译环境相对应的配置变量值。

#### 操作数

应支持以下操作数：

- `path_var`
    
    配置变量名。应支持 POSIX.1‐2017 系统接口卷中定义的 `fpathconf`() 函数描述里表格“变量”列中的所有变量（去掉外层花括号）。实现可添加其他本地变量。

- `pathname`
    
    要针对其确定 `path_var` 所指定变量的路径名。

- `system_var`
    
    配置变量名。应支持以下所有变量：
    
    - POSIX.1‐2017 系统接口卷中 `sysconf`() 函数描述里表格“变量”列中的名称（去掉外层花括号），但对应于 `_SC_CLK_TCK`、`_SC_GETGR_R_SIZE_MAX` 和 `_SC_GETPW_R_SIZE_MAX` 的条目除外。
        
        为兼容早期版本，还应支持以下变量名：`POSIX2_C_BIND`、`POSIX2_C_DEV`、`POSIX2_CHAR_TERM`、`POSIX2_FORT_DEV`、`POSIX2_FORT_RUN`、`POSIX2_LOCALEDEF`、`POSIX2_SW_DEV`、`POSIX2_UPE`、`POSIX2_VERSION`，它们应等价于带下划线前缀的同名变量。此要求可能在未来版本中移除。
    
    - POSIX.1‐2017 系统接口卷中 `confstr`() 函数的 `name` 参数所使用的符号常量名称，去掉 `_CS_` 前缀。
    
    - POSIX.1‐2017 基础定义卷中 `<limits.h>` 头文件描述里“最大值”和“最小值”标题下列出的符号常量名称（去掉外层花括号）。
        
        为兼容早期版本，还应支持以下变量名：`POSIX2_BC_BASE_MAX`、`POSIX2_BC_DIM_MAX`、`POSIX2_BC_SCALE_MAX`、`POSIX2_BC_STRING_MAX`、`POSIX2_COLL_WEIGHTS_MAX`、`POSIX2_EXPR_NEST_MAX`、`POSIX2_LINE_MAX`、`POSIX2_RE_DUP_MAX`，它们应等价于带下划线前缀的同名变量。此要求可能在未来版本中移除。
    
    实现可添加其他本地值。
