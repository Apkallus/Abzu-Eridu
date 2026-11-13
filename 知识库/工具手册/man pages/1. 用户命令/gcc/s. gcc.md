[官网](https://gcc.gnu.org/)
- [用户手册](https://gcc.gnu.org/onlinedocs/gcc/)
- [内部手册](https://gcc.gnu.org/onlinedocs/gccint/)

[手册](https://man7.org/linux/man-pages/man1/gcc.1.html)

## 简要目录

https://gcc.gnu.org/onlinedocs/gcc/

1. GCC 支持的编程语言
2. GCC 支持的语言标准
3. GCC 命令选项
4. C 实现定义行为
5. C++ 实现定义行为
6. C 语言族的扩展
7. GCC 提供的内建函数
8. C++ 语言扩展
9. GNU Objective-C 特性
10. 二进制兼容性
11. `gcov`——测试覆盖率程序
12. `gcov-tool`——离线 gcda 配置文件处理工具
13. `gcov-dump`——离线 gcda 与 gcno 配置文件转储工具
14. `lto-dump`——用于转储 LTO 目标文件的工具
15. GCC 已知问题与故障的常见原因
16. 报告缺陷
17. 如何获取 GCC 帮助
18. 为 GCC 开发做贡献

- [资助自由软件]
- [GNU 工程与 GNU/Linux]
- [GNU 通用公共许可证]
- [GNU 自由文档许可证]
- [GCC 贡献者]
- [附录 A 索引]


## 手册

https://man7.org/linux/man-pages/man1/gcc.1.html

```sh
gcc [-c|-S|-E] [-std=standard]
    [-g] [-pg] [-Olevel]
    [-Wwarn...] [-Wpedantic]
    [-Idir...] [-Ldir...]
    [-Dmacro[=defn]...] [-Umacro]
    [-foption...] [-mmachine-option...]
    [-o outfile] [@file] infile...
```

### 控制输出类型的选项

- `-o file`  
    将输出放入文件 file 中。

### 请求或抑制警告的选项

- `-w`  
    抑制所有警告信息。