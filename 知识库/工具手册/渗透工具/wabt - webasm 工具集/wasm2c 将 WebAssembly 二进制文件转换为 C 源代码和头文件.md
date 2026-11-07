# `wasm2c` — 将 WebAssembly 二进制文件转换为 C 源代码和头文件

## 概要

```sh
wasm2c [options] filename
```

## 描述

`wasm2c` 读取 WebAssembly 二进制格式的文件，并将其转换为 C 源文件和头文件。

选项如下：

- `--help`  
    打印此帮助消息

- `--version`  
    打印版本信息

- `-v`, `--verbose`  
    多次使用以获得更多信息

- `-o`, `--output=FILENAME`  
    生成的 C 源文件的输出文件；默认使用 `stdout`

- `--num-outputs=NUM`  
    要写入的输出文件数量

- `-n`, `--module-name=MODNAME`  
    正在生成的模块的唯一名称。此名称会作为前缀添加到每个生成的 C 符号。默认使用名称段中的模块名。如果不存在，则使用输入文件名作为默认值。

- `--disable-exceptions`  
    禁用实验性异常处理

- `--disable-mutable-globals`  
    禁用导入/导出可变全局变量

- `--disable-saturating-float-to-int`  
    禁用饱和浮点到整数运算符

- `--disable-sign-extension`  
    禁用符号扩展运算符

- `--disable-simd`  
    禁用 `SIMD` 支持

- `--enable-threads`  
    启用线程支持

- `--enable-function-references`  
    启用类型化函数引用

- `--disable-multi-value`  
    禁用多值

- `--disable-tail-call`  
    禁用尾调用支持

- `--disable-bulk-memory`  
    禁用批量内存操作

- `--disable-reference-types`  
    禁用引用类型（`externref`）

- `--disable-annotations`  
    禁用自定义注解语法

- `--enable-code-metadata`  
    启用代码元数据

- `--enable-gc`  
    启用垃圾回收

- `--disable-memory64`  
    禁用 64 位内存

- `--disable-multi-memory`  
    禁用多内存

- `--disable-extended-const`  
    禁用扩展常量表达式

- `--disable-relaxed-simd`  
    禁用宽松 `SIMD`

- `--enable-custom-page-sizes`  
    启用自定义页大小

- `--enable-compact-imports`  
    启用紧凑导入段

- `--enable-wide-arithmetic`  
    启用宽算术

- `--enable-all`  
    启用所有特性

## 示例

解析二进制文件 `test.wasm`，并写出 `test.c` 和 `test.h`：

```console
$ wasm2c test.wasm -o test.c
```

解析 `test.wasm`，写出 `test.c` 和 `test.h`，但忽略调试名称（如果有）：

```console
$ wasm2c test.wasm --no-debug-names -o test.c
```

## 另请参阅

[wasm-interp(1)]、[wasm-objdump(1)]、[wasm-stats(1)]、[wasm-strip(1)]、[wasm-validate(1)]、[wasm2wat(1)]、[wast2json(1)]、[wat-desugar(1)]、[wat2wasm(1)]、[spectest-interp(1)]

## 缺陷

如果发现缺陷，请在以下地址报告：

<https://github.com/WebAssembly/wabt/issues>

2026 年 8 月 25 日 · Debian