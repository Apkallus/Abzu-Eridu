[F5 NGINX 主页](https://docs.nginx.com/)
- [NGINX 开源版主页 - 参考](https://nginx.org/en/docs/)
- [NGINX 主页 - 指南](https://docs.nginx.com/nginx/)
    - 同时包含开源版与商业版
    - 功能
        - 搜索
        - 页面切换到 md 格式
        - 页面链接到 github 文档

[nginx 文档 github](https://github.com/nginx/documentation)

## Admin Guide

### Basic Functionality

#### Create NGINX Plus and NGINX Configuration Files —— 配置文件

https://github.com/nginx/documentation/blob/main/content/nginx/admin-guide/basic-functionality/managing-configuration-files.md

NGINX 和 NGINX Plus 使用基于文本的配置文件，默认名为 **nginx.conf**。

NGINX Plus：在 Linux 中默认位置是 `/etc/nginx`，在 FreeBSD 中为 `/usr/local/etc/nginx`。

NGINX 开源版：位置取决于安装 NGINX 所用的软件包系统以及操作系统。通常为 `/usr/local/nginx/conf`、`/etc/nginx` 或 `/usr/local/etc/nginx` 之一。

你可以通过 `nginx -V` 命令输出中的 `--conf-path=` 参数验证确切的配置文件路径：

```shell
 nginx -V 2>&1 | awk -F: '/configure arguments/ {print $2}' | xargs -n1
```

示例输出：

```none
--prefix=/etc/nginx
--sbin-path=/usr/sbin/nginx
--modules-path=/usr/lib64/nginx/modules
--conf-path=/etc/nginx/nginx.conf          # 配置文件的路径
--error-log-path=/var/log/nginx/error.log
--http-log-path=/var/log/nginx/access.log
--pid-path=/var/run/nginx.pid
--...<更多参数>
```

##### 指令

配置文件由 _指令_ 及其参数组成。简单（单行）指令以分号（`;`）结尾。其他指令则充当“容器”，用于将相关指令分组在一起。容器用花括号（`{}`）括起来，通常称为 _块_。以下是一些简单指令的示例。

```nginx
user             nobody;
error_log        logs/error.log notice;
worker_processes 1;
```

##### 特定功能的配置文件

为了更便于维护配置，可以将其拆分为一组特定功能的文件，存放在 `/etc/nginx/conf.d` 目录中，并在主 **nginx.conf** 文件中使用 [include](https://nginx.org/en/docs/ngx_core_module.html#include) 指令引用这些特定功能文件的内容。

```nginx
include conf.d/http;
include conf.d/stream;
include conf.d/exchange-enhanced;
```

##### 上下文

一些顶级指令称为 _上下文_，用于将适用于不同流量类型的指令分组在一起：

- [events](https://nginx.org/en/docs/ngx_core_module.html#events) – 通用连接处理
- [http](https://nginx.org/en/docs/http/ngx_http_core_module.html#http) – HTTP 流量
- [mail](https://nginx.org/en/docs/mail/ngx_mail_core_module.html#mail) – 邮件流量
- [stream](https://nginx.org/en/docs/stream/ngx_stream_core_module.html#stream) – TCP 和 UDP 流量

放置在这些上下文之外的指令称为位于 _main_ 上下文中。

###### 虚拟服务器

在每个流量处理上下文中，可包含一个或多个 `server` 块，用于定义 _虚拟服务器_，以控制请求的处理。可在 `server` 上下文中包含的指令因流量类型而异。

对于 HTTP 流量（`http` 上下文），每个 [server](https://nginx.org/en/docs/http/ngx_http_core_module.html#server) 指令控制对特定域或 IP 地址上资源的请求处理。`server` 上下文中的一个或多个 [location](https://nginx.org/en/docs/http/ngx_http_core_module.html#location) 上下文定义如何处理特定的 URI 集合。

对于邮件和 TCP/UDP 流量（[mail](https://nginx.org/en/docs/mail/ngx_mail_core_module.html) 和 [stream](https://nginx.org/en/docs/stream/ngx_stream_core_module.html) 上下文），每个 `server` 指令控制到达特定 TCP 端口或 UNIX 套接字的流量处理。

###### 包含多个上下文的示例配置文件

以下配置说明了上下文的使用。

```nginx
user nobody; # 'main' 上下文中的指令

events {
    # 连接处理配置
}

http {
    # 特定于 HTTP 的配置，并影响所有虚拟服务器

    server {
        # HTTP 虚拟服务器 1 的配置
        location /one {
            # 处理以 '/one' 开头的 URI 的配置
        }
        location /two {
            # 处理以 '/two' 开头的 URI 的配置
        }
    }

    server {
        # HTTP 虚拟服务器 2 的配置
    }
}

stream {
    # 特定于 TCP/UDP 的配置，并影响所有虚拟服务器
    server {
        # TCP 虚拟服务器 1 的配置
    }
}
```

###### 继承

通常，_子_ 上下文——包含在另一个上下文（其 _父_ 上下文）中的上下文——会继承父级中包含的指令设置。某些指令可以出现在多个上下文中，在这种情况下，可以通过在子上下文中包含该指令来覆盖从父级继承的设置。有关示例，请参见 [proxy_set_header](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_set_header) 指令。

##### 重新加载配置文件

要使配置文件的更改生效，必须重新加载它。你可以重启 `nginx` 进程，或发送 `reload` 信号来重新加载配置，而不会中断当前请求的处理。有关详细信息，请参见 [在运行时控制 NGINX 进程]。

使用 NGINX Plus，你无需重新加载配置，即可动态重新配置上游组中服务器之间的[负载均衡]。你还可以使用 NGINX Plus API 和键值存储来动态控制访问，例如[基于客户端 IP 地址]。


## nginx documentation

### Modules reference

#### ngx_http_core_module

https://nginx.org/en/docs/http/ngx_http_core_module.html

##### Embedded Variables —— 内嵌变量

`ngx_http_core_module` 模块支持名称与 Apache 服务器变量相匹配的内嵌变量。首先，这些变量代表客户端请求头字段，例如 `$http_user_agent`、`$http_cookie` 等。此外还有其他变量：

- `$arg_`*name*
    请求行中的参数 *name*

- `$args`
    请求行中的参数

##### location

**语法：**

```nginx
location [ = | ~ | ~* | ^~ ] uri { ... }
location $variable { ... }
location @name { ... }
```

**默认：** —

**上下文：** `server`, `location`

根据请求 URI 或变量值（1.31.5）设置配置。

匹配是针对规范化 URI 进行的：先解码以“`%XX`”形式编码的文本，解析对相对路径组件“`.`”和“`..`”的引用，并可能将两个或多个相邻斜杠[压缩](https://nginx.org/en/docs/http/ngx_http_core_module.html#merge_slashes)为一个斜杠。

`location` 可以由前缀字符串、正则表达式或谓词（1.31.5）定义。正则表达式通过前置的“`~*`”修饰符（用于不区分大小写匹配）或“`~`”修饰符（用于区分大小写匹配）指定。谓词通过前置的“`$`”指定，并包含一个在请求处理期间求值的变量。如果变量值非空且不等于“`0`”，则 Predicate Locations（使用变量时） 匹配。

要查找与给定请求匹配的 `location`，nginx 首先检查使用前缀字符串定义的 `location`（前缀 `location`）。其中，最长匹配前缀的 `location` 会被选中并记住。然后按配置文件中出现的顺序检查正则表达式。正则表达式搜索在第一个匹配处终止，并使用相应配置。如果未找到与正则表达式匹配的项，则按配置文件中出现的顺序检查 Predicate Locations。如果没有任何 Predicate Locations 匹配，则使用先前记住的前缀 `location` 的配置。

`location` 块可以嵌套，但有一些下文提到的例外。

对于 macOS 和 Cygwin 等不区分大小写的操作系统，前缀字符串匹配会忽略大小写（0.7.7）。但是，比较仅限于单字节区域设置。

正则表达式可以包含捕获（0.7.40），之后可在其他指令中使用，参见[正则表达式捕获](https://nginx.org/en/docs/regex_captures.html)。

如果最长匹配的前缀 `location` 具有“`^~`”修饰符，则不检查正则表达式和 Predicate Locations。

此外，使用“`=`”修饰符可以定义 URI 与 `location` 的精确匹配。如果找到精确匹配，搜索终止。例如，如果“`/`”请求频繁发生，定义“`location = /`”将加速这些请求的处理，因为第一次比较后搜索就终止。显然，这样的 `location` 不能包含嵌套 `location`。

> **注意**
>
> 在 0.7.1 到 0.8.41 版本中，如果请求匹配了不带“`=`”和“`^~`”修饰符的前缀 `location`，搜索也会终止，并且不检查正则表达式。

下面用示例说明：

```nginx
# 精确匹配并立即终止：请求 `/`
location = / {
    [ configuration A ]
}

# 最长前缀匹配：请求 `/index.html` 
location / {
    [ configuration B ]
}

# 最长前缀匹配：请求 `/documents/document.html`
location /documents/ {
    [ configuration C ]
}

# 匹配并立即终止，不检查正则表达式：请求 `/images/1.gif` 
location ^~ /images/ {
    [ configuration D ]
}

# 正则表达式匹配，不区分大小写：请求 `/documents/1.jpg` 
location ~* \.(gif|jpg|jpeg)$ {
    [ configuration E ]
}

# 变量匹配：请求 `/documents/index.html?pred=1` 
location $arg_pred {
    [ configuration F ]
}
```

“`@`”前缀定义命名 `location`。此类 `location` 不用于常规请求处理，而是用于请求重定向。它们不能嵌套，也不能包含嵌套 `location`。

前缀尾部斜杠解析：
- 如果 `location` 由以前缀字符串定义且该字符串以斜杠字符结尾，并且请求由 [proxy_pass]、[fastcgi_pass]、[uwsgi_pass]、[scgi_pass]、[memcached_pass] 或 [grpc_pass] 之一处理，则会执行特殊处理。

- 对于 URI 等于该字符串但没有尾部斜杠的请求，将返回代码为 301 的永久重定向，指向追加斜杠后的请求 URI（即为常见的重定向来源）

##### alias

**语法：** `alias path;`

**默认：** —

**上下文：** `location`

定义对指定 location 的替换。例如，使用以下配置

```nginx
location /i/ {
    alias /data/w3/images/;
}
```

当请求“`/i/top.gif`”时，将发送文件 `/data/w3/images/top.gif`。

`path` 值可包含变量，但 `$document_root` 和 `$realpath_root` 除外。

如果在使用正则表达式定义的 location 内使用 `alias`，则其值指定完整文件路径（0.7.40）。此类路径通常应引用正则表达式中包含的捕获：

```nginx
location ~ ^/users/(.+\.(?:gif|jpe?g|png))$ {
    alias /data/w3/images/$1;
}
```

如果在谓词 location 内使用 `alias`，则其值指定完整文件路径。

当 location 匹配指令值的最后一部分时：

```nginx
location /images/ {
    alias /data/w3/images/;
}
```

最好改用 [root](https://nginx.org/en/docs/http/ngx_http_core_module.html#root) 指令：

```nginx
location /images/ {
    root /data/w3;
}
```

