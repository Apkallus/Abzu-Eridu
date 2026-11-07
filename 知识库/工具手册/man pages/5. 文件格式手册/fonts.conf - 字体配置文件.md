https://www.freedesktop.org/software/fontconfig/fontconfig-user.html

# fonts-conf

## 名称

`fonts.conf` —— 字体配置文件

## 概要

```
/etc/fonts/fonts.conf
/etc/fonts/fonts.dtd
/etc/fonts/conf.d
$XDG_CONFIG_HOME/fontconfig/conf.d
$XDG_CONFIG_HOME/fontconfig/fonts.conf
~/.fonts.conf.d
~/.fonts.conf
```

## 描述

Fontconfig 是一个库，旨在提供系统级字体配置、自定义以及应用程序访问字体的能力。

## 功能概述

Fontconfig 包含两个核心模块：配置模块根据 XML 文件构建内部配置；匹配模块接受字体模式并返回最接近的匹配字体。

### 字体配置

配置模块由 `FcConfig` 数据类型、`libexpat` 和 `FcConfigParse` 组成。`FcConfigParse` 会遍历 XML 树，并用其中发现的数据修改配置。从外部视角看，配置该库包括生成有效的 XML 树并将其传给 `FcConfigParse`。应用程序可用来更改运行中配置的唯一其他机制，是向应用程序提供的字体文件列表中添加字体和目录。

其目标是让字体配置相对静态，并尽可能被多个应用程序共享。希望这样能在从一个应用程序向另一个应用程序传递名称时，带来更稳定的字体选择。选择 XML 作为配置文件格式，是因为它便于外部代理编辑，同时能保留正确的结构和语法。

字体配置与字体匹配是分离的；需要自行进行匹配的应用程序可以从库中访问可用字体并执行私有匹配。其意图是允许应用程序从库中挑选合适的功能，而不是强迫它们在库与私有配置机制之间二选一。希望这样可以确保所有应用程序的字体配置都能集中在一处。集中字体配置将简化和规范化字体安装与自定义。

### 字体属性

虽然字体模式可以包含几乎任意属性，但有一些具有关联类型的已知属性。Fontconfig 使用其中一些属性进行字体匹配和字体补全。其他属性则作为便利信息提供给应用程序的渲染机制。

| 属性 | 类型 | 描述 |
|---|---|---|
| `family` | `String` | 字体族名称 |
| `familylang` | `String` | 每个字体族对应的语言 |
| `style` | `String` | 字体样式。覆盖 weight 和 slant |
| `stylelang` | `String` | 每个样式对应的语言 |
| `fullname` | `String` | 字体全名（通常包含样式） |
| `fullnamelang` | `String` | 每个全名对应的语言 |
| `slant` | `Int` | 斜体、倾斜或罗马体 |
| `weight` | `Int` | 细体、中等、半粗、粗体或黑体 |
| `width` | `Int` | 压缩、正常或扩展 |
| `size` | `Double` | 点大小 |
| `aspect` | `Double` | 在 hinting 前水平拉伸字形 |
| `pixelsize` | `Double` | 像素大小 |
| `spacing` | `Int` | 比例、双宽、等宽或字符单元格 |
| `foundry` | `String` | 字体铸造厂名称 |
| `antialias` | `Bool` | 字形是否可以抗锯齿 |
| `hintstyle` | `Int` | 自动 hinting 样式 |
| `hinting` | `Bool` | 光栅化器是否应使用 hinting |
| `verticallayout` | `Bool` | 使用垂直布局 |
| `autohint` | `Bool` | 使用自动 hinter 而不是普通 hinter |
| `globaladvance` | `Bool` | 使用字体全局 advance 数据（已弃用） |
| `file` | `String` | 保存字体的文件名 |
| `index` | `Int` | 字体在文件中的索引 |
| `ftface` | `FT_Face` | 使用指定的 FreeType face 对象 |
| `rasterizer` | `String` | 正在使用的光栅化器（已弃用） |
| `outline` | `Bool` | 字形是否为轮廓 |
| `scalable` | `Bool` | 字形是否为轮廓或具有颜色 |
| `dpi` | `Double` | 目标每英寸点数 |
| `rgba` | `Int` | `unknown`、`rgb`、`bgr`、`vrgb`、`vbgr`、`none` —— 子像素几何 |
| `scale` | `Double` | point->pixel 转换的缩放因子（已弃用） |
| `minspace` | `Bool` | 消除行间距中的前导 |
| `charset` | `CharSet` | 字体编码的 Unicode 字符 |
| `lang` | `String` | 此字体支持的 RFC-3066 风格语言列表 |
| `fontversion` | `Int` | 字体版本号 |
| `capability` | `String` | 字体中的布局能力列表 |
| `fontformat` | `String` | 字体格式的字符串名称 |
| `embolden` | `Bool` | 光栅化器应合成加粗字体 |
| `embeddedbitmap` | `Bool` | 使用嵌入位图而不是轮廓 |
| `decorative` | `Bool` | 样式是否为装饰性变体 |
| `lcdfilter` | `Int` | LCD 滤镜类型 |
| `namelang` | `String` | 用于 `familylang`、`stylelang` 和 `fullnamelang` 默认值的语言名称 |
| `fontfeatures` | `String` | 要启用的 OpenType 特性标签列表 |
| `prgname` | `String` | 正在运行程序的名称 |
| `postscriptname` | `String` | PostScript 中的字体族名称 |
| `color` | `Bool` | 是否有任何字形具有颜色 |
| `symbol` | `Bool` | 字体是否使用 MS symbol-font 编码 |
| `fontvariations` | `String` | 可变字体中轴的逗号分隔字符串 |
| `variable` | `Bool` | 字体是否为可变字体 |
| `fonthashint` | `Bool` | 字体是否具有 hinting |
| `order` | `Int` | 字体的顺序号 |
| `desktop` | `String` | 当前桌面名称 |
| `namedinstance` | `Bool` | 字体是否为命名实例 |
| `fontwarapper` | `String` | 字体包装格式，当前值为 `WOFF`、`WOFF2`、`SFNT`（用于任何其他 SFNT 字体）以及 `CFF`（用于独立 CFF 字体）。 |

### 字体匹配

Fontconfig 通过测量给定模式到系统中所有可用字体的距离来执行匹配，并选择最接近的匹配字体。这确保始终会返回一个字体，但不确保它一定与请求的模式相似。

字体匹配从应用程序构造的模式开始。结果字体的期望属性会收集到一个模式中。模式的每个属性可以包含一个或多个值；这些值按优先级顺序列出；列表中靠前的匹配被认为比靠后的匹配“更接近”。

初始模式会通过应用配置中针对模式找到的编辑指令列表进行修改；每条指令由一个匹配谓词和一组编辑操作组成。它们按照在配置中出现的顺序执行。每个匹配都会导致应用关联的编辑操作序列。

在模式被编辑之后，会执行一系列默认替换以规范化可用属性集；这避免了较低层在渲染期间不断为各种字体属性提供默认值。

规范化后的字体模式最终会与所有可用字体进行匹配。对于若干属性，会测量模式到字体的距离：`foundry`、`charset`、`family`、`lang`、`spacing`、`pixelsize`、`style`、`slant`、`weight`、`antialias`、`rasterizer` 和 `outline`。此列表按优先级排序——比较此列表中较早元素的结果比比较较晚元素的结果权重更高。

此规则有一个特殊情况；字体族名称被拆分为两种绑定：强绑定和弱绑定。强字体族名称在匹配中比 `lang` 元素具有更高优先级，而弱字体族名称比 `lang` 元素具有更低优先级。这允许在文档指定的任何字体不可用时，由文档语言驱动字体选择。

表示该字体的模式会被扩充，以包含模式中存在但字体本身中不存在的任何属性；这允许应用程序通过匹配系统传递渲染指令或任何其他数据。最后，会应用配置中针对字体找到的编辑指令列表。修改后的模式会返回给应用程序。

返回值包含足够的信息来定位和光栅化字体，包括文件名、像素大小和其他渲染数据。由于涉及的信息均不属于 FreeType 库，应用程序可以自由使用任何光栅化引擎，甚至直接访问所标识的字体文件。

配置中的匹配/编辑序列分两遍执行，因为本质上需要两种不同的操作——第一种是修改字体选择方式；为字体族设置别名并添加合适的默认值。第二种是修改所选字体的光栅化方式。这些操作必须应用于所选字体，而不是原始模式，因为经常会发生错误匹配。

### 字体名称

Fontconfig 为模式提供了一种文本表示，库既可以接受也可以生成。该表示分为三部分：首先是字体族名称列表，其次是点大小列表，最后是附加属性列表：

```
<families>-<point sizes>:<name1>=<values1>:<name2>=<values2>...
```

列表中的值用逗号分隔。名称无需同时包含字体族或点大小；它们可以被省略。此外，还有一些符号常量可同时表示名称和值。以下是一些示例：

名称, 含义

- `Times-12`  
    12 点 Times Roman
- `Times-12:bold`  
    12 点 Times Bold
- `Courier:italic`  
    默认大小的 Courier Italic
- `Monospace:matrix=1 .1 0 1`  
    用户偏好的等宽字体，并带有人工倾斜

字体族名称中的 `\`、`-`、`:` 和 `,` 字符必须前置 `\` 字符，以避免被误解。类似地，包含 `\`、`=`、`_`、`:` 和 `,` 的值也必须前置 `\` 字符。读取字体名称时，`\` 字符会从字体族名称和值中剥离。

## 调试应用程序

为了帮助诊断字体和应用程序问题，fontconfig 在构建时保留了大量内部调试功能。它由 `FC_DEBUG` 环境变量控制。该变量的值被解释为一个数字，该值中的每一位控制不同的调试消息。

| 名称 | 值 | 含义 |
|---|---|---|
| `MATCH` | 1 | 字体匹配的简要信息 |
| `MATCHV` | 2 | 详细的字体匹配信息 |
| `EDIT` | 4 | 监视 match/test/edit 执行 |
| `FONTSET` | 8 | 跟踪启动时字体信息的加载 |
| `CACHE` | 16 | 监视缓存文件的写入 |
| `CACHEV` | 32 | 详细的缓存文件写入信息 |
| `PARSE` | 64 | （已不再使用） |
| `SCAN` | 128 | 监视为构建缓存而扫描的字体文件 |
| `SCANV` | 256 | 详细的字体文件扫描信息 |
| `MEMORY` | 512 | 监视 fontconfig 内存使用 |
| `CONFIG` | 1024 | 监视加载了哪些配置文件 |
| `LANGSET` | 2048 | 转储用于构造 lang 值的字符集 |
| `MATCH2` | 4096 | 显示模式中的字体匹配变换 |

将所需调试级别的值相加，并在运行应用程序前将该值（以十进制）赋给 `FC_DEBUG` 环境变量。这些语句的输出会发送到 stdout。

## 语言标签

数据库中的每个字体都包含其支持的语言列表。这是通过比较字体的 Unicode 覆盖范围与每种语言的正字法计算得出的。语言使用 RFC-3066 兼容的命名方式标记，分为两部分——ISO 639 语言标签，后跟连字符和 ISO 3166 国家代码。连字符和国家代码可以省略。

Fontconfig 在库中内置了若干语言的正字法。除了重新构建库之外，没有提供添加新语言的规定。它目前支持 ISO 639-1 中命名的 139 种语言中的 122 种、ISO 639-2 中具有两字母代码的 141 种语言，以及另外 30 种仅有三字母代码的语言。同时具有两字母和三字母代码的语言仅提供两字母代码。

对于在多个地区使用且字符集差异很大的语言，fontconfig 包含按地区划分的正字法。这包括阿塞拜疆语、库尔德语、普什图语、提格里尼亚语和中文。

## 配置文件格式

fontconfig 的配置文件以 XML 格式存储；这种格式使外部配置工具更容易编写，并确保它们生成语法正确的配置文件。由于 XML 文件是纯文本，专家用户也可以使用文本编辑器进行操作。

fontconfig 的文档类型定义位于外部实体 `fonts.dtd` 中；它通常存储在默认字体配置目录（`/etc/fonts`）中。每个配置文件应包含以下结构：

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
...
</fontconfig>
```

### `<fontconfig>`

```xml
<fontconfig>
```

这是字体配置的顶层元素，可以按任意顺序包含 `<dir>`、`<cachedir>`、`<include>`、`<match>` 和 `<alias>` 元素。

### `<dir prefix="default" salt="">`

```xml
<dir prefix="default" salt="">
```

此元素包含一个目录名，该目录将被扫描以查找字体文件，并加入可用字体集合。

如果 `prefix` 设置为 `"default"` 或 `"cwd"`，当前工作目录将作为路径前缀添加到该值之前。如果 `prefix` 设置为 `"xdg"`，`XDG_DATA_HOME` 环境变量中的值将作为路径前缀添加。更多细节请参见 XDG Base Directory Specification。如果 `prefix` 设置为 `"relative"`，当前文件的路径将添加到该值之前。

`salt` 属性会影响缓存文件名的确定。例如，当容器中同一路径下具有不同字体集，并且从主机的不同字体路径共享字体时，这很有用。

### `<cachedir prefix="default">`

```xml
<cachedir prefix="default">
```

此元素包含一个目录名，用于存储或读取字体信息缓存。如果配置文件中指定了多个元素，则列表中第一个可访问的目录将用于存储缓存文件。如果它以 `~` 开头，则指用户主目录中的目录。如果 `prefix` 设置为 `"xdg"`，`XDG_CACHE_HOME` 环境变量中的值将作为路径前缀添加。更多细节请参见 XDG Base Directory Specification。默认目录是 `$XDG_CACHE_HOME/fontconfig`，其中包含名为 `<hash value>-<architecture>.cache-<version>` 的缓存文件，其中 `<version>` 是 fontconfig 缓存文件版本号（当前为 8）。

### `<include ignore_missing="no" prefix="default">`

```xml
<include ignore_missing="no" prefix="default">
```

此元素包含附加配置文件或目录的名称。如果是目录，则该目录中以 ASCII 数字（U+0030 - U+0039）开头并以字符串 `.conf` 结尾的每个文件都将按排序顺序处理。当 `FcConfigParse` 遍历 XML 数据类型时，文件内容也会通过将文件名传递给 `FcConfigLoadAndParse` 而并入配置。如果 `ignore_missing` 设置为 `"yes"` 而不是默认的 `"no"`，则缺失的文件或目录不会触发库的警告消息。如果 `prefix` 设置为 `"xdg"`，`XDG_CONFIG_HOME` 环境变量中的值将作为路径前缀添加。更多细节请参见 XDG Base Directory Specification。

### `<config>`

```xml
<config>
```

此元素提供了一个整合附加配置信息的位置。`<config>` 可以按任意顺序包含 `<blank>` 和 `<rescan>` 元素。

### `<description domain="fontconfig-conf">`

```xml
<description domain="fontconfig-conf">
```

此元素用于保存描述某个配置用途的字符串。该字符串可以通过 gettext 翻译。`domain` 需要设置为适当的名称以应用翻译。fontconfig 会尝试使用 gettext 中的 `domain` 获取翻译。

### `<blank>`

```xml
<blank>
```

字体通常包含“损坏”的字形，它们出现在编码中，但在屏幕上绘制为空白。在 `<blank>` 元素中，将每个应显示为空的 Unicode 字符放入一个 `<int>` 元素。此集合之外但绘制为空的字符将从字体支持的字符集中省略。

### `<remap-dir prefix="default" as-path="" salt="">`

```xml
<remap-dir prefix="default" as-path="" salt="">
```

此元素包含一个目录名，该目录将在缓存信息中映射为路径 `as-path`。如果目录名是通过 bind mount 或符号链接指向系统中另一个目录的别名，并且该另一个目录很可能已存在缓存字体信息，则这很有用。

`salt` 属性与 `<dir>` 元素一样会影响缓存文件名的确定。

### `<reset-dirs />`

```xml
<reset-dirs />
```

此元素移除由 `<dir>` 元素添加的所有字体目录。这对于从系统字体目录覆盖为仅使用自己的字体目录很有用。

### `<rescan>`

```xml
<rescan>
```

`<rescan>` 元素包含一个 `<int>` 元素，指示自动检查字体配置更改之间的默认间隔。当此间隔过去时，Fontconfig 将验证所有配置文件和目录，并自动重建内部数据结构。

### `<selectfont>`

```xml
<selectfont>
```

此元素用于拒绝/允许字体被列出或匹配。它包含 `acceptfont` 和 `rejectfont` 元素。此列表仅在加载缓存时应用一次。因此，如果你想按某些模式过滤，模式只会与缓存中的内容进行评估。换句话说，除 `"scan"` 之外的目标模式不会产生任何效果。

### `<acceptfont>`

```xml
<acceptfont>
```

被 `acceptfont` 元素匹配的字体会被“允许列名”；此类字体会被显式包含在用于解析列表和匹配请求的字体集中；将它们包含在此列表中可保护它们不被 `rejectfont` 元素“拒绝列名”。`Acceptfont` 元素包含用于匹配字体的 `glob` 和 `pattern` 元素。

### `<rejectfont>`

```xml
<rejectfont>
```

被 `rejectfont` 元素匹配的字体会被“拒绝列名”；此类字体会从用于解析列表和匹配请求的字体集中排除，就像它们不存在于系统中一样。`Rejectfont` 元素包含用于匹配字体的 `glob` 和 `pattern` 元素。

### `<glob>`

```xml
<glob>
```

`Glob` 元素包含 shell 风格的文件名匹配模式（包括 `?` 和 `*`），这些模式根据字体的完整路径名匹配字体。如果它以 `~` 开头，则指用户主目录中的目录。这可用于排除一组目录（`/usr/share/fonts/uglyfont*`）或特定字体文件类型（`*.pcf.gz`），但后一种机制相当依赖文件名约定，而文件名约定并不可靠。请注意，glob 仅适用于目录，不适用于单个字体。

### `<pattern>`

```xml
<pattern>
```

`Pattern` 元素对传入字体执行列表式匹配；也就是说，它们包含一组元素及关联值。如果所有这些元素都具有匹配值，则模式匹配该字体。这可用于根据字体属性（可缩放、粗体等）选择字体，这比使用文件扩展名更可靠。`Pattern` 元素包含 `patelt` 元素。

### `<patelt name="property">`

```xml
<patelt name="property">
```

`Patelt` 元素包含单个模式元素和值列表。它们必须具有 `name` 属性，用于指示模式元素名称。`Patelt` 元素包含 `int`、`double`、`string`、`matrix`、`bool`、`charset` 和 `const` 元素。

### `<match target="pattern">`

```xml
<match target="pattern">
```

此元素首先包含一个（可能为空的）`<test>` 元素列表，然后包含一个（可能为空的）`<edit>` 元素列表。匹配所有测试的模式将接受所有编辑。如果 `target` 设置为 `"font"` 而不是默认的 `"pattern"`，则此元素应用于匹配结果产生的字体名，而不是要匹配的字体模式。如果 `target` 设置为 `"scan"`，则此元素在扫描字体以构建 fontconfig 数据库时应用。

### `<test qual="any" name="property" target="default" compare="eq">`

```xml
<test qual="any" name="property" target="default" compare="eq">
```

此元素包含单个值，该值与目标（`'pattern'`、`'font'`、`'scan'` 或 `'default'`）的属性 `"property"` 进行比较（可替换为上面看到的任何属性名）。`compare` 可以是 `"eq"`、`"not_eq"`、`"less"`、`"less_eq"`、`"more"`、`"more_eq"`、`"contains"` 或 `"not_contains"`。`qual` 可以是默认值 `"any"`，此时只要与属性关联的任意值与测试值匹配，匹配就成功；也可以是 `"all"`，此时与属性关联的所有值都必须匹配测试值。`ignore-blanks` 接受布尔值。如果 `ignore-blanks` 设置为 `"true"`，比较时会忽略字符串中的任何空白。这仅在 `compare="eq"` 或 `compare="not_eq"` 时生效。在 `<match target="font">` 元素中使用时，`<test>` 元素中的 `target=` 属性选择是匹配原始模式还是字体。`"default"` 选择外层 `<match>` 元素所选择的目标。

### `<edit name="property" mode="assign" binding="weak">`

```xml
<edit name="property" mode="assign" binding="weak">
```

此元素包含表达式元素列表（任意值或运算符元素）。表达式元素在运行时求值，并修改属性 `"property"`。修改取决于 `"property"` 是否被关联的 `<test>` 元素之一匹配；如果是，则修改可能影响第一个匹配值。插入到属性中的任何值都会获得指定的绑定（`"strong"`、`"weak"` 或 `"same"`），其中 `"same"` 绑定使用匹配模式元素中的值。`mode` 为以下之一：

| 模式 | 有匹配 | 无匹配 |
|---|---|---|
| `"assign"` | 替换匹配值 | 替换所有值 |
| `"assign_replace"` | 替换所有值 | 替换所有值 |
| `"prepend"` | 插入到匹配值之前 | 插入到列表头部 |
| `"prepend_first"` | 插入到列表头部 | 插入到列表头部 |
| `"append"` | 追加到匹配值之后 | 追加到列表末尾 |
| `"append_last"` | 追加到列表末尾 | 追加到列表末尾 |
| `"delete"` | 删除匹配值 | 删除所有值 |
| `"delete_all"` | 删除所有值 | 删除所有值 |

### `<int>`, `<double>`, `<string>`, `<bool>`

```xml
<int>
<double>
<string>
<bool>
```

这些元素包含指示类型的单个值。`<bool>` 元素包含 `true` 或 `false`。解析浮点数存在一个重要限制——fontconfig 要求尾数必须以数字开头，而不是小数点，因此对于纯小数值请插入前导零（例如使用 `0.5` 而不是 `.5`，使用 `-0.5` 而不是 `-.5`）。

### `<matrix>`

```xml
<matrix>
```

此元素包含仿射变换的四个数值表达式。最简单情况下，它们将是四个 `<double>` 元素，但也可以是更复杂的表达式。

### `<range>`

```xml
<range>
```

此元素包含范围表示的两个 `<int>` 元素。

### `<charset>`

```xml
<charset>
```

此元素包含至少一个表示 Unicode 码点的 `<int>` 元素，或更多。

### `<langset>`

```xml
<langset>
```

此元素包含至少一个 RFC-3066 风格语言的 `<string>` 元素，或更多。

### `<name>`

```xml
<name>
```

保存属性名称。求值为模式中该属性的第一个值。如果不存在 `target` 属性，则默认为 `'default'`；在这种情况下，在 `target="font"` 匹配期间，属性从字体模式返回；在 `target="pattern"` 匹配期间，则从模式返回。该属性也可以取 `'font'` 或 `'pattern'` 值，以显式选择使用哪个模式。在 `target="pattern"` 的匹配中使用 `target` 为 `'font'` 是错误的。

### `<const>`

```xml
<const>
```

保存常量名称；这些常量始终是整数，并作为常见字体值的符号名称：

| 常量 | 属性 | 值 |
|---|---|---|
| `thin` | `weight` | 0 |
| `extralight` | `weight` | 40 |
| `ultralight` | `weight` | 40 |
| `light` | `weight` | 50 |
| `demilight` | `weight` | 55 |
| `semilight` | `weight` | 55 |
| `book` | `weight` | 75 |
| `regular` | `weight` | 80 |
| `normal` | `weight` | 80 |
| `medium` | `weight` | 100 |
| `demibold` | `weight` | 180 |
| `semibold` | `weight` | 180 |
| `bold` | `weight` | 200 |
| `extrabold` | `weight` | 205 |
| `ultrabold` | `weight` | 205 |
| `black` | `weight` | 210 |
| `heavy` | `weight` | 210 |
| `extrablack` | `weight` | 215 |
| `ultrablack` | `weight` | 215 |
| `roman` | `slant` | 0 |
| `italic` | `slant` | 100 |
| `oblique` | `slant` | 110 |
| `ultracondensed` | `width` | 50 |
| `extracondensed` | `width` | 63 |
| `condensed` | `width` | 75 |
| `semicondensed` | `width` | 87 |
| `normal` | `width` | 100 |
| `semiexpanded` | `width` | 113 |
| `expanded` | `width` | 125 |
| `extraexpanded` | `width` | 150 |
| `ultraexpanded` | `width` | 200 |
| `proportional` | `spacing` | 0 |
| `dual` | `spacing` | 90 |
| `mono` | `spacing` | 100 |
| `charcell` | `spacing` | 110 |
| `unknown` | `rgba` | 0 |
| `rgb` | `rgba` | 1 |
| `bgr` | `rgba` | 2 |
| `vrgb` | `rgba` | 3 |
| `vbgr` | `rgba` | 4 |
| `none` | `rgba` | 5 |
| `lcdnone` | `lcdfilter` | 0 |
| `lcddefault` | `lcdfilter` | 1 |
| `lcdlight` | `lcdfilter` | 2 |
| `lcdlegacy` | `lcdfilter` | 3 |
| `hintnone` | `hintstyle` | 0 |
| `hintslight` | `hintstyle` | 1 |
| `hintmedium` | `hintstyle` | 2 |
| `hintfull` | `hintstyle` | 3 |

### `<or>`, `<and>`, `<plus>`, `<minus>`, `<times>`, `<divide>`

```xml
<or>
<and>
<plus>
<minus>
<times>
<divide>
```

这些元素对表达式元素列表执行指定操作。`<or>` 和 `<and>` 是布尔运算，不是按位运算。

### `<eq>`, `<not_eq>`, `<less>`, `<less_eq>`, `<more>`, `<more_eq>`, `<contains>`, `<not_contains`

```xml
<eq>
<not_eq>
<less>
<less_eq>
<more>
<more_eq>
<contains>
<not_contains
```

这些元素比较两个值，并产生布尔结果。

### `<not>`

```xml
<not>
```

反转其单个表达式元素的布尔含义。

### `<if>`

```xml
<if>
```

此元素接受三个表达式元素；如果第一个值为真，则产生第二个值，否则产生第三个值。

### `<alias>`

```xml
<alias>
```

`Alias` 元素为将一种字体族替换为另一种字体族所需的一组常见匹配操作提供了简写。它们包含一个 `<family>` 元素，后跟可选的 `<prefer>`、`<accept>` 和 `<default>` 元素。匹配 `<family>` 元素的字体会被编辑为：将 `<prefer>` 的字体族列表前置到匹配的 `<family>` 之前，将 `<accept>` 可接受的字体族追加到匹配的 `<family>` 之后，并将 `<default>` 字体族追加到字体族列表末尾。

### `<family>`

```xml
<family>
```

保存单个字体族名称。

### `<prefer>`, `<accept>`, `<default>`

```xml
<prefer>
<accept>
<default>
```

这些元素包含供 `<alias>` 元素使用的 `<family>` 元素列表。

## 示例配置文件

### 系统配置文件

这是一个系统级配置文件的示例。

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<!-- /etc/fonts/fonts.conf 文件，用于配置系统字体访问 -->
<fontconfig>
  <!--
    在这些目录中查找字体
  -->
  <dir>/usr/share/fonts</dir>
  <dir>/usr/X11R6/lib/X11/fonts</dir>

  <!--
    接受已弃用的“mono”别名，将其替换为“monospace”
  -->
  <match target="pattern">
    <test qual="any" name="family">
      <string>mono</string>
    </test>
    <edit name="family" mode="assign">
      <string>monospace</string>
    </edit>
  </match>

  <!--
    不包含任何已知别名的名称将追加“sans-serif”
  -->
  <match target="pattern">
    <test qual="all" name="family" compare="not_eq">
      <string>sans-serif</string>
    </test>
    <test qual="all" name="family" compare="not_eq">
      <string>serif</string>
    </test>
    <test qual="all" name="family" compare="not_eq">
      <string>monospace</string>
    </test>
    <edit name="family" mode="append_last">
      <string>sans-serif</string>
    </edit>
  </match>

  <!--
    加载每用户自定义文件，但如果不存在则不报错
  -->
  <include ignore_missing="yes" prefix="xdg">
    fontconfig/fonts.conf
  </include>

  <!--
    加载本地自定义文件，但如果没有任何文件则不报错
  -->
  <include ignore_missing="yes">conf.d</include>
  <include ignore_missing="yes">local.conf</include>

  <!--
    将常见字体名别名到可用的 TrueType 字体。
    这些别名用相似的 TrueType 字体替换 Type1 字体，以改善屏幕显示效果。
  -->
  <alias>
    <family>Times</family>
    <prefer>
      <family>Times New Roman</family>
    </prefer>
    <default>
      <family>serif</family>
    </default>
  </alias>
  <alias>
    <family>Helvetica</family>
    <prefer>
      <family>Arial</family>
    </prefer>
    <default>
      <family>sans</family>
    </default>
  </alias>
  <alias>
    <family>Courier</family>
    <prefer>
      <family>Courier New</family>
    </prefer>
    <default>
      <family>monospace</family>
    </default>
  </alias>

  <!--
    为标准名称提供必需的别名。
    在用户配置文件之后执行这些操作，以便优先使用其中的任何别名
  -->
  <alias>
    <family>serif</family>
    <prefer>
      <family>Times New Roman</family>
    </prefer>
  </alias>
  <alias>
    <family>sans</family>
    <prefer>
      <family>Arial</family>
    </prefer>
  </alias>
  <alias>
    <family>monospace</family>
    <prefer>
      <family>Andale Mono</family>
    </prefer>
  </alias>

  <--
    OR 运算符需求示例；
    如果“family”包含“Courier New”或“Courier”，
    则添加“monospace”作为替代
  -->
  <match target="pattern">
    <test name="family" compare="eq">
      <string>Courier New</string>
    </test>
    <edit name="family" mode="prepend">
      <string>monospace</string>
    </edit>
  </match>
  <match target="pattern">
    <test name="family" compare="eq">
      <string>Courier</string>
    </test>
    <edit name="family" mode="prepend">
      <string>monospace</string>
    </edit>
  </match>

</fontconfig>
```

### 用户配置文件

这是一个位于 `$XDG_CONFIG_HOME/fontconfig/fonts.conf` 的每用户配置文件示例。

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<!--
  $XDG_CONFIG_HOME/fontconfig/fonts.conf，用于每用户字体配置
-->
<fontconfig>

  <!--
    私有字体目录
  -->
  <dir prefix="xdg">fonts</dir>

  <!--
    使用 rgb 子像素排序以改善 LCD 屏幕上的字形外观。
    影响渲染但不影响匹配的更改应始终使用 target="font"。
  -->
  <match target="font">
    <edit name="rgba" mode="assign">
      <const>rgb</const>
    </edit>
  </match>
  <!--
    当中文请求 serif 时使用文泉驿正黑字体
  -->
  <match>
    <!--
      如果你不想为 zh-tw 等使用文泉驿正黑字体，
      可以使用 zh-cn 代替 zh。
      请注意，即使设置 zh-cn，它仍然会匹配 zh。
      如果不喜欢这种行为，可以使用 compare="eq"
      代替 compare="contains"。
    -->
    <test name="lang" compare="contains">
      <string>zh</string>
    </test>
    <test name="family">
      <string>serif</string>
    </test>
    <edit name="family" mode="prepend">
      <string>WenQuanYi Zen Hei</string>
    </edit>
  </match>
  <!--
    当日语请求 sans-serif 时使用 VL Gothic 字体
  -->
  <match>
    <test name="lang" compare="contains">
      <string>ja</string>
    </test>
    <test name="family">
      <string>sans-serif</string>
    </test>
    <edit name="family" mode="prepend">
      <string>VL Gothic</string>
    </edit>
  </match>
</fontconfig>
```

## 文件

`fonts.conf` 包含 fontconfig 库的配置信息，包括用于查找字体信息的目录，以及在尝试匹配可用字体之前编辑程序指定字体模式的说明。它采用 XML 格式。

`conf.d` 是外部应用程序或本地管理员管理的附加配置文件目录的常规名称。以十进制数字开头的文件名按字典序排序，并用作附加配置文件。所有这些文件均为 XML 格式。主 `fonts.conf` 文件在 `<include>` 指令中引用此目录。

`fonts.dtd` 是描述配置文件格式的 DTD。

`$XDG_CONFIG_HOME/fontconfig/conf.d` 和 `~/.fonts.conf.d` 是每用户配置目录（通常为自动生成）的常规名称，尽管实际位置在全局 `fonts.conf` 文件中指定。请注意，`~/.fonts.conf.d` 现已弃用。在未来的版本中，默认不会读取它。

`$XDG_CONFIG_HOME/fontconfig/fonts.conf` 和 `~/.fonts.conf` 是每用户字体配置的常规位置，尽管实际位置在全局 `fonts.conf` 文件中指定。请注意，`~/.fonts.conf` 现已弃用。在未来的版本中，默认不会读取它。

`$XDG_CACHE_HOME/fontconfig/*.cache-*` 和 `~/.fontconfig/*.cache-*` 是未在每目录缓存中找到的字体信息的常规存储库。此文件由 fontconfig 自动维护。请注意，`~/.fontconfig/*.cache-*` 现已弃用。在未来的版本中，默认不会读取它。

## 环境变量

`FONTCONFIG_FILE` 用于覆盖默认配置文件。

`FONTCONFIG_PATH` 用于覆盖默认配置目录。

`FONTCONFIG_SYSROOT` 用于设置默认 sysroot 目录。

`FC_DEBUG` 用于输出详细的调试消息。更多细节请参见“调试应用程序”一节。

`FC_DBG_MATCH_FILTER` 用于过滤模式。它接受逗号分隔的对象名称列表，并且仅在 `FC_DEBUG` 包含 `MATCH2` 时生效。更多细节请参见“调试应用程序”一节。

`FC_LANG` 用于在查询中指定默认语言作为弱绑定。如果未设置，默认语言将根据当前 locale 确定。

`FONTCONFIG_USE_MMAP` 用于控制是否对缓存文件使用 `mmap(2)`（如果可用）。它接受布尔值。fontconfig 会检查缓存文件是否存储在可安全使用 `mmap(2)` 的文件系统上。显式设置此环境变量将导致跳过此检查，并强制使用或不使用 `mmap(2)`。

`SOURCE_DATE_EPOCH` 用于确保 `fc-cache(1)` 以确定性方式生成文件，以支持可重现构建。当设置为 UNIX 时间戳的数字表示时，fontconfig 会优先使用此值，而不是输入文件的修改时间，以确定哪些缓存文件需要重新生成。如果未设置 `SOURCE_DATE_EPOCH`（或它比目录的 mtime 更新），则现有行为不变。

## 另请参阅

`fc-cat(1)`、`fc-cache(1)`、`fc-list(1)`、`fc-match(1)`、`fc-query(1)`、[SOURCE_DATE_EPOCH](https://reproducible-builds.org/specs/source-date-epoch/)。

## 版本

Fontconfig 版本 2.15.0