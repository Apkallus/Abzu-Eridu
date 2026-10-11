https://www.varnish-software.com/developers/documentation/

[速查表](https://www.varnish-software.com/developers/tutorials/vsl-cheatsheet/)

## Tutorials

### Example VCL template

Varnish 的内置 VCL 策略极为保守，其核心原则是避免缓存有状态及个性化内容。通过严格遵循 HTTP 标准中的缓存规则，Varnish 在默认配置下即可确保安全。然而在许多实际生产环境中，后端服务器往往无法提供规范的缓存头信息，这将导致缓存命中率偏低。

在本教程中，我们将展示一系列适用于 Varnish 的可定制 VCL 示例。我们将逐一解析各个 VCL 模板的功能特性，并最终将其整合为一个完整的 VCL 配置文件。

#### 1. 后端定义

首要步骤是定义后端（Backend），即 Varnish 获取内容的源站服务器。

```vcl
backend server1 {
     .host = "127.0.0.1";
     .port = "8080";
     .max_connections = 100;
     .probe = {
         .request =
             "HEAD / HTTP/1.1"
             "Host: localhost"
             "Connection: close"
             "User-Agent: Varnish Health Probe";
         .interval  = 10s;
         .timeout   = 5s;
         .window    = 5;
         .threshold = 3;
     }
     .connect_timeout        = 5s;
     .first_byte_timeout     = 90s;
     .between_bytes_timeout  = 2s;
 }
```

##### 后端连接信息

每个后端定义都必须包含一个名称，上述示例中的名称为 `server1`。`.host` 和 `.port` 属性分别用于指定后端的地址与端口号。

在上述示例中，源站（通常为 Apache 或 Nginx 服务器）与 Varnish 部署在同一台机器上，因此使用了 IP 地址 `127.0.0.1`（即 `localhost`）。由于 HTTP 客户端通常占用 80 端口，传统的 Web 服务器会被配置为监听其他端口。示例中使用了 `8080` 端口，因此需确保后端服务也已配置为监听该端口。

若源站服务器位于其他主机，请相应调整 `.host` 属性的值。该属性同时支持 IP 地址和主机名。

`.max_connections` 属性用于限制 Varnish 向后端建立的并发连接数。一旦超出此限制，后续的后端请求将会失败。



### Varnish Configuration Language (VCL)

https://www.varnish-software.com/developers/tutorials/varnish-configuration-language-vcl/

#### VCL 子程序与返回动作

正如 [Varnish Cache 用户指南的内置子程序章节] 所述，系统提供了多个内置子程序。当 [有限状态机] 进入相应状态时，这些子程序会被执行。尽管每个子程序都具有 [内置 VCL] 行为，但可以通过编写自定义 VCL 来修改其逻辑。

##### 客户端侧子程序

客户端侧子程序是指执行流程中不与后端交互的部分。由于无需等待可能响应缓慢的后端，其执行路径是最快的。[缓存命中流程] 就是仅涉及客户端侧子程序的典型执行路径示例。

###### vcl_recv()

```vcl
sub vcl_recv { ... }
```

当接收到请求时调用 `vcl_recv` 子程序。这可能是来自客户端的常规 HTTP 请求、内部 ESI 子请求，甚至是先前请求的重启。

支持的返回动作

-   `return(fail)`：触发致命错误。等同于 `return(synth(503, "VCL Failed"))`。
-   `return(synth(status code, reason))`：使用指定的状态码和原因短语返回合成内容。
-   `return(restart)`：重启事务，增加重启计数器；若达到 `max_restarts` 限制则失败。
-   `return(pass)`：绕过缓存。
-   `return(pipe)`：切换到管道模式。
-   `return(hash)`：在缓存中查找对象。
-   `return(purge)`：从缓存中清除对象及其变体。
-   `return(vcl(label))`：加载带标签的 VCL 配置并调用其 `vcl_recv` 子程序。

#### 后端子程序

后端子程序负责与源服务器进行交互。此类子程序仅有三个，在流程图中它们属于灰色框区域，是[缓存未命中流程]和[缓存绕过流程]的汇聚点。

后端子程序的执行速度通常慢于客户端侧对应的子程序，这主要是因为这些子程序必须等待数据通过网络传输完成。

##### vcl_backend_fetch

```vcl
sub vcl_backend_fetch { ... }
```

`vcl_backend_fetch` 子程序负责向源服务器发送 HTTP 请求并触发后端获取操作。

支持的返回动作

-   `return(fail)`：触发致命错误。等同于 `return(synth(503, "VCL Failed"))`。
-   `return(fetch)`：从后端获取对象。
-   `return(error(status code, reason))`：以后端错误的形式返回合成错误，并流转至 `vcl_backend_error`。
-   `return(abandon)`：放弃后端请求并流转至 `vcl_synth`（除非该请求为后台获取）。等同于 `return(synth(503, "VCL Failed"))`。



##### vcl_backend_response

```vcl
sub vcl_backend_response { ... }
```

当 Varnish 收到由 `vcl_backend_fetch` 触发的后端获取所产生的 HTTP 响应时，将调用 `vcl_backend_response` 子程序。

在 `vcl_backend_response` 中会执行一系列检查，以决定是否将对象存入缓存以及缓存的时长。

如[缓存绕过流程]所述，被判定为不可缓存的内容将被标记为 Hit-For-Miss。

支持的返回动作

-   `return(fail)`：触发致命错误。等同于 `return(synth(503, "VCL Failed"))`。
-   `return(deliver)`：从后端获取对象主体并将内容交付给所有等待的客户端请求。此过程支持并行处理及流式传输。
-   `return(retry)`：重试后端事务，增加重试计数器；若达到 `max_retries` 上限则失败。
-   `return(error(status code, reason))`：以后端错误的形式返回合成错误，并流转至 `vcl_backend_error`。
-   `return(pass(duration))`：针对不可缓存对象启用 Hit-For-Pass 机制，使后续对该资源的请求直接从 `vcl_recv` 流转至 `vcl_pass`。
-   `return(abandon)`：放弃后端请求并流转至 `vcl_synth`（除非该请求为后台获取）。等同于 `return(synth(503, "VCL Failed"))`。

#### VCL objects and variables

https://www.varnish-software.com/developers/tutorials/varnish-configuration-language-vcl/#vcl-objects-and-variables

##### Request variables

###### ⚔️ 顶层请求与边缘侧包含

边缘侧包含（ESI）是一种标记标签，用于在边缘节点组装内容，其 `src` 属性指向一个 HTTP 端点。

以下是一个 ESI 示例：

```html
<esi:include src="/header" />
```

Varnish 会解析 ESI 标签，并通过内部子请求调用 `src` 属性中指定的 HTTP 端点。

> 服务器端请求伪造功能
> - 结构：
>     - 标签可省略末尾自闭合符号 `/`，但需保留空格
>     - 属性 src 
>         - 可省略引号
>         - 无法省略协议
> - 即使前缀 `>` 闭合尖括号未成功逃逸出标签（浏览器视角），但后续载荷仍被解析为外层的有效 ESI 标记

在请求级别，可以使用 `req.esi_level` 变量检查嵌套深度，并使用 `req.esi` 变量切换 ESI 支持。

当处于 ESI 子请求中时，还可以获取有关发起该子请求的顶层请求的上下文信息。[`req_top`] 对象提供了该上下文：

-   `req_top.url`
    返回父请求的 URL。
-   `req_top.http.*`
    包含父请求的请求头。
-   `req_top.method`
    返回父请求的请求方法。
-   `req_top.proto`
    返回父请求的协议。

> 如果在非 ESI 上下文中使用 `req_top`，其值将与 `req` 对象完全相同。

如果您想知道顶层请求是否正在访问主页，可以使用以下 VCL 代码：

```vcl
vcl 4.1;
import std;

sub vcl_recv {
    if (req.esi_level > 0 && req_top.url == "/") {
        std.log("ESI call for the homepage");
    }
}
```

此示例将使用 `std.log()` 函数把 `ESI call for the homepage` 记录到 Varnish 的共享内存日志中。

##### Backend response variables

###### VFP 相关后端响应变量

还有一些与 Varnish Fetch Processors (VFP) 相关的后端响应变量。这些布尔值变量允许您切换特定功能：

-   [`beresp.do_esi`]
    用于启用 ESI 解析。
-   [`beresp.do_stream`]
    用于禁用 HTTP 流式传输。
-   [`beresp.do_gzip`]
    用于显式压缩非 gzip 内容。
-   [`beresp.do_gunzip`]
    用于显式解压 gzip 内容，并将纯文本版本存储在缓存中。

