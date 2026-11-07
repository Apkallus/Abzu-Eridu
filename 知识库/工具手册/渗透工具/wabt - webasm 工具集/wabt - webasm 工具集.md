https://github.com/WebAssembly/wabt/tree/main

[工具文档](https://webassembly.github.io/wabt/doc/wasm2c.1.html)

## 安装

最简单：使用预编译包，直接仓库安装，或下载 github 发布的预构建包

```sh
sudo apt install wabt
```

更复杂：使用源码安装，需额外 git 一批子模块

## 使用


### wasm2c

```sh
# 反编译 .wasm，输出 .c .h
wasm2c test.wasm -o test.c
```

得到 wasm 对 c 的直接映射，并非反编译