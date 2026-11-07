https://docs.python.org/zh-cn/3/library/io.html

# io --- 处理流的核心工具

## 概述

`io` 模块提供了 Python 用于处理各种 I/O 类型的主要工具。三种主要的 I/O类型分别为: `文本 I/O`, `二进制 I/O` 和 `原始 I/O`。

### 文本 I/O

文本I/O预期并生成 `str` 对象。

### 二进制 I/O

二进制 I/O（也称为 `缓冲 I/O`）接受 [字节型对象] 并生成 `bytes` 对象。 

### 原始 I/O

原始 I/O (也称为 `非缓冲 I/O`) 通常用作二进制和文本流的低级构建块。 

## 类的层次结构

### I/O 基类

#### class io.RawIOBase

```py
class io.RawIOBase
```

原始二进制流的基类。 它继承自 [IOBase]。

原始二进制流通常会提供对下层 OS 设备或 API 的低层级访问

#### BufferedIOBase

```py
class io.BufferedIOBase
```

支持某种缓冲的二进制流的基类。 它继承自 [IOBase]。

##### read1()

```py
read1(size=-1, /)
```

读取并返回至多 `size` 个字节

### 文本 I/O

#### class io.TextIOBase

```py
class io.TextIOBase
```

文本流的基类。 该类提供了基于字符和行的流 I/O 的接口。 它继承自 `IOBase`。

- `buffer`  
    由 `TextIOBase` 处理的下层二进制缓冲区（一个 `BufferedIOBase` 或 `RawIOBase` 实例）
