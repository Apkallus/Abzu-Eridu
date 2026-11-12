https://man.archlinux.org/man/terminfo.5.en

## NAME

`terminfo` - 终端能力数据库

## SYNOPSIS

```
/usr/share/terminfo/*/*
```

## DESCRIPTION

*Terminfo* 是一个描述终端的数据库，供面向屏幕的程序使用，例如 "nvi(1)"、"lynx(1)"、"mutt(1)" 以及其他 curses 应用，这些程序使用对 "curses(3X)" 等库的高层调用。非 curses 应用也可通过低层调用使用它，这些应用可以是面向屏幕的（例如 "clear(1)"）或非屏幕的（例如 "tabs(1)"）。

*Terminfo* 通过给出终端具备的一组能力、指定如何执行屏幕操作，以及指定填充要求和初始化序列来描述终端。

本文档描述 *ncurses* 版本 6.6（补丁 20251230）。

### terminfo 条目语法

*terminfo* 中的条目由一系列字段组成：

- 每个字段以逗号“,”结尾（内嵌逗号可以用反斜杠转义，或写成“\054”）。
- 字段之间的空白被忽略。
- *terminfo* 条目中的第一个字段从第一列开始。
- 换行和前导空白（空格或制表符）可用于格式化条目以提高可读性。解析条目时会移除这些内容。

`infocmp` 的 `-f` 和 `-W` 选项依赖这一点来格式化 if-then-else 表达式，或强制最大行宽。生成的格式化终端描述可以被 `tic` 读取。

- 每个终端的第一个字段给出该终端已知的名称，名称之间用“|”字符分隔。

第一个名称是终端最常见的缩写（其主名称），最后一个名称应为完整标识该终端的长名称（见 "longname(3X)"），其他所有名称都被视为主终端名称的同义词（别名）。

X/Open Curses 建议除最后一个名称外的所有名称都应小写且不含空格；最后一个名称可以包含大写和空格以提高可读性。

本实现没有那么严格；它允许主名称和别名中使用混合大小写。如果最后一个名称没有内嵌空格，它允许该名称同时作为别名和详细名称（但会就此歧义发出警告）。

- 第一列以“#”开头的行被视为注释。

虽然注释行在任何位置都有效，但 `captoinfo` 和 `infotocap`（`tic` 的别名）的输出会移动注释，使其只出现在条目之间。

终端名称（除了最后一个详细条目）应使用以下约定选择。构成终端的特定硬件应有一个根名称，例如“hp2621”。此名称不应包含连字符。硬件可处于的模式或用户偏好应通过追加连字符和模式后缀来表示。因此，处于 132 列模式的 vt100 应为 vt100-w。在可能的情况下应使用以下后缀：

| 后缀 | 示例 | 含义 |
|---|---|---|
| -*nn* | aaa-60 | 屏幕上的行数 |
| -*n*p | c100-4p | 内存页数 |
| -am | vt100-am | 带自动边距（通常为默认） |
| -m | ansi-m | 单色模式；抑制颜色 |
| -mc | wy30-mc | Magic cookie；高亮时使用空格 |
| -na | c100-na | 无方向键（保持在本地） |
| -nam | vt100-nam | 无自动边距 |
| -nl | hp2621-nl | 无状态行 |
| -ns | hp2626-ns | 无状态行 |
| -rv | c100-rv | 反显 |
| -s | vt100-s | 启用状态行 |
| -vb | wy370-vb | 使用可见响铃而不是蜂鸣 |
| -w | vt100-w | 宽模式（> 80 列，通常为 132） |

关于终端命名约定的更多信息，见 "term(7)" 手册页。

### terminfo 能力语法

terminfo 条目由若干*能力*组成，即终端具有的特性，或用于行使终端特性的方法。

在第一个字段（给出终端条目的名称）之后，应有一个或多个*能力*字段。这些是 Boolean、numeric 或 string 名称及其对应值：

- Boolean 能力存在时为真，不存在时为假。Boolean 能力没有显式值。
- Numeric 能力在名称后跟“#”，然后是无符号十进制整数值。
- String 能力在名称后跟“=”，然后是构成能力值的字符串。

String 能力可以拆分成多行，就像组成终端条目的字段可以拆分成多行一样。虽然字段之间的空白被忽略，但字符串值内部的内嵌空白会保留，行首的前导空白除外。

任何能力都可以被*取消*，即从终端条目中抑制，方法是在其名称后跟“@”而不是能力值。

### 类似终端

如果有两个非常相似的终端，一个（变体）可以定义为与另一个（基础）相同，但有某些例外。在变体的定义中，可以给出 string 能力 `use` 并带上基础终端的名称：

- 在 `use` 之前给出的能力覆盖由 `use` 命名的基础类型中的能力。
- 如果有多个 `use` 能力，它们按相反顺序合并。也就是说，最右边的 `use` 引用先处理，然后是其左边的，依此类推。
- 条目中显式给出的能力覆盖由 `use` 引用引入的能力。

能力可以通过在导入它的 use 引用左侧放置 `xx@` 来取消，其中 *xx* 是能力。例如，条目

```
2621-nl, smkx@, rmkx@, use=2621,
```

定义一个 2621-nl，它没有 `smkx` 或 `rmkx` 能力，因此在可视模式下不会打开功能键标签。这对于终端的不同的模式或不同的用户偏好很有用。

通过 `use` 包含的条目可以包含已取消的能力，其效果与这些取消直接内联在使用终端条目中相同。

### 标准能力

以下表格列出了 *ncurses* 在 *terminfo* 终端类型描述中识别并可被使用 *terminfo* 的代码使用的能力。

- 能力名称标识程序员使用 *terminfo* API 访问该能力时所用的符号。
- TI（*terminfo*）代码是编写或更新终端类型条目的人使用的短名称。

在可能的情况下，这些代码与 ANSI X3.64-1979 标准的代码相同或相似（该标准现已被 ECMA-48 取代，后者使用相同或非常相似的名称）。语义也旨在与规范一致。

*terminfo* 代码没有硬性长度限制，但 *ncurses* 维持一个 5 字符的非正式限制，以保持它们简短，并允许源文件 *Caps* 中的制表符整齐对齐。（某些标准代码无论如何都会超过此限制。）

- TC（*termcap*）代码是 *ncurses* 相应 API 所使用的代码。（某些能力是新增的，其名称并非源自 BSD *termcap*。）
- 描述字段试图传达能力的语义。

描述字段使用少量记号。

- `(P)`  
    表示可以指定填充。
- `(P*)`  
    表示填充可能随受影响输出行数成比例变化。
- `#`*i*  
    表示字符串能力的第 *i* 个参数；程序员应将字符串连同列出的参数传给 "tparm(3X)"。

如果描述未列出参数，将字符串传给 "tparm(3X)" 可能会产生意外行为，例如字符串包含百分号时。

| Boolean Capability Name | TI | TC | Description |
|---|---|---|---|
| `auto_left_margin` | `bw` | `bw` | cub1 从第 0 列环绕到最后一列 |
| `auto_right_margin` | `am` | `am` | 终端具有自动边距 |
| `no_esc_ctlc` | `xsb` | `xb` | beehive（f1=escape，f2=ctrl C） |
| `ceol_standout_glitch` | `xhp` | `xs` | 突出显示不会被覆盖擦除（hp） |
| `eat_newline_glitch` | `xenl` | `xn` | 80 列后忽略换行（concept） |
| `erase_overstrike` | `eo` | `eo` | 可以用空白擦除叠印 |
| `generic_type` | `gn` | `gn` | 通用线路类型 |
| `hard_copy` | `hc` | `hc` | 硬拷贝终端 |
| `has_meta_key` | `km` | `km` | 有 meta 键（即设置第 8 位） |
| `has_status_line` | `hs` | `hs` | 有额外状态行 |
| `insert_null_glitch` | `in` | `in` | 插入模式区分空字符 |
| `memory_above` | `da` | `da` | 显示内容可保留在屏幕上方 |
| `memory_below` | `db` | `db` | 显示内容可保留在屏幕下方 |
| `move_insert_mode` | `mir` | `mi` | 在插入模式下移动是安全的 |
| `move_standout_mode` | `msgr` | `ms` | 在突出显示模式下移动是安全的 |
| `over_strike` | `os` | `os` | 终端可以叠印 |
| `status_line_esc_ok` | `eslok` | `es` | 转义可在状态行上使用 |
| `dest_tabs_magic_smso` | `xt` | `xt` | 制表符具有破坏性，magic so 字符（t1061） |
| `tilde_glitch` | `hz` | `hz` | 无法打印 ~（Hazeltine） |
| `transparent_underline` | `ul` | `ul` | 下划线字符叠印 |
| `xon_xoff` | `xon` | `xo` | 终端使用 xon/xoff 握手 |
| `needs_xon_xoff` | `nxon` | `nx` | 填充不会起作用，需要 xon/xoff |
| `prtr_silent` | `mc5i` | `5i` | 打印机不会在屏幕上回显 |
| `hard_cursor` | `chts` | `HC` | 光标难以看见 |
| `non_rev_rmcup` | `nrrmc` | `NR` | smcup 不会反转 rmcup |
| `no_pad_char` | `npc` | `NP` | 填充字符不存在 |
| `non_dest_scroll_region` | `ndscr` | `ND` | 滚动区域是非破坏性的 |
| `can_change` | `ccc` | `cc` | 终端可以重新定义现有颜色 |
| `back_color_erase` | `bce` | `ut` | 屏幕用背景色擦除 |
| `hue_lightness_saturation` | `hls` | `hl` | 终端仅使用 HLS 颜色表示法（Tektronix） |
| `col_addr_glitch` | `xhpa` | `YA` | hpa/mhpa 能力仅支持正向移动 |
| `cr_cancels_micro_mode` | `crxm` | `YB` | 使用 cr 会关闭微模式 |
| `has_print_wheel` | `daisy` | `YC` | 打印机需要操作员更换字符集 |
| `row_addr_glitch` | `xvpa` | `YD` | vpa/mvpa 能力仅支持正向移动 |
| `semi_auto_right_margin` | `sam` | `YE` | 在最后一列打印会产生回车 |
| `cpi_changes_res` | `cpix` | `YF` | 更改字符间距会改变分辨率 |
| `lpi_changes_res` | `lpix` | `YG` | 更改行间距会改变分辨率 |

| Numeric Capability Name | TI | TC | Description |
|---|---|---|---|
| `columns` | `cols` | `co` | 行中的列数 |
| `init_tabs` | `it` | `it` | 初始时每 # 个空格一个制表位 |
| `lines` | `lines` | `li` | 屏幕或页面上的行数 |
| `lines_of_memory` | `lm` | `lm` | 内存行数（若 > lines）。0 表示可变 |
| `magic_cookie_glitch` | `xmc` | `sg` | smso 或 rmso 留下的空白字符数 |
| `padding_baud_rate` | `pb` | `pb` | 需要填充的最低波特率 |
| `virtual_terminal` | `vt` | `vt` | 虚拟终端编号（CB/unix） |
| `width_status_line` | `wsl` | `ws` | 状态行的列数 |
| `num_labels` | `nlab` | `Nl` | 屏幕上的标签数 |
| `label_height` | `lh` | `lh` | 每个标签的行数 |
| `label_width` | `lw` | `lw` | 每个标签的列数 |
| `max_attributes` | `ma` | `ma` | 终端可处理的最大组合属性数 |
| `maximum_windows` | `wnum` | `MW` | 可定义窗口的最大数量 |
| `max_colors` | `colors` | `Co` | 屏幕上的最大颜色数 |
| `max_pairs` | `pairs` | `pa` | 屏幕上的最大颜色对数 |
| `no_color_video` | `ncv` | `NC` | 不能与颜色一起使用的视频属性 |

以下 numeric 能力存在于 SVr4.0 term 结构中，但尚未在手册页中记录。它们随 SVr4 的打印机支持引入。

| Numeric Capability Name | TI | TC | Description |
|---|---|---|---|
| `buffer_capacity` | `bufsz` | `Ya` | 打印前缓冲的字节数 |
| `dot_vert_spacing` | `spinv` | `Yb` | 垂直针间距（针/英寸） |
| `dot_horz_spacing` | `spinh` | `Yc` | 水平点间距（点/英寸） |
| `max_micro_address` | `maddr` | `Yd` | micro_..._address 中的最大值 |
| `max_micro_jump` | `mjump` | `Ye` | parm_..._micro 中的最大值 |
| `micro_col_size` | `mcs` | `Yf` | 微模式下的字符步长 |
| `micro_line_size` | `mls` | `Yg` | 微模式下的行步长 |
| `number_of_pins` | `npins` | `Yh` | 打印头的针数 |
| `output_res_char` | `orc` | `Yi` | 水平分辨率（单位/行） |
| `output_res_line` | `orl` | `Yj` | 垂直分辨率（单位/行） |
| `output_res_horz_inch` | `orhi` | `Yk` | 水平分辨率（单位/英寸） |
| `output_res_vert_inch` | `orvi` | `Yl` | 垂直分辨率（单位/英寸） |
| `print_rate` | `cps` | `Ym` | 打印速率（字符/秒） |
| `wide_char_size` | `widcs` | `Yn` | 双宽模式下的字符步长 |
| `buttons` | `btns` | `BT` | 鼠标上的按钮数 |
| `bit_image_entwining` | `bitwin` | `Yo` | 每个位图行的遍数 |
| `bit_image_type` | `bitype` | `Yp` | 位图设备类型 |

| String Capability Name | TI | TC | Description |
|---|---|---|---|
| `back_tab` | `cbt` | `bt` | 反向制表（P） |
| `bell` | `bel` | `bl` | 可听信号（响铃）（P） |
| `carriage_return` | `cr` | `cr` | 回车（P*）（P*） |
| `change_scroll_region` | `csr` | `cs` | 将区域改为第 #1 行到第 #2 行（P） |
| `clear_all_tabs` | `tbc` | `ct` | 清除所有制表位（P） |
| `clear_screen` | `clear` | `cl` | 清除屏幕并将光标移到起始位置（P*） |
| `clr_eol` | `el` | `ce` | 清除到行尾（P） |
| `clr_eos` | `ed` | `cd` | 清除到屏幕末尾（P*） |
| `column_address` | `hpa` | `ch` | 水平位置 #1，绝对（P） |
| `command_character` | `cmdch` | `CC` | 原型中终端可设置的命令字符 !? |
| `cursor_address` | `cup` | `cm` | 移到第 #1 行第 #2 列 |
| `cursor_down` | `cud1` | `do` | 向下一行 |
| `cursor_home` | `home` | `ho` | 光标移到起始位置（如果没有 cup） |
| `cursor_invisible` | `civis` | `vi` | 使光标不可见 |
| `cursor_left` | `cub1` | `le` | 向左移一个空格 |
| `cursor_mem_address` | `mrcup` | `CM` | 相对于内存的光标寻址，移到第 #1 行第 #2 列 |
| `cursor_normal` | `cnorm` | `ve` | 使光标显示为正常（撤销 civis/cvvis） |
| `cursor_right` | `cuf1` | `nd` | 非破坏性空格（向右移一个空格） |
| `cursor_to_ll` | `ll` | `ll` | 最后一行，第一列（如果没有 cup） |
| `cursor_up` | `cuu1` | `up` | 向上一行 |
| `cursor_visible` | `cvvis` | `vs` | 使光标非常可见 |
| `delete_character` | `dch1` | `dc` | 删除字符（P*） |
| `delete_line` | `dl1` | `dl` | 删除行（P*） |
| `dis_status_line` | `dsl` | `ds` | 禁用状态行 |
| `down_half_line` | `hd` | `hd` | 向下半行 |
| `enter_alt_charset_mode` | `smacs` | `as` | 开始替代字符集（P） |
| `enter_blink_mode` | `blink` | `mb` | 打开闪烁 |
| `enter_bold_mode` | `bold` | `md` | 打开粗体（额外亮度）模式 |
| `enter_ca_mode` | `smcup` | `ti` | 启动使用 cup 的程序时发送的字符串 |
| `enter_delete_mode` | `smdc` | `dm` | 进入删除模式 |
| `enter_dim_mode` | `dim` | `mh` | 打开半亮模式 |
| `enter_insert_mode` | `smir` | `im` | 进入插入模式 |
| `enter_secure_mode` | `invis` | `mk` | 打开空白模式（字符不可见） |
| `enter_protected_mode` | `prot` | `mp` | 打开保护模式 |
| `enter_reverse_mode` | `rev` | `mr` | 打开反显模式 |
| `enter_standout_mode` | `smso` | `so` | 开始突出显示模式 |
| `enter_underline_mode` | `smul` | `us` | 开始下划线模式 |
| `erase_chars` | `ech` | `ec` | 擦除 #1 个字符（P） |
| `exit_alt_charset_mode` | `rmacs` | `ae` | 结束替代字符集（P） |
| `exit_attribute_mode` | `sgr0` | `me` | 关闭所有属性 |
| `exit_ca_mode` | `rmcup` | `te` | 结束使用 cup 的程序时发送的字符串 |
| `exit_delete_mode` | `rmdc` | `ed` | 结束删除模式 |
| `exit_insert_mode` | `rmir` | `ei` | 退出插入模式 |
| `exit_standout_mode` | `rmso` | `se` | 退出突出显示模式 |
| `exit_underline_mode` | `rmul` | `ue` | 退出下划线模式 |
| `flash_screen` | `flash` | `vb` | 可见响铃（可能不移动光标） |
| `form_feed` | `ff` | `ff` | 硬拷贝终端换页（P*） |
| `from_status_line` | `fsl` | `fs` | 从状态行返回 |
| `init_1string` | `is1` | `i1` | 初始化字符串 |
| `init_2string` | `is2` | `is` | 初始化字符串 |
| `init_3string` | `is3` | `i3` | 初始化字符串 |
| `init_file` | `if` | `if` | 初始化文件名 |
| `insert_character` | `ich1` | `ic` | 插入字符（P） |
| `insert_line` | `il1` | `al` | 插入行（P*） |
| `insert_padding` | `ip` | `ip` | 在插入的字符后插入填充 |
| `key_backspace` | `kbs` | `kb` | 退格键 |
| `key_catab` | `ktbc` | `ka` | 清除所有制表位键 |
| `key_clear` | `kclr` | `kC` | 清除屏幕或擦除键 |
| `key_ctab` | `kctab` | `kt` | 清除制表位键 |
| `key_dc` | `kdch1` | `kD` | 删除字符键 |
| `key_dl` | `kdl1` | `kL` | 删除行键 |
| `key_down` | `kcud1` | `kd` | 下箭头键 |
| `key_eic` | `krmir` | `kM` | 在插入模式下由 rmir 或 smir 发送 |
| `key_eol` | `kel` | `kE` | 清除到行尾键 |
| `key_eos` | `ked` | `kS` | 清除到屏幕末尾键 |
| `key_f0` | `kf0` | `k0` | F0 功能键 |
| `key_f1` | `kf1` | `k1` | F1 功能键 |
| `key_f10` | `kf10` | `k;` | F10 功能键 |
| `key_f2` | `kf2` | `k2` | F2 功能键 |
| `key_f3` | `kf3` | `k3` | F3 功能键 |
| `key_f4` | `kf4` | `k4` | F4 功能键 |
| `key_f5` | `kf5` | `k5` | F5 功能键 |
| `key_f6` | `kf6` | `k6` | F6 功能键 |
| `key_f7` | `kf7` | `k7` | F7 功能键 |
| `key_f8` | `kf8` | `k8` | F8 功能键 |
| `key_f9` | `kf9` | `k9` | F9 功能键 |
| `key_home` | `khome` | `kh` | 起始键 |
| `key_ic` | `kich1` | `kI` | 插入字符键 |
| `key_il` | `kil1` | `kA` | 插入行键 |
| `key_left` | `kcub1` | `kl` | 左箭头键 |
| `key_ll` | `kll` | `kH` | 左下键（起始下移） |
| `key_npage` | `knp` | `kN` | 下一页键 |
| `key_ppage` | `kpp` | `kP` | 上一页键 |
| `key_right` | `kcuf1` | `kr` | 右箭头键 |
| `key_sf` | `kind` | `kF` | 前滚键 |
| `key_sr` | `kri` | `kR` | 回滚键 |
| `key_stab` | `khts` | `kT` | 设置制表位键 |
| `key_up` | `kcuu1` | `ku` | 上箭头键 |
| `keypad_local` | `rmkx` | `ke` | 离开小键盘传输模式 |
| `keypad_xmit` | `smkx` | `ks` | 进入小键盘传输模式 |
| `lab_f0` | `lf0` | `l0` | 功能键 f0 上的标签（若不为 f0） |
| `lab_f1` | `lf1` | `l1` | 功能键 f1 上的标签（若不为 f1） |
| `lab_f10` | `lf10` | `la` | 功能键 f10 上的标签（若不为 f10） |
| `lab_f2` | `lf2` | `l2` | 功能键 f2 上的标签（若不为 f2） |
| `lab_f3` | `lf3` | `l3` | 功能键 f3 上的标签（若不为 f3） |
| `lab_f4` | `lf4` | `l4` | 功能键 f4 上的标签（若不为 f4） |
| `lab_f5` | `lf5` | `l5` | 功能键 f5 上的标签（若不为 f5） |
| `lab_f6` | `lf6` | `l6` | 功能键 f6 上的标签（若不为 f6） |
| `lab_f7` | `lf7` | `l7` | 功能键 f7 上的标签（若不为 f7） |
| `lab_f8` | `lf8` | `l8` | 功能键 f8 上的标签（若不为 f8） |
| `lab_f9` | `lf9` | `l9` | 功能键 f9 上的标签（若不为 f9） |
| `meta_off` | `rmm` | `mo` | 关闭 meta 模式 |
| `meta_on` | `smm` | `mm` | 打开 meta 模式（第 8 位开启） |
| `newline` | `nel` | `nw` | 换行（行为如回车后跟换行） |
| `pad_char` | `pad` | `pc` | 填充字符（代替空字符） |
| `parm_dch` | `dch` | `DC` | 删除 #1 个字符（P*） |
| `parm_delete_line` | `dl` | `DL` | 删除 #1 行（P*） |
| `parm_down_cursor` | `cud` | `DO` | 向下 #1 行（P*） |
| `parm_ich` | `ich` | `IC` | 插入 #1 个字符（P*） |
| `parm_index` | `indn` | `SF` | 向前滚动 #1 行（P） |
| `parm_insert_line` | `il` | `AL` | 插入 #1 行（P*） |
| `parm_left_cursor` | `cub` | `LE` | 向左移动 #1 个字符（P） |
| `parm_right_cursor` | `cuf` | `RI` | 向右移动 #1 个字符（P*） |
| `parm_rindex` | `rin` | `SR` | 向后滚动 #1 行（P） |
| `parm_up_cursor` | `cuu` | `UP` | 向上 #1 行（P*） |
| `pkey_key` | `pfkey` | `pk` | 编程功能键 #1 以键入字符串 #2 |
| `pkey_local` | `pfloc` | `pl` | 编程功能键 #1 以在本地执行字符串 #2 |
| `pkey_xmit` | `pfx` | `px` | 编程功能键 #1 以传输字符串 #2 |
| `print_screen` | `mc0` | `ps` | 打印屏幕内容 |
| `prtr_off` | `mc4` | `pf` | 关闭打印机 |
| `prtr_on` | `mc5` | `po` | 打开打印机 |
| `repeat_char` | `rep` | `rp` | 重复字符 #1 #2 次（P*） |
| `reset_1string` | `rs1` | `r1` | 重置字符串 |
| `reset_2string` | `rs2` | `r2` | 重置字符串 |
| `reset_3string` | `rs3` | `r3` | 重置字符串 |
| `reset_file` | `rf` | `rf` | 重置文件名 |
| `restore_cursor` | `rc` | `rc` | 将光标恢复到上次 save_cursor 的位置 |
| `row_address` | `vpa` | `cv` | 垂直位置 #1 绝对（P） |
| `save_cursor` | `sc` | `sc` | 保存当前光标位置（P） |
| `scroll_forward` | `ind` | `sf` | 向上滚动文本（P） |
| `scroll_reverse` | `ri` | `sr` | 向下滚动文本（P） |
| `set_attributes` | `sgr` | `sa` | 定义视频属性 #1-#9（PG9） |
| `set_tab` | `hts` | `st` | 在每一行的当前列设置制表位 |
| `set_window` | `wind` | `wi` | 当前窗口为第 #1-#2 行、第 #3-#4 列 |
| `tab` | `ht` | `ta` | 制表到下一个 8 空格硬件制表位 |
| `to_status_line` | `tsl` | `ts` | 移到状态行第 #1 列 |
| `underline_char` | `uc` | `uc` | 给字符加下划线并越过它 |
| `up_half_line` | `hu` | `hu` | 向上半行 |
| `init_prog` | `iprog` | `iP` | 用于初始化的程序的路径名 |
| `key_a1` | `ka1` | `K1` | 小键盘左上 |
| `key_a3` | `ka3` | `K3` | 小键盘右上 |
| `key_b2` | `kb2` | `K2` | 小键盘中心 |
| `key_c1` | `kc1` | `K4` | 小键盘左下 |
| `key_c3` | `kc3` | `K5` | 小键盘右下 |
| `prtr_non` | `mc5p` | `pO` | 为 #1 个字节打开打印机 |
| `char_padding` | `rmp` | `rP` | 类似 ip，但在插入模式下 |
| `acs_chars` | `acsc` | `ac` | 图形字符集对，基于 vt100 |
| `plab_norm` | `pln` | `pn` | 编程标签 #1 以显示字符串 #2 |
| `key_btab` | `kcbt` | `kB` | 反向制表键 |
| `enter_xon_mode` | `smxon` | `SX` | 打开 xon/xoff 握手 |
| `exit_xon_mode` | `rmxon` | `RX` | 关闭 xon/xoff 握手 |
| `enter_am_mode` | `smam` | `SA` | 打开自动边距 |
| `exit_am_mode` | `rmam` | `RA` | 关闭自动边距 |
| `xon_character` | `xonc` | `XN` | XON 字符 |
| `xoff_character` | `xoffc` | `XF` | XOFF 字符 |
| `ena_acs` | `enacs` | `eA` | 启用替代字符集 |
| `label_on` | `smln` | `LO` | 打开软标签 |
| `label_off` | `rmln` | `LF` | 关闭软标签 |
| `key_beg` | `kbeg` | `@1` | 开始键 |
| `key_cancel` | `kcan` | `@2` | 取消键 |
| `key_close` | `kclo` | `@3` | 关闭键 |
| `key_command` | `kcmd` | `@4` | 命令键 |
| `key_copy` | `kcpy` | `@5` | 复制键 |
| `key_create` | `kcrt` | `@6` | 创建键 |
| `key_end` | `kend` | `@7` | 结束键 |
| `key_enter` | `kent` | `@8` | 输入/发送键 |
| `key_exit` | `kext` | `@9` | 退出键 |
| `key_find` | `kfnd` | `@0` | 查找键 |
| `key_help` | `khlp` | `%1` | 帮助键 |
| `key_mark` | `kmrk` | `%2` | 标记键 |
| `key_message` | `kmsg` | `%3` | 消息键 |
| `key_move` | `kmov` | `%4` | 移动键 |
| `key_next` | `knxt` | `%5` | 下一个键 |
| `key_open` | `kopn` | `%6` | 打开键 |
| `key_options` | `kopt` | `%7` | 选项键 |
| `key_previous` | `kprv` | `%8` | 上一个键 |
| `key_print` | `kprt` | `%9` | 打印键 |
| `key_redo` | `krdo` | `%0` | 重做键 |
| `key_reference` | `kref` | `&1` | 引用键 |
| `key_refresh` | `krfr` | `&2` | 刷新键 |
| `key_replace` | `krpl` | `&3` | 替换键 |
| `key_restart` | `krst` | `&4` | 重启键 |
| `key_resume` | `kres` | `&5` | 恢复键 |
| `key_save` | `ksav` | `&6` | 保存键 |
| `key_suspend` | `kspd` | `&7` | 挂起键 |
| `key_undo` | `kund` | `&8` | 撤销键 |
| `key_sbeg` | `kBEG` | `&9` | 移位开始键 |
| `key_scancel` | `kCAN` | `&0` | 移位取消键 |
| `key_scommand` | `kCMD` | `*1` | 移位命令键 |
| `key_scopy` | `kCPY` | `*2` | 移位复制键 |
| `key_screate` | `kCRT` | `*3` | 移位创建键 |
| `key_sdc` | `kDC` | `*4` | 移位删除字符键 |
| `key_sdl` | `kDL` | `*5` | 移位删除行键 |
| `key_select` | `kslt` | `*6` | 选择键 |
| `key_send` | `kEND` | `*7` | 移位结束键 |
| `key_seol` | `kEOL` | `*8` | 移位清除到行尾键 |
| `key_sexit` | `kEXT` | `*9` | 移位退出键 |
| `key_sfind` | `kFND` | `*0` | 移位查找键 |
| `key_shelp` | `kHLP` | `#1` | 移位帮助键 |
| `key_shome` | `kHOM` | `#2` | 移位起始键 |
| `key_sic` | `kIC` | `#3` | 移位插入字符键 |
| `key_sleft` | `kLFT` | `#4` | 移位左箭头键 |
| `key_smessage` | `kMSG` | `%a` | 移位消息键 |
| `key_smove` | `kMOV` | `%b` | 移位移动键 |
| `key_snext` | `kNXT` | `%c` | 移位下一个键 |
| `key_soptions` | `kOPT` | `%d` | 移位选项键 |
| `key_sprevious` | `kPRV` | `%e` | 移位上一个键 |
| `key_sprint` | `kPRT` | `%f` | 移位打印键 |
| `key_sredo` | `kRDO` | `%g` | 移位重做键 |
| `key_sreplace` | `kRPL` | `%h` | 移位替换键 |
| `key_sright` | `kRIT` | `%i` | 移位右箭头键 |
| `key_srsume` | `kRES` | `%j` | 移位恢复键 |
| `key_ssave` | `kSAV` | `!1` | 移位保存键 |
| `key_ssuspend` | `kSPD` | `!2` | 移位挂起键 |
| `key_sundo` | `kUND` | `!3` | 移位撤销键 |
| `req_for_input` | `rfi` | `RF` | 发送下一个输入字符（用于 pty） |
| `key_f11` | `kf11` | `F1` | F11 功能键 |
| `key_f12` | `kf12` | `F2` | F12 功能键 |
| `key_f13` | `kf13` | `F3` | F13 功能键 |
| `key_f14` | `kf14` | `F4` | F14 功能键 |
| `key_f15` | `kf15` | `F5` | F15 功能键 |
| `key_f16` | `kf16` | `F6` | F16 功能键 |
| `key_f17` | `kf17` | `F7` | F17 功能键 |
| `key_f18` | `kf18` | `F8` | F18 功能键 |
| `key_f19` | `kf19` | `F9` | F19 功能键 |
| `key_f20` | `kf20` | `FA` | F20 功能键 |
| `key_f21` | `kf21` | `FB` | F21 功能键 |
| `key_f22` | `kf22` | `FC` | F22 功能键 |
| `key_f23` | `kf23` | `FD` | F23 功能键 |
| `key_f24` | `kf24` | `FE` | F24 功能键 |
| `key_f25` | `kf25` | `FF` | F25 功能键 |
| `key_f26` | `kf26` | `FG` | F26 功能键 |
| `key_f27` | `kf27` | `FH` | F27 功能键 |
| `key_f28` | `kf28` | `FI` | F28 功能键 |
| `key_f29` | `kf29` | `FJ` | F29 功能键 |
| `key_f30` | `kf30` | `FK` | F30 功能键 |
| `key_f31` | `kf31` | `FL` | F31 功能键 |
| `key_f32` | `kf32` | `FM` | F32 功能键 |
| `key_f33` | `kf33` | `FN` | F33 功能键 |
| `key_f34` | `kf34` | `FO` | F34 功能键 |
| `key_f35` | `kf35` | `FP` | F35 功能键 |
| `key_f36` | `kf36` | `FQ` | F36 功能键 |
| `key_f37` | `kf37` | `FR` | F37 功能键 |
| `key_f38` | `kf38` | `FS` | F38 功能键 |
| `key_f39` | `kf39` | `FT` | F39 功能键 |
| `key_f40` | `kf40` | `FU` | F40 功能键 |
| `key_f41` | `kf41` | `FV` | F41 功能键 |
| `key_f42` | `kf42` | `FW` | F42 功能键 |
| `key_f43` | `kf43` | `FX` | F43 功能键 |
| `key_f44` | `kf44` | `FY` | F44 功能键 |
| `key_f45` | `kf45` | `FZ` | F45 功能键 |
| `key_f46` | `kf46` | `Fa` | F46 功能键 |
| `key_f47` | `kf47` | `Fb` | F47 功能键 |
| `key_f48` | `kf48` | `Fc` | F48 功能键 |
| `key_f49` | `kf49` | `Fd` | F49 功能键 |
| `key_f50` | `kf50` | `Fe` | F50 功能键 |
| `key_f51` | `kf51` | `Ff` | F51 功能键 |
| `key_f52` | `kf52` | `Fg` | F52 功能键 |
| `key_f53` | `kf53` | `Fh` | F53 功能键 |
| `key_f54` | `kf54` | `Fi` | F54 功能键 |
| `key_f55` | `kf55` | `Fj` | F55 功能键 |
| `key_f56` | `kf56` | `Fk` | F56 功能键 |
| `key_f57` | `kf57` | `Fl` | F57 功能键 |
| `key_f58` | `kf58` | `Fm` | F58 功能键 |
| `key_f59` | `kf59` | `Fn` | F59 功能键 |
| `key_f60` | `kf60` | `Fo` | F60 功能键 |
| `key_f61` | `kf61` | `Fp` | F61 功能键 |
| `key_f62` | `kf62` | `Fq` | F62 功能键 |
| `key_f63` | `kf63` | `Fr` | F63 功能键 |
| `clr_bol` | `el1` | `cb` | 清除到行首 |
| `clear_margins` | `mgc` | `MC` | 清除左右软边距 |
| `set_left_margin` | `smgl` | `ML` | 在当前列设置左软边距（不在 BSD *termcap* 中） |
| `set_right_margin` | `smgr` | `MR` | 在当前列设置右软边距 |
| `label_format` | `fln` | `Lf` | 标签格式 |
| `set_clock` | `sclk` | `SC` | 设置时钟，#1 时 #2 分 #3 秒 |
| `display_clock` | `dclk` | `DK` | 显示时钟 |
| `remove_clock` | `rmclk` | `RC` | 移除时钟 |
| `create_window` | `cwin` | `CW` | 定义窗口 #1，从 #2,#3 到 #4,#5 |
| `goto_window` | `wingo` | `WG` | 转到窗口 #1 |
| `hangup` | `hup` | `HU` | 挂断电话 |
| `dial_phone` | `dial` | `DI` | 拨打号码 #1 |
| `quick_dial` | `qdial` | `QD` | 不检查直接拨打号码 #1 |
| `tone` | `tone` | `TO` | 选择按键音拨号 |
| `pulse` | `pulse` | `PU` | 选择脉冲拨号 |
| `flash_hook` | `hook` | `fh` | 闪断叉簧 |
| `fixed_pause` | `pause` | `PA` | 暂停 2-3 秒 |
| `wait_tone` | `wait` | `WA` | 等待拨号音 |
| `user0` | `u0` | `u0` | 用户字符串 #0 |
| `user1` | `u1` | `u1` | 用户字符串 #1 |
| `user2` | `u2` | `u2` | 用户字符串 #2 |
| `user3` | `u3` | `u3` | 用户字符串 #3 |
| `user4` | `u4` | `u4` | 用户字符串 #4 |
| `user5` | `u5` | `u5` | 用户字符串 #5 |
| `user6` | `u6` | `u6` | 用户字符串 #6 |
| `user7` | `u7` | `u7` | 用户字符串 #7 |
| `user8` | `u8` | `u8` | 用户字符串 #8 |
| `user9` | `u9` | `u9` | 用户字符串 #9 |
| `orig_pair` | `op` | `op` | 将默认颜色对设为其原始值 |
| `orig_colors` | `oc` | `oc` | 将所有颜色对设为原始颜色对 |
| `initialize_color` | `initc` | `Ic` | 将颜色 #1 初始化为（#2,#3,#4） |
| `initialize_pair` | `initp` | `Ip` | 将颜色对 #1 初始化为 fg=（#2,#3,#4），bg=（#5,#6,#7） |
| `set_color_pair` | `scp` | `sp` | 将当前颜色对设为 #1 |
| `set_foreground` | `setf` | `Sf` | 设置前景色 #1 |
| `set_background` | `setb` | `Sb` | 设置背景色 #1 |
| `change_char_pitch` | `cpi` | `ZA` | 将每英寸字符数改为 #1 |
| `change_line_pitch` | `lpi` | `ZB` | 将每英寸行数改为 #1 |
| `change_res_horz` | `chr` | `ZC` | 将水平分辨率改为 #1 |
| `change_res_vert` | `cvr` | `ZD` | 将垂直分辨率改为 #1 |
| `define_char` | `defc` | `ZE` | 定义字符 #1，#2 点宽，下伸 #3 |
| `enter_doublewide_mode` | `swidm` | `ZF` | 进入双宽模式 |
| `enter_draft_quality` | `sdrfq` | `ZG` | 进入草稿质量模式 |
| `enter_italics_mode` | `sitm` | `ZH` | 进入斜体模式 |
| `enter_leftward_mode` | `slm` | `ZI` | 开始向左托架移动 |
| `enter_micro_mode` | `smicm` | `ZJ` | 开始微移动模式 |
| `enter_near_letter_quality` | `snlq` | `ZK` | 进入 NLQ 模式 |
| `enter_normal_quality` | `snrmq` | `ZL` | 进入正常质量模式 |
| `enter_shadow_mode` | `sshm` | `ZM` | 进入阴影打印模式 |
| `enter_subscript_mode` | `ssubm` | `ZN` | 进入下标模式 |
| `enter_superscript_mode` | `ssupm` | `ZO` | 进入上标模式 |
| `enter_upward_mode` | `sum` | `ZP` | 开始向上托架移动 |
| `exit_doublewide_mode` | `rwidm` | `ZQ` | 结束双宽模式 |
| `exit_italics_mode` | `ritm` | `ZR` | 结束斜体模式 |
| `exit_leftward_mode` | `rlm` | `ZS` | 结束左移模式 |
| `exit_micro_mode` | `rmicm` | `ZT` | 结束微移动模式 |
| `exit_shadow_mode` | `rshm` | `ZU` | 结束阴影打印模式 |
| `exit_subscript_mode` | `rsubm` | `ZV` | 结束下标模式 |
| `exit_superscript_mode` | `rsupm` | `ZW` | 结束上标模式 |
| `exit_upward_mode` | `rum` | `ZX` | 结束反向字符移动 |
| `micro_column_address` | `mhpa` | `ZY` | 类似微模式下的 column_address |
| `micro_down` | `mcud1` | `ZZ` | 类似微模式下的 cursor_down |
| `micro_left` | `mcub1` | `Za` | 类似微模式下的 cursor_left |
| `micro_right` | `mcuf1` | `Zb` | 类似微模式下的 cursor_right |
| `micro_row_address` | `mvpa` | `Zc` | 类似微模式下的 row_address #1 |
| `micro_up` | `mcuu1` | `Zd` | 类似微模式下的 cursor_up |
| `order_of_pins` | `porder` | `Ze` | 将软件位与打印头针对应 |
| `parm_down_micro` | `mcud` | `Zf` | 类似微模式下的 parm_down_cursor |
| `parm_left_micro` | `mcub` | `Zg` | 类似微模式下的 parm_left_cursor |
| `parm_right_micro` | `mcuf` | `Zh` | 类似微模式下的 parm_right_cursor |
| `parm_up_micro` | `mcuu` | `Zi` | 类似微模式下的 parm_up_cursor |
| `select_char_set` | `scs` | `Zj` | 选择字符集 #1 |
| `set_bottom_margin` | `smgb` | `Zk` | 在当前行设置底边距 |
| `set_bottom_margin_parm` | `smgbp` | `Zl` | 在第 #1 行设置底边距，或（如果未给出 smgtp）从底部数 #2 行 |
| `set_left_margin_parm` | `smglp` | `Zm` | 在第 #1 列设置左（右）边距 |
| `set_right_margin_parm` | `smgrp` | `Zn` | 在第 #1 列设置右边距 |
| `set_top_margin` | `smgt` | `Zo` | 在当前行设置顶边距 |
| `set_top_margin_parm` | `smgtp` | `Zp` | 在第 #1 行设置顶（底）边距 |
| `start_bit_image` | `sbim` | `Zq` | 开始打印位图图形 |
| `start_char_set_def` | `scsd` | `Zr` | 开始字符集定义 #1，该集合有 #2 个字符 |
| `stop_bit_image` | `rbim` | `Zs` | 停止打印位图图形 |
| `stop_char_set_def` | `rcsd` | `Zt` | 结束字符集 #1 的定义 |
| `subscript_characters` | `subcs` | `Zu` | 可作下标的字符列表 |
| `superscript_characters` | `supcs` | `Zv` | 可作上标的字符列表 |
| `these_cause_cr` | `docr` | `Zw` | 打印这些字符中的任何一个都会产生回车 |
| `zero_motion` | `zerom` | `Zx` | 后续字符不移动 |

以下 string 能力存在于 SVr4.0 term 结构中，但最初未在手册页中记录。

| String Capability Name | TI | TC | Description |
|---|---|---|---|
| `char_set_names` | `csnm` | `Zy` | 从字符集名称列表生成第 #1 项 |
| `key_mouse` | `kmous` | `Km` | 发生了鼠标事件 |
| `mouse_info` | `minfo` | `Mi` | 鼠标状态信息 |
| `req_mouse_pos` | `reqmp` | `RQ` | 请求鼠标位置 |
| `get_mouse` | `getm` | `Gm` | Curses 应获取按钮事件，参数 #1 未记录。 |
| `set_a_foreground` | `setaf` | `AF` | 将前景色设为 #1，使用 ANSI 转义 |
| `set_a_background` | `setab` | `AB` | 将背景色设为 #1，使用 ANSI 转义 |
| `pkey_plab` | `pfxl` | `xl` | 编程功能键 #1 以键入字符串 #2 并显示字符串 #3 |
| `device_type` | `devt` | `dv` | 指示语言、代码集支持 |
| `code_set_init` | `csin` | `ci` | 多代码集的初始化序列 |
| `set0_des_seq` | `s0ds` | `s0` | 切换到代码集 0（EUC 集 0，ASCII） |
| `set1_des_seq` | `s1ds` | `s1` | 切换到代码集 1 |
| `set2_des_seq` | `s2ds` | `s2` | 切换到代码集 2 |
| `set3_des_seq` | `s3ds` | `s3` | 切换到代码集 3 |
| `set_lr_margin` | `smglr` | `ML` | 将左右边距都设为 #1、#2。（ML 不在 BSD termcap 中）。 |
| `set_tb_margin` | `smgtb` | `MT` | 将上下边距都设为 #1、#2 |
| `bit_image_repeat` | `birep` | `Xy` | 重复位图单元 #1 #2 次 |
| `bit_image_newline` | `binel` | `Zz` | 移到下一行位图 |
| `bit_image_carriage_return` | `bicr` | `Yv` | 移到同一行的开头 |
| `color_names` | `colornm` | `Yw` | 给出颜色 #1 的名称 |
| `define_bit_image_region` | `defbi` | `Yx` | 定义矩形位图区域 |
| `end_bit_image_region` | `endbi` | `Yy` | 结束位图区域 |
| `set_color_band` | `setcolor` | `Yz` | 切换到色带颜色 #1 |
| `set_page_length` | `slines` | `YZ` | 将页长设为 #1 行 |
| `display_pc_char` | `dispc` | `S1` | 显示 PC 字符 #1 |
| `enter_pc_charset_mode` | `smpch` | `S2` | 进入 PC 字符显示模式 |
| `exit_pc_charset_mode` | `rmpch` | `S3` | 退出 PC 字符显示模式 |
| `enter_scancode_mode` | `smsc` | `S4` | 进入 PC 扫描码模式 |
| `exit_scancode_mode` | `rmsc` | `S5` | 退出 PC 扫描码模式 |
| `pc_term_options` | `pctrm` | `S6` | PC 终端选项 |
| `scancode_escape` | `scesc` | `S7` | 扫描码仿真的转义 |
| `alt_scancode_esc` | `scesa` | `S8` | 扫描码仿真的替代转义 |

XSI Curses 标准添加了这些硬拷贝能力。它们在一些 4.1 之后的 System V curses 版本中使用，例如 Solaris 2.5 和 IRIX 6.x。除了 `YI` 之外，这些能力的 `ncurses` termcap 名称是自创的。根据 XSI Curses 标准，它们没有 termcap 名称。如果你编译的 terminfo 条目使用这些，它们可能与 SVr4.1 之后的 System V terminfo 条目在二进制上不兼容；请注意！

| String Capability Name | TI | TC | Description |
|---|---|---|---|
| `enter_horizontal_hl_mode` | `ehhlm` | `Xh` | 进入水平高亮模式 |
| `enter_left_hl_mode` | `elhlm` | `Xl` | 进入左高亮模式 |
| `enter_low_hl_mode` | `elohlm` | `Xo` | 进入低高亮模式 |
| `enter_right_hl_mode` | `erhlm` | `Xr` | 进入右高亮模式 |
| `enter_top_hl_mode` | `ethlm` | `Xt` | 进入顶高亮模式 |
| `enter_vertical_hl_mode` | `evhlm` | `Xv` | 进入垂直高亮模式 |
| `set_a_attributes` | `sgr1` | `sA` | 定义第二组视频属性 #1-#6 |
| `set_pglen_inch` | `slength` | `YI` | 将页长设为 #1 百分之一英寸（某些实现使用 sL 作为 termcap）。 |

### 用户定义能力

上一节列出了*标准*能力。有些是深奥的，支持终端模拟器未实现的功能，或者可能从未在制造的硬件中实现。有时，模拟器具有通过标准能力难以或无法表示的特定功能。

*ncurses* 通过允许用户定义能力来解决这一限制。`tic` 和 `infocmp` 程序为此提供了 `-x` 选项。使用 `-x` 时，`tic` 将未知能力视为用户定义。也就是说，如果 `tic` 遇到它不认识的能力名称，程序会从能力值的语法推断能力的类型（Boolean、numeric 或 string），并为该能力创建扩展表条目。"use_extended_names(3X)" 使此信息有条件地可供应用使用。*ncurses* 库函数向调用者提供能力数据，其解释主要取决于应用。

- *ncurses* 将名称以“k”开头的用户定义 string 能力视为功能键。
- 由 `tic` 确定的能力类型（Boolean、numeric 或 string）可以通过成功调用 "tigetflag(3X)"、"tigetnum(3X)" 和 "tigetstr(3X)" 来推断。
- 如果能力名称恰好是两个字符，该能力也可通过 termcap 接口使用。

虽然 *termcap* 被称为可扩展，因为它不强制任何能力，但实际上它一直局限于 *terminfo* 实现所定义的能力。通常，在 *termcap* 应用中仅使用 Boolean 和 numeric 类型的用户定义能力，以避免超出 *termcap* 实现及其应用所假设的 1023 字节限制。具体来说，对扩展功能键集（超过 60 个编号键和少数特殊命名键）的支持最好通过 *terminfo* 提供的更长名称来实现。

*ncurses* 库使用了其中一些用户定义能力，如 "user_caps(5)" 所述。对于其他用户定义能力（包括功能键），请查阅终端数据库的源形式 *terminfo.src*，在“NCURSES USER-DEFINABLE CAPABILITIES”标题下。

### 示例条目

以下条目描述一个 ANSI X3.64（或 ECMA-48）标准终端（下称“ANSI 标准”），是典型现代终端 *terminfo* 条目的代表。

```
ansi|ansi/pc-term compatible with color,
        am, mc5i, mir, msgr,
        colors#8, cols#80, it#8, lines#24, ncv#3, pairs#64,
        acsc=+\020\,\021-\030.^Y0\333`\004a\261f\370g\361h\260
             j\331k\277l\332m\300n\305o~p\304q\304r\304s_t\303
             u\264v\301w\302x\263y\363z\362{\343|\330}\234~\376,
        bel=^G, blink=\E[5m, bold=\E[1m, cbt=\E[Z, clear=\E[H\E[J,
        cr=^M, cub=\E[%p1%dD, cub1=\E[D, cud=\E[%p1%dB, cud1=\E[B,
        cuf=\E[%p1%dC, cuf1=\E[C, cup=\E[%i%p1%d;%p2%dH,
        cuu=\E[%p1%dA, cuu1=\E[A, dch=\E[%p1%dP, dch1=\E[P,
        dl=\E[%p1%dM, dl1=\E[M, ech=\E[%p1%dX, ed=\E[J, el=\E[K,
        el1=\E[1K, home=\E[H, hpa=\E[%i%p1%dG, ht=\E[I, hts=\EH,
        ich=\E[%p1%d@, il=\E[%p1%dL, il1=\E[L, ind=^J,
        indn=\E[%p1%dS, invis=\E[8m, kbs=^H, kcbt=\E[Z, kcub1=\E[D,
        kcud1=\E[B, kcuf1=\E[C, kcuu1=\E[A, khome=\E[H, kich1=\E[L,
        mc4=\E[4i, mc5=\E[5i, nel=\r\E[S, op=\E[39;49m,
        rep=%p1%c\E[%p2%{1}%-%db, rev=\E[7m, rin=\E[%p1%dT,
        rmacs=\E[10m, rmpch=\E[10m, rmso=\E[m, rmul=\E[m,
        s0ds=\E(B, s1ds=\E)B, s2ds=\E*B, s3ds=\E+B,
        setab=\E[4%p1%dm, setaf=\E[3%p1%dm,
        sgr=\E[0;10%?%p1%t;7%;
                   %?%p2%t;4%;
                   %?%p3%t;7%;
                   %?%p4%t;5%;
                   %?%p6%t;1%;
                   %?%p7%t;8%;
                   %?%p9%t;11%;m,
        sgr0=\E[0;10m, smacs=\E[11m, smpch=\E[11m, smso=\E[7m,
        smul=\E[4m, tbc=\E[3g, u6=\E[%i%d;%dR, u7=\E[6n,
        u8=\E[?%[;0123456789]c, u9=\E[c, vpa=\E[%i%p1%dd,
```

条目可以通过在除第一行外的每行开头放置空白来延续到多行。注释可以包含在以“#”开头的行中。*terminfo* 中的能力有三种类型：

- Boolean 能力，指示终端具有某种特定特性，
- numeric 能力，给出终端的大小或特定延迟的大小，以及
- string 能力，给出可用于执行特定终端操作的序列。

### 能力类型

所有能力都有名称。例如，ANSI 标准终端具有*自动边距*（即，当到达行尾时自动回车和换行）这一事实由能力 `am` 指示。因此 ansi 的描述包含 `am`。Numeric 能力后跟字符“#”，然后是一个正值。因此，指示终端列数的 `cols` 对 ansi 给出的值为“80”。Numeric 能力的值可以使用 C 编程语言约定以十进制、八进制或十六进制指定（例如，255、0377 和 0xff 或 0xFF）。

最后，string 值的能力，例如 `el`（清除到行尾序列），由两字符代码、“=”以及以紧随其后的“,”结尾的字符串给出。

String 值的能力中提供了若干转义序列，以便于在那里编码字符：

- `\E` 和 `\e` 都映射到 ESCAPE 字符，
- `^`*x* 对任何适当的 *x* 映射到 control-*x*，以及
- 序列

`\n`、`\l`、`\r`、`\t`、`\b`、`\f` 和 `\s`

分别产生

*换行*、*换行（line-feed）*、*回车*、*制表*、*退格*、*换页* 和 *空格*。

X/Open Curses 未说明“适当的 *x*”可能是什么。实际上，那是可打印 ASCII 图形字符。特殊情况“^?”被解释为 DEL（127）。在所有其他情况下，字符值在逻辑上与 0x1f 进行“与”运算，映射到 0 到 31 范围内的 ASCII 控制码。

其他转义包括

- `\^` 表示 `^`，
- `\\` 表示 `\`，
- `\,` 表示逗号，
- `\:` 表示 `:`，
- 以及 `\0` 表示空字符。

`\0` 将产生 \200，它不会终止字符串，但在大多数终端上表现为空字符，前提是指定了 CS7。参见 "stty(1)"。

这种特殊行为的原因是保持编译后的 terminfo 文件与其他实现（例如记录此行为的 SVr4 系统）的二进制兼容性。编译后的 terminfo 文件使用以空字符结尾的字符串，没有长度信息。修改这一点将需要新的二进制格式，而这无法与其他实现配合工作。

最后，字符可以在 `\` 后以三位八进制数字给出。

延迟（以毫秒为单位）可以出现在 string 能力的任何位置，括在 $<..> 括号中，如 `el`=\EK$<5>，填充字符由 "tputs(3X)" 提供以产生此延迟。

- 延迟必须是精度最多一位小数的数字；它可以后跟后缀“*”或“/”或两者。
- “*”表示所需的填充与操作影响的行数成比例，给出的量是每受影响单位所需的填充。（在插入字符的情况下，因子仍然是受影响的*行*数。）

通常，如果设备具有 `xon` 能力，填充是建议性的；它用于成本计算，但不触发延迟。

- “/”后缀表示填充是强制性的，即使在具有 `xon` 表示流控制的设备上，也强制延迟给定的毫秒数。

有时必须注释掉个别能力。为此，在能力名称前放置一个句点。例如，参见上面示例中的第二个 `ind`。

### 获取编译后的描述

*ncurses* 中的终端描述存储在终端数据库中。这些数据库通过其路径名找到，可以配置为目录树或哈希数据库（见 "term(5)"），

库使用编译内置的路径名列表，可以通过环境变量覆盖。在开始搜索之前，*ncurses* 检查搜索列表，消除重复项和找不到终端数据库的路径名。*ncurses* 库读取第一个通过其一致性检查的描述。

- 首先检查环境变量 `TERMINFO`，寻找包含终端描述的终端数据库。
- 接下来，*ncurses* 在 *$HOME/.terminfo* 中查找编译后的描述。

这是一个可选特性，可能完全从库中省略，或被限制以防止特权应用意外使用。

- 接下来，如果设置了环境变量 *TERMINFO_DIRS*，*ncurses* 将该变量的内容解释为要搜索的终端数据库的冒号分隔路径名列表。

空路径名（即，如果变量以冒号开头或结尾，或包含相邻冒号）被解释为系统位置 */usr/share/terminfo*。

- 最后，*ncurses* 搜索这些编译内置位置：

    - 目录列表（/usr/share/terminfo），以及
    - 系统 terminfo 目录 */usr/share/terminfo*

`TERMINFO` 变量可以包含终端描述而不是终端数据库的路径名。如果此变量以“hex:”或“b64:”开头，则 *ncurses* 从十六进制或 base64 编码的数据读取终端描述，如果该描述与所寻求的名称匹配，则使用它。此编码数据可以使用 `tic` 或 `infocmp` 的“-Q”选项设置。

上述内容涉及 *ncurses* 的常见配置，它使用以 *terminfo* 格式准备的终端描述。虽然 *termcap* 表达力较弱，*ncurses* 也可以配置为读取 *termcap* 描述。在该配置中，它在系统终端数据库之后检查 *TERMCAP* 和 *TERMPATH* 变量（分别用于内容和搜索路径）。

### 准备描述

我们现在概述如何准备终端描述。准备终端描述的最有效方式是模仿 *terminfo* 中类似终端的描述，并逐步构建描述，使用 *vi* 或其他面向屏幕的程序对部分描述进行检查，以确保它们正确。请注意，非常不寻常的终端可能会暴露 *terminfo* 文件描述它能力的缺陷，或测试程序的屏幕处理代码中的错误。

要正确获得插入行的填充（如果终端制造商没有记录它），一个严峻的测试是在 9600 波特下编辑一个大文件，从屏幕中间删除 16 行左右，然后快速按几次“u”键。如果终端出错，通常需要更多填充。可以对插入字符使用类似的测试。

### 基本能力

终端每行的列数由 `cols` numeric 能力给出。如果终端是 CRT，则屏幕上的行数由 `lines` 能力给出。如果终端在到达右边距时环绕到下一行开头，则它应具有 `am` 能力。如果终端可以清除其屏幕，使光标留在起始位置，则由 `clear` string 能力给出。如果终端是叠印（而不是在字符叠印时清除位置），则它应具有 `os` 能力。如果终端是打印终端，没有软拷贝单元，则同时给出 `hc` 和 `os`。（`os` 适用于存储示波器终端，例如 TEKTRONIX 4010 系列，以及硬拷贝和 APL 终端。）如果有代码将光标移到当前行的左边缘，则将其作为 `cr` 给出。（通常这是回车，control/M。）如果有代码产生可听信号（响铃、蜂鸣等），则将其作为 `bel` 给出。

如果有代码将光标向左移动一个位置（例如退格），该能力应作为 `cub1` 给出。类似地，向右、向上和向下移动的代码应分别作为 `cuf1`、`cuu1` 和 `cud1` 给出。这些本地光标移动不应改变它们经过的文本，例如，通常不会使用“`cuf1`= ”因为空格会擦除移过的字符。

这里非常重要的一点是，*terminfo* 中编码的本地光标移动在 CRT 终端的左边缘和上边缘是未定义的。程序绝不应尝试在左边缘周围退格，除非给出了 `bw`，也绝不应尝试从顶部本地向上移动。为了向上滚动文本，程序将转到屏幕左下角并发送 `ind`（索引）字符串。

为了向下滚动文本，程序转到屏幕左上角并发送 `ri`（反向索引）字符串。字符串 `ind` 和 `ri` 在不在屏幕各自角落时是未定义的。

滚动序列的参数化版本是 `indn` 和 `rin`，它们与 `ind` 和 `ri` 语义相同，除了它们接受一个参数，并滚动那么多行。除了在屏幕的适当边缘外，它们也是未定义的。

`am` 能力告诉光标在输出文本时是否粘在屏幕右边缘，但这不一定适用于从最后一列的 `cuf1`。从左边距唯一定义的本地移动是，如果给出了 `bw`，则从左边距的 `cub1` 将移到上一行的右边缘。如果未给出 `bw`，则效果未定义。例如，这对于在屏幕边缘绘制方框很有用。如果终端具有开关可选的自动边距，*terminfo* 文件通常假设它开启；即 `am`。如果终端有移动到下一行第一列的命令，该命令可以作为 `nel`（换行）给出。该命令是否清除当前行的剩余部分并不重要，因此如果终端没有 `cr` 和 `lf`，仍可能从其中之一或两者构造出可用的 `nel`。

这些能力足以描述硬拷贝和“玻璃 tty”终端。因此，33 型电传打字机描述为

```
33|tty33|tty|model 33 teletype,
        bel=^G, cols#72, cr=^M, cud1=^J, hc, ind=^J, os,
```

而 Lear Siegler ADM-3 描述为

```
adm3|3|lsi adm3,
        am, bel=^G, clear=^Z, cols#80, cr=^M, cub1=^H, cud1=^J,
        ind=^J, lines#24,
```

### 参数化字符串

光标寻址和其他需要终端中参数的字符串由参数化 string 能力描述，其中包含类似 *printf* 的转义，如 *%x*。例如，要寻址光标，给出 `cup` 能力，使用两个参数：要寻址到的行和列。（行和列从零开始编号，指的是用户可见的物理屏幕，而不是任何不可见的内存。）如果终端具有内存相对光标寻址，可以用 `mrcup` 表示。

参数机制使用栈和特殊的 `%` 代码来操作它。通常一个序列会将其中一个参数压入栈，然后以某种格式打印它。打印（例如，“%d”）是一种特殊情况。其他操作，包括“%t”，会从栈中弹出其操作数。注意更复杂的操作通常是必要的，例如在 `sgr` 字符串中。

`%` 编码具有以下含义：

- `%%`  
    输出“%”
- `%[[[:]flags][width[.precision]][doxXs]`  
    同 "printf(3)"，标志为 *[-+#]* 和 *space*。使用“:”允许下一个字符为“-”标志，避免将“%-”解释为操作符。
- `%c`  
    像 `printf` 中的 %c 一样打印 *pop()*
- `%s`  
    像 `printf` 中的 %s 一样打印 *pop()*
- `%p`*[1-9]*  
    压入第 *i* 个参数
- `%P`*[a-z]*  
    将动态变量 *[a-z]* 设为 *pop()*
- `%g`*[a-z]*  
    获取动态变量 *[a-z]* 并压入它
- `%P`*[A-Z]*  
    将静态变量 *[a-z]* 设为 *pop()*
- `%g`*[A-Z]*  
    获取静态变量 *[a-z]* 并压入它

“静态”和“动态”这两个术语具有误导性。历史上，这只是两组不同的变量，它们的值在 "tparm(3X)" 调用之间不会被重置。然而，这一事实在其他实现中并未记录。依赖它将对可移植性产生不利影响：

- SVr2 curses 支持*动态*变量。这些变量仅由 `%P` 操作符设置。对于给定变量，如果未先用 `%P` 设置就使用 `%g`，将产生不可预测的结果，因为在 `tparm` 函数中，动态变量是栈上未初始化的局部数组。
- SVr3.2 curses 支持*静态*变量。这些变量是 *TERMINAL* 结构（在 `term.h` 中声明）中的数组，并在 `setupterm` 函数分配数据时自动清零。
- SVr4 curses 没有对*动态/静态*变量特性做进一步改进。
- Solaris XPG4 curses 不区分*动态*和*静态*变量。它们相同。与 SVr4 curses 一样，XPG4 curses 不显式初始化它们。
- 在版本 6.3 之前，*ncurses* 将*动态*和*静态*变量都存储在持久存储中，初始化为零。
- 从版本 6.3 开始，*ncurses* 以与 SVr4 相同的方式存储*静态*和*动态*变量。

    - 与其他实现不同，*ncurses* 在第一个 `%g` 或 `%P` 操作符之前将动态变量清零。
    - 与 SVr2 一样，*ncurses* 中动态变量的作用域在当前 `tparm` 调用内。如果需要持久存储，请使用静态变量。

- `%'`*c*`'`  
    字符常量 *c*
- `%{`*nn*`}`  
    整数常量 *nn*
- `%l`  
    压入 strlen(pop)
- `%+`、`%-`、`%*`、`%/`、`%m`  
    算术（`%m` 是*取模*）：*push(pop() op pop())*
- `%&`、`%|`、`%^`  
    位运算（“与”、“或”和异或）：*push(pop() op pop())*
- `%=`、`%>`、`%<`  
    逻辑运算：*push(pop() op pop())*
- `%A`、`%O`  
    逻辑“与”和“或”运算（用于条件）
- `%!`、`%~`  
    一元运算（逻辑补和位补）：*push(op pop())*
- `%i`  
    将前两个参数加 1（用于 ANSI 终端）
- `%?` *expr* `%t` *thenpart* `%e` *elsepart* `%;`  
    这形成 if-then-else。`%e` *elsepart* 是可选的。通常 `%?` *expr* 部分将值压入栈，`%t` 将其弹出，测试它是否非零（真）。如果为零（假），控制传递到 `%e`（else）部分。

可以像 Algol 68 那样形成 else-if 链：

`%?` c1 `%t` b1 `%e` c2 `%t` b2 `%e` c3 `%t` b3 `%e` c4 `%t` b4 `%e` `%;`

其中 ci 是条件，bi 是主体。

使用 `tic` 或 `infocmp` 的 `-f` 选项查看 if-then-else 的结构。某些字符串，例如 `sgr`，写成一行时可能非常复杂。`-f` 选项将字符串拆分成行，并将各部分缩进。

二元运算采用后缀形式，操作数按通常顺序排列。也就是说，要得到 x-5，应使用“%gx%{5}%-”。`%P` 和 `%g` 变量在转义字符串求值之间是持久的。

考虑 HP2645，要到达第 3 行第 12 列，需要发送 \E&a12c03Y 并填充 6 毫秒。这里行和列的顺序是颠倒的，行和列都打印为两位数字。相应的终端描述这样表示：

```
cup=\E&a%p2%dc%p1%dY$<6>,
```

Microterm ACT-IV 需要发送当前行和列，前面加 `^T`，行和列简单地以二进制编码，

```
cup=^T%p1%c%p2%c
```

使用“%c”的终端需要能够使光标退格（`cub1`），并在屏幕上将光标上移一行（`cuu1`）。这是必要的，因为发送 `\n` `^D` 和 `\r` 并不总是安全的，系统可能会更改或丢弃它们。（处理 terminfo 的库例程设置 tty 模式，使制表符从不展开，因此发送 \t 是安全的。这对 Ann Arbor 4080 来说是必不可少的。）

最后一个例子是 LSI ADM-3A，它使用偏移一个空格的的行和列，因此

```
cup=\E=%p1%' '%+%c%p2%' '%+%c
```

在发送“\E=”后，它压入第一个参数，压入空格的 ASCII 值（32），将它们相加（用和替换前两个值压入栈），并将该值作为字符输出。然后对第二个参数做同样的事。使用栈可以进行更复杂的算术。

### 光标移动

如果终端有快速回到起始位置（屏幕最左上角）的方法，则可以将其作为 `home` 给出；类似地，快速到达左下角的方法可以作为 `ll` 给出；这可能涉及从起始位置用 `cuu1` 向上移动，但程序本身绝不应这样做（除非 `ll` 这样做），因为它无法假设从起始位置向上移动的效果。注意起始位置与寻址到 (0,0) 相同：屏幕左上角，而不是内存左上角。（因此，HP 终端上的 \EH 序列不能用于 `home`。）

如果终端具有行或列绝对光标寻址，则可以分别作为单参数能力 `hpa`（水平位置绝对）和 `vpa`（垂直位置绝对）给出。有时这些比更通用的两参数序列更短（如 hp2645），可以优先于 `cup` 使用。如果存在参数化本地移动（例如，向右移动 *n* 个空格），则可以作为 `cud`、`cub`、`cuf` 和 `cuu` 给出，带一个参数指示移动多少空格。如果终端没有 `cup`，这些主要有用，例如 TEKTRONIX 4025。

如果终端在运行使用这些能力的程序时需要处于特殊模式，则进入和退出此模式的代码可以作为 `smcup` 和 `rmcup` 给出。例如，具有多页内存的 Concept 等终端会出现这种情况。如果终端只有内存相对光标寻址而没有屏幕相对光标寻址，则必须将屏幕大小的窗口固定到终端中，以便光标寻址正常工作。这也用于 TEKTRONIX 4025，其中 `smcup` 将命令字符设为 terminfo 使用的字符。如果 `smcup` 序列在输出 `rmcup` 序列后不会恢复屏幕（恢复到输出 `rmcup` 之前的状态），则指定 `nrrmc`。

### 边距

SVr4（和 X/Open Curses）列出了几个用于设置边距的 string 能力。其中两个用于终端，另外六个用于打印机。

- 两个终端能力假设终端可能具有在当前光标列位置设置左和/或右边距的能力。
- 打印机能力假设打印机可能具有两种类型的能力：

    - 使用当前行位置设置顶部和/或底部边距的能力，以及
    - 用于在给出行数或列数的情况下设置顶部、底部、左、右边距的参数化能力。

实际上，分为“终端”和“打印机”并不合适：

- AT&T SVr4 终端数据库为 AT&T 硬件使用了四次 `smgl`。

四个中有三个是打印机。它们缺乏通过指定列来设置左/右边距的能力。

- 其他（非 AT&T）终端可能支持边距，但使用与 AT&T 不同的假设。

例如，DEC VT420 支持左/右边距，但只使用列参数。更复杂的是，VT420 使用两个设置来完全启用左/右边距（左/右边距模式和原点模式）。前者启用边距，使打印文本在边距内换行，但后者需要防止光标寻址超出这些边距。

- 两个 DEC VT420 左/右边距都用单个控制序列设置。如果省略其中一个，相应边距被设为显示的左或右边缘（而不是保持边距不变）。

以下是边距相关能力：

名称、描述

- `smgl`  
    在当前列设置左边距
- `smgr`  
    在当前列设置右边距
- `smgb`  
    在当前行设置底边距
- `smgt`  
    在当前行设置顶边距
- `smgbp`  
    在第 *N* 行设置底边距
- `smglp`  
    在第 *N* 列设置左边距
- `smgrp`  
    在第 *N* 列设置右边距
- `smgtp`  
    在第 *N* 行设置顶边距
- `smglr`  
    将左右边距都设为 *L* 和 *R*
- `smgtb`  
    将上下边距都设为 *T* 和 *B*

编写使用这些 string 能力的应用时，应首先检查每对能力是否都设置了，还是只设置了一个：

- 如果 `smglp` 和 `smgrp` 都设置，则每个都使用一个参数 *N*，分别给出左边距和右边距的列号。
- 如果 `smgtp` 和 `smgbp` 都设置，则分别用于设置顶边距和底边距：

    - `smgtp` 使用一个参数 *N*，即顶边距的行号。
    - `smgbp` 使用两个参数 *N* 和 *M*，给出底边距的行号，第一个从页面顶部计数，第二个从底部计数。这适应了不同制造商打印机中指定底边距的两种风格。

在为具有可设置底边距的打印机制作 terminfo 条目时，应根据打印机仅使用第一个或第二个参数。在开发使用 `smgbp` 设置底边距的应用时，必须给出两个参数。

相反，当一对中只有一个能力被设置时：

- 如果 `smglp` 和 `smgrp` 中只有一个被设置，则它使用两个参数，按顺序给出左边距和右边距的列号。
- 同样，如果 `smgtp` 和 `smgbp` 中只有一个被设置，则它使用两个参数，按顺序给出顶边距和底边距，从页面顶部计数。

在为需要同时设置左右或上下边距的打印机制作 terminfo 条目时，应只定义 `smglp` 和 `smgrp` 或 `smgtp` 和 `smgbp` 对中的一个能力，另一个不设置。

除了非常旧的终端描述（例如为 SVr4 开发的描述）外，刚刚描述的方案应视为过时。在 SVr4 发布后期添加了一组改进的能力（`smglr` 和 `smgtb`），它们显式使用两个参数设置左/右或上/下边距。

设置边距时，行值和列值从零开始。

应定义 `mgc` string 能力。"tabs(1)" 等应用依赖它来重置所有边距。

### 区域清除

如果终端可以从当前位置清除到行尾，光标留在原处，则应作为 `el` 给出。如果终端可以从行首清除到当前位置（含），光标留在原处，则应作为 `el1` 给出。如果终端可以从当前位置清除到显示末尾，则应作为 `ed` 给出。`Ed` 仅从行的第一列定义。（因此，如果没有真正的 `ed`，可以通过请求删除大量行来模拟。）

### 插入/删除行和垂直移动

如果终端可以在光标所在行之前打开一个新的空白行，则应作为 `il1` 给出；这仅从行的第一个位置执行。然后光标必须出现在新空白行上。如果终端可以删除光标所在的行，则应作为 `dl1` 给出；这仅从要删除的行的第一个位置执行。接受一个参数并插入或删除那么多行的 `il1` 和 `dl1` 版本可以作为 `il` 和 `dl` 给出。

如果终端有可设置的滚动区域（如 vt100），则设置它的命令可以用 `csr` 能力描述，该能力接受两个参数：滚动区域的顶行和底行。唉，使用此命令后光标位置是未定义的。

可以通过在适当选择的区域上使用 `csr` 来获得插入或删除行的效果；`sc` 和 `rc`（保存和恢复光标）命令可能有助于确保合成的插入/删除字符串不移动光标。（注意 "ncurses(3X)" 库会自动进行这种合成，因此你不需要为具有 `csr` 的条目编写插入/删除字符串）。

构造插入和删除的另一种方法可能是使用索引与某些终端（如 HP-700/90 系列，但该系列也有插入/删除）上的内存锁定功能相结合。

在许多没有真正插入/删除行功能的终端上，也可以使用 `ri` 或 `ind` 在屏幕顶部或底部插入行，即使在具有这些功能的终端上，这通常也更快。

如果每个滚动窗口实际上是屏幕大小画布上的视口，则应设置 Boolean `non_dest_scroll_region`。要测试此能力，请在屏幕中间创建一个滚动区域，向底行写入内容，将光标移到区域顶部，然后执行 `ri`，接着执行 `dl1` 或 `ind`。如果由 `ri` 从区域底部滚出的数据重新出现，则滚动是非破坏性的。System V 和 X/Open Curses 期望 `ind`、`ri`、`indn` 和 `rin` 模拟破坏性滚动；它们的文档警告你，除非情况属实，否则不要定义 `csr`。此 `curses` 实现更为宽松，如果定义了 `ndsrc`，则会在滚动后执行显式擦除。

如果终端具有将窗口定义为内存一部分的能力，所有命令都影响该窗口，则应作为参数化字符串 `wind` 给出。四个参数按顺序是内存中的起始和结束行以及内存中的起始和结束列。

如果终端可以保留上方的显示内存，则应给出 `da` 能力；如果可以保留下方的显示内存，则应给出 `db`。这些指示删除行或滚动可能会从下方带来非空白行，或者用 `ri` 向后滚动可能会带下非空白行。

### 插入/删除字符

关于插入/删除字符，有两种基本的智能终端，可以使用 *terminfo* 描述。最常见的插入/删除字符操作只影响当前行上的字符，并严格将字符移出行尾。其他终端，例如 Concept 100 和 Perkin Elmer Owl，区分屏幕上已键入和未键入的空白，在插入或删除时仅移动到屏幕上未键入的空白，该空白要么被消除，要么扩展为两个未键入的空白。

你可以通过清除屏幕然后键入由光标移动分隔的文本来确定你拥有哪种终端。在“abc”和“def”之间使用本地光标移动（不是空格）键入“abc    def”。然后将光标定位在“abc”之前，并将终端置于插入模式。如果键入字符导致行的其余部分严格移动，并且字符从行尾掉落，则你的终端不区分空白和未键入位置。如果“abc”移到“def”上，然后随着你插入而在当前行尾周围一起移动并移到下一行，则你拥有第二种类型的终端，应给出能力 `in`，它代表“插入空字符”。

虽然这些是逻辑上独立的属性（单行与多行插入模式，以及未键入空白的特殊处理），但我们没有看到过插入模式无法用单一属性描述的终端。

Terminfo 可以描述具有插入模式的终端，以及发送简单序列以在当前行打开空白位置的终端。将进入插入模式的序列作为 `smir` 给出。将离开插入模式的序列作为 `rmir` 给出。现在将发送要插入的字符之前所需的任何序列作为 `ich1` 给出。大多数具有真正插入模式的终端不会给出 `ich1`；发送序列以打开屏幕位置的终端应在此处给出它。

如果你的终端两者都有，插入模式通常优于 `ich1`。技术上，除非终端实际需要两者结合使用，否则不应同时给出两者。因此，某些非 curses 应用如果两者都存在会混淆；症状是在使用插入的更新中出现重复字符。这一要求现在很少见；大多数 `ich` 序列不需要先前的 smir，大多数 smir 插入模式不需要在每个字符前使用 `ich1`。因此，新的 `curses` 实际上假设情况如此，并根据情况使用 `rmir`/`smir` 或 `ich`/`ich1`（但不同时使用）。如果你必须为足够旧、需要两者的终端编写要在新 curses 下使用的条目，请将 `rmir`/`smir` 序列包含在 `ich1` 中。

如果需要插入后填充，则将其作为毫秒数在 `ip` 中给出（string 选项）。插入单个字符后可能需要发送的任何其他序列也可以在 `ip` 中给出。如果你的终端既需要置于“插入模式”，又需要特殊代码在每个插入字符之前，则可以同时给出 `smir`/`rmir` 和 `ich1`，两者都会被使用。`ich` 能力带一个参数 *n*，将重复 `ich1` 的效果 *n* 次。

如果在不在插入模式时键入的字符之间需要填充，则将其作为毫秒数填充在 `rmp` 中给出。

有时需要在插入模式下移动以删除同一行上的字符（例如，如果插入位置后有制表符）。如果你的终端允许在插入模式下移动，则可以给出能力 `mir` 以加快这种情况下的插入。省略 `mir` 只会影响速度。某些终端（尤其是 Datamedia 的）由于其插入模式的工作方式，不能有 `mir`。

最后，你可以指定 `dch1` 删除单个字符，`dch` 带一个参数 *n* 删除 *n* 个字符，并通过给出 `smdc` 和 `rmdc` 进入和退出删除模式（`dch1` 工作需要终端处于的任何模式）。

擦除 *n* 个字符的命令（等同于输出 *n* 个空格而不移动光标）可以作为一个参数的 `ech` 给出。

### 高亮、下划线和可见响铃

如果你的终端有一种或多种显示属性，可以用多种不同方式表示。你应选择一种显示形式作为*突出显示模式*，代表一种良好、高对比度、悦目的格式，用于高亮错误消息和其他引人注意的内容。（如果有选择，反显加半亮很好，或仅反显。）进入和退出突出显示模式的序列分别作为 `smso` 和 `rmso` 给出。如果切换到突出显示模式或从中切出的代码在屏幕上留下一个甚至两个空白，如 TVI 912 和 Teleray 1061 那样，则应给出 `xmc` 以说明留下多少空格。

开始下划线和结束下划线的代码可以分别作为 `smul` 和 `rmul` 给出。如果终端有给当前字符加下划线并将光标右移一个空格的代码，例如 Microterm Mime，则可以将其作为 `uc` 给出。

进入各种高亮模式的其他能力包括 `blink`（闪烁）、`bold`（粗体或额外亮度）、`dim`（暗淡或半亮）、`invis`（空白或不可见文本）、`prot`（保护）、`rev`（反显）、`sgr0`（关闭*所有*属性模式）、`smacs`（进入替代字符集模式）和 `rmacs`（退出替代字符集模式）。单独打开这些模式中的任何一个可能会或可能不会关闭其他模式。

如果有序列设置任意模式组合，则应作为 `sgr`（设置属性）给出，接受 9 个参数。每个参数为零（0）或非零，对应属性是开还是关。9 个参数按顺序是：突出显示、下划线、反显、闪烁、暗淡、粗体、空白、保护、替代字符集。并非所有模式都需要由 `sgr` 支持，只需那些存在对应单独属性命令的模式。

例如，DEC vt220 支持大多数模式：

| tparm 参数 | 属性 | 转义序列 |
|---|---|---|
| none | none | \E[0m |
| p1 | standout | \E[0;1;7m |
| p2 | underline | \E[0;4m |
| p3 | reverse | \E[0;7m |
| p4 | blink | \E[0;5m |
| p5 | dim | 不可用 |
| p6 | bold | \E[0;1m |
| p7 | invis | \E[0;8m |
| p8 | protect | 未使用 |
| p9 | altcharset | ^O（关） ^N（开） |

我们通过关闭任何现有模式来开始每个转义序列，因为没有快速方法确定它们是否活动。突出显示设置为反显和粗体的组合。vt220 终端有保护模式，尽管它通常不在 sgr 中使用，因为它保护屏幕上的字符免受主机擦除。altcharset 模式也不同，它是 ^O 或 ^N，取决于它是关还是开。如果所有模式都打开，结果序列是 \E[0;1;4;5;7;8m^N。

某些序列对不同的模式是共同的。例如，当 p1 或 p3 为真时（即，如果突出显示或反显模式打开），会输出 ;7。

写出上述序列及其依赖关系得到

| 序列 | 何时输出 | terminfo 翻译 |
|---|---|---|
| \E[0 | 总是 | \E[0 |
| ;1 | 如果 p1 或 p6 | %?%p1%p6%\|%t;1%; |
| ;4 | 如果 p2 | %?%p2%\|%t;4%; |
| ;5 | 如果 p4 | %?%p4%\|%t;5%; |
| ;7 | 如果 p1 或 p3 | %?%p1%p3%\|%t;7%; |
| ;8 | 如果 p7 | %?%p7%\|%t;8%; |
| m | 总是 | m |
| ^N 或 ^O | 如果 p9 则 ^N，否则 ^O | %?%p9%t^N%e^O%; |

将所有这些放入 sgr 序列得到：

```
    sgr=\E[0%?%p1%p6%|%t;1%;%?%p2%t;4%;%?%p4%t;5%;
        %?%p1%p3%|%t;7%;%?%p7%t;8%;m%?%p9%t\016%e\017%;,
```

记住，如果指定 sgr，还必须指定 sgr0。此外，某些实现依赖在给出 sgr0 时也给出 sgr，但并非所有 terminfo 条目都必然有 sgr 字符串。许多 terminfo 条目源自没有 sgr 字符串的 termcap 条目。添加 sgr 字符串的唯一缺点是 termcap 还假设 sgr0 不会退出替代字符集模式。

具有“magic cookie”故障（`xmc`）的终端在收到模式设置序列时会放置特殊的“cookie”，这影响显示算法，而不是为每个字符添加额外位。某些终端，例如 HP 2621，在移到新行或寻址光标时会自动离开突出显示模式。使用突出显示模式的程序应在移动光标或发送换行之前退出突出显示模式，除非存在 `msgr` 能力，断言在突出显示模式下移动是安全的。

如果终端有闪烁屏幕以安静指示错误的方法（响铃替代），则可以将其作为 `flash` 给出；它不得移动光标。

如果光标不在底行时需要使其比正常更可见（例如，使不闪烁的下划线变为更易找到的块或闪烁下划线），则将此序列作为 `cvvis` 给出。如果有方法使光标完全不可见，则将其作为 `civis` 给出。应给出能力 `cnorm`，它撤销这两种模式的效果。

如果你的终端正确生成带下划线的字符（不需要特殊代码），即使它不叠印，则你应给出能力 `ul`。如果一个字符叠印另一个字符后两者都留在屏幕上，则指定能力 `os`。如果叠印可以用空白擦除，则应通过给出 `eo` 来表示。

### 小键盘和功能键

如果终端有小键盘，按键时发送代码，则可以给出此信息。注意，无法处理小键盘仅在本地工作的情况（例如，这适用于未移位的 HP 2621 键）。如果小键盘可以设置为发送或不发送，则将这些代码作为 `smkx` 和 `rmkx` 给出。否则假设小键盘始终发送。

左箭头、右箭头、上箭头、下箭头和起始键发送的代码可以分别作为 `kcub1`、`kcuf1`、`kcuu1`、`kcud1` 和 `khome` 给出。如果有 f0、f1、……、f10 等功能键，它们发送的代码可以作为 `kf0`、`kf1`、……、`kf10` 给出。如果这些键的标签不是默认的 f0 到 f10，则标签可以作为 `lf0`、`lf1`、……、`lf10` 给出。

可以给出某些其他特殊键发送的代码：

- `kll`（起始下移），
- `kbs`（退格），
- `ktbc`（清除所有制表位），
- `kctab`（清除此列的制表位），
- `kclr`（清除屏幕或擦除键），
- `kdch1`（删除字符），
- `kdl1`（删除行），
- `krmir`（退出插入模式），
- `kel`（清除到行尾），
- `ked`（清除到屏幕末尾），
- `kich1`（插入字符或进入插入模式），
- `kil1`（插入行），
- `knp`（下一页），
- `kpp`（上一页），
- `kind`（向前/向下滚动），
- `kri`（向后/向上滚动），
- `khts`（在此列设置制表位）。

此外，如果小键盘具有包含四个方向键的 3×3 阵列，则其他五个键可以作为 `ka1`、`ka3`、`kb2`、`kc1` 和 `kc3` 给出。当需要 3×3 方向板的效果时，这些键很有用。

编程功能键的字符串可以作为 `pfkey`、`pfloc` 和 `pfx` 给出。编程屏幕标签的字符串应指定为 `pln`。这些字符串中的每一个都接受两个参数：要编程的功能键编号（0 到 10）和用于编程的字符串。超出此范围的功能键编号可能会以依赖终端的方式编程未定义的键。这些能力的区别在于：`pfkey` 使按下给定键等同于用户键入给定字符串；`pfloc` 使字符串由终端在本地执行；`pfx` 使字符串传输到计算机。

能力 `nlab`、`lw` 和 `lh` 定义可编程屏幕标签的数量及其宽度和高度。如果有打开和关闭标签的命令，则分别在 `smln` 和 `rmln` 中给出。`smln` 通常在一个或多个 pln 序列之后输出，以确保更改可见。

### 制表符和初始化

少数能力仅用于管理制表位。

- 如果终端具有硬件制表符，则将前进到下一个制表位的字符序列指定为 `tab`（`ht`）string 能力的值（通常为 Control+I）。
- 将后退（向左移动）到前一个制表位的字符序列指定为 `back_tab`（`cbt`）string 能力的值。

按照惯例，如果终端模式配置为由主机而不是终端展开制表符，则应用不应使用 `tab`（`ht`）或 `back_tab`（`cbt`）能力，即使它们存在，因为用户可能没有正确设置制表位。

- 如果终端具有在终端通电时每 *n* 个字符单元设置的硬件制表位，则将 *n* 指定为 numeric 能力 `init_tabs`（`it`）的值。

`tset` 和 `tput init` 命令将 `init_tabs`（`it`）能力的存在解释为暗示终端负责制表位展开，以及将其制表位设置为其值的指令。如果终端具有可保存在非易失性存储器中的制表位，则其 *terminfo* 类型描述可以假设它们已正确设置。

其他能力包括

- `is1`、`is2` 和 `is3`，终端的初始化字符串，
- `iprog`，为初始化终端而要运行的程序的路径名，
- 以及 `if`，包含长初始化字符串的文件名。

这些字符串预期将终端设置为与 terminfo 描述其余部分一致的模式。它们通常由 `tput` 程序的 *init* 选项在用户每次登录时发送到终端。它们将按以下顺序打印：

- 运行程序  
    `iprog`
- 输出  
    `is1` 和 `is2`
- 使用以下方式设置边距  
    `mgc` 或 `smglp` 和 `smgrp` 或 `smgl` 和 `smgr`
- 使用以下方式设置制表位  
    `tbc` 和 `hts`
- 打印文件  
    `if`
- 最后输出  
    `is3`。

大多数初始化使用 `is2` 完成。可以通过将公共序列放在 `is2` 中，将特殊情况放在 `is1` 和 `is3` 中，在不重复字符串的情况下设置特殊终端模式。

一组从完全未知状态进行更彻底重置的序列可以作为 `rs1`、`rs2`、`rf` 和 `rs3` 给出，分别类似于 `is1`、`is2`、`if` 和 `is3`。这些字符串由 `tput` 的 *reset* 选项或 `reset` 程序（`tset` 的别名）输出，后者在终端进入卡死状态时使用。通常仅当命令在屏幕上产生恼人的影响并且登录时不需要时，才将命令放在 `rs1`、`rs2`、`rs3` 和 `rf` 中。例如，将 vt100 设置为 80 列模式的命令通常是 `is2` 的一部分，但它会导致恼人的屏幕故障，并且通常不需要，因为终端通常已经处于 80 列模式。

`reset` 程序以与 *init* 程序相同的顺序写入包括 `iprog` 等在内的字符串，使用 `rs1` 等而不是 `is1` 等。如果任何 `rs1`、`rs2`、`rs3` 或 `rf` 重置能力字符串缺失，则 `reset` 程序回退到相应的初始化能力字符串。

如果有设置和清除制表位的命令，则可以将它们作为 `tbc`（清除所有制表位）和 `hts`（在每行的当前列设置制表位）给出。如果需要比这更复杂的序列来设置制表位，则可以将序列放在 `is2` 或 `if` 中。

`tput reset` 命令使用与 `reset` 命令相同的功能字符串，尽管这两个程序（`tput` 和 `reset`）提供不同的命令行选项。

实际上，这些 terminfo 能力在制表位初始化中并不常用（尽管 `tabs` 程序需要它们）：

- 几乎所有硬件终端（至少那些支持制表位的终端）都将制表位初始化为每*八*列：

唯一的例外是 AT&T 2300 系列，它将制表位设置为每*五*列。

- 特别是，常用作现代终端模拟器模型的硬件终端的开发者提供了文档，证明*八*列是标准。
- 因此，终端初始化程序 `tput` 和 `tset` 仅在 `it`（`init_tabs`）能力设置为*八*以外的值时，才直接使用 `tbc`（`clear_all_tabs`）和 `hts`（`set_tab`）能力。

### 延迟和填充

许多较旧和较慢的终端不支持 XON/XOFF 或 DTR 握手，包括硬拷贝终端和一些非常古老的 CRT（例如，包括 DEC VT100）。这些可能需要在某些光标移动和屏幕更改后使用填充字符。

如果终端使用 xon/xoff 握手进行流控制（即，当其输入缓冲区接近满时，它会自动向主机发出 ^S），则设置 `xon`。此能力抑制填充的发出。你也可以为实际上没有速度限制的内存映射控制台设备设置它。仍应包含填充信息，以便例程可以就相对成本做出更好的决策，但不会传输实际的填充字符。

如果给出了 `pb`（填充波特率），则在低于 `pb` 值的波特率下抑制填充。如果条目没有填充波特率，则是否发出填充完全由 `xon` 控制。

如果终端需要空（零）字符以外的字符作为填充，则可以将其作为 `pad` 给出。仅使用 `pad` 字符串的第一个字符。

### 状态行

某些终端有额外的“状态行”，软件通常不使用（因此不计入终端的 `lines` 能力）。

最简单的情况是状态行可光标寻址，但不属于屏幕上的主滚动区域；Heathkit H19 具有这种状态行，初始化时设置了 23 行滚动区域的 24 行 VT100 也是如此。这种情况由 `hs` 能力指示。

某些带状态行的终端需要特殊序列来访问状态行。这些可以表示为带单个参数 `tsl` 的字符串，它将光标带到状态行上给定的零原点列。能力 `fsl` 必须返回到上次 `tsl` 之前的主屏幕光标位置。你可能需要将 `sc`（保存光标）和 `rc`（恢复光标）的字符串值嵌入 `tsl` 和 `fsl` 中以实现这一点。

通常假设状态行的宽度与终端宽度相同。如果情况并非如此，则可以使用 numeric 能力 `wsl` 指定。

擦除或空白状态行的命令可以指定为 `dsl`。

Boolean 能力 `eslok` 指定转义序列、制表符等在状态行中正常工作。

*ncurses* 实现尚未使用这些能力中的任何一个。在此记录它们，以防它们变得重要。

### 线条图形

许多终端具有可用于绘制表单的替代字符集。Terminfo 和 `curses` 内置支持 VT100 支持的大多数绘图字符，并添加了 AT&T 4410v1 的一些字符。此替代字符集可以由 `acsc` 能力指定。

| ACS 名称 | 值 | 符号 | ASCII 回退 | 字形名称 |
|---|---|---|---|---|
| `ACS_RARROW` | 0x2b | + | `>` | 指向右的箭头 |
| `ACS_LARROW` | 0x2c | , | `<` | 指向左的箭头 |
| `ACS_UARROW` | 0x2d | - | `^` | 指向上的箭头 |
| `ACS_DARROW` | 0x2e | . | `v` | 指向下的箭头 |
| `ACS_BLOCK` | 0x30 | 0 | `#` | 实心方块 |
| `ACS_DIAMOND` | 0x60 | ` | `+` | 菱形 |
| `ACS_CKBOARD` | 0x61 | a | `:` | 棋盘（点画） |
| `ACS_DEGREE` | 0x66 | f | `\` | 度数符号 |
| `ACS_PLMINUS` | 0x67 | g | `#` | 正/负 |
| `ACS_BOARD` | 0x68 | h | `#` | 方格板 |
| `ACS_LANTERN` | 0x69 | i | `#` | 灯笼符号 |
| `ACS_LRCORNER` | 0x6a | j | `+` | 右下角 |
| `ACS_URCORNER` | 0x6b | k | `+` | 右上角 |
| `ACS_ULCORNER` | 0x6c | l | `+` | 左上角 |
| `ACS_LLCORNER` | 0x6d | m | `+` | 左下角 |
| `ACS_PLUS` | 0x6e | n | `+` | 大加号或交叉 |
| `ACS_S1` | 0x6f | o | `~` | 扫描线 1 |
| `ACS_S3` | 0x70 | p | `-` | 扫描线 3 |
| `ACS_HLINE` | 0x71 | q | `-` | 水平线 |
| `ACS_S7` | 0x72 | r | `-` | 扫描线 7 |
| `ACS_S9` | 0x73 | s | `_` | 扫描线 9 |
| `ACS_LTEE` | 0x74 | t | `+` | 向右的 T 形 |
| `ACS_RTEE` | 0x75 | u | `+` | 向左的 T 形 |
| `ACS_BTEE` | 0x76 | v | `+` | 向上的 T 形 |
| `ACS_TTEE` | 0x77 | w | `+` | 向下的 T 形 |
| `ACS_VLINE` | 0x78 | x | `\|` | 垂直线 |
| `ACS_LEQUAL` | 0x79 | y | `<` | 小于或等于 |
| `ACS_GEQUAL` | 0x7a | z | `>` | 大于或等于 |
| `ACS_PI` | 0x7b | { | `*` | 希腊字母 pi |
| `ACS_NEQUAL` | 0x7c | \| | `!` | 不等于 |
| `ACS_STERLING` | 0x7d | } | `f` | 英镑符号 |
| `ACS_BULLET` | 0x7e | ~ | `o` | 项目符号 |

关于表格本身有几点说明：

- X/Open Curses 错误地声明 *lantern* 的映射为大写“I”，尽管 Unix 实现使用小写“i”映射。
- DEC VT100 使用替代字符集功能实现图形，临时切换*模式*并发送 0x60（96）到 0x7e（126）范围内的字符（表中的 **acsc 值**列）。
- AT&T 终端添加了该范围之外的图形字符。

该范围内的某些字符与 VT100 不匹配；据推测它们是在 AT&T 终端中使用的：*方格板*替换 VT100 *换行*符号，而*灯笼符号*替换 VT100 *垂直制表*符号。控制字符的其他 VT100 符号（*水平制表*、*回车*和*换行*）在 curses 中未（重新）使用。

定义新设备图形集的最佳方法是将一列添加到本表的副本中，用于你的终端，给出在 `smacs`/`rmacs` 切换之间发出时将渲染为相应图形的字符。然后从右到左按顺序读取 VT100/你的终端字符对；这些成为 ACSC 字符串。

### 颜色处理

*curses* 库函数 `init_pair` 和 `init_color` 操作本节讨论的*颜色对*和*颜色*（颜色值或索引，例如“1=红”）（有关这些及相关函数的详细信息，见 "curs_color(3X)"）。

大多数彩色终端在颜色管理方法上要么是“类 Tektronix”，要么是“类 HP”。

- *类 Tektronix* 终端定义一组 *n* 种颜色（其中 *n* 通常为 8），可以独立更改字符单元前景和背景颜色，将它们混合成 *n*×*n* 个颜色对。ANSI 标准终端是类 Tektronix 的。
- 在*类 HP*终端上，用户必须分别设置每个颜色对；前景和背景不能独立更改。最多可以从 2×*m* 种不同颜色配置 *m* 个颜色对。

一些基本颜色管理能力与颜色编码方法无关。Numeric 能力 `max_colors`（`colors`）和 `max_pairs`（`pairs`）指定设备可以同时显示的最大颜色数和颜色对数。`orig_pair`（`op`）（“原始对”）string 能力将前景和背景颜色重置为终端的默认值。`orig_colors`（`oc`）（“原始颜色”）string 能力将所有颜色或颜色对重置为终端的默认值。某些终端类型（包括许多 PC 终端模拟器）使用当前背景色而不是通电默认背景擦除屏幕区域；这些应声明 Boolean 能力 `back_color_erase`（`bce`）。

虽然 *curses* 库使用*颜色对*（反映某些设备无法独立设置前景和背景颜色），但有单独的能力用于设置这些特性：

- 要在 Tektronix 型终端上更改当前前景或背景颜色，请使用 `setaf`（设置 ANSI 前景）和 `setab`（设置 ANSI 背景）或 `setf`（设置前景）和 `setb`（设置背景）。这些接受一个参数，即颜色编号。SVr4 文档仅描述 `setaf`/`setab`；XPG4 草案说：“如果终端支持 ANSI 转义序列来设置背景和前景，则它们应分别编码为 `setaf` 和 `setab`。”
- 如果终端支持其他转义序列来设置背景和前景，则它们应分别编码为 `setf` 和 `setb`。`vidputs` 和 "refresh(3X)" 函数如果定义了 `setaf` 和 `setab` 能力则使用它们。

`setaf`/`setab` 和 `setf`/`setb` 能力各接受一个 numeric 参数。`setaf`/`setab` 的参数值 0-7 可移植定义如下（中间列是 `curses` 或 *ncurses* 库头文件中可用的符号 #define）。终端硬件可以随意映射这些，但 RGB 值指示颜色空间中的正常位置。

| 颜色 | #define | 值 | RGB |
|---|---|---|---|
| 黑 | `COLOR_BLACK` | 0 | 0, 0, 0 |
| 红 | `COLOR_RED` | 1 | max, 0, 0 |
| 绿 | `COLOR_GREEN` | 2 | 0, max, 0 |
| 黄 | `COLOR_YELLOW` | 3 | max, max, 0 |
| 蓝 | `COLOR_BLUE` | 4 | 0, 0, max |
| 品红 | `COLOR_MAGENTA` | 5 | max, 0, max |
| 青 | `COLOR_CYAN` | 6 | 0, max, max |
| 白 | `COLOR_WHITE` | 7 | max, max, max |

`setf`/`setb` 的参数值历史上对应不同的映射，即，

| 颜色 | #define | 值 | RGB |
|---|---|---|---|
| 黑 | `COLOR_BLACK` | 0 | 0, 0, 0 |
| 蓝 | `COLOR_BLUE` | 1 | 0, 0, max |
| 绿 | `COLOR_GREEN` | 2 | 0, max, 0 |
| 青 | `COLOR_CYAN` | 3 | 0, max, max |
| 红 | `COLOR_RED` | 4 | max, 0, 0 |
| 品红 | `COLOR_MAGENTA` | 5 | max, 0, max |
| 黄 | `COLOR_YELLOW` | 6 | max, max, 0 |
| 白 | `COLOR_WHITE` | 7 | max, max, max |

重要的是不要混淆两组颜色能力；否则显示中红色/蓝色将互换。

在类 HP 终端上，使用带颜色对编号参数的 `scp` 来设置哪个颜色对是当前颜色对。

某些终端允许修改*颜色值*：

- 在类 Tektronix 终端上，能力 `ccc` 可能存在，表示颜色可以修改。如果是这样，`initc` 能力将接受一个颜色编号（0 到 `colors` - 1）和另外三个描述颜色的参数。这三个参数默认解释为 RGB（红、绿、蓝）值。如果存在 Boolean 能力 `hls`，则它们改为 HLS（色调、亮度、饱和度）索引。范围取决于终端。
- 在类 HP 终端上，`initp` 可能提供更改颜色对值的能力。它将接受七个参数；一个颜色对编号（0 到 `max_pairs` - 1），以及两个三元组，首先描述背景，然后描述前景颜色。这些参数必须是（红、绿、蓝）或（色调、亮度、饱和度），取决于 `hls`。

在某些彩色终端上，颜色与高亮冲突。你可以使用 `ncv` 能力注册这些冲突。这是一个位掩码，表示启用颜色时不使用的属性。与 `curses` 理解的属性的对应关系如下：

| 属性 | 位 | 十进制 | 由...设置 |
|---|---|---|---|
| `A_STANDOUT` | 0 | 1 | `sgr` |
| `A_UNDERLINE` | 1 | 2 | `sgr` |
| `A_REVERSE` | 2 | 4 | `sgr` |
| `A_BLINK` | 3 | 8 | `sgr` |
| `A_DIM` | 4 | 16 | `sgr` |
| `A_BOLD` | 5 | 32 | `sgr` |
| `A_INVIS` | 6 | 64 | `sgr` |
| `A_PROTECT` | 7 | 128 | `sgr` |
| `A_ALTCHARSET` | 8 | 256 | `sgr` |
| `A_HORIZONTAL` | 9 | 512 | `sgr1` |
| `A_LEFT` | 10 | 1024 | `sgr1` |
| `A_LOW` | 11 | 2048 | `sgr1` |
| `A_RIGHT` | 12 | 4096 | `sgr1` |
| `A_TOP` | 13 | 8192 | `sgr1` |
| `A_VERTICAL` | 14 | 16384 | `sgr1` |
| `A_ITALIC` | 15 | 32768 | `sitm` |

例如，在许多 IBM PC 控制台上，下划线属性与前景蓝色冲突，在颜色模式下不可用。这些应具有 `ncv` 能力值 2。

SVr4 curses 对 `ncv` 不做任何处理，*ncurses* 识别它并优化输出以支持颜色。

### 杂项

如果终端需要空（零）字符以外的字符作为填充，则可以将其作为 pad 给出。仅使用 pad 字符串的第一个字符。如果终端没有填充字符，请指定 npc。注意 *ncurses* 实现了 termcap 兼容的 `PC` 变量；尽管应用可以将此值设置为空以外的值，*ncurses* 将首先测试 `npc`，如果终端没有填充字符则使用 napms。

如果终端可以向上或向下移动半行，则可以用 `hu`（上半行）和 `hd`（下半行）表示。这主要用于硬拷贝终端上的上标和下标。如果硬拷贝终端可以弹出到下一页（换页），则将其作为 `ff` 给出（通常为 control/L）。

如果有命令将给定字符重复给定次数（以节省传输大量相同字符的时间），则可以用参数化字符串 `rep` 表示。第一个参数是要重复的字符，第二个是重复次数。因此，tparm(repeat_char, 'x', 10) 与“xxxxxxxxxx”相同。

如果终端有可设置的命令字符，例如 TEKTRONIX 4025，则可以用 `cmdch` 表示。选择一个原型命令字符，它在所有能力中使用。此字符在 `cmdch` 能力中给出以标识它。某些 Unix 系统支持以下约定：在环境中搜索 `CC` 变量，如果找到，则所有出现的原型字符都替换为环境变量中的字符。

不代表特定已知终端类型的终端描述，例如 *switch*、*dialup*、*patch* 和 *network*，应包含 `gn`（通用）能力，以便程序可以抱怨它们不知道如何与终端通信。（此能力不适用于转义序列已知的*虚拟*终端描述。）

如果终端有充当 shift 键的“meta 键”，设置传输的任何字符的第 8 位，则可以用 `km` 表示这一事实。否则，软件将假设第 8 位是奇偶校验，通常会被清除。如果存在打开和关闭此“meta 模式”的字符串，则可以将它们作为 `smm` 和 `rmm` 给出。

如果终端的内存行数多于一次在屏幕上显示的行数，则可以用 `lm` 表示内存行数。`lm`#0 值表示行数不固定，但内存仍多于屏幕上显示的行数。

如果终端是 Unix 虚拟终端协议支持的终端之一，则终端编号可以作为 `vt` 给出。

控制连接到终端的辅助打印机的介质复制字符串可以给出为 `mc0`：打印屏幕内容，`mc4`：关闭打印机，`mc5`：打开打印机。当打印机打开时，发送到终端的所有文本都将发送到打印机。打印机打开时文本是否也显示在终端屏幕上未定义。变体 `mc5p` 接受一个参数，并让打印机保持开启指定数量的字符，然后关闭打印机。参数不应超过 255。在 `mc5p` 生效期间，所有文本（包括 `mc4`）都透明地传递给打印机。

### 故障和脑损伤

不允许显示“~”字符的 Hazeltine 终端应指示 `hz`。

在 `am` 环绕后立即忽略换行的终端，例如 Concept 和 vt100，应指示 `xenl`。

如果 `el` 需要用来摆脱突出显示（而不是仅仅在其上写入正常文本），则应给出 `xhp`。

Teleray 终端，其制表符将所有移过的字符变为空白，应指示 `xt`（破坏性制表符）。注意：指示此的变量现在是“dest_tabs_magic_smso”；在旧版本中，它是 teleray_glitch。此故障也被认为意味着不可能将光标定位在“magic cookie”上，要擦除突出显示模式，反而需要使用删除和插入行。*ncurses* 实现忽略此故障。

Beehive Superbee 无法正确传输转义或 control/C 字符，具有 `xsb`，指示 f1 键用于转义，f2 用于 control/C。（只有某些 Superbee 有这个问题，取决于 ROM。）注意在较旧的 terminfo 版本中，此能力称为“beehive_glitch”；现在称为“no_esc_ctl_c”。

其他特定的终端问题可以通过添加更多形式为 `x`*x* 的能力来纠正。

### 长条目的陷阱

长的 terminfo 条目不太可能成为问题；迄今为止，没有任何条目接近 terminfo 的 4096 字节字符串表最大值。不幸的是，termcap 转换受到更严格的限制（1023 字节），因此长 terminfo 条目的 termcap 转换可能导致问题。

4.3BSD 和旧版本 `tgetent` 的手册页指示用户为 termcap 条目分配 1024 字节缓冲区。条目由 termcap 库以空字符结尾，因此 termcap 条目的最大安全长度为 1k-1（1023）字节。取决于应用和使用的 termcap 库做什么，以及 `tgetent` 搜索的终端类型在 termcap 文件中的位置，可能会发生几种坏事：

- 一些 termcap 库打印警告消息，
- 一些在发现条目长于 1023 字节时退出，
- 一些既不退出也不警告，不做任何有用的事，以及
- 一些只是将条目截断为 1023 字节。

一些应用程序为 termcap 条目分配超过推荐的 1K；其他则不。

每个 termcap 条目都有两个重要的关联大小：在“tc”展开之前和之后。“tc”是将另一个 termcap 条目附加到当前条目末尾以添加其能力的能力。如果 termcap 条目不使用“tc”能力，那么两个长度当然相同。

“tc 展开前”长度是最重要的，因为它不仅影响该特定终端的用户。这是条目在 /etc/termcap 中存在时的长度，减去反斜杠-换行对，`tgetent` 在读取时将其剥离。一些 termcap 库也剥离最后的换行（GNU termcap 不这样做）。现在假设：

- 展开前的 termcap 条目长于 1023 字节，
- 并且应用只分配了 1k 缓冲区，
- 并且 termcap 库（如 BSD/OS 1.1 和 GNU 中的库）将整个条目读入缓冲区，无论其长度如何，以查看它是否是它想要的条目，
- 并且 `tgetent` 正在搜索的终端类型要么是长条目，要么在 termcap 文件中出现在长条目之后，要么根本不出现（因此 `tgetent` 必须搜索整个 termcap 文件）。

那么 `tgetent` 将覆盖内存，可能是其栈，并可能导致程序核心转储。像 telnet 这样的程序特别容易受到攻击；现代 telnet 会自动传递终端类型等值。对于像 SunOS 4.1.3 和 Ultrix 4.4 那样在读取过长的 termcap 条目时打印警告消息的 termcap 库，结果几乎同样不理想。如果 termcap 库截断长条目，如 OSF/1 3.0，它在这里不会死亡，但会为终端返回错误的数据。

“tc 展开后”长度将产生与上述类似的影响，但只对实际将 *TERM* 设置为该终端类型的人，因为 `tgetent` 在找到它正在寻找的终端类型后才进行“tc”展开，而不是在搜索期间。

总之，长于 1023 字节的 termcap 条目在各种 termcap 库和应用的组合上可能导致核心转储、警告或错误操作。如果即使在“tc”展开之前也太长，那么即使对于一些其他终端类型的用户和 *TERM* 变量没有 termcap 条目的用户，也会产生这种影响。

在 -C（转换为 termcap）模式下，*ncurses* 的 "tic(1M)" 实现在 termcap 转换的 tc 前长度过长时发出警告消息。-c（检查）选项还检查解析后（tc 展开后）的长度。

## FILES

- `/usr/share/terminfo`  
    编译后的终端描述数据库目录

## EXTENSIONS

旧实现不支持在 *$HOME/.terminfo* 和 *TERMINFO_DIRS* 中搜索终端描述。

一些 SVr4 `curses` 实现以及 SVr4 之前的所有实现不解释参数字符串中的 %A 和 %O 操作符。

SVr4/XPG4 未指定 `msgr` 是否允许在替代字符集模式下移动（此类模式可能除其他外将 CR 和 NL 映射为不触发本地移动的字符）。*ncurses* 实现在 `ALTCHARSET` 模式下忽略 `msgr`。这增加了 XPG4 实现做出相反解释时可能需要为 *ncurses* 制作的 terminfo 条目关闭 `msgr` 的可能性。

*ncurses* 库以略微非标准的方式处理插入字符和插入字符模式，以获得更好的更新效率。参见上面的 **插入/删除字符** 小节。

`set_clock` 和 `display_clock` 的参数替换在 SVr4 或 X/Open Curses 中未记录。它们是从 AT&T 505 终端的文档中推断出来的。

小心分配 `kmous` 能力。*ncurses* 库希望将其解释为 `KEY_MOUSE`，供终端和 xterm 等能在键盘输入流中返回鼠标跟踪信息的模拟器使用。

X/Open Curses 未提及斜体。可移植应用必须假设 numeric 能力是带符号的 16 位值。这包括 *no_color_video*（`ncv`）能力。与 `ncv` 一起用于斜体的 32768 掩码值可能与缺失或取消的 `ncv` 混淆。如果斜体应与颜色一起工作，则必须指定 `ncv` 值，即使它为零。

*terminfo* 和 *curses* 的不同商业移植支持 X/Open Curses 的不同子集以及（在某些情况下）不同的扩展。以下是截至 1995 年 10 月的准确摘要，此后商业 Unix 市场收缩并失去多样性。

- SVr4、Solaris 和 *ncurses* 支持所有 SVr4 能力。
- IRIX 支持 SVr4 集，并添加了一个未记录的扩展 string 能力（`set_pglen`）。
- SVr1 和 Ultrix 支持 *terminfo* 能力的受限子集。Boolean 以 `xon_xoff` 结尾；numeric 以 `width_status_line` 结尾；string 以 `prtr_non` 结尾。
- HP/UX 支持 SVr1 子集，加上 SVr[234] numeric 能力 `num_labels`、`label_height`、`label_width`，加上功能键 11 到 63，加上 `plab_norm`、`label_on` 和 `label_off`，加上若干不兼容的字符串表扩展。
- AIX 支持 SVr1 子集，加上功能键 11 到 63，加上若干不兼容的字符串表扩展。
- OSF/1 同时支持 SVr4 集和 AIX 扩展。

## PORTABILITY

不要指望编译后的（二进制）*terminfo* 条目在商业 Unix 系统之间可移植。至少两个 *terminfo* 实现（HP-UX 和 AIX 的）在 SVr1 之后偏离了其他 System V Unix，向字符串表添加了扩展能力，这些能力（在二进制格式中）与随后的 System V 和 X/Open Curses 扩展冲突。

## AUTHORS

Zeyd M. Ben-Halim、Eric S. Raymond、Thomas E. Dickey。基于 Pavel Curtis 的 *pcurses*。

## SEE ALSO

"infocmp(1M)"、"tabs(1)"、"tic(1M)"、"curses(3X)"、"curs_color(3X)"、"curs_terminfo(3X)"、"curs_variables(3X)"、"printf(3)"、"term_variables(3X)"、"term(5)"、"user_caps(5)"