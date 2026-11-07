# 字体

1. 在用户目录下创建用户级字体数据目录
    ```sh
    mkdir -p ~/.local/share/fonts
    ```
    
2. 复制字体文件到目录
3. 刷新字体缓存
    ```sh
    fc-cache -fv
    ```

4. 查看字体是否被正确加载
5. 在用户目录下创建用户级字体配置文件

    ```sh
    mkdir -p ~/.config/fontconfig
    touch .config/fontconfig/fonts.conf
    ```

6. 设置新字体为通用等宽字体族 `monospace` 的优先项
    ```xml
    <?xml version="1.0"?>
    <!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
    <fontconfig>
        <alias>
            <family>monospace</family>
            <prefer><family>JetBrains Maple Mono</family></prefer>
        </alias>
    </fontconfig>
    ```
## fonts-conf(5)

### 文件 

`fonts.conf` 包含 fontconfig 库的配置信息，包括用于查找字体信息的目录，以及在尝试匹配可用字体之前编辑程序指定字体模式的说明。它采用 XML 格式。

`/etc/fonts/fonts.conf`

用于配置系统字体访问

例如
```xml
...
<!-- Font directory list -->

    <dir>/usr/share/fonts</dir>
    <dir>/usr/local/share/fonts</dir>
    <dir prefix="xdg">fonts</dir>
    <!-- the following element will be removed in the future -->
    <dir>~/.fonts</dir>
...
```

### 配置文件格式

fontconfig 的配置文件以 XML 格式存储

每个配置文件应包含以下结构：

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
...
</fontconfig>
```

#### `<dir prefix="default" salt="">`

```xml
<dir prefix="default" salt="">
```

此元素包含一个目录名，该目录将被扫描以查找字体文件，并加入可用字体集合。

如果 `prefix` 设置为 `"default"` 或 `"cwd"`，当前工作目录将作为路径前缀添加到该值之前。如果 `prefix` 设置为 `"xdg"`，`XDG_DATA_HOME` 环境变量中的值将作为路径前缀添加。更多细节请参见 XDG Base Directory Specification。如果 `prefix` 设置为 `"relative"`，当前文件的路径将添加到该值之前。

#### `<alias>`

```xml
<alias>
```

`Alias` 元素为将一种字体族替换为另一种字体族所需的一组常见匹配操作提供了简写。它们包含一个 `<family>` 元素，后跟可选的 `<prefer>`、`<accept>` 和 `<default>` 元素。匹配 `<family>` 元素的字体会被编辑为：将 `<prefer>` 的字体族列表前置到匹配的 `<family>` 之前，将 `<accept>` 可接受的字体族追加到匹配的 `<family>` 之后，并将 `<default>` 字体族追加到字体族列表末尾。


#### `<family>`

```xml
<family>
```

保存单个字体族名称。

#### `<prefer>`, `<accept>`, `<default>`

```xml
<prefer>
<accept>
<default>
```

这些元素包含供 `<alias>` 元素使用的 `<family>` 元素列表。

## XDG 基础目录规范

### 3 环境变量

`$XDG_DATA_HOME` 定义用户特定数据文件应相对于哪个基础目录存储。如果 `$XDG_DATA_HOME` 未设置或为空，则应使用默认值 `$HOME/.local/share`。

> 即，全局配置文件中的数据项 `<dir prefix="xdg">fonts</dir>` 最终为 `$HOME/.local/share/fonts`。此处即用户字体数据目录


`$XDG_CONFIG_HOME` 定义用户特定的配置文件应相对于哪个基础目录存储。如果 `$XDG_CONFIG_HOME` 未设置或为空，则应使用默认值 `$HOME/.config`。
> 即，全局配置文件中的配置项 `<cachedir prefix="xdg">fontconfig</cachedir>` 最终为 `$HOME/.config/fontconfig/fonts.conf`。此处即用户字体配置

## fc-cache — 构建字体信息缓存文件

`fc-cache` 扫描系统上的字体目录，并为使用 fontconfig 处理字体的应用程序构建字体信息缓存文件。

```sh
# 目录中新增字体后刷新，查看进度信息
fc-cache -fv
```

## fc-list — 列出可用字体

`fc-list` 列出系统中可供使用 fontconfig 的应用程序使用的字体和样式。如果指定了任何元素，则只打印这些元素。否则，除非请求详细输出，否则打印字体族和样式。

```sh
# 查看字体是否被正确应用，虽然 fc-list 拥有其匹配功能，但简单使用 grep
fc-list | grep 字体名
```