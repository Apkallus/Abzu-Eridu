https://httpd.apache.org/docs/2.4/sections.html

# Configuration Sections —— 配置段

配置文件中的指令可能应用于整个服务器，也可能被限制为仅应用于特定目录、文件、主机或 URL。本文档描述如何使用配置段容器或 `.htaccess` 文件来更改其他配置指令的作用域。

## 配置段容器的类型

容器有两种基本类型。大多数容器会针对每个请求进行求值。所包含的指令仅应用于匹配这些容器的请求。另一方面，`<IfDefine>`、`<IfModule>` 和 `<IfVersion>` 容器仅在服务器启动和重启时求值。如果它们的条件在启动时为真，则所包含的指令将应用于所有请求。如果条件不为真，则所包含的指令将被忽略。

`<IfDefine>` 指令括起仅当在 `httpd` 命令行上定义了适当参数时才会应用的指令。例如，使用以下配置，仅当使用 `httpd -DClosedForNow` 启动服务器时，所有请求才会被重定向到另一个站点：

```apache
<IfDefine ClosedForNow>
    Redirect "/" "http://otherserver.example.com/"
</IfDefine>
```

`<IfModule>` 指令非常相似，不同之处在于它括起仅当服务器中有特定模块可用时才会应用的指令。该模块必须在服务器中静态编译，或者必须动态编译并且其 `LoadModule` 行必须位于配置文件中更早的位置。仅当你需要配置文件在是否安装某些模块的情况下都能工作时，才应使用此指令。不应用于括起你希望始终工作的指令，因为它可能会抑制有关缺少模块的有用错误消息。

在以下示例中，`MimeMagicFile` 指令仅在 `mod_mime_magic` 可用时才会应用。

```apache
<IfModule mod_mime_magic.c>
    MimeMagicFile "conf/magic"
</IfModule>
```

`<IfVersion>` 指令与 `<IfDefine>` 和 `<IfModule>` 非常相似，不同之处在于它括起仅当正在执行特定版本的服务器时才会应用的指令。此模块专为必须处理不同 httpd 版本和不同配置的测试套件和大型网络而设计。

```apache
<IfVersion >= 2.4>
    # 这仅在版本大于或等于 2.4.0 时发生。
</IfVersion>
```

`<IfDefine>`、`<IfModule>` 和 `<IfVersion>` 可以通过在其测试前加上 "!" 来应用否定条件。此外，这些段可以嵌套以实现更复杂的限制。

## 文件系统、Web 空间和布尔表达式

最常用的配置段容器是更改文件系统或 Web 空间中特定位置配置的容器。两者之间的区别：

- 文件系统是操作系统所看到的磁盘视图。例如，在默认安装中，Apache httpd 
  - 在 Unix 文件系统中位于 `/usr/local/apache2`
  - 在 Windows 文件系统中位于 `"c:/Program Files/Apache Group/Apache2"`。（请注意，即使在 Windows 中，Apache httpd 配置文件中也应始终使用正斜杠作为路径分隔符。）
- Web 空间是 Web 服务器交付并由客户端看到的站点视图。因此，Web 空间中的路径 `/dir/` 对应于 Unix 上默认 Apache httpd 安装的文件系统中的路径 `/usr/local/apache2/htdocs/dir/`。Web 空间无需直接映射到文件系统，因为网页可以从数据库或其他位置动态生成。

### 文件系统容器

`<Directory>` 和 `<Files>` 指令及其正则表达式对应项将指令应用于文件系统的各部分。包含在 `<Directory>` 段中的指令应用于指定的文件系统目录及该目录的所有子目录（以及这些目录中的文件）。使用 .htaccess 文件也可以获得相同的效果。例如，在以下配置中，将为 `/var/web/dir1` 目录及所有子目录启用目录索引。

```apache
<Directory "/var/web/dir1">
    Options +Indexes
</Directory>
```

包含在 `<Files>` 段中的指令应用于具有指定名称的任何文件，无论它位于哪个目录中。因此，例如，以下配置指令在放置于配置文件的主段中时，将拒绝访问任何名为 `private.html` 的文件，无论它在何处被找到。

```apache
<Files "private.html">
    Require all denied
</Files>
```

要针对在文件系统特定部分中找到的文件，可以组合使用 `<Files>` 和 `<Directory>` 段。例如，以下配置将拒绝访问 `/var/web/dir1/private.html`、`/var/web/dir1/subdir2/private.html`、`/var/web/dir1/subdir3/private.html`，以及在 `/var/web/dir1/` 目录下找到的任何其他 `private.html` 实例。

```apache
<Directory "/var/web/dir1">
    <Files "private.html">
        Require all denied
    </Files>
</Directory>
```

### Web 空间容器

另一方面，`<Location>` 指令及其正则表达式对应项更改 Web 空间中内容的配置。例如，以下配置阻止访问任何以 /private 开头的 URL 路径。特别是，它将应用于对 `http://yoursite.example.com/private`、`http://yoursite.example.com/private123` 和 `http://yoursite.example.com/private/dir/file.html` 的请求，以及任何其他以 `/private` 字符串开头的请求。

```apache
<LocationMatch "^/private">
    Require all denied
</LocationMatch>
```

`<Location>` 指令无需与文件系统有任何关系。例如，以下示例展示了如何将特定 URL 映射到由 `mod_status` 提供的内部处理器。文件系统上无需存在名为 `server-status` 的文件。

```apache
# 将 URL 映射到内置处理器：
<Location "/server-status">
    SetHandler server-status
</Location>

# 将 URL 路径映射到反向代理后端：
<Location "/app">
    ProxyPass "http://backend.example.com/"
    ProxyPassReverse "http://backend.example.com/"
</Location>

# 拒绝访问 URL 路径，无论它由什么提供服务：
<Location "/private">
    Require all denied
</Location>
```

由于 `<Location>` 操作的是 URL 而不是文件系统路径，因此它是代理配置和模块提供端点的适当容器。

### 重叠的 Web 空间

为了拥有两个重叠的 URL，必须考虑某些段或指令的求值顺序。对于 `<Location>`，这将是：

```apache
<Location "/foo">
</Location>
<Location "/foo/bar">
</Location>
```

另一方面，`<Alias>` 的映射顺序相反：

```apache
Alias "/foo/bar" "/srv/www/uncommon/bar"
Alias "/foo"     "/srv/www/common/foo"
```

`ProxyPass` 指令也是如此：

```apache
ProxyPass "/special-area" "http://special.example.com" smax=5 max=10
ProxyPass "/" "balancer://mycluster/" stickysession=JSESSIONID|jsessionid nofailover=On
```

### 通配符和正则表达式

`<Directory>`、`<Files>` 和 `<Location>` 指令都可以使用 C 标准库中 `fnmatch` 那样的 shell 风格通配符。字符 `*` 匹配任何字符序列，`?` 匹配任何单个字符，`[*seq*]` 匹配 *seq* 中的任何字符。`/` 字符不会被任何通配符匹配；必须显式指定。

如果需要更灵活的匹配，每个容器都有正则表达式（regex）对应项 `<DirectoryMatch>`、`<FilesMatch>` 和 `<LocationMatch>`，允许在选择匹配时使用 Perl 兼容的正则表达式。但请参阅下面关于配置合并的部分，以了解使用正则表达式段将如何更改指令的应用方式。

一个更改所有用户目录配置的非正则通配符段可以如下所示：

```apache
<Directory "/home/*/public_html">
    Options Indexes
</Directory>
```

使用正则表达式段，我们可以一次拒绝访问多种类型的图像文件：

```apache
<FilesMatch "\.(?i:gif|jpe?g|png)$">
    Require all denied
</FilesMatch>
```

包含**命名组和反向引用**的正则表达式会以相应的大写名称添加到环境中。这允许在表达式和 `mod_rewrite` 等模块中引用文件路径和 URL 的元素。

```apache
<DirectoryMatch "^/var/www/combined/(?<SITENAME>[^/]+)">
    Require ldap-group "cn=%{env:MATCH_SITENAME},ou=combined,o=Example"
</DirectoryMatch>
```

### 布尔表达式

`<If>` 指令根据可由布尔表达式表示的条件更改配置。例如，以下配置在 HTTP Referer 头不以 "http://www.example.com/" 开头时拒绝访问。

```apache
<If "!(%{HTTP_REFERER} -strmatch 'http://www.example.com/*')">
    Require all denied
</If>
```

### 何时使用什么

在文件系统容器和 Web 空间容器之间进行选择实际上相当容易。
- 当将指令应用于驻留在文件系统中的对象时，始终使用 `<Directory>` 或 `<Files>`。
- 当将指令应用于不驻留在文件系统中的对象（例如从数据库生成的网页）时，使用 `<Location>`。

重要的是，在尝试限制对文件系统中对象的访问时，**绝不要**使用 `<Location>`。这是因为许多不同的 Web 空间位置（URL）可能映射到同一个文件系统位置，从而使你的限制可以被绕过。例如，考虑以下配置：

```apache
<Location "/dir/">
    Require all denied
</Location>
```

如果请求是 `http://yoursite.example.com/dir/`，这工作正常。但如果你在不区分大小写的文件系统上呢？那么你的限制可以通过请求 `http://yoursite.example.com/DIR/` 轻松绕过。相比之下，`<Directory>` 指令将应用于从该位置提供的任何内容，无论它如何被调用。（一个例外是文件系统链接。同一个目录可以使用符号链接放置在文件系统的多个部分中。`<Directory>` 指令将跟随符号链接而不重置路径名。因此，为了最高级别的安全性，应使用适当的 `Options` 指令禁用符号链接。）

如果你也许认为这一切都不适用于你，因为你使用的是区分大小写的文件系统，请记住，还有许多其他方式可以将多个 Web 空间位置映射到同一个文件系统位置。因此，只要可以，你应始终使用文件系统容器。然而，此规则有一个例外。将配置限制放在 `<Location "/">` 段中是完全可以安全，因为此段将应用于所有请求，无论具体 URL 是什么。

### 段的嵌套

某些段类型可以嵌套在其他段类型内部。一方面，`<Files>` 可以在 `<Directory>` 内使用。另一方面，`<If>` 可以在 `<Directory>`、`<Location>` 和 `<Files>` 段内使用（但不能在另一个 `<If>` 内）。命名段的正则表达式对应项行为相同。

嵌套段在同一类型的非嵌套段之后合并。

## 虚拟主机

`<VirtualHost>` 容器括起应用于特定主机的指令。当从同一台机器为多个主机提供服务且每个主机具有不同配置时，这很有用。有关更多信息，请参阅虚拟主机文档。

## 代理

`<Proxy>` 和 `<ProxyMatch>` 容器仅将所包含的配置指令应用于通过 `mod_proxy` 的代理服务器访问的、匹配指定 URL 的站点。例如，以下配置将仅允许一部分客户端使用代理服务器访问 `www.example.com` 网站：

```apache
<Proxy "http://www.example.com/*">
    Require host yournetwork.example.com
</Proxy>
```

## 允许使用哪些指令？

要了解哪些指令允许在哪些类型的配置段中使用，请检查该指令的上下文。在 `<Directory>` 段中允许的所有内容在语法上也允许在 `<DirectoryMatch>`、`<Files>`、`<FilesMatch>`、`<Location>`、`<LocationMatch>`、`<Proxy>` 和 `<ProxyMatch>` 段中。但是，有一些例外：

- `AllowOverride` 指令仅在 `<Directory>` 段中工作。
- `FollowSymLinks` 和 `SymLinksIfOwnerMatch` `Options` 仅在 `<Directory>` 段或 `.htaccess` 文件中工作。
- `Options` 指令不能在 `<Files>` 和 `<FilesMatch>` 段中使用。

## 段如何合并

配置段按非常特定的顺序应用。由于这可能对配置指令的解释方式产生重要影响，因此理解其工作方式很重要。

合并顺序为：

1. `<Directory>`（正则表达式除外）和 `.htaccess` 同时执行（如果允许，`.htaccess` 覆盖 `<Directory>`）
2. `<DirectoryMatch>`（以及 `<Directory "~">`）
3. `<Files>` 和 `<FilesMatch>` 同时执行
4. `<Location>` 和 `<LocationMatch>` 同时执行
5. `<If>` 段，即使它们被包含在任何前述上下文中。

一些重要说明：

- 除 `<Directory>` 外，在每个组内，段按它们在配置文件中出现的顺序处理。例如，对 *`/foo/bar`* 的请求将匹配 `<Location "/foo/bar">` 和 `<Location "/foo">`（本例中为第 4 组）：两个段都将被求值，但按它们在配置文件中出现的顺序。
- `<Directory>`（上面的第 1 组）按目录组件从最短到最长的顺序处理（无论它们在配置文件中出现的顺序如何）。例如，`<Directory "/var/web/dir">` 将在 `<Directory "/var/web/dir/subdir">` 之前处理。
- 如果多个 `<Directory>` 段应用于同一目录，则按配置文件顺序处理。当多个 `<DirectoryMatch>`、`<Files>`、`<FilesMatch>`、`<Location>` 或 `<LocationMatch>` 段匹配同一资源时，同样如此。
- 通过 `Include` 指令包含的配置将视为位于包含文件中 `Include` 指令所在的位置。
- `<VirtualHost>` 段内的段在虚拟主机定义之外相应段*之后*应用。这允许虚拟主机覆盖主服务器配置。请注意，与其他段类型不同，每个请求仅选择一个 `<VirtualHost>`——来自多个匹配 vhost 的指令从不合并。有关如何选择 vhost 的详细信息，请参阅虚拟主机匹配。
- 当请求由 `mod_proxy` 提供服务时，`<Proxy>` 容器在处理顺序中取代 `<Directory>` 容器。
- 在 `<If>` 内部和外部混合相关配置指令时应谨慎，因为会影响合并顺序。显式使用 `<Else>` 可能会有所帮助。
- 当在 `.htaccess` 中使用 `<If>` 时，父目录中的所包含指令将在子目录中的非包含指令*之后*合并。
- ⚠️ **注意：`<Location>` 内的 `<Limit>` 可能静默授予访问权限** — 使用 `<Limit>` 在 `<Location>` 段内将授权限制为特定 HTTP 方法可能会产生意外结果。对于未在 `<Limit>` 中列出的方法，包含的 `<Location>` 段被视为没有授权要求——这实际上授予了访问权限并覆盖了原本适用的任何 `<Directory>` 限制。请改用 `<LimitExcept>`，或应用不带方法限制的授权。

> **技术说明**
>
> 实际上，在名称转换阶段（使用 `Aliases` 和 `DocumentRoots` 将 URL 映射到文件名）之前会执行一个 `<Location>`/`<LocationMatch>` 序列。此序列的结果在转换完成后被完全丢弃。

### 模块与配置段之间的关系

阅读配置段如何合并后经常出现的一个问题与像 `mod_rewrite` 这样的特定模块的指令如何以及何时处理有关。答案并不简单，需要一点背景知识。每个 httpd 模块管理自己的配置，其在 httpd.conf 中的每个指令在特定上下文中指定一部分配置。httpd 在读取时并不执行命令。

在运行时，httpd 核心按上述顺序遍历已定义的配置段，以确定哪些适用于当前请求。当第一个段匹配时，它被视为该请求的当前配置。如果后续段也匹配，则在这两个段中任一段具有指令的每个模块都有机会在两个段之间合并其配置。结果是第三个配置，此过程一直持续到所有配置段都被求值。

在上述步骤之后，HTTP 请求的“真正”处理开始：每个模块都有机会运行并执行它喜欢的任何任务。它们可以从 httpd 核心检索自己最终合并的配置，以确定它们应如何行动。

一个例子可以帮助可视化整个过程。以下配置使用 `mod_headers` 的 `Header` 指令设置特定的 HTTP 头。对于对 `/example/index.html` 的请求，httpd 将在 `CustomHeaderName` 头中设置什么值？

```apache
<Directory "/">
    Header set CustomHeaderName one
    <FilesMatch ".*">
        Header set CustomHeaderName three
    </FilesMatch>
</Directory>

<Directory "/example">
    Header set CustomHeaderName two
</Directory>
```

- `Directory "/"` 匹配，创建初始配置，将 `CustomHeaderName` 头设置为值 `one`。
- `Directory "/example"` 匹配，并且由于 `mod_headers` 在其代码中指定在合并时覆盖，创建新配置，将 `CustomHeaderName` 头设置为值 `two`。
- `FilesMatch ".*"` 匹配，出现另一个合并机会，导致 `CustomHeaderName` 头被设置为值 `three`。
- 最终在 HTTP 请求处理的后续步骤中，`mod_headers` 将被调用，它将收到将 `CustomHeaderName` 头设置为值 `three` 的配置。`mod_headers` 通常使用此配置来执行其工作，即设置 foo 头。这并不意味着模块不能执行更复杂的操作，比如丢弃不需要或已弃用的指令等。

> 即，此处并非忽略之前被覆盖的段，而是在下一轮继续解析

这对 `.htaccess` 也成立，因为它们在合并顺序中与 `Directory` 具有相同的优先级。要理解的重要概念是，像 `Directory` 和 `FilesMatch` 这样的配置段不能与像 `Header` 或 `RewriteRule` 这样的模块特定指令相比，因为它们在不同的层面上运作。

### 一些有用的示例

下面是一个人工示例，展示合并顺序。假设它们都适用于该请求，此示例中的指令将按 A > B > C > D > E 的顺序应用。

```apache
<Location "/">
    E
</Location>

<Files "f.html">
    D
</Files>

<VirtualHost *>
    <Directory "/a/b">
        B
    </Directory>
</VirtualHost>

<DirectoryMatch "^.*b$">
    C
</DirectoryMatch>

<Directory "/a/b">
    A
</Directory>
```

对于一个更具体的示例，考虑以下情况。无论 `<Directory>` 段中放置了什么访问限制，`<Location>` 段都将最后求值，并将允许对服务器的不受限访问。换句话说，合并顺序很重要，所以要小心！

```apache
<Location "/">
    Require all granted
</Location>

# 哎呀！这个 <Directory> 段将没有效果
<Directory "/">
    <RequireAll>
        Require all granted
        Require not host badguy.example.com
    </RequireAll>
</Directory>
```