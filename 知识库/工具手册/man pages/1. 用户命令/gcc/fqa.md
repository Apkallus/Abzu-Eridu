https://gcc.gnu.org/faq.html

# GCC 常见问题解答

本 FAQ 试图回答与 GCC 相关的具体问题。关于 C、C++ 和 Fortran 的一般信息，请分别查阅 [comp.lang.c FAQ](https://c-faq.com) 和 [C++ FAQ](https://isocpp.org/faq/)。

其他 GCC 相关 FAQ：[libstdc++-v3](https://gcc.gnu.org/onlinedocs/libstdc++/faq.html)。

---

# 问题

1. “一般信息”
    1. “如何修复缺陷或添加功能？”
    2. “GCC 能在我的平台上工作吗？”
2. “安装”
    1. “如何安装多个版本的 GCC”
    2. “动态链接器无法找到 GCC 库”
    3. “`libstdc++`/`libio` 测试在 `--enable-shared` 下严重失败”
    4. “GCC 找不到 GNU as/GNU ld”
    5. “cpp：Usage:... 错误”
3. “测试套件问题”
    1. “如何将 `-fnew-abi` 等标志传递给测试套件？”
    2. “如何使用多个选项运行测试套件？”
4. “其他”
    1. “友元模板”
    2. “`dynamic_cast`、`throw`、`typeid` 无法与共享库配合使用”
    3. “为什么需要 `autoconf`、`bison`、`xgettext`、`automake` 等？”
    4. “为什么我不能构建共享库？”
    5. “构建 C++ 时，链接器说我的构造函数、析构函数或虚表未定义，但我已定义它们”

---

# 一般信息

## 如何修复缺陷或添加功能？

有很多方法可以让问题得到修复。下面的列表可能不完整，但涵盖了许多常见情况。这些方法大致按照普通 GCC 用户（即不熟悉 GCC 内部实现的人）的处理难度从高到低排列，难度以修复缺陷所需的时间衡量。没有哪种替代方案一定优于其他方案；每种方案都有其优点和缺点。

- 自己修复。如果你足够努力，这种方案可能会产生结果，但很可能需要大量时间；并且，取决于你的工作质量以及你的改动所能带来的预期收益，你的代码可能永远不会进入 GCC 的正式发布版本。
- “向 GCC 缺陷跟踪系统报告问题”，并希望有人愿意帮你修复。虽然这当然可能，而且经常发生，但并不能保证。你不应期望这种方式能获得商业支持组织那样的响应，因为阅读 GCC 缺陷报告的人即使选择帮助你，也是在志愿付出时间。
- 雇人帮你修复。有许多公司和个人为 GCC 提供支持。这种方案需要花钱，但相对更可能得到结果。

---

## GCC 能在我的平台上工作吗？

GCC 的宿主/目标特定安装说明包含有关在特定平台上安装或使用 GCC 时已知问题的信息。这些说明包含在发布版源码的 `INSTALL/specific.html` 中，[最新版本](https://gcc.gnu.org/install/specific.html)始终可在 GCC 网站上获得。在那里你还可以找到[成功构建报告](https://gcc.gnu.org/pipermail/gcc-testresults/)。

---

# 安装

## 如何安装多个版本的 GCC

可能需要在同一系统上安装多个版本的编译器。这可以通过在配置时使用不同的前缀路径以及少量符号链接来实现。

基本上，用不同的 `--prefix` 选项配置两个编译器，然后分别构建并安装每个编译器。假设你希望 `gcc` 是最新编译器并位于 `/usr/local/bin`；还假设你希望 `gcc2` 是较旧的 gcc2 编译器，也位于 `/usr/local/bin`。

最简单的方法是用 `--prefix=/usr/local/gcc` 配置新的 GCC，用 `--prefix=/usr/local/gcc2` 配置较旧的 gcc2。构建并安装两个编译器。然后创建从 `/usr/local/bin/gcc` 到 `/usr/local/gcc/bin/gcc` 的符号链接，以及从 `/usr/local/bin/gcc2` 到 `/usr/local/gcc2/bin/gcc` 的符号链接。为 `g++`、`c++` 和 `g77` 编译器驱动创建类似的链接。

使用符号链接的另一种替代方案是使用 `--program-transform-name` 选项进行配置。该选项指定一个 `sed` 命令，用于处理安装后的程序名。使用它，你可以例如让所有新版 GCC 程序安装为 `new-gcc` 之类的名称。你仍然需要为新旧 GCC 指定不同的 `--prefix` 选项，因为只有可执行程序名会被转换。区别在于，你（作为管理员）不必设置符号链接，但必须在你（作为用户）的 `PATH` 中指定额外的目录。`--program-transform-name` 的一个复杂之处在于，`sed` 命令不可避免地包含对 shell 有特殊意义的字符，必须正确转义；此外，命令中不能使用 `^` 或 `$`。下面这个选项会为新安装的 GCC 程序加上 `new-` 前缀：

```
--program-transform-name='s,\\\\(.*\\\\),new-\\\\1,'
```

配合上面的 `--prefix` 选项，这会将新的 GCC 程序安装到 `/usr/local/gcc/bin`，名称带有 `new-` 前缀。如果你有多个 GCC 版本，并希望确保自己调用的是哪个版本，可以使用 `--program-transform-name`。

如果使用 `--prefix`，GCC 可能难以在系统中定位 GNU 汇编器或链接器；“GCC 找不到 GNU as/GNU ld”说明了如何处理。

另一个可能更简单的选项是使用 `--program-prefix=` 或 `--program-suffix=` 配置选项。因此，如果你要安装 GCC 2.95.2，并且不想干扰 `/usr/local/bin/` 中当前的 GCC 版本，可以执行：

```sh
configure --program-suffix=-2.95.2 <other configure options>
```

这应该会使 GCC 安装为 `/usr/local/bin/gcc-2.95.2`，而不是 `/usr/local/bin/gcc`。

---

## 动态链接器无法找到 GCC 库

这个问题表现为程序启动时找不到它们依赖的共享库。（这通常围绕 `libstdc++` 出现。）

GCC 不会指定 runpath 来让动态链接器在运行时找到动态库。

简短的解释是：如果你总是向链接器传递 `-R` 选项，你的程序就会依赖可能通过 NFS 挂载的目录；当 NFS 服务器宕机时，程序——即使是那些不需要这些目录的程序——也可能不必要地挂起。（SunOS 实际上总是为每个 `-L` 选项传递 `-R` 选项；这是个坏主意，因此在 Solaris 中已被移除。）

但是，如果你觉得自己确实需要自动向链接器传递这样的选项，可以将其添加到 GCC specs 文件中。该文件可以使用 `gcc -dumpspecs` 创建，并通过 `-specs=` 选项传递给 GCC。你可以根据平台和链接器，将 `-R` 或 `-rpath` 等链接器标志添加到 `*link` 或 `*lib` specs 中。

另一种方法是使用 `-Wl,option` 语法，要求 GCC 将标志 `option` 传递给链接器。

还有一种替代方案是在 `gcc`、`g++` 或 `ld` 周围安装一个包装脚本，将适当的目录添加到环境变量 `LD_RUN_PATH` 或等价变量中（同样，这取决于平台）。

---

## GCC 找不到 GNU as/GNU ld

GCC 会在 `PATH` 中搜索汇编器和链接器，但它只会在搜索 GCC 可执行文件中硬编码的目录列表之后才这样做。由于在大多数平台上，硬编码列表包含系统汇编器和链接器所在的目录，你可能必须采取以下措施之一，才能让 GCC 使用这些程序的 GNU 版本。

为确保 GCC 找到 GNU 汇编器（GNU 链接器）——[某些配置](https://gcc.gnu.org/install/specific.html)需要它们——你应该使用与 GCC 相同的 `--prefix` 选项配置这些程序。然后构建并安装 GNU as（GNU ld），再继续构建 GCC。

另一种替代方案是在命令 `gcc -print-search-dirs | grep '^programs:'` 打印的任意目录中创建指向 GNU as 和 ld 的链接。如果 `ld` 已存在，指向 `ld` 的链接应命名为 `real-ld`。如果你在编译 GCC 时这些链接不存在，可能还必须在构建目录中创建它们，包括 `gcc` 目录内以及所有 `gcc/stage*` 子目录中。

GCC 2.95 允许你指定要使用的汇编器和链接器的完整路径名。配置标志是 `--with-as=/path/to/as` 和 `--with-ld=/path/to/ld`。GCC 会尝试先使用这些路径名，然后在标准搜索目录中查找 `as` 或 `(real-)ld`。如果在配置时发现指定的程序是 GNU 工具，则无需使用 `--with-gnu-as` 和 `--with-gnu-ld`；这些标志会被自动检测。该选项的一个缺点是，如果指定的文件名存在，它不允许你用命令行选项 `-B/path/` 覆盖汇编器和链接器的搜索路径。

---

## cpp：Usage:... 错误

如果你在构建 GCC 时（特别是在构建 `__mulsi3` 时）遇到类似下面的错误，那么你的环境变量很可能有问题。

```log
cpp: Usage: /usr/lib/gcc-lib/i586-unknown-linux-gnulibc1/2.7.2.3/cpp
[switches] input output
```

首先在环境中的 `LIBRARY_PATH` 或 `GCC_EXEC_PREFIX` 里查找显式的 `.`。如果没有找到显式的 `.`，则在这些变量中查找空路径名。注意，这些变量开头或结尾的 `:` 是隐式的 `.`，会导致问题。

另请注意，这些路径中的 `'::'` 也会导致类似问题。

---

# 测试套件问题

## 如何将 `-fnew-abi` 等标志传递给测试套件？

如果直接调用 `runtest`，可以使用 `--tool_opts` 选项，例如：

```sh
runtest --tool_opts "-fnew-abi -fno-honor-std" <other options>
```

或者，如果使用 `make check`，可以使用 `make` 变量 `RUNTESTFLAGS`，例如：

```sh
make RUNTESTFLAGS="--tool_opts '-fnew-abi -fno-honor-std'" check-g++
```

---

## 如何使用多个选项运行测试套件？

如果直接调用 `runtest`，可以使用 `--target_board` 选项，例如：

```sh
runtest --target_board "unix{-fPIC,-fpic,}" <other options>
```

或者，如果使用 `make check`，可以使用 `make` 变量 `RUNTESTFLAGS`，例如：

```sh
make RUNTESTFLAGS="--target_board 'unix{-fPIC,-fpic,}'" check-gcc
```

上述任一示例都会将测试运行三次：一次使用 `-fPIC`，一次使用 `-fpic`，一次不添加额外标志。

这种技术在多库目标上尤其有用。

---

# 其他

## 友元模板

为了使模板函数的特化成为（可能是模板的）类的友元，你必须通过在该函数名后附加尖括号来显式声明该友元函数是模板，并且该模板函数必须已经声明。下面是一个例子：

```cpp
template <typename T> class foo {
  friend void bar(foo<T>);
}
```

上面的声明声明了一个名为 `bar` 的非模板函数，因此必须为 `foo` 的**每个**特化显式定义它。`bar` 的模板定义不行，因为它与上面的非模板声明无关。因此，你最终必须写成：

```cpp
void bar(foo<int>) { /* ... */ }
void bar(foo<void>) { /* ... */ }
```

如果你本意是让 `bar` 成为模板函数，就应该按如下方式前向声明它。注意，由于模板函数声明引用了模板类，模板类也必须前向声明：

```cpp
template <typename T>
class foo;

template <typename T>
void bar(foo<T>);

template <typename T>
class foo {
  friend void bar<>(foo<T>);
};

template <typename T>
void bar(foo<T>) { /* ... */ }
```

在这种情况下，模板实参列表可以留空，因为它可以从函数实参隐式推导出来，但尖括号必须存在，否则该声明会被视为非模板函数。此外，在某些情况下，你可能必须显式指定模板实参，以消除歧义。

ANSI/ISO C++ 标准最后公开评论草案中的一个错误，以及先前 GCC 版本会接受此类友元声明作为模板声明的事实，导致人们认为前向声明没有必要；但根据标准的最终版本，它是必要的。

---

## `dynamic_cast`、`throw`、`typeid` 无法与共享库配合使用

GCC 3.0 系列中的新 C++ ABI 使用地址比较而不是字符串比较来确定类型相等。这带来了更好的性能。像其他必须出现在最终可执行文件中的对象一样，这些 `std::type_info` 对象具有所谓的模糊链接（vague linkage），因为它们并不紧密绑定到任何特定的翻译单元（目标文件）。编译器必须在任何需要它们存在的翻译单元中生成它们，然后依赖链接和加载过程确保最终可执行文件中只有一个处于活动状态。使用静态链接时，所有这些符号在链接时解析；但使用动态链接时，进一步的解析发生在加载时。你必须确保共享库中的对象针对可执行文件和其他共享库中的对象进行解析。

- 对于链接到共享库的程序，不需要额外的预防措施。
- 不能使用 `-Bsymbolic` 选项创建共享库，因为这会阻止上述解析。
- 如果使用 `dlopen` 从共享库显式加载代码，你必须做几件事。首先，通过使用 `-E` 标志链接可执行文件来导出其中的全局符号（如果你以通常方式从编译器驱动 `g++` 调用链接器，则必须将其指定为 `-Wl,-E`）。你还必须通过向 `dlopen` 提供 `RTLD_GLOBAL` 标志，使已加载库中的外部符号可供后续库使用。符号解析可以是立即的或延迟的。

模板实例化是另一种用户可见的、具有模糊链接的对象情况，需要类似的解析。如果你不采取上述预防措施，你可能会发现：具有相同实参列表但在多个翻译单元中实例化的模板实例化，会有多个地址，具体取决于在哪个翻译单元中取地址。（这*不是*具有模糊链接并预期在链接与加载期间解析的对象类型的详尽列表。）

如果你担心链接或加载过程中不同对象因同名而冲突，则应使用命名空间来消除歧义。给具有全局链接的不同对象赋予相同名称，违反了单一定义规则（ODR）`[basic.def.odr]`。

有关 GCC 如何实现这些及其他 C++ 特性的更多细节，请阅读 [C++ ABI 规范](https://itanium-cxx-abi.github.io/cxx-abi/)。注意，必须解析的 `std::type_info` 对象都以 `_ZTS` 开头。有关 `-E` 和 `-Bsymbolic` 标志的说明，请参阅 `ld` 的文档。

---

## 为什么需要 `autoconf`、`bison`、`xgettext`、`automake` 等？

如果你使用从一个快照到下一个快照更新的 `diff`，或者使用 SVN 仓库，你可能需要若干额外程序来构建 GCC。

这些程序包括但不限于 `autoconf`、`automake`、`bison` 和 `xgettext`。

这是必要的，因为 `diff` 和 `cvs` 都不能保持时间戳正确。这会导致生成文件出现问题，因为 `make` 可能认为这些生成文件已过期，并尝试重新生成它们。

一个简单的解决方法是在 GCC 的 `contrib` 子目录中使用 `gcc_update` 脚本，它会透明地处理此问题，无需安装任何额外工具。

如果你修改了一些源码，或者从 SVN 构建，可能还需要[一些额外工具](https://gcc.gnu.org/install/prerequisites.html#TOC1)。

---

## 为什么我不能构建共享库？

构建共享库时，你可能会从链接器收到类似 `assert pure-text failed:` 或 `DP relative code in file` 的错误消息。

这种错误发生在你链接共享库时未能向 `gcc` 提供正确的标志。

即使共享库的所有 `.o` 文件都使用正确的 PIC 选项编译，也可能出现此错误。构建共享库时，`gcc` 会编译额外代码并包含到库中。该额外代码也必须使用正确的 PIC 选项编译。

在链接行中添加正确的 PIC 选项（`-fpic` 或 `-fPIC`）来创建共享库，可以在以这种方式支持 PIC 的目标上解决此问题。例如：

```sh
gcc -c -fPIC myfile.c
gcc -shared -o libmyfile.so -fPIC myfile.o
```

---

## 构建 C++ 时，链接器说我的构造函数、析构函数或虚表未定义，但我已定义它们

ISO C++ 标准规定，类中所有非纯虚的虚方法都必须定义，但不要求对违反此规则的情况进行任何诊断 `[class.virtual]/8`。基于这一假设，GCC 只会在定义类的第一个此类非内联方法的翻译单元中，生成隐式定义的构造函数、赋值运算符、析构函数和该类的虚表。

因此，如果你未能定义这个特定方法，链接器可能会抱怨缺少看似无关的符号的定义。不幸的是，为了改进此错误消息，可能有必要修改链接器，而这并不总是能够做到。

解决方案是确保所有非纯虚方法都已定义。注意，即使析构函数被声明为纯虚，也必须定义它 `[class.dtor]/7`。

---

如有关于 GCC 使用的问题，请查阅这些网页和 [GCC 手册](https://gcc.gnu.org/onlinedocs/)。如果仍无法解决，[gcc-help@gcc.gnu.org](mailto:gcc-help@gcc.gnu.org) 邮件列表可能会有帮助。欢迎在我们的开发者列表 [gcc@gcc.gnu.org](mailto:gcc@gcc.gnu.org) 上对这些网页和 GCC 开发提出意见。我们的所有[邮件列表](https://gcc.gnu.org/lists.html)都有公开归档。

版权所有 (C) [Free Software Foundation, Inc.](https://www.fsf.org)  
允许在任何媒介中逐字复制和分发整篇文章，前提是保留此声明。

这些页面由 [GCC 团队](https://gcc.gnu.org/about.html)维护。最后修改于 2026-07-21。