https://manpages.debian.org/unstable/genisoimage/genisoimage.1.en.html

# genisoimage

## 名称

`genisoimage` - 创建带可选 Rock Ridge 属性的 ISO9660/Joliet/HFS 文件系统

## 概要

```sh
genisoimage [options] [-o filename] pathspec [pathspec ...]
```

## 描述

`genisoimage` 是一个预 mastering 程序，用于生成 ISO9660/Joliet/HFS 混合文件系统。

`genisoimage` 能够生成由 Rock Ridge Interchange Protocol 指定的 System Use Sharing Protocol records（SUSP）。这用于向 Unix 主机进一步描述 ISO9660 文件系统中的文件，并提供诸如长文件名、UID/GID、POSIX 权限、符号链接以及块设备和字符设备文件等信息。

如果指定了 Joliet 或 HFS 混合命令行选项，`genisoimage` 将创建 Joliet 或 HFS 所需的额外文件系统元数据。否则，`genisoimage` 将生成纯 ISO9660 文件系统。

`genisoimage` 可以生成*真正的*（或*共享的*）HFS 混合文件系统。从 Macintosh 访问时，相同的文件会作为 HFS 文件出现；从其他机器访问时，则作为 ISO9660 文件出现。HFS 代表 *Hierarchical File System*，是 Macintosh 计算机上使用的原生文件系统。

作为替代方案，`genisoimage` 可以为每个文件生成 *Apple Extensions to ISO9660*。这些扩展在从 Macintosh 访问时为每个文件提供 CREATOR、TYPE 和某些 Finder 标志。参见下文 **HFS MACINTOSH FILE FORMATS** 一节。

`genisoimage` 对给定目录树拍摄快照，并生成一个二进制映像，该映像写入块设备后将对应 ISO9660 和/或 HFS 文件系统。

写入 ISO9660 文件系统的每个文件都必须具有 8.3 格式的文件名（最多 8 个字符、一个句点、最多 3 个字符，全部大写），即使使用了 Rock Ridge 也是如此。此文件名用于无法利用 Rock Ridge 扩展的系统（例如 MS-DOS），并且同一目录中的每个文件名必须不同于该目录中的其他文件名。`genisoimage` 通常通过强制将 Unix 文件名转为大写并按需截断来尝试形成正确的名称，但当截断后的名称并非全部唯一时，这通常会产生不理想的结果。`genisoimage` 会为每个文件名分配权重；如果发现两个原本相同的名称，则优先级较低的名称会被重命名，并包含一个保证唯一的 3 位数字。例如，两个文件 `foo.bar` 和 `foo.bar.~1~` 可能被渲染为 `FOO.BAR;1` 和 `FOO000.BAR;1`。

当与各种 HFS 选项一起使用时，`genisoimage` 将尝试识别以多种 Apple/Unix 文件格式存储的文件，并复制数据分叉和资源分叉以及任何相关的 Finder 信息。关于 `genisoimage` 支持的格式，参见下文 **HFS MACINTOSH FILE FORMATS** 一节。

请注意，`genisoimage` 并非设计用于直接与刻录机通信。大多数刻录机具有专有命令集，因制造商而异，你需要专用工具来实际刻录光盘。`wodim` 就是这样的工具之一。最新版本的 `wodim` 可从 [http://www.cdrkit.org/](http://www.cdrkit.org/) 获取。

`pathspec` 是要复制到 ISO9660 文件系统中的目录树的路径。可以指定多个路径，`genisoimage` 将合并所有指定路径组成部分中找到的文件，以形成文件系统映像。

如果指定了 `-graft-points` 选项，则可以将路径移植到根目录以外的位置，并且可以将文件或目录以不同于源文件系统中的名称移植到 cdrom 映像上。用几个例子最容易说明。首先假设本地文件 `../old.lis` 存在，并且你希望将其包含在 cdrom 映像中。

```text
foo/bar/=../old.lis
```

将把 `old.lis` 包含在 cdrom 映像的 `/foo/bar/old.lis` 处，而

```text
foo/bar/xxx=../old.lis
```

将把 `old.lis` 包含在 cdrom 映像的 `/foo/bar/xxx` 处。同样的语法也可用于目录。`genisoimage` 将创建所需的任何目录，以使移植点存在于 cdrom 映像上——这些目录不需要出现在某个路径中。默认情况下，以这种方式动态创建的任何目录将具有权限 `0555`，并且看起来由运行 `genisoimage` 的用户拥有。如果你希望中间目录具有其他权限或所有者，请参见 `-uid`、`-gid`、`-dir-mode`、`-file-mode` 和 `-new-dir-mode`。

当使用 Cygnus 的 cygwin（可从 [http://www.cygwin.com/](http://www.cygwin.com/) 获取）编译时，`genisoimage` 也可在 Windows 机器上运行。因此，本手册页中大多数对 *Unix* 的引用都可以替换为 *Win32*。

## 选项

若干选项可以在 `.genisoimagerc` 配置文件中以及命令行上指定为默认值。如果某个参数在两处都指定，则使用命令行中的设置。关于此文件的格式和可能位置的详细信息，请参见“genisoimagerc(5)”。

- `-abstract` `file`  
    指定摘要文件名。空间为 37 个字符。等价于 `.genisoimagerc` 文件中的 `ABST`。

- `-A` `application_id`  
    指定将写入卷头的文本字符串。它应描述光盘上将包含的应用程序。空间为 128 个字符。等价于 `.genisoimagerc` 文件中的 `APPI`。

- `-allow-limited-size`  
    处理大于 2GiB 且难以在 ISO9660 中表示的文件时，将其以缩小的可见文件大小添加到 ISO9660，并以正确的可见文件大小添加到 UDF 系统。结果是文件系统不一致，用户需要确保他们确实使用 UDF 而不是 ISO9660 驱动来读取此类磁盘。隐含启用 `-udf`。

- 
    ```text
    -allow-leading-dots
    -ldots
    ```
    允许 ISO9660 文件名以句点开头。通常，前导句点会被替换为下划线，以保持 MS-DOS 兼容性。  
    这违反 ISO9660 标准，但在许多系统上恰好可用。请谨慎使用。

- `-allow-lowercase`  
    此选项允许小写字符出现在 ISO9660 文件名中。  
    这违反 ISO9660 标准，但在某些系统上恰好可用。请谨慎使用。

- `-allow-multidot`  
    此选项允许 ISO9660 文件名中出现多个句点。前导句点不受此选项影响，可以通过 `-allow-leading-dots` 单独允许。  
    这违反 ISO9660 标准，但在许多系统上恰好可用。请谨慎使用。

- `-biblio` `file`  
    指定书目文件名。空间为 37 个字符。等价于 `.genisoimagerc` 文件中的 `BIBL`。

- 
    ```text
    -cache-inodes
    -no-cache-inodes
    ```
    启用或禁用 inode 和设备号缓存，以查找文件的硬链接。如果 `genisoimage` 找到硬链接（具有多个名称的文件），该文件也将在 CD 上被硬链接，因此文件内容只出现一次。这有助于节省空间。`-cache-inodes` 在类 Unix 操作系统上是默认值，但在某些其他系统（如 Cygwin）上默认是 `-no-cache-inodes`，因为在这些系统上不能安全地假定 inode 号唯一。（某些版本的 Cygwin 使用弱哈希算法创建伪造的 inode 号，可能产生重复。）如果两个文件具有相同的 inode 号但不是指向同一文件的硬链接，`genisoimage -cache-inodes` 将无法正确工作。`-no-cache-inodes` 在所有情况下都是安全的，但在这种情况下 `genisoimage` 无法检测硬链接，因此生成的 CD 映像可能比必要的大。

- `-alpha-boot` `alpha_boot_image`  
    指定制作 Alpha/SRM 可启动 CD 时要使用的启动映像的路径和文件名。路径名必须相对于传递给 `genisoimage` 的源路径。

- `-hppa-bootloader` `hppa_bootloader_image`  
    指定制作 HPPA 可启动 CD 时要使用的启动映像的路径和文件名。路径名必须相对于传递给 `genisoimage` 的源路径。还需要其他选项，至少需要内核文件名和启动命令行。更多信息请参见下文 **HPPA NOTES** 一节。

- `-hppa-cmdline` `hppa_boot_command_line`  
    指定制作可启动 CD 时传递给 HPPA 引导加载程序的命令行。参数用空格或逗号分隔。必须向 `genisoimage` 传递更多选项，至少需要内核文件名和引导加载程序文件名。更多信息请参见下文 **HPPA NOTES** 一节。

- 
    ```text
    -hppa-kernel-32 hppa_kernel_32
    -hppa-kernel-64 hppa_kernel_64
    ```
    指定制作 HPPA 可启动 CD 时要使用的 32 位和/或 64 位内核映像的路径和文件名。路径名必须相对于传递给 `genisoimage` 的源路径。还需要其他选项，至少需要引导加载程序文件名和启动命令行。更多信息请参见下文 **HPPA NOTES** 一节。

- `-hppa-ramdisk` `hppa_ramdisk_image`  
    指定制作 HPPA 可启动 CD 时要使用的 ramdisk 映像的路径和文件名。路径名必须相对于传递给 `genisoimage` 的源路径。此参数是可选的。还需要其他选项，至少需要内核文件名和启动命令行。更多信息请参见下文 **HPPA NOTES** 一节。

- `-mips-boot` `mips_boot_image`  
    指定制作 SGI/big-endian MIPS 可启动 CD 时要使用的启动映像的路径和文件名。路径名必须相对于传递给 `genisoimage` 的源路径。此选项可以多次指定，最多存储 15 个启动映像。

- `-mipsel-boot` `mipsel_boot_image`  
    指定制作 DEC/little-endian MIPS 可启动 CD 时要使用的启动映像的路径和文件名。路径名必须相对于传递给 `genisoimage` 的源路径。

- 
    ```text
    -B img_sun4,img_sun4c,img_sun4m,img_sun4d,img_sun4e
    -sparc-boot img_sun4,img_sun4c,img_sun4m,img_sun4d,img_sun4e
    ```
    指定制作 SPARC 系统可启动 CD 所需的启动映像的逗号分隔列表。分区 0 用于 ISO9660 映像，第一个映像文件映射到分区 1。逗号分隔列表最多可有 7 个字段，包括空字段。此选项是制作 Sun SPARC 系统可启动 CD 所必需的。如果指定了 `-B` 或 `-sparc-boot`，则生成映像的第一个扇区将包含 Sun 磁盘标签。此磁盘标签为 ISO9660 映像指定切片 0，并为使用此选项指定的启动映像指定切片 1 到 7。每个额外启动映像内的字节偏移 512 到 8191 必须包含适用于相应 SPARC 架构的主引导程序。每个映像的其余部分通常包含用于主内核启动阶段的 UFS 文件系统。

    实现的启动方法是 SunOS 4.x 和 SunOS 5.x 中的方法。但是，它不依赖于 SunOS 内部结构，而只依赖于 Open Boot prom 的属性，因此它应可用于任何用于 SPARC 系统的操作系统。更多信息另请参见下文 **NOTES** 一节。

    如果使用特殊文件名 `...`，则实际及所有后续启动分区都映射到前一个分区。如果以 `-G` `image` `-B` `...` 调用 `genisoimage`，则所有启动分区都映射到包含 ISO9660 文件系统映像的分区，并且位于光盘前 16 个扇区中的通用启动映像将用于所有架构。

- `-G` `generic_boot_image`  
    指定制作通用可启动 CD 时要使用的通用启动映像的路径和文件名。启动映像将放置在 CD 的前 16 个扇区中，位于 ISO9660 主卷描述符之前。如果此选项与 `-sparc-boot` 一起使用，Sun 磁盘标签将覆盖通用启动映像的前 512 字节。

- `-b` `eltorito_boot_image`  
    指定为 x86 PC 制作 El Torito 可启动 CD 时要使用的启动映像的路径和文件名。路径名必须相对于传递给 `genisoimage` 的源路径。此选项是制作 El Torito 可启动 CD 所必需的。启动映像必须正好为 1200 kB、1440 kB 或 2880 kB，`genisoimage` 在创建输出 ISO9660 文件系统时将使用此大小。PC BIOS 将使用该映像模拟软盘，因此第一个 512 字节扇区应包含 PC 启动代码。例如，如果启动映像是基于 LILO 的启动软盘，这将起作用。

    如果启动映像不是软盘映像，则需要添加 `-hard-disk-boot` 或 `-no-emul-boot`。如果系统不应从模拟磁盘启动，请使用 `-no-boot`。

    如果未指定 `-sort`，启动映像会以低优先级（+2）排序到介质开头。如果不喜欢这样，需要为启动映像指定排序权重 0。

- `-eltorito-alt-boot`  
    使用一组新的 El Torito 启动参数开始。单张 CD 上最多可存储 63 个 El Torito 启动条目。

- `-hard-disk-boot`  
    指定用于创建 El Torito 可启动 CD 的启动映像是硬盘映像。该映像必须以包含单个分区的主引导记录开头。

- `-no-emul-boot`  
    指定用于创建 El Torito 可启动 CD 的启动映像是“无仿真”映像。系统将加载并执行此映像，而不执行任何磁盘仿真。

- `-no-boot`  
    指定创建的 El Torito CD 应标记为不可启动。系统将为该映像提供模拟驱动器，但会从标准启动设备启动。

- `-boot-load-seg` `segment_address`  
    指定无仿真 El Torito CD 的启动映像的加载段地址。

- `-boot-load-size` `load_sectors`  
    指定无仿真模式下要加载的“虚拟”（512 字节）扇区数。默认是加载整个启动文件。如果不是 4 的倍数，某些 BIOS 可能会出现问题。

- `-boot-info-table`  
    指定将在启动文件中偏移 8 处修补一个包含 CD-ROM 布局信息的 56 字节表。如果给出此选项，启动文件将*在源文件系统中被修改*，因此如果此文件不易重新生成，请制作副本！关于此表的描述，参见 **EL TORITO BOOT INFO TABLE** 一节。

- `-C` `last_sess_start,next_sess_start`  
    此选项用于创建 CD Extra 或多会话光盘的第二会话或更高级会话的映像。`-C` 接受两个用逗号分隔的数字。第一个是应追加到的光盘最后会话中的第一个扇区。第二个数字是新会话的起始扇区号。正确的数字可以通过调用 `wodim -msinfo ...` 获取。如果 `-C` 与 `-M` 一起使用，`genisoimage` 将创建一个旨在作为前一会话延续的文件系统映像。如果 `-C` 不与 `-M` 一起使用，`genisoimage` 将创建一个旨在用于 CD Extra 第二会话的文件系统映像。这是一种多会话 CD，第一会话保存音频数据，第二会话保存 ISO9660 文件系统。

- `-c` `boot_catalog`  
    指定启动目录的路径和文件名，El Torito 可启动 CD 需要它。路径名必须相对于传递给 `genisoimage` 的源路径。此文件将插入到输出树中，而不会在源文件系统中创建，因此请确保指定的文件名不与现有文件冲突，否则它将被排除。通常选择类似 `boot.catalog` 的名称。

    如果未指定 `-sort`，启动目录会以低优先级（+1）排序到介质开头。如果不喜欢这样，需要为启动目录指定排序权重 0。

- `-check-oldnames`  
    检查从旧会话导入的所有文件名是否符合 ISO9660 文件命名规则。没有此选项时，仅检查长度超过 31 个字符的名称，因为这些文件严重违反 ISO9660 标准。

- `-check-session` `file`  
    检查所有旧会话是否符合实际的 `genisoimage` ISO9660 文件命名规则。这是一个高级选项，组合了 `-M` `file` `-C 0,0 -check-oldnames`。关于参数 `file`，参见 `-M` 的描述。

- `-copyright` `file`  
    指定版权信息，通常是光盘上的文件名。空间为 37 个字符。等价于 `.genisoimagerc` 文件中的 `COPY`。

- `-d`  
    不要为没有句点的文件附加句点。  
    这违反 ISO9660 标准，但在许多系统上恰好可用。请谨慎使用。

- `-D`  
    不要使用深层目录重定位，而是按我们看到的方式打包它们。  
    如果未选择 ISO9660:1999，这违反 ISO9660 标准，但在许多系统上恰好可用。请谨慎使用。

- `-dir-mode` `mode`  
    将用于创建映像的目录模式覆盖为 `mode`，以 `chmod(1)` 中的 4 位权限位指定。此选项自动启用 Rock Ridge 扩展。

- `-dvd-video`  
    生成符合 DVD-Video 的 UDF 文件系统。这是通过排序相应文件内容的顺序并在需要时在文件之间添加填充来完成的。请注意，排序仅在 DVD-Video 文件名仅包含大写字符时有效。

    请注意，为了获得符合 DVD-Video 的文件系统映像，你需要准备符合 DVD-Video 的目录树。这要求结果 DVD 的根目录中有目录 `VIDEO_TS`（全大写），通常还有另一个目录 `AUDIO_TS`。`VIDEO_TS` 需要包含符合 DVD-Video 文件系统所需的所有文件（文件名必须全部大写）。

- `-f`  
    生成文件系统时跟随符号链接。当不使用此选项时，如果启用了 Rock Ridge，符号链接将使用 Rock Ridge 录入，否则将被忽略。

- `-file-mode` `mode`  
    将用于创建映像的普通文件模式覆盖为 `mode`，以 `chmod(1)` 中的 4 位权限位指定。此选项自动启用 Rock Ridge 扩展。

- `-gid` `gid`  
    将从源文件读取的组 ID 覆盖为 `gid` 的值。指定此选项会自动启用 Rock Ridge 扩展。

- `-gui`  
    切换 GUI 行为。这目前会使输出更详细，但将来可能有其他效果。

- `-graft-points`  
    允许对文件名使用移植点。如果使用此选项，将检查所有文件名中的移植点。文件名在第一个未转义的等号处分割。如果指定了 `-graft-points`，所有出现的 `\` 和 `=` 字符都必须用 `\` 转义。

- `-hide` `glob`  
    隐藏任何匹配 `glob`（shell 通配符模式）的文件，使其不在 ISO9660 或 Rock Ridge 目录中显示。`glob` 可以匹配文件名或路径的任何部分。如果 `glob` 匹配目录，则该目录的内容将被隐藏。为了匹配目录名，请确保路径名不包含尾部 `/` 字符。所有隐藏文件仍将写入输出 CD 映像文件。另请参见 `-hide-joliet` 和 `README.hide`。此选项可以多次使用。

- `-hide-list` `file`  
    包含要隐藏的 shell 通配符列表的文件。参见 `-hide`。

- `-hidden` `glob`  
    为匹配 `glob`（shell 通配符模式）的文件和目录添加隐藏（存在）ISO9660 目录属性。此属性将阻止某些 MS-DOS 和 Windows 命令显示这些文件。`glob` 可以匹配文件名或路径的任何部分。为了匹配目录名，请确保路径名不包含尾部 `/` 字符。此选项可以多次使用。

- `-hidden-list` `file`  
    包含要获取隐藏属性的 shell 通配符列表的文件。参见 `-hidden`。

- `-hide-joliet` `glob`  
    隐藏匹配 `glob`（shell 通配符模式）的文件和目录，使其不在 Joliet 目录中显示。`glob` 可以匹配文件名或路径的任何部分。如果 `glob` 匹配目录，则该目录的内容将被隐藏。为了匹配目录名，请确保路径名不包含尾部 `/` 字符。所有隐藏文件仍将写入输出 CD 映像文件。此选项通常与 `-hide` 一起使用。另请参见 `README.hide`。此选项可以多次使用。

- `-hide-joliet-list` `file`  
    包含要从 Joliet 树中隐藏的 shell 通配符列表的文件。参见 `-hide-joliet`。

- `-hide-joliet-trans-tbl`  
    从 Joliet 树中隐藏 `TRANS.TBL` 文件。这些文件在 Joliet 环境中通常没有意义，因为它们列出了真实名称和 ISO9660 名称，而这两个名称可能都与 Joliet 名称不同。

- `-hide-rr-moved`  
    在 Rock Ridge 树中将目录 `RR_MOVED` 重命名为 `.rr_moved`。似乎无法从 Rock Ridge 树中完全隐藏 `RR_MOVED` 目录。此选项只会让不了解此目录用途的人觉得可见树不那么令人困惑。如果你需要完全没有 `RR_MOVED` 目录，应使用 `-D`。请注意，如果指定了 `-D`，生成的文件系统不符合 ISO9660 level-1，并且将无法在 MS-DOS 上读取。另请参见 **NOTES** 一节。

- `-input-charset` `charset`  
    输入字符集，定义本地文件名中使用的字符。要获取有效字符集名称列表，请调用 `genisoimage -input-charset help`。要获得 1:1 映射，可以使用 `default` 作为字符集名称。默认初始值在基于 DOS 的系统上为 `cp437`，在所有其他系统上为 `iso8859-1`。更多详细信息请参见下文 **CHARACTER SETS** 一节。

- `-output-charset` `charset`  
    输出字符集，定义 Rock Ridge 文件名中将使用的字符。默认为输入字符集。更多详细信息请参见下文 **CHARACTER SETS** 一节。

- `-iso-level` `level`  
    设置 ISO9660 符合级别。有效数字为 1 到 4。

    对于级别 1，文件只能由一个区段组成，文件名限制为 8.3 个字符。

    对于级别 2，文件只能由一个区段组成。

    对于级别 3，没有限制（除 ISO-9660:1988 外）适用。

    对于从 1 到 3 的所有 ISO9660 级别，所有文件名都限制为大写字母、数字和下划线（`_`）。文件名限制为 31 个字符，目录嵌套限制为 8 层，路径名限制为 255 个字符。

    级别 4 正式不存在，但 `genisoimage` 将其映射到 ISO-9660:1999，即 ISO9660 版本 2。

    对于级别 4，将发出增强卷描述符，其版本号和文件结构版本号设置为 2。目录嵌套不限于 8 层，文件无需包含句点，句点也没有特殊含义，文件名没有版本号，文件名最长可达 207 个字符；如果使用 Rock Ridge，则为 197 个字符。

    创建版本 2 映像时，`genisoimage` 会发出增强卷描述符，它类似于主卷描述符但不完全相同。注意不要使用有缺陷的软件，通过假定第二个 PVD 副本并将此假定 PVD 副本修补为 El Torito VD 来使 ISO9660 映像可启动。

- `-J`  
    除常规 ISO9660 文件名外，还生成 Joliet 目录记录。当光盘要在 Windows 机器上使用时，这特别有用。Joliet 文件名以 Unicode 指定，每个路径组成部分最长可达 64 个 Unicode 字符。请注意，Joliet 不是标准——只有 Microsoft Windows 和 Linux 系统可以读取 Joliet 扩展。为了更好的可移植性，考虑同时使用 Joliet 和 Rock Ridge 扩展。

- `-joliet-long`  
    允许 Joliet 文件名最长可达 103 个 Unicode 字符，而不是 64 个。这破坏 Joliet 规范，但似乎可用。请谨慎使用。

- `-jcharset` `charset`  
    `-J -input-charset` `charset` 的组合。更多详细信息请参见下文 **CHARACTER SETS** 一节。

- `-l`  
    允许完整的 31 字符文件名。通常 ISO9660 文件名将采用与 MS-DOS 兼容的 8.3 格式，即使 ISO9660 标准允许文件名最多 31 个字符。如果使用此选项，光盘在 MS-DOS 系统上可能难以使用，但在大多数其他系统上可以工作。请谨慎使用。

- `-L`  
    过时选项；请改用 `-allow-leading-dots`。

- `-jigdo-jigdo` `jigdo_file`  
    除文件系统映像外，还生成 `jigdo` `.jigdo` 元数据文件。更多信息请参见下文 **JIGDO NOTES** 一节。

- `-jigdo-template` `template_file`  
    除文件系统映像外，还生成 `jigdo` `.template` 文件。更多信息请参见下文 **JIGDO NOTES** 一节。

- `-jigdo-min-file-size` `size`  
    指定要在 `.jigdo` 文件中列出的文件的最小大小。默认值（也是允许的最小值）为 1KB。更多信息请参见下文 **JIGDO NOTES** 一节。

- `-jigdo-force-md5` `path`  
    指定一个文件模式，其中文件*必须*包含在由 `-md5-list` 提供的外部 MD5 列表中。更多信息请参见下文 **JIGDO NOTES** 一节。

- `-jigdo-exclude` `path`  
    指定一个文件模式，其中文件不会列在 `.jigdo` 文件中。更多信息请参见下文 **JIGDO NOTES** 一节。

- `-jigdo-map` `path`  
    指定 jigdo 文件的模式映射（例如 `Debian=/mirror/debian`）。更多信息请参见下文 **JIGDO NOTES** 一节。

- `-md5-list` `md5_file`  
    指定一个文件，其中包含要包含在 `.jigdo` 文件中的文件的 MD5 校验和、大小和路径名。更多信息请参见下文 **JIGDO NOTES** 一节。

- `-jigdo-template-compress` `algorithm`  
    指定用于模板数据的压缩算法。当前支持 gzip 和 bzip2，默认是 gzip。更多信息请参见下文 **JIGDO NOTES** 一节。

- `-log-file` `log_file`  
    将所有错误、警告和信息性消息重定向到 `log_file`，而不是标准错误。

- `-m` `glob`  
    排除匹配 `glob`（shell 通配符模式）的文件，不将其写入 CD-ROM。`glob` 可以匹配文件名组成部分或完整路径名。此选项可以多次使用。例如：

    ```sh
    genisoimage -o rom -m '*.o' -m core -m foobar
    ```

    将排除所有以 `.o` 结尾的文件，或名为 `core` 或 `foobar` 的文件。请注意，如果你有一个名为 `foobar` 的目录，它（当然还有其所有后代）也将被排除。

- `-exclude-list` `file`  
    包含要排除的 shell 通配符列表的文件。参见 `-m`。

- `-max-iso9660-filenames`  
    允许 ISO9660 文件名最长可达 37 个字符。此选项启用 `-N`，因为额外名称空间取自为文件版本号保留的空间。  
    这违反 ISO9660 标准，但在许多系统上恰好可用。尽管符合规范的应用程序需要提供至少 37 个字符的缓冲区空间，但使用此选项创建的光盘可能导致读取操作系统中的缓冲区溢出。请极其谨慎使用。

- 
    ```text
    -M path
    -M device
    -dev device
    ```
    指定要合并的现有 ISO9660 映像的路径。替代形式接受 SCSI 设备说明符，其语法与 `wodim` 的 `dev=` 参数相同。`genisoimage` 的输出将是一个新会话，应写入 `-M` 指定映像的末尾。通常这要求用于写入映像的 CD 刻录机具有多会话能力。此选项只能与 `-C` 一起使用。

- `-N`  
    省略 ISO9660 文件名中的版本号。  
    这违反 ISO9660 标准，但反正没有人真正使用版本号。请谨慎使用。

- `-new-dir-mode` `mode`  
    指定在文件系统映像中创建新目录时要使用的模式，为 `chmod(1)` 中使用的 4 位数字。默认值为 `0555`。

- 
    ```text
    -nobak
    -no-bak
    ```
    在 ISO9660 文件系统上排除备份文件；即文件名包含字符 `~` 或 `#`，或以 `.bak` 结尾的文件。这些通常是 Unix 文本编辑器的备份文件。

- `-force-rr`  
    不要对以前的会话使用自动 Rock Ridge 属性识别。这可以绕过例如 NERO Burning ROM 创建的映像的问题。

- `-no-rr`  
    不要使用以前会话中的 Rock Ridge 属性。当 `genisoimage` 在旧会话上发现非法 Rock Ridge 签名时，这可能有助于避免问题。

- `-no-split-symlink-components`  
    不要拆分符号链接组成部分，而是开始新的 Continuation Area（CE）。这可能会浪费一些空间，但 SunOS 4.1.4 cdrom 驱动程序在读取拆分的符号链接组成部分时存在缺陷。

    如今此选项是否有用值得怀疑。

- `-no-split-symlink-fields`  
    不要拆分符号链接字段，而是开始新的 Continuation Area（CE）。这可能会浪费一些空间，但 SunOS 4.1.4 和 Solaris 2.5.1 cdrom 驱动程序在读取拆分的符号链接字段时存在缺陷（可能丢失 `/`）。

    如今此选项是否有用值得怀疑。

- `-o` `filename`  
    指定 ISO9660 文件系统映像的输出文件。这可以是磁盘文件、磁带驱动器，也可以直接对应光盘写入器的设备名。如果未指定，则使用 stdout。请注意，输出也可以是常规磁盘分区的块设备，在这种情况下，可以正常挂载 ISO9660 文件系统以验证其生成正确。

- `-pad`  
    在整个映像末尾填充 150 个扇区（300 kB）。此选项默认启用。如果与 `-B` 一起使用，则在 ISO9660 分区和启动分区之间插入填充，使第一个启动分区从 16 的倍数扇区号开始。

    需要填充，因为许多操作系统（例如 Linux）在其文件系统 I/O 中实现了预读缺陷。这些缺陷会导致位于轨道末尾附近的文件出现读取错误，特别是当光盘以 Track At Once 模式写入，或者数据轨道之后跟着 CD 音频轨道时。

- `-no-pad`  
    不要在末尾填充 150 个扇区（300 kB），也不要使启动分区从 16 个扇区的倍数开始。

- `-path-list` `file`  
    包含要添加到 ISO9660 文件系统的 `pathspec` 目录和文件名列表的文件。此 pathspec 列表在命令行上出现的任何 pathspec 之后处理。如果参数为 `-`，则从标准输入读取列表。

- `-P`  
    过时选项；请改用 `-publisher`。

- `-publisher` `publisher_id`  
    指定将写入卷头的文本字符串。它应描述 CD-ROM 的出版商，通常包含邮寄地址和电话号码。空间为 128 个字符。等价于 `.genisoimagerc` 文件中的 `PUBL`。

- `-p` `preparer_id`  
    指定将写入卷头的文本字符串。它应描述 CD-ROM 的准备者，通常包含邮寄地址和电话号码。空间为 128 个字符。等价于 `.genisoimagerc` 文件中的 `PREP`。

- `-creation-date` `epoch`  
    指定用作卷描述符中的创建、修改和生效日期，以及动态创建的文件和重定位的日期。以自 1970-01-01 00:00:00 +0000（UTC）以来的秒数指定；如果为 0，则使用当前时间。

- `-print-size`  
    以扇区大小（2048 字节）的倍数打印估计的文件系统大小并退出。Disk At Once 模式以及直接管道到 `wodim` 时某些 CD-R 驱动器需要此选项，在这些情况下 `wodim` 需要预先知道文件系统映像的大小。旧版本的 `mkisofs` 将此信息（以及其他信息）写入 `stderr`。由于发现难以解析，现在也将不带其他信息的数字打印到 `stdout`。如果你喜欢编写简单的 shell 脚本，可以重定向 `stderr` 并从 `stdout` 捕获数字。可以这样：

    ```sh
    cdblocks=`genisoimage -print-size -quiet ...`
    genisoimage ... | wodim ... tsize=${cdblocks}s -
    ```

- `-quiet`  
    这使 `genisoimage` 更加不详细。将不提供进度输出。

- `-R`  
    使用 Rock Ridge 协议生成 SUSP 和 RR 记录，以进一步描述 ISO9660 文件系统上的文件。

- `-r`  
    这类似于 `-R` 选项，但文件所有权和模式设置为更有用的值。uid 和 gid 设置为零，因为它们通常只在作者系统上有用，对客户端无用。所有文件读取位都设置为真，以便文件在客户端上全局可读。如果为文件设置了任何执行位，则设置所有执行位，以便可执行文件在客户端上全局可执行。如果为目录设置了任何搜索位，则设置所有搜索位，以便目录在客户端上全局可搜索。所有写位都清除，因为文件系统在任何情况下都将以只读方式挂载。如果设置了任何特殊模式位，则清除它们，因为文件锁在只读文件系统上无用，并且对于 uid 0 或 gid 0 来说 set-id 位不可取。在 Win32 上使用时，执行位将在*所有*文件上设置。这是由于 Win32 上缺少文件权限以及 Cygwin POSIX 仿真层。另请参见 `-uid`、`-gid`、`-dir-mode`、`-file-mode` 和 `-new-dir-mode`。

- `-relaxed-filenames`  
    允许 ISO9660 文件名包含除小写字母外的所有 7 位 ASCII 字符。  
    这违反 ISO9660 标准，但在许多系统上恰好可用。请谨慎使用。

- `-root` `dir`  
    将所有文件和目录移动到映像中的 `dir`。这本质上与使用 `-graft-points` 并在每个 pathspec 前添加 `dir` 相同，但更易于使用。`dir` 实际上可以有多层深。它使用与其他移植点相同的权限创建。

- `-old-root` `dir`  
    当写入多会话映像且先前（或更旧）会话使用 `-root` `dir` 写入时，此选项是必需的。使用前一会话中未找到的目录名会导致 `genisoimage` 中止并报错。没有此选项，`genisoimage` 将无法找到未修改的文件，并被迫将其数据再次写入映像。`-root` 和 `-old-root` 旨在一起用于增量备份。初始会话例如使用：`genisoimage -root backup_1` `dirs`。下一次使用 `genisoimage -root backup_2 -old-root backup_1` `dirs` 的增量备份将对这些目录拍摄另一份快照。第一份快照将在 `backup_1` 中找到，第二份在 `backup_2` 中，但只有修改或新增的文件需要写入第二会话。没有这些选项，新文件将被添加，旧文件将被保留。但如果文件被修改，旧文件将被覆盖。通过从 CD 复制整个目录回来恢复文件也会恢复被有意删除的文件。访问文件的多个旧版本需要操作系统支持选择要挂载哪些会话。

- `-sort` `sort_file`  
    对介质上的文件位置进行排序。排序由包含文件名和排序偏移权重对的文件控制。如果权重较高，文件将位于更靠近介质开头的位置；如果权重较低，文件将位于更靠近介质末尾的位置。文件名和权重之间只能有一个空格或制表符，权重必须是行上的最后字符。文件名包括直到但不包括行上最后一个空格或制表符字符的所有字符。这是为了允许文件名中或末尾有空格字符。此选项**不会**排序 ISO9660 目录中出现的文件名顺序。它排序文件数据写入 CD 映像的顺序，这对于优化 CD 上的数据布局很有用。更多详细信息请参见 `README.sort`。

- `-sparc-boot` `img_sun4,img_sun4c,img_sun4m,img_sun4d,img_sun4e`  
    参见上文 `-B`。

- `-sparc-label` `label`  
    设置使用 `-sparc-boot` 创建的 Sun 磁盘标签的 Sun 磁盘标签名称。

- `-split-output`  
    将输出映像拆分为多个约 1 GB 的文件。这有助于在不支持大文件的操作系统上创建 DVD 大小的 ISO9660 映像。写入 DVD 时，`wodim` 会将多个文件连接成单个轨道。要使 `-split-output` 工作，必须指定 `-o` `filename`。生成的输出映像将命名为：`filename_00`、`filename_01`、`filename_02`……

- `-stream-media-size` `#`  
    选择流式操作并将介质大小设置为 `#` 个扇区。这允许你将 `tar(1)` 程序的输出管道到 `genisoimage`，并创建 ISO9660 文件系统，而无需中间 tar 归档文件。如果指定了此选项，`genisoimage` 从 `stdin` 读取并创建名为 `STREAM.IMG` 的文件。文件的最大大小（含填充）比指定介质大小少 200 个扇区。如果指定了 `-no-pad`，则文件大小比指定介质大小少 50 个扇区。如果文件较小，`genisoimage` 将写入填充。这可能需要一段时间。

    选项 `-stream-media-size` 仅创建简单 ISO9660 文件系统，不得与多会话或混合文件系统选项一起使用。

- `-stream-file-name` `name`  
    保留供将来使用。

- `-sunx86-boot` `UFS_img,,,AUX1_img`  
    指定制作 Solaris x86 系统可启动 CD 所需的文件系统映像的逗号分隔列表。

    请注意，分区 1 用于 ISO9660 映像，分区 2 是整个磁盘，因此分区 1 和 2 不得被外部分区数据使用。第一个映像文件映射到分区 0。逗号分隔列表中可以有空字段，分区 1 和 2 的列表项必须为空。支持的最大分区数为 8（尽管 Solaris x86 分区表最多可支持 16 个分区），因此不可能指定超过 6 个分区映像。此选项是制作 Solaris x86 系统可启动 CD 所必需的。

    如果指定了 `-sunx86-boot`，则生成映像的第一个扇区将包含 PC fdisk 标签，其中 Solaris 类型 0x82 的 fdisk 分区从偏移 512 开始并跨越整个 CD。此外，对于 Solaris 类型 0x82 的 fdisk 分区，在 CD 第一个扇区的偏移 1024 处有一个 SVr4 磁盘标签。此磁盘标签为用于启动 PC 的第一个（通常为 UFS 类型）文件系统映像指定切片 0，并为 ISO9660 映像指定切片 1。切片 2 跨越整个 CD，切片 3……切片 7 可用于使用此选项指定的额外文件系统映像。

    Solaris x86 启动 CD 使用 1024 字节大小的主引导程序，它使用 **El-Torito no-emulation** 启动模式，以及位于 CD 扇区 1..15 中的次级通用引导程序。因此，必须同时指定 `-b` `bootimage` `-no-emul-boot` 和 `-G` `genboot`。

- `-sunx86-label` `label`  
    设置使用 `-sunx86-boot` 创建的 SVr4 磁盘标签的 SVr4 磁盘标签名称。

- `-sysid` `ID`  
    指定系统 ID。空间为 32 个字符。等价于 `.genisoimagerc` 文件中的 `SYSI`。

- `-T`  
    在 CD-ROM 上的每个目录中生成文件 `TRANS.TBL`，可用于不支持 Rock Ridge 的系统，以帮助建立正确的文件名。文件中还存在指示块设备和字符设备主设备号和次设备号的信息，并且每个符号链接都给出了链接文件的名称。

- `-table-name` `table_name`  
    替代翻译表文件名（见上文）。隐含 `-T`。如果要创建多会话映像，必须使用与前一会话相同的名称。

- `-ucs-level` `level`  
    设置 Joliet SVD 中的 Unicode 符合级别。默认级别为 3。可以使用此选项将其设置为 1..3。

- `-udf`  
    在生成的文件系统映像中包含 UDF 文件系统支持。UDF 支持目前处于 alpha 状态，因此无法创建仅 UDF 映像。UDF 数据结构目前与 Joliet 结构耦合，因此当前实现有许多陷阱。没有 UID/GID 支持，没有 POSIX 权限支持，没有符号链接支持。请注意，除了真实 UDF 数据结构所需的空间外，UDF 还会浪费光盘开头约扇区 20 到扇区 256 的空间。

- `-uid` `uid`  
    将从源文件读取的 uid 覆盖为 `uid` 的值。指定此选项会自动启用 Rock Ridge 扩展。

- `-use-fileversion`  
    选项 `-use-fileversion` 允许 `genisoimage` 使用文件系统中的文件版本号。如果未指定该选项，`genisoimage` 为所有文件创建版本号 1。文件版本是范围 `;1` 到 `;32767` 的字符串。此选项在 VMS 上是默认值。

- `-U`  
    允许“未翻译”的文件名，完全违反上述 ISO9660 标准。启用以下标志：`-d -l -N -allow-leading-dots -relaxed-filenames -allow-lowercase -allow-multidot -no-iso-translate`。允许文件名中出现多个 `.` 字符，以及混合大小写文件名。这在 HP-UX 上很有用，因为内置的 `cdfs` 文件系统不识别任何扩展。请极其谨慎使用。

- `-no-iso-translate`  
    不要转换对 ISO9660 文件名无效的字符 `#` 和 `~`。尽管无效，但这些字符经常被 Microsoft 系统使用。  
    这违反 ISO9660 标准，但在许多系统上恰好可用。请谨慎使用。

- `-V` `volid`  
    指定要写入主块的卷 ID（卷名或标签）。空间为 32 个字符。等价于 `.genisoimagerc` 文件中的 `VOLI`。卷 ID 被 Solaris 卷管理器用作挂载点，并在各种其他平台（如 Windows 和 Apple Mac OS）上作为分配给光盘的标签。

- `-volset` `ID`  
    指定卷集 ID。空间为 128 个字符。等价于 `.genisoimagerc` 文件中的 `VOLS`。

- `-volset-size` `#`  
    将卷集大小设置为 `#`。卷集大小是 CD 卷集中的 CD 数量。卷集是一个或多个卷的集合，文件集记录在这些卷上。

    卷集不打算用于创建编号 CD 集，例如操作系统安装 CD 集的一部分。卷集更多用于记录无法放入单个卷的大型目录树。卷集的每个卷都包含对记录在卷上的所有目录和文件的描述，这些卷的序列号小于或等于当前卷分配的卷集大小。

    `genisoimage` 目前不支持大于 1 的 `-volset-size`。

    在每个命令行上，选项 `-volset-size` 必须在 `-volset-seqno` 之前指定。

- `-volset-seqno` `#`  
    将卷集序列号设置为 `#`。卷集序列号是 CD 集中当前 CD 的索引号。在每个命令行上，选项 `-volset-size` 必须在 `-volset-seqno` 之前指定。

- `-v`  
    详细执行。如果在命令行上给出两次，将打印额外调试信息。

- `-x` `glob`  
    与 `-m` `glob` 相同。

- `-z`  
    为透明压缩文件生成特殊 `RRIP` 记录。这仅对支持透明解压缩的主机有用和有趣，例如 Linux 2.4.14 或更高版本。必须指定 `-R` 或 `-r` 以启用 Rock Ridge，并在运行 `genisoimage` 之前使用 `mkzftree` 实用程序生成压缩文件。请注意，透明压缩是非标准 Rock Ridge 扩展。生成的光盘只有在 Linux 上使用时才能透明读取。在其他操作系统上，你需要手动调用 `mkzftree` 来解压缩文件。

## HFS 选项

- `-hfs`  
    创建 ISO9660/HFS 混合 CD。此选项应与 `-map`、`-magic` 和/或下面给出的各种*双短横线*选项一起使用。

- `-apple`  
    创建带有 Apple 扩展的 ISO9660 CD。类似于 `-hfs`，不同之处在于添加的是 Apple Extensions to ISO9660，而不是创建 HFS 混合卷。以前的 `genisoimage` 版本如果指定了 `-apple`，默认会包含 Rock Ridge 属性。此版本的 `genisoimage` 不再这样做。如果你希望拥有 Rock Ridge 属性，需要单独指定。

- `-map` `mapping_file`  
    使用 `mapping_file` 根据文件名的扩展名设置文件的 CREATOR 和 TYPE 信息。仅当文件不是已知 Apple/Unix 文件格式之一时，才会映射文件名。参见下文 **HFS CREATOR/TYPE** 一节。

- `-magic` `magic_file`  
    通过使用文件的*魔数*（通常是文件的前几个字节）来设置 CREATOR 和 TYPE 信息。仅当文件不是已知 Apple/Unix 文件格式之一，或者文件名扩展名尚未使用 `-map` 映射时，才使用 `magic_file`。更多详细信息请参见下文 **HFS CREATOR/TYPE** 一节。

- `-hfs-creator` `creator`  
    为所有文件设置默认 CREATOR。必须正好为 4 个字符。更多详细信息请参见下文 **HFS CREATOR/TYPE** 一节。

- `-hfs-type` `type`  
    为所有文件设置默认 TYPE。必须正好为 4 个字符。更多详细信息请参见下文 **HFS CREATOR/TYPE** 一节。

- `-probe`  
    在文件内容中搜索所有已知 Apple/Unix 文件格式。关于这些格式的更多信息，参见下文 **HFS MACINTOSH FILE FORMATS** 一节。但是，检查 *MacBinary* 和 *AppleSingle* 文件的唯一方法是打开并读取它们，因此此选项可能会增加处理时间。如果已知使用的 Apple/Unix 格式，最好使用下面给出的一个或多个*双短横线*选项。

- `-no-desktop`  
    不要创建（空的）Desktop 文件。当 CD 在 Macintosh 上使用时，将创建新的 HFS Desktop 文件（并存储在 System Folder 中）。默认情况下，空 Desktop 文件会添加到 HFS 卷中。

- `-mac-name`  
    使用 HFS 文件名作为 ISO9660、Joliet 和 Rock Ridge 文件名的起点。更多信息请参见下文 **HFS MACINTOSH FILENAMES** 一节。

- `-boot-hfs-file` `driver_file`  
    安装 `driver_file`，它*可能*使 CD 在 Macintosh 上可启动。参见下文 **HFS BOOT DRIVER** 一节。（Alpha）。

- `-part`  
    生成 HFS 分区表。默认情况下，不生成分区表，但某些较旧的 Macintosh CD-ROM 驱动程序需要 CD-ROM 上有 HFS 分区表才能识别混合 CD-ROM。

- `-auto` `AutoStart_file`  
    使 HFS CD 使用 QuickTime 2.0 Autostart 功能启动应用程序或文档。给定文件名必须是位于 CD 顶层的文档或应用程序名称。文件名必须少于 12 个字符。（Alpha）。

- `-cluster-size` `size`  
    设置 PC Exchange 文件的簇或分配单元大小（以字节为单位）。隐含 `--exchange`。参见下文 **HFS MACINTOSH FILE FORMATS** 一节。

- `-hide-hfs` `glob`  
    从 HFS 卷中隐藏 `glob`（shell 通配符模式）。文件或目录仍将存在于 ISO9660 和/或 Joliet 目录中。`glob` 可以匹配文件名的任何部分。可以排除多个 glob。示例：

    ```sh
    genisoimage -o rom -hfs -hide-hfs '*.o' -hide-hfs foobar
    ```

    将从 HFS 卷中排除所有以 `.o` 结尾的文件或名为 `foobar` 的文件。请注意，如果你有一个名为 `foobar` 的目录，它（当然还有其所有后代）也将被排除。`glob` 也可以是相对于命令行上给出的源目录的路径名。示例：

    ```sh
    genisoimage -o rom -hfs -hide-hfs src/html src
    ```

    将仅从 `src` 目录中排除名为 `html` 的文件或目录。树中任何其他名为 `html` 的文件或目录都不会被排除。应与 `-hide` 和/或 `-hide-joliet` 一起使用。为了匹配目录名，请确保模式不包含尾部 `/` 字符。更多详细信息请参见 `README.hide`。

- `-hide-hfs-list` `file`  
    指定包含要隐藏的通配符模式列表的文件，如 `-hide-hfs` 中所述。

- `-hfs-volid` `hfs_volid`  
    HFS 分区的卷名。这是在 Macintosh 上分配给光盘的名称，并替换与 `-V` 一起使用的 `volid`。

- `-icon-position`  
    使用 Apple/Unix 文件中的图标位置信息（如果存在）。图标将出现在与 Macintosh 桌面上相同的位置。文件夹在屏幕上的位置和大小、其滚动位置、文件夹视图（以大图标、小图标等查看）也会保留。（Alpha）。

- `-root-info` `file`  
    设置 HFS 卷根文件夹的位置、屏幕大小、滚动位置、文件夹视图等。更多信息请参见 `README.rootinfo`。（Alpha）

- `-prep-boot` `file`  
    PReP 启动映像文件。最多允许 4 个。更多信息请参见 `README.prep_boot`。（Alpha）

- `-chrp-boot`  
    添加 CHRP 启动头。

- `-input-hfs-charset` `charset`  
    输入字符集，定义与 `-mac-name` 一起使用时 HFS 文件名中使用的字符。默认字符集为 `cp10000`（Mac Roman）。更多详细信息请参见下文 **CHARACTER SETS** 和 **HFS MACINTOSH FILENAMES** 两节。

- `-output-hfs-charset` `charset`  
    输出字符集，定义 HFS 文件名中将使用的字符。默认为输入字符集。更多详细信息请参见下文 **CHARACTER SETS** 一节。

- `-hfs-unlock`  
    默认情况下，`genisoimage` 将创建锁定的 HFS 卷。此选项使卷保持未锁定，以便其他应用程序（例如 `hfsutils`）可以修改该卷。关于使用此选项的警告，参见下文 **HFS PROBLEMS/LIMITATIONS** 一节。

- `-hfs-bless` `folder_name`  
    “Bless”给定目录（文件夹）。这通常是 *System Folder*，用于创建 HFS 可启动 CD。目录名称必须是 `genisoimage` 所看到的完整路径名。例如，如果给定 pathspec 是 `./cddata`，而所需文件夹名为 `System Folder`，则完整路径名为 `"/cddata/System Folder"`（如果名称包含空格，请记住使用引号）。

- `-hfs-parms` `parameters`  
    覆盖用于创建 HFS 文件系统的某些参数。正常情况不太可能使用。详细信息请参见 `libhfs_iso/hybrid.h` 源文件。

- `--cap`  
    查找 AUFS CAP Macintosh 文件。仅搜索 CAP Apple/Unix 文件格式。除非给出其他*双短横线*选项，否则禁用搜索其他可能的 Apple/Unix 文件格式。

- `--netatalk`  
    查找 NETATALK Macintosh 文件。

- `--double`  
    查找 AppleDouble Macintosh 文件。

- `--ethershare`  
    查找 Helios EtherShare Macintosh 文件。

- `--ushare`  
    查找 IPT UShare Macintosh 文件。

- `--exchange`  
    查找 PC Exchange Macintosh 文件。

- `--sgi`  
    查找 SGI Macintosh 文件。

- `--xinet`  
    查找 XINET Macintosh 文件。

- `--macbin`  
    查找 MacBinary Macintosh 文件。

- `--single`  
    查找 AppleSingle Macintosh 文件。

- `--dave`  
    查找 Thursby Software Systems DAVE Macintosh 文件。

- `--sfm`  
    查找 Microsoft's Services for Macintosh 文件（仅 NT）（Alpha）。

- `--osx-double`  
    查找 Mac OS X AppleDouble Macintosh 文件。

- `--osx-hfs`  
    查找 Mac OS X HFS Macintosh 文件。

## 字符集

`genisoimage` 以 POSIX 兼容的方式将文件名作为 8 位字符串处理。要表示所有语言的所有编码，8 位字符是不够的。Unicode 或 ISO-10646 定义的字符编码至少需要 21 位来表示所有已知语言。它们可以用 *UTF-32*、*UTF-16* 或 *UTF-8* 编码表示。UTF-32 使用普通 32 位编码，但似乎不常见。UTF-16 被 Microsoft 在 Win32 中使用，缺点是 16 位字符不符合 POSIX 文件系统接口。

现代 Unix 操作系统可能使用 UTF-8 编码文件名。每个 32 位字符由一个或多个 8 位字符表示。如果字符以 *ISO-8859-1*（用于中欧和北美）编码，则它与 UTF-32 或 UTF-16 编码的 Unicode 字符 1:1 映射。如果字符以 *7 位 ASCII*（用于美国和其他字符集有限的国家）编码，则它与 UTF-32、UTF-16 或 UTF-8 编码的 Unicode 字符 1:1 映射。在 UTF-8 中不能表示为单个字节的字符代码（如果值 > 0x7F）使用映射到多个 8 位字符的转义序列。

如果所有操作系统都使用 UTF-8，`genisoimage` 就不需要重新编码文件名中的字符。不幸的是，Apple 使用完全非标准的编码，而 Microsoft 使用的 Unicode 编码与 POSIX 文件名接口不兼容。

对于所有非 UTF-8 编码的操作系统，每个字节实际代表的字符取决于本地操作系统使用的*字符集*或*代码页*（Microsoft 使用的名称）——字符集中的字符将反映用户设置的区域或自然语言。

通常，字符代码 0x00-0x1f 是控制字符，代码 0x20-0x7f 是 7 位 ASCII 字符，（在 PC 和 Mac 上）0x80-0xff 用于其他字符。

由于使用的字符/符号远多于 256 个，因此字符集中只表示一小部分。因此，相同的字符代码在不同字符集中可能代表不同的字符。所以，例如在中欧生成的文件名，在东欧的机器上查看时可能不会显示相同的字符。

更复杂的是，不同的操作系统对区域或语言使用不同的字符集。例如，`é`（带尖音符的小写 e）的字符代码在 PC 上可能是字符代码 0x82，在 Macintosh 上是代码 0x8e，在西欧的 Unix 系统上是代码 0xe9，而在 Unicode 中是代码 0x000e9。

只要并非所有操作系统和应用程序都使用相同的字符集作为文件名基础，就可能需要指定文件名使用的字符集以及文件名在 CD 上应显示的字符集。

有四个选项可以指定要使用的字符集：

- `-input-charset`  
    定义你在主机上使用的本地字符集。任何发生的字符集转换都将使用此字符集作为起点。默认输入字符集在基于 MS-DOS 的系统上为 `cp437`，在所有其他系统上为 `iso8859-1`。如果给出 `-J`，输入字符集的 Unicode 等价物将用于 Joliet 目录。`-jcharset` 等同于 `-input-charset -J`。

- `-output-charset`  
    定义 CD 上 Rock Ridge 名称将使用的字符集。默认为输入字符集。

- `-input-hfs-charset`  
    定义用于从各种 Apple/Unix 文件格式解码的 HFS 文件名的 HFS 字符集。仅与 `-mac-name` 一起使用时有用。更多信息请参见 **HFS MACINTOSH FILENAMES**。默认为 `cp10000`（Mac Roman）。

- `-output-hfs-charset`  
    定义用于从正在使用的输入字符集创建 HFS 文件名的 HFS 字符集。在大多数情况下，这将来自使用 `-input-charset` 给出的字符集。默认为输入 HFS 字符集。

`genisoimage` 内置了许多字符集。要获取列表，请使用 `-input-charset help`。如果 `genisoimage` 使用 *iconv* 支持构建，此列表不包括从当前 locale 派生的字符集。

对于任何字符集选项，可以通过将文件名作为选项参数来从文件读取额外字符集。仅当给定名称与某个内置字符集不匹配时，才会读取给定文件。

字符集文件的格式与可从 [http://www.unicode.org/Public/MAPPINGS](http://www.unicode.org/Public/MAPPINGS) 获取的映射文件相同。此格式为：

- 第 1 列是输入字节码（十六进制，如 `0xXX`）  
    第 2 列是 Unicode（十六进制，如 `0xXXXX`）  
    行的其余部分被忽略。

任何空行、没有上述格式两（或更多）列的行或注释行（以 `#` 字符开头）都将被忽略，不会产生任何警告。任何缺失的输入代码都映射到 Unicode 字符 0x0000。

请注意，虽然支持 UTF-8，但不支持其他 Unicode 编码，如 UCS-2/UTF-16 和 UCS-4/UTF-32，因为 POSIX 操作系统无法原生处理它们。

可以通过将关键字 `default` 用作任何字符集选项的参数来定义 1:1 字符集映射。这是旧版本 `mkisofs` 的行为。

从输入文件名生成的 ISO9660 文件名不会从输入字符集转换。ISO9660 字符集是 ASCII 字符的非常有限子集，因此任何转换都没有意义。

`genisoimage` 无法转换的任何字符都将替换为 `_` 字符。

## HFS CREATOR/TYPE

Macintosh 文件有两个与其关联的属性，用于定义哪个应用程序创建了该文件，即 *CREATOR*，以及文件包含什么数据，即 *TYPE*。两者都是（正好）4 个字母的字符串。通常这允许 Macintosh 用户双击文件并启动正确的应用程序等。特定文件的 CREATOR 和 TYPE 可以通过在 Macintosh 上使用 ResEdit（或类似工具）之类的东西找到。

CREATOR 和 TYPE 信息存储在所有各种 Apple/Unix 编码文件中。对于其他文件，可以使用*映射*文件（通过 `-map`）基于文件名的扩展名和/或使用文件的*魔数*（通常是前几个字节中的*签名*）来设置 CREATOR 和 TYPE（通过 `-magic`）。如果同时给出这两个选项，它们在命令行上的顺序很重要。如果先给出 `-map`，则先尝试文件名扩展名匹配，再尝试魔数匹配。但是，如果先给出 `-magic`，则先尝试魔数匹配，再尝试文件名扩展名匹配。

如果未使用映射或 magic 文件，或者未找到匹配项，则可以通过 `.genisoimagerc` 文件中的条目或使用 `-hfs-creator` 和/或 `-hfs-type` 设置所有常规文件的默认 CREATOR 和 TYPE，否则默认 CREATOR 和 TYPE 为 `Unix` 和 `TEXT`。

*映射*文件的格式与 `aufs` 使用的 *afpfile* 格式相同。此文件有五列，分别为*扩展名*、*文件转换*、*CREATOR*、*TYPE* 和*注释*。以 `#` 字符开头的行是注释行，会被忽略。示例文件如下：

| EXTN | XLate | CREATOR | TYPE | 注释 |
| --- | --- | --- | --- | --- |
| `.tif` | `Raw` | `'8BIM'` | `'TIFF'` | "Photoshop TIFF 图像" |
| `.hqx` | `Ascii` | `'BnHq'` | `'TEXT'` | "BinHex 文件" |
| `.doc` | `Raw` | `'MSWD'` | `'WDBN'` | "Word 文件" |
| `.mov` | `Raw` | `'TVOD'` | `'MooV'` | "QuickTime 影片" |
| `*` | `Ascii` | `'ttxt'` | `'TEXT'` | "文本文件" |

其中：

- 第一列 `EXTN` 定义要映射的 Unix 文件名扩展名。对于不匹配的任何文件名扩展名，默认映射使用 `*` 字符定义。

- `Xlate` 列定义 Unix 和 Macintosh 文件之间的文本转换类型，`genisoimage` 会忽略它，但保留它是为了与 `aufs`(1) 兼容。尽管 `genisoimage` 不改变文件内容，但如果二进制文件的 TYPE 设置为 `TEXT`，它在 Macintosh 上*可能*会被错误读取。因此，默认 TYPE 的更好选择可能是 `????`。

- `CREATOR` 和 `TYPE` 关键字必须为 4 个字符长，并括在单引号中。

- 注释字段括在双引号中——`genisoimage` 会忽略它，但保留它是为了与 `aufs` 兼容。

*magic* 文件的格式几乎与 `file(1)` 命令使用的 `magic(5)` 文件相同。

此文件有四列，以制表符分隔，分别为*字节偏移*、*类型*、*测试*和*消息*。以 `#` 字符开头的行是注释行，会被忽略。示例文件如下：

| off | 类型 | 测试 | 消息 |
| --- | --- | --- | --- |
| `0` | `string` | `GIF8` | `8BIM GIFf GIF image` |
| `0` | `beshort` | `0xffd8` | `8BIM JPEG image data` |
| `0` | `string` | `SIT!` | `SIT! SIT! StuffIt Archive` |
| `0` | `string` | `\037\235` | `LZIV ZIVU standard Unix compress` |
| `0` | `string` | `\037\213` | `GNUz ZIVU gzip compressed data` |
| `0` | `string` | `%!` | `ASPS TEXT Postscript` |
| `0` | `string` | `\004%!` | `ASPS TEXT PC Postscript with a ^D to start` |
| `4` | `string` | `moov` | `txtt MooV QuickTime movie file (moov)` |
| `4` | `string` | `mdat` | `txtt MooV QuickTime movie file (mdat)` |

该文件的格式在 `magic(5)` 中描述。这里唯一的区别是，对于 magic 文件中的每个条目，初始偏移的*消息*必须是 4 个字符的 CREATOR，后跟 4 个字符的 TYPE——它们之间的空白是可选的。此行上的任何其他字符都将被忽略。续行（以 `>` 开头）也会被忽略，即仅使用初始偏移行。

使用 `-magic` 可能会显著增加处理时间，因为必须打开并读取每个文件以找到其魔数。

总之，对于所有文件，默认 CREATOR 为 `Unix`，默认 TYPE 为 `TEXT`。可以通过 `.genisoimagerc` 文件中的条目或使用 `-hfs-creator` 和/或 `-hfs-type` 更改这些值。

如果文件是已知 Apple/Unix 格式之一（并且已选择该格式），则 CREATOR 和 TYPE 取自存储在 Apple/Unix 文件中的值。

其他文件可以通过其文件名扩展名（使用 `-map`）或魔数（使用 `-magic`）设置 CREATOR 和 TYPE。如果在*映射*文件中使用了默认匹配，则这些值将覆盖默认 CREATOR 和 TYPE。

完整的 CREATOR/TYPE 数据库可在 [http://www.angelfire.com/il/szekely/](http://www.angelfire.com/il/szekely/) 找到。

## HFS MACINTOSH 文件格式

Macintosh 文件有两个部分，称为*数据分叉*和*资源分叉*。其中任一部分都可以为空。Unix（以及许多其他操作系统）只能处理具有一个部分（或分叉）的文件。更复杂的是，Macintosh 文件还有许多与其关联的属性——最重要的可能是 TYPE 和 CREATOR。同样，Unix 没有这些类型属性的概念。

例如，一个 Macintosh 文件可能是 JPEG 图像，其中图像存储在数据分叉中，桌面缩略图存储在资源分叉中。通常，跨平台有用的是数据分叉中的信息。

因此，要在 Unix 文件系统上存储 Macintosh 文件，必须找到一种方法来处理两个分叉和额外属性（称为 *Finder info*）。不幸的是，似乎每个在 Unix 上存储 Macintosh 文件的软件包都选择了完全不同的存储方法。

`genisoimage`（部分）支持的 Apple/Unix 格式有：

- CAP AUFS 格式  
    数据分叉存储在文件中。资源分叉位于子目录 `.resource` 中，文件名与数据分叉相同。Finder info 位于子目录 `.finderinfo` 中，文件名相同。

- AppleDouble/Netatalk  
    数据分叉存储在文件中。资源分叉存储在文件名前缀为 `%` 的文件中。Finder info 也存储在同一 `%` 文件中。Netatalk 使用相同格式，但资源分叉/Finder info 存储在子目录 `.AppleDouble` 中，文件名与数据分叉相同。

- AppleSingle  
    数据结构与上述类似，不同之处在于两个分叉和 Finder info 都存储在一个文件中。

- Helios EtherShare  
    数据分叉存储在文件中。资源分叉和 Finder info 一起位于子目录 `.rsrc` 中，文件名与数据分叉相同。

- IPT UShare  
    类似于 EtherShare 格式，但 Finder info 的存储方式略有不同。

- MacBinary  
    两个分叉和 Finder info 都存储在一个文件中。

- Apple PC Exchange  
    Macintosh 用于在 DOS（FAT）磁盘上存储 Apple 文件。数据分叉存储在文件中。资源分叉位于子目录 `resource.frk`（或 `RESOURCE.FRK`）中。Finder info 作为一条记录存储在文件 `finder.dat`（或 `FINDER.DAT`）中。每个数据分叉目录有单独的 `finder.dat`。

    注意：`genisoimage` 需要知道 PC Exchange 文件所在磁盘（或从其复制而来）的原生 FAT 簇大小。此大小由 `-cluster-size` 给出。簇或分配大小可以通过 DOS 实用程序 `chkdsk` 找到。

    可能不适用于 PC Exchange v2.2 或更高版本文件（随 MacOS 8.1 提供）。使用 Linux 时，包含 PC Exchange 文件的 DOS 介质应挂载为 `msdos` 类型（不是 `vfat`）。

- SGI/XINET  
    SGI 机器挂载 HFS 磁盘时使用。数据分叉存储在文件中。资源分叉位于子目录 `.HSResource` 中，文件名相同。Finder info 作为一条记录存储在文件 `.HSancillary` 中。每个数据分叉目录有单独的 `.HSancillary`。

- Thursby Software Systems DAVE  
    允许 Macintosh 在 SMB 服务器上存储 Apple 文件。数据分叉存储在文件中。资源分叉位于子目录 `resource.frk` 中。使用 AppleDouble 格式存储资源分叉。

- Services for Macintosh  
    NT 服务器在 NTFS 文件系统上存储文件的格式。数据分叉存储为 `filename`。资源分叉存储为名为 `filename:AFP_Resource` 的 NTFS 流。Finder info 存储为名为 `filename:Afp_AfpInfo` 的 NTFS 流。NTFS 流通常对用户不可见。

    警告：`genisoimage` 仅部分支持 SFM 格式。如果存储在 NT 服务器上的 HFS 文件或文件夹名称包含非法 NT 字符，NT 会将这些字符转换为 *Private Use Unicode* 字符。这些字符是：`" * / < > ? \ |` 以及作为文件名最后一个字符的空格或句点、字符代码 0x01 到 0x1f（控制字符）和 Apple 的苹果标志。

    不幸的是，这些私有 Unicode 字符无法被 `genisoimage` NT 可执行文件读取。因此，任何包含这些字符的文件或目录名都将被忽略——包括任何此类目录的内容。

- Mac OS X AppleDouble  
    当 HFS/HFS+ 文件由 Mac OS X 复制或保存到非 HFS 文件系统（例如 UFS、NFS 等）时，文件以 AppleDouble 格式存储。数据分叉存储在文件中。资源分叉存储在文件名前缀为 `._` 的文件中。Finder info 也存储在同一 `._` 文件中。

- Mac OS X HFS（Alpha）  
    实际上不是 Apple/Unix 编码，而是 Mac OS X 系统上的实际 HFS/HFS+ 文件。数据分叉存储在文件中。资源分叉存储在具有相同名称并带有后缀 `/rsrc` 的伪文件中。Finder info 只能通过 Mac OS X 库调用获得。

    另请参见 `README.macosx`。

    仅在 Mac OS X 上使用时有效。

    如果发现文件的资源分叉长度为零且 finderinfo 为空，则假定它没有任何 Apple/Unix 编码——因此可以使用其他方法设置 TYPE 和 CREATOR。

`genisoimage` 将尝试从 finder info 设置 CREATOR、TYPE、日期以及可能的其他标志。此外，如果存在，Macintosh 文件名将从 finder info 设置，否则 Macintosh 名称基于 Unix 文件名——参见下文 **HFS MACINTOSH FILENAMES** 一节。

使用 `-apple` 时，TYPE 和 CREATOR 存储在 ISO9660 目录记录中的可选 System Use 或 *SUSP* 字段中——方式与 Rock Ridge 属性大致相同。事实上，为了方便，Apple 扩展添加在现有 Rock Ridge 属性的开头（即，要获得 Apple 扩展，你也会获得 Rock Ridge 扩展）。

Apple 扩展要求资源分叉存储为 ISO9660 *关联*文件。这就像存储在 ISO9660 文件系统中的任何普通文件一样，不同之处在于目录记录中设置了关联文件标志（第 2 位）。此文件与数据分叉（非 Apple 机器看到的文件）具有相同的名称。关联文件通常被其他操作系统忽略。

使用 `-hfs` 时，TYPE 和 CREATOR 以及其他 finder info 存储在单独的 HFS 目录中，在 ISO9660 卷上不可见。HFS 目录引用上述相同的数据和资源分叉文件。

在大多数情况下，使用 `-hfs` 比使用 `-apple` 更好，因为后者对文件名施加了有限的 ISO9660 字符限制。但是，Apple 扩展确实具有优势：文件在磁盘上打包得更高效，并且可能在一张 CD 上容纳更多文件。

## HFS MACINTOSH 文件名

在可能的情况下，Apple/Unix 文件存储的 HFS 文件名将用于 CD 的 HFS 部分。但是，并非所有 Apple/Unix 编码都随 finderinfo 存储 HFS 文件名。在这些情况下，使用 Unix 文件名——并对特殊字符进行转义。特殊字符包括 `/` 和代码超过 127 的字符。

AUFS 通过使用 `:` 后跟两位十六进制字符代码来转义这些字符。Netatalk 和 EtherShare 有类似的方案，但使用 `%` 而不是 `:`。

如果 `genisoimage` 找不到 HFS 文件名，则使用 Unix 名称，并将任何 `%xx` 或 `:xx` 字符（`xx` 是两位十六进制数字）转换为单个字符代码。如果 `xx` 不是十六进制数字（`[0-9a-fA-F]`），则保持原样——尽管任何剩余的 `:` 都会转换为 `%`，因为 `:` 是 HFS 目录分隔符。必须小心，因为普通的 Unix 文件带有 `%xx` 或 `:xx` 也会被转换。例如：

- `This:2fFile`  
    转换为 `This/File`

- `This:File`  
    转换为 `This%File`

- `This:t7File`  
    转换为 `This%t7File`

尽管 HFS 文件名似乎支持大写和小写字母，但文件系统不区分大小写，即文件名 `aBc` 和 `AbC` 相同。如果在目录中发现具有相同 HFS 名称的文件，`genisoimage` 将尝试通过向其中一个文件名添加 `_` 字符来生成唯一名称。

如果文件存在 HFS 文件名，`genisoimage` 可以使用 `-mac-name` 将此名称用作 ISO9660、Joliet 和 Rock Ridge 文件名的起点。没有 HFS 名称的普通 Unix 文件仍将使用其 Unix 名称。例如：

如果一个 MacBinary（或 PC Exchange）文件在 Unix 文件系统上存储为 `someimage.gif.bin`，但包含名为 `someimage.gif` 的 HFS 文件，则该名称将出现在 CD 的 HFS 部分。但是，由于 `genisoimage` 使用 Unix 名称作为其他名称的起点，生成的 ISO9660 名称可能是 `SOMEIMAG.BIN`，Joliet/Rock Ridge 名称将是 `someimage.gif.bin`。此选项将使用 HFS 文件名作为起点，ISO9660 名称可能是 `SOMEIMAG.GIF`，Joliet/Rock Ridge 名称将是 `someimage.gif`。

`-mac-name` 目前不能与 `-T` 一起工作——`TRANS.TBL` 文件中将使用 Unix 名称，而不是 Macintosh 名称。

用于将任何 HFS 文件名转换为 Joliet/Rock Ridge 文件名的字符集默认为 `cp10000`（Mac Roman）。可以使用 `-input-hfs-charset` 指定使用的字符集。其他内置 HFS 字符集有：`cp10006`（MacGreek）、`cp10007`（MacCyrillic）、`cp10029`（MacLatin2）、`cp10079`（MacIcelandandic）和 `cp10081`（MacTurkish）。

注意：从各种 Apple/Unix 格式获取的 HFS 文件名使用的字符代码不会被转换，因为假定它们使用正确的 Apple 字符集。只有从 HFS 文件名派生的 Joliet/Rock Ridge 名称才会被转换。

现有的 `genisoimage` 代码将过滤掉 ISO9660 和 Joliet 文件名的任何非法字符，但由于 `genisoimage` 期望直接处理 Unix 名称，因此它保持 Rock Ridge 名称不变。但是，由于 `/` 是合法的 HFS 文件名字符，`-mac-name` 会将 Rock Ridge 文件名中的 `/` 转换为 `_`。

如果使用 Apple 扩展，则只有 ISO9660 文件名会出现在 Macintosh 上。但是，由于 Macintosh ISO9660 驱动程序可以使用 *Level 2* 文件名，你可以在 Macintosh 上使用 `-allow-multidot` 等选项而不出现问题——但仍要注意名称，例如 `this.file.name` 将转换为 `THIS.FILE`，即只有一个 `.`；文件名 `abcdefgh` 将被视为 `ABCDEFGH`，但 `abcdefghi` 将被视为 `ABCDEFGHI.`，即末尾带一个 `.`——不知道这是 Macintosh 问题还是 `genisoimage`/`mkhybrid` 问题。在 Macintosh 上查看时，所有文件名都将为大写。当然，DOS/Win3.X 机器将无法看到 Level 2 文件名……

## HFS 自定义卷/文件夹图标

要给 HFS CD 自定义图标，请确保根（顶层）文件夹包含标准 Macintosh 卷图标文件。要在 Macintosh 上为卷提供自定义图标，必须在卷的“Get Info”框中将图标粘贴到卷图标上。这会在根文件夹中创建一个名为 `Icon\r` 的不可见文件（`\r` 是回车字符）。

自定义文件夹图标非常相似——文件夹本身存在一个名为 `Icon\r` 的不可见文件。

创建 `genisoimage` 可使用的自定义图标的最简单方法可能是在 Mac 上格式化一张空白 HFS 软盘，并将图标粘贴到其“Get Info”框中。如果使用安装了 HFS 模块的 Linux，请挂载软盘：

```sh
mount -t hfs /dev/fd0 /mnt/floppy
```

默认情况下，软盘将作为 CAP 文件系统挂载。然后使用类似以下命令运行 `genisoimage`：

```sh
genisoimage --cap -o output source_dir /mnt/floppy
```

如果你不使用 Linux，可以使用 `hfsutils` 从软盘复制图标文件。但是必须小心，因为图标文件包含控制字符。例如：

```sh
hmount /dev/fd0
hdir -a
hcopy -m Icon^V^M icon_dir/icon
```

其中 `^V^M` 是 control-V 后跟 control-M。然后使用类似以下命令运行 `genisoimage`：

```sh
genisoimage --macbin -o output source_dir icon_dir
```

创建/使用自定义文件夹图标的过程非常相似——将图标粘贴到文件夹的“Get Info”框中，并将生成的 `Icon\r` 文件传输到 `genisoimage` 源树中的相关目录。

你可能希望从 ISO9660 和 Joliet 树中隐藏图标文件。

要为 Joliet CD 提供自定义图标，请遵循 [http://www.cdrfaq.org/faq03.html#S3-21-1](http://www.cdrfaq.org/faq03.html#S3-21-1) 中的说明。

## HFS 启动驱动程序

*可能*可以使混合 CD 在 Macintosh 上可启动。

可启动 HFS CD 需要 Apple CD-ROM（或兼容）驱动程序、可启动 HFS 分区以及必要的 System、Finder 等文件。

可以使用 `apple_driver` 实用程序从任何其他 Macintosh 可启动 CD-ROM 获取驱动程序。然后可以将此文件与 `-boot-hfs-file` 一起使用。

HFS 分区（即我们情况下的混合磁盘）必须包含合适的 System Folder，同样来自另一张 CD-ROM 或磁盘。

要使分区可启动，必须设置其*启动块*。启动块位于分区的前两个块中。对于不可启动分区，启动块全为零。通常，当在 Macintosh 磁盘上将 System 文件复制到分区时，启动块会填充许多必需设置——不幸的是，我不知道启动块的完整规范，因此我猜测以下内容可行。

因此，实用程序 `apple_driver` 还会从给定 CD-ROM 上找到的第一个 HFS 分区提取启动块，并将其用于 `genisoimage` 创建的 HFS 分区。

*请注意：* 通过使用 Apple CD 的驱动程序并将 Apple 软件复制到你的 CD，你有义务遵守 Apple Computer, Inc. 软件许可协议。

## EL TORITO 启动信息表

当给出 `-boot-info-table` 时，`genisoimage` 将通过在该文件的偏移 8 处插入一个 56 字节的*启动信息表*来修改由 `-b` 指定的启动文件。此修改在源文件系统中进行，因此如果此文件不易重新创建，请确保使用副本！此文件包含在启动时可能无法轻松或可靠获得的指针。

此表的格式如下；所有整数均采用 7.3.1 节（“小端”）格式。

```text
偏移  名称        大小     含义
8     bi_pvd      4 字节   主卷描述符的 LBA
12    bi_file     4 字节   启动文件的 LBA
16    bi_length   4 字节   启动文件长度（字节）
20    bi_csum     4 字节   32 位校验和
24    bi_reserved 40 字节  保留
```

32 位校验和是从字节偏移 64 开始的启动文件中所有 32 位字的总和。所有线性块地址（LBA）均以 CD 扇区（通常为 2048 字节）给出。

## HPPA 注意事项

要制作 HPPA 可启动 CD，至少必须指定引导加载程序文件（`-hppa-bootloader`）、内核映像文件（32 位、64 位或两者，取决于硬件）以及启动命令行（`-hppa-cmdline`）。某些系统可以启动 32 位或 64 位内核，如果两者都存在，固件将选择一个。可选地，可以使用 `-hppa-cmdline` 使用 ramdisk 作为根文件系统。

## JIGDO 注意事项

Jigdo 是一种帮助分发大型文件（如 CD 和 DVD 映像）的工具；更多详细信息请参见 [http://atterer.org/jigdo/](http://atterer.org/jigdo/)。Debian CD 和 DVD ISO 映像以 jigdo 格式发布在 Web 上，以便最终用户更高效地下载它们。

要使用 `genisoimage` 在 ISO 映像旁边创建 jigdo 和模板文件，你必须首先按以下格式生成将要使用的文件列表：

```text
MD5sum   文件大小  路径
32 字符  12 字符   到行尾
```

MD5sum 必须以标准十六进制表示法书写，文件大小必须列出文件大小（字节），路径必须列出文件的绝对路径。例如：

```text
00006dcd58ff0756c36d2efae21be376         14736  /mirror/debian/file1
000635c69b254a1be8badcec3a8d05c1        211822  /mirror/debian/file2
00083436a3899a09633fc1026ef1e66e         22762  /mirror/debian/file3
```

拥有此文件后，使用所有常规命令行参数调用 `genisoimage`。使用 `-jigdo-jigdo` 和 `-jigdo-template` 指定 jigdo 和模板文件的输出文件名，并使用 `-md5-list` 传入 MD5 列表的位置。

如果有你不希望添加到 jigdo 文件中的文件（例如，如果它们可能经常更改），请使用 `-jigdo-exclude` 指定它们。如果你想在文件写入映像时验证某些文件，请使用 `-jigdo-force-md5` 指定它们。如果有任何文件不匹配，`genisoimage` 将中止。这两个选项都以正则表达式作为输入。可以进一步根据大小限制将要使用的文件集——使用 `-jigdo-min-file-size` 选项。

最后，jigdo 代码需要知道如何将它收到的文件映射到镜像式配置上。使用 `-jigdo-map` 指定如何映射路径。使用 `Debian=/mirror/debian` 将导致所有以 `/mirror/debian` 开头的路径在输出 jigdo 文件中映射为 `Debian:<file>`。

## 示例

要在文件 `cd.iso` 中创建普通 ISO9660 文件系统映像，其中目录 `cd_dir` 将成为 CD 的根目录，请调用：

```console
% genisoimage -o cd.iso cd_dir
```

要创建源目录 `cd_dir` 带 Rock Ridge 扩展的 CD：

```console
% genisoimage -o cd.iso -R cd_dir
```

要创建源目录 `cd_dir` 带 Rock Ridge 扩展的 CD，其中所有文件至少具有读权限并且所有文件归 `root` 所有，请调用：

```console
% genisoimage -o cd.iso -r cd_dir
```

要将 tar 归档直接写入稍后将包含带 tar 归档的简单 ISO9660 文件系统的 CD，请调用：

```console
% tar cf - . | genisoimage -stream-media-size 333000 | \
  wodim dev=b,t,l -dao tsize=333000s -
```

要创建源目录 `cd_dir` 带 Joliet 和 Rock Ridge 扩展的 HFS 混合 CD：

```console
% genisoimage -o cd.iso -R -J -hfs cd_dir
```

要从包含 Netatalk Apple/Unix 文件的源目录 `cd_dir` 创建 HFS 混合 CD：

```console
% genisoimage -o cd.iso --netatalk cd_dir
```

要从源目录 `cd_dir` 创建 HFS 混合 CD，并根据文件 "mapping" 中列出的文件名扩展名为所有文件提供 CREATOR 和 TYPE：

```console
% genisoimage -o cd.iso -map mapping cd_dir
```

要从源目录 `cd_dir` 和 `another_dir` 创建带 Apple Extensions to ISO9660 的 CD。所有已知 Apple/Unix 格式的文件都会被解码，任何其他文件将根据文件 `magic` 中给出的魔数提供 CREATOR 和 TYPE：

```console
% genisoimage -o cd.iso -apple -magic magic -probe \
  cd_dir another_dir
```

以下示例将不同文件放到 CD 上，这些文件都具有名称 README，但作为 ISO9660/Rock Ridge、Joliet 或 HFS CD 查看时内容不同。

当前目录包含：

```console
% ls -F
README.hfs README.joliet README.Unix cd_dir/
```

以下命令将目录 `cd_dir` 的内容以及三个 README 文件放到 CD 上——但从三个文件系统中的每一个只能看到一个：

```console
% genisoimage -o cd.iso -hfs -J -r -graft-points \
  -hide README.hfs -hide README.joliet \
  -hide-joliet README.hfs -hide-joliet README.Unix \
  -hide-hfs README.joliet -hide-hfs README.Unix \
  README=README.hfs README=README.joliet \
  README=README.Unix cd_dir
```

即，文件 README.hfs 将在 HFS CD 上显示为 README，另外两个 README 文件将被隐藏。Joliet 和 ISO9660/Rock Ridge CD 类似。

隐藏选项的组合可能会产生各种奇怪的结果……

## 注意事项

`genisoimage` 可以安全地以 suid root 安装。在创建多会话映像时，可能需要这样做以允许 `genisoimage` 读取前一会话。

如果 `genisoimage` 正在创建带 Rock Ridge 属性的文件系统映像，并且源目录树的目录嵌套级别对 ISO9660 来说太深，`genisoimage` 将执行深层目录重定位。这会导致 CD 根目录中出现名为 `RR_MOVED` 的目录。你无法避免此目录。

不同平台的许多启动代码选项互斥，因为启动块不能共存，即不同平台在映像中共享相同的数据位置。详情请参见 [http://lists.debian.org/debian-cd/2006/12/msg00109.html](http://lists.debian.org/debian-cd/2006/12/msg00109.html)。

## 缺陷

任何硬链接到未复制到 ISO9660 文件系统的树中的文件，其文件引用计数将不正确。

不检查根目录 `.` 条目中的 SUSP 记录以验证 Rock Ridge 增强的存在。在多会话模式下添加数据时读取旧会话时存在此问题。

在多会话模式下添加数据时，不能正确读取重定位目录。如果新会话不包含深层目录，则任何重定位的深层目录都会丢失。

从 `TRANS.TBL` 进行多会话时不会重用 `RR_MOVED`。

在多会话模式下不会为 `RR_MOVED` 创建 `whole_name` 条目。

可能还有其他缺陷。请向维护者报告。

## HFS 问题/限制

我不得不对我期望修改后的 libhfs 例程如何工作做出若干假设，但是可能存在我未曾想到或遇到这些假设失败的情况。因此我不能保证 `genisoimage` 会按预期工作（尽管我还没有遇到重大问题）。大多数 HFS 功能工作正常，但有些未完全测试。这些在上文标记为 *Alpha*。

尽管 HFS 文件名似乎支持大写和小写字母，但文件系统不区分大小写，即文件名 `aBc` 和 `AbC` 相同。如果在目录中发现具有相同 HFS 名称的文件，`genisoimage` 将尝试通过向其中一个文件名添加 `_` 字符来生成唯一名称。

共享前 31 个字符的 HFS 文件/目录名将用 `_N`（十进制数）替换最后几个字符以生成唯一名称。

“移植”Apple/Unix 文件或目录时必须小心（方法 and 语法见上文）。不能为 Apple/Unix 编码的文件/目录使用新名称。例如，如果要将名为 `oldname` 的 Apple/Unix 编码文件添加到 CD，你不能使用命令行：

```sh
genisoimage -o output.raw -hfs -graft-points newname=oldname cd_dir
```

`genisoimage` 将无法解码 `oldname`。但是，只要不尝试像上面那样给它们新名称，就可以移植 Apple/Unix 编码的文件或目录。

使用多会话选项 `-M` 和 `-C` 创建 HFS 卷时，只有最后会话中的文件会位于 HFS 卷中。即 `genisoimage` 无法将以前会话中的现有文件*添加*到 HFS 卷。

但是，如果每个会话都使用 `-part` 创建，则在 Mac 上挂载时每个会话将显示为单独的卷。在这种情况下，值得使用 `-V` 或 `-hfs-volid` 为每个会话提供唯一的卷名，否则每个“卷”将在桌面上以相同名称出现。

符号链接（与所有其他非普通文件一样）不会添加到 HFS 目录。

混合卷可能比包含相同数据的纯 ISO9660 卷更大。在某些情况下（例如 DVD 大小的卷），差异可能很大。随着 HFS 卷变大，分配块大小（文件可占用的最小空间量）也会变大。对于 650MB CD，分配块为 10kB；对于 4.7GB DVD，大约为 70kB。

HFS 卷中的最大文件数约为 65500——尽管实际限制会略低于此。

生成的混合卷可以在 Unix 机器上使用 hfsutils 例程访问。但是，无法对卷进行更改，因为它被设置为**锁定**。选项 `-hfs-unlock` 将创建未锁定的输出映像——但是不应更改卷的内容（除非你确实知道自己在做什么），因为它不是“真正的”HFS 卷。

`-mac-name` 目前不能与 `-T` 一起工作——`TRANS.TBL` 文件中将使用 Unix 名称，而不是 Macintosh 名称。

尽管 `genisoimage` 不改变文件内容，但如果二进制文件的 TYPE 设置为 `TEXT`，它在 Macintosh 上*可能*会被错误读取。因此，默认 TYPE 的更好选择可能是 `????`。

`-mac-boot-file` 可能完全不能工作……

可能不适用于 PC Exchange v2.2 或更高版本文件（随 MacOS 8.1 提供）。使用 Linux 时，包含 PC Exchange 文件的 DOS 介质应挂载为 `msdos` 类型（不是 `vfat`）。

SFM 格式仅部分支持——参见上文 **HFS MACINTOSH FILE FORMATS** 一节。

不能将 `-sparc-boot` 或 `-generic-boot` 与 `-boot-hfs-file` 或 `-prep-boot` 一起使用。

`genisoimage` 应该能够创建超过 4Gb 的 HFS 混合映像，尽管尚未完全测试。

## 另请参见

“genisoimagerc(5)”、“wodim(1)”、`mkzftree`(8)、“magic(5)”。

## 作者

`genisoimage` 源自 2006 年 5 月 cdrtools 2.01.01a08 包中的 `mkisofs`（以及从 2007 年 3 月 cdrtools 2.01.01a24 中提取的少量更新），来自 [http://cdrecord.berlios.de/](http://cdrecord.berlios.de/)，但现在是 **cdrkit** 套件的一部分，由 Joerg Jaspert、Eduard Bloch、Steve McIntyre、Peter Samuelson、Christian Fromme、Ben Hutchings 和其他贡献者维护。维护者可通过 `debburn-devel@lists.alioth.debian.org` 联系，或参见 **cdrkit** 项目网站 [http://www.cdrkit.org/](http://www.cdrkit.org/)。

Eric Youngdale 编写了 `mkisofs` 的第一批版本（1993–1998）。Jörg Schilling 编写了 SCSI 传输库及其接口，并自 1999 年以来维护 `mkisofs`。James Pearson 使用 Robert Leslie 的 `libhfs` 编写了 HFS 混合代码。Pearson、Schilling、Jungshik Shin 和 Jaakko Heinonen 为字符集转换代码做出了贡献。**cdrkit** 维护者自 2006 年以来维护 `genisoimage`。

```text
Copyright 1993-1998 by Yggdrasil Computing, Inc.
Copyright 1996-1997 by Robert Leslie
Copyright 1997-2001 by James Pearson
Copyright 1999-2006 by Jörg Schilling
Copyright 2007 by Jörg Schilling (originating few updates)
Copyright 2002-2003 by Jungshik Shin
Copyright 2003 by Jaakko Heinonen
Copyright 2006 by the Cdrkit maintainers
```

如果你想参与 `genisoimage` 的开发，可以按照 [http://alioth.debian.org/mail/?group_id=31006](http://alioth.debian.org/mail/?group_id=31006) 上的说明加入 **cdrkit** 开发者邮件列表。该列表的电子邮件地址是 `debburn-devel@lists.alioth.debian.org`。这也是用户支持问题的地址。请注意，**cdrkit** 和 **cdrtools** 没有关联。

## 致谢

UNIX 是 The Open Group 在美国和其他国家的注册商标。