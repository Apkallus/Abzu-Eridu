https://nginx.org/en/docs/http/ngx_http_upstream_module.html

# 模块 ngx_http_upstream_module

`ngx_http_upstream_module` 模块用于定义服务器组，这些服务器组可由 [proxy_pass]、[fastcgi_pass]、[uwsgi_pass]、[scgi_pass]、[memcached_pass] 和 [grpc_pass] 指令引用。

## 示例配置

```nginx
upstream backend {
    server backend1.example.com       weight=5;
    server backend2.example.com:8080;
    server unix:/tmp/backend3;

    server backup1.example.com:8080   backup;
    server backup2.example.com:8080   backup;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

支持动态配置并带定期 [健康检查] 的服务器组作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供：

```nginx
resolver 10.0.0.1;

upstream dynamic {
    zone upstream_dynamic 64k;

    server backend1.example.com      weight=5;
    server backend2.example.com:8080 fail_timeout=5s slow_start=30s;
    server 192.0.2.1                 max_fails=3;
    server backend3.example.com      resolve;
    server backend4.example.com      service=http resolve;

    server backup1.example.com:8080  backup;
    server backup2.example.com:8080  backup;
}

server {
    location / {
        proxy_pass http://dynamic;
        health_check;
    }
}
```

## 指令

### upstream

- 语法：`upstream name { ... }`
- 默认：—
- 上下文：`http`

定义服务器组。服务器可以监听不同端口。此外，监听 TCP 和 UNIX 域套接字的服务器可以混合使用。

示例：

```nginx
upstream backend {
    server backend1.example.com weight=5;
    server 127.0.0.1:8080       max_fails=3 fail_timeout=30s;
    server unix:/tmp/backend3;

    server backup1.example.com  backup;
}
```

默认情况下，请求使用加权轮询均衡方法在服务器之间分发。在上例中，每 7 个请求将按如下方式分发：5 个请求发往 `backend1.example.com`，第二个和第三个服务器各 1 个请求。如果与某台服务器通信时发生错误，请求将传递给下一台服务器，依此类推，直到尝试所有正常工作的服务器。如果无法从任何服务器获得成功响应，客户端将收到与最后一台服务器通信的结果。

### server

- 语法：`server address [parameters];`
- 默认：—
- 上下文：`upstream`

定义服务器的 `address` 和其他 `parameters`。地址可以指定为域名或 IP 地址（可带端口），或指定为以 `unix:` 前缀开头的 UNIX 域套接字路径。如果未指定端口，则使用端口 80。解析为多个 IP 地址的域名会一次定义多个服务器。

可定义以下参数：

- `weight=number`  
  设置服务器权重，默认 1。

- `max_conns=number`  
  限制到被代理服务器的同时活动连接最大数量（1.11.5）。默认值为零，表示无限制。如果服务器组不位于[共享内存](#zone)中，则限制按每个工作进程生效。  
  
  > 如果启用[空闲 keepalive](#keepalive) 连接、多个 [workers](../ngx_core_module.html#worker_processes) 和[共享内存](#zone)，则到被代理服务器的活动连接和空闲连接总数可能超过 `max_conns` 值。  
  >  
  > 从版本 1.5.9 到 1.11.5 之前，此参数作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

- `max_fails=number`  
  设置在 `fail_timeout` 参数指定的持续时间内与服务器通信失败应发生的次数，以认为服务器在同样由 `fail_timeout` 参数指定的持续时间内不可用。默认失败次数为 1。零值禁用尝试计数。什么算作失败尝试由 [proxy_next_upstream]、[fastcgi_next_upstream]、[uwsgi_next_upstream]、[scgi_next_upstream]、[memcached_next_upstream] 和 [grpc_next_upstream] 指令定义。

- `fail_timeout=time`  
  设置  
  - 在认为服务器不可用之前，指定次数的与服务器通信失败应发生的时间；  
  - 以及服务器被视为不可用的时间段。  
  
  默认情况下，参数设置为 10 秒。

- `backup`  
  将服务器标记为备份服务器。当主服务器不可用时，请求将传递给该服务器。  
  
  > 此参数不能与 [hash](#hash)、[ip_hash](#ip_hash) 和 [random](#random) 负载均衡方法一起使用。

- `down`  
  将服务器标记为永久不可用。

- `resolve`  
  监控与服务器域名对应的 IP 地址变化，并自动修改上游配置而无需重启 nginx（1.5.12）。服务器组必须位于[共享内存](#zone)中。  
  为使此参数生效，必须在 [http](ngx_http_core_module.html#resolver) 块或相应的 [upstream](#resolver) 块中指定 `resolver` 指令。  
  > 在 1.27.3 版本之前，此参数仅作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

- `service=name`  
  启用解析 DNS [SRV](https://datatracker.ietf.org/doc/html/rfc2782) 记录并设置服务 `name`（1.9.13）。为使此参数生效，必须为服务器指定 [resolve](#resolve) 参数，并指定不带端口号的主机名。  
  如果服务名不包含点（`.`），则构造符合 [RFC](https://datatracker.ietf.org/doc/html/rfc2782) 的名称，并将 TCP 协议添加到服务前缀。例如，要查找 `_http._tcp.backend.example.com` SRV 记录，需要指定指令：  
  ```nginx
  server backend.example.com service=http resolve;
  ```  
  如果服务名包含一个或多个点，则通过连接服务前缀和服务器名来构造名称。例如，要查找 `_http._tcp.backend.example.com` 和 `server1.backend.example.com` SRV 记录，需要指定指令：  
  ```nginx
  server backend.example.com service=_http._tcp resolve;
  server example.com service=server1.backend resolve;
  ```  
  最高优先级的 SRV 记录（具有相同最低数字优先级值的记录）解析为主服务器，其余 SRV 记录解析为备份服务器。如果为服务器指定了 [backup](#backup) 参数，则高优先级 SRV 记录解析为备份服务器，其余 SRV 记录被忽略。  
  > 在 1.27.3 版本之前，此参数仅作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

- `route=string`  
  设置服务器路由名称。  
  > 在 1.29.6 版本之前，此参数仅作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

- `drain`  
  将服务器置于“排空”模式（1.13.6）。在此模式下，只有[绑定](#sticky)到该服务器的请求才会被代理到它。  
  > 在 1.13.6 版本之前，此参数只能通过 [API] 模块更改。  
  >  
  > 在 1.29.6 版本之前，此参数仅作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

此外，以下参数作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供：

- `slow_start=time`  
  设置 `time`，在此期间服务器将在不健康服务器变为[健康]或服务器在被认为[不可用](#fail_timeout)一段时间后变为可用时，将其权重从零恢复到标称值。默认值为零，即禁用慢启动。  
  > 此参数不能与 [hash](#hash)、[ip_hash](#ip_hash) 和 [random](#random) 负载均衡方法一起使用。

> 如果组中只有一台服务器，则忽略 `max_fails`、`fail_timeout` 和 `slow_start` 参数，并且此类服务器永远不会被视为不可用。

### zone

- 语法：`zone name [size];`
- 默认：—
- 上下文：`upstream`

此指令出现在版本 1.9.0 中。

定义共享内存区的 `name` 和 `size`，该内存区保存组配置和工作进程之间共享的运行时状态。多个组可以共享同一个区。在这种情况下，只需指定一次 `size`。

此外，作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分，此类组允许更改组成员关系或修改特定服务器的设置而无需重启 nginx。配置可通过 [API] 模块访问（1.13.3）。

> 在 1.13.3 版本之前，配置只能通过由 [upstream_conf] 处理的特殊位置访问。

### state

- 语法：`state file;`
- 默认：—
- 上下文：`upstream`

此指令出现在版本 1.9.7 中。

指定一个 `file`，用于保存动态可配置组的状态。

示例：

```nginx
state /var/lib/nginx/state/servers.conf; # Linux 路径
state /var/db/nginx/state/servers.conf;  # FreeBSD 路径
```

状态目前仅限于带参数的服务器列表。解析配置时会读取该文件，并且每次上游配置[更改]时都会更新该文件。应避免直接更改文件内容。此指令不能与 [server](#server) 指令一起使用。

> 在[配置重载](../control.html#reconfiguration)或[二进制升级](../control.html#upgrade)期间所做的更改可能会丢失。  
>  
> 此指令作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

### hash

- 语法：`hash key [consistent];`
- 默认：—
- 上下文：`upstream`

此指令出现在版本 1.7.2 中。

为服务器组指定负载均衡方法，其中客户端-服务器映射基于哈希后的 `key` 值。`key` 可以包含文本、变量及其组合。注意，向组中添加或从组中移除服务器可能会导致大多数键重新映射到不同服务器。该方法与 [Cache::Memcached](https://metacpan.org/pod/Cache::Memcached) Perl 库兼容。

如果指定了 `consistent` 参数，则将改用 [ketama](https://www.metabrew.com/article/libketama-consistent-hashing-algo-memcached-clients) 一致性哈希方法。该方法确保当向组中添加或从组中移除服务器时，只有少量键会重新映射到不同服务器。这有助于缓存服务器实现更高的缓存命中率。该方法与 [Cache::Memcached::Fast](https://metacpan.org/pod/Cache::Memcached::Fast) Perl 库兼容，`ketama_points` 参数设置为 160。

### ip_hash

- 语法：`ip_hash;`
- 默认：—
- 上下文：`upstream`

指定组应使用一种负载均衡方法，其中请求基于客户端 IP 地址在服务器之间分发。客户端 IPv4 地址的前三个八位字节或整个 IPv6 地址用作哈希键。该方法确保来自同一客户端的请求始终传递给同一服务器，除非该服务器不可用。在后一种情况下，客户端请求将传递给另一台服务器。很可能也始终是同一台服务器。

> 从版本 1.3.2 和 1.2.2 开始支持 IPv6 地址。

如果需要临时移除其中一台服务器，应使用 `down` 参数标记它，以保留当前客户端 IP 地址的哈希。

示例：

```nginx
upstream backend {
    ip_hash;

    server backend1.example.com;
    server backend2.example.com;
    server backend3.example.com down;
    server backend4.example.com;
}
```

> 在版本 1.3.1 和 1.2.2 之前，无法为使用 `ip_hash` 负载均衡方法的服务器指定权重。

### keepalive

- 语法：`keepalive connections [local];`
- 默认：`keepalive 32 local;`
- 上下文：`upstream`

此指令出现在版本 1.1.4 中。

启用或禁用与上游服务器的 keepalive 连接缓存。自 1.29.7 起，默认激活连接缓存，并且这些连接不在不同 [locations](ngx_http_core_module.html#location) 之间[共享](#keepalive_local)。

`local` 参数（1.29.7）禁用跨不同位置共享缓存的 keepalive 连接，即使上游服务器地址匹配。如果未指定 `local` 参数，则任何到同一上游服务器的匹配缓存连接都可以重用，无论位置如何。

`connections` 参数设置每个工作进程缓存中保留的空闲 keepalive 连接的最大数量。当超过此数量时，最近最少使用的连接将被关闭。零值禁用与上游服务器的 keepalive 连接。

> 自 1.29.7 起，keepalive 连接默认启用，每个工作进程默认限制为 `32` 个连接。

> 特别应注意，`keepalive` 指令不限制 nginx 工作进程可以打开到上游服务器的连接总数。`connections` 参数应设置为足够小的数字，以便上游服务器也能处理新的传入连接。

> 在 1.29.7 之前，使用默认轮询方法以外的负载均衡方法时，必须在 `keepalive` 指令之前激活它们。

带 keepalive 连接的 memcached 上游示例配置：

```nginx
upstream memcached_backend {
    server 127.0.0.1:11211;
    server 10.0.0.2:11211;

    keepalive 32;
}

server {
    ...

    location /memcached/ {
        set $memcached_key $uri;
        memcached_pass memcached_backend;
    }

}
```

对于 HTTP，[proxy_http_version] 指令应设置为 `1.1`（自 1.29.7 起为默认值）或设置为 `2`，并且应清除 `Connection` 头字段。以下示例适用于 1.29.7 之前的版本：

```nginx
upstream http_backend {
    server 127.0.0.1:8080;

    keepalive 16;
}

server {
    ...

    location /http/ {
        proxy_pass http://http_backend;
        # proxy_http_version 1.1; # 1.29.7 之前
        # proxy_set_header Connection ""; # 1.29.7 之前
        ...
    }
}
```

> 或者，可以通过向上游服务器传递 `Connection: Keep-Alive` 头字段来使用 HTTP/1.0 持久连接，但不推荐此方法。

对于 FastCGI 服务器，需要设置 [fastcgi_keep_conn] 才能使 keepalive 连接工作：

```nginx
upstream fastcgi_backend {
    server 127.0.0.1:9000;

    keepalive 8;
}

server {
    ...

    location /fastcgi/ {
        fastcgi_pass fastcgi_backend;
        fastcgi_keep_conn on;
        ...
    }
}
```

> SCGI 和 uwsgi 协议没有 keepalive 连接的概念。

### keepalive_requests

- 语法：`keepalive_requests number;`
- 默认：`keepalive_requests 1000;`
- 上下文：`upstream`

此指令出现在版本 1.15.3 中。

设置可通过一个 keepalive 连接服务的最大请求数。达到最大请求数后，连接关闭。

定期关闭连接是释放每连接内存分配所必需的。因此，使用过高的最大请求数可能导致内存使用过多，不推荐。

> 在 1.19.10 版本之前，默认值为 100。

### keepalive_time

- 语法：`keepalive_time time;`
- 默认：`keepalive_time 1h;`
- 上下文：`upstream`

此指令出现在版本 1.19.10 中。

限制可通过一个 keepalive 连接处理请求的最长时间。达到此时间后，连接将在后续请求处理之后关闭。

### keepalive_timeout

- 语法：`keepalive_timeout timeout;`
- 默认：`keepalive_timeout 60s;`
- 上下文：`upstream`

此指令出现在版本 1.15.3 中。

设置到上游服务器的空闲 keepalive 连接保持打开的超时时间。

### ntlm

- 语法：`ntlm;`
- 默认：—
- 上下文：`upstream`

此指令出现在版本 1.9.2 中。

允许代理带 [NTLM 认证](https://en.wikipedia.org/wiki/Integrated_Windows_Authentication)的请求。一旦客户端发送带有以 `Negotiate` 或 `NTLM` 开头的 `Authorization` 头字段值的请求，上游连接就会绑定到客户端连接。进一步的客户端请求将通过同一上游连接代理，保持认证上下文。

为使 NTLM 认证工作，必须启用与上游服务器的 keepalive 连接。[proxy_http_version] 指令应设置为 `1.1`（自 1.29.7 起为默认值）或设置为 `2`，并且应清除 `Connection` 头字段。以下示例适用于 1.29.7 之前的版本：

```nginx
upstream http_backend {
    server 127.0.0.1:8080;

    ntlm;
}

server {
    ...

    location /http/ {
        proxy_pass http://http_backend;
        # proxy_http_version 1.1; # 1.29.7 之前
        # proxy_set_header Connection ""; # 1.29.7 之前
        ...
    }
}
```

> 使用默认轮询方法以外的负载均衡方法时，必须在 `ntlm` 指令之前激活它们。  
>  
> 此指令作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

### least_conn

- 语法：`least_conn;`
- 默认：—
- 上下文：`upstream`

此指令出现在版本 1.3.1 和 1.2.2 中。

指定组应使用一种负载均衡方法，其中请求传递给活动连接数最少的服务器，并考虑服务器权重。如果有多台此类服务器，则使用加权轮询均衡方法依次尝试它们。

### least_time

- 语法：
  ```nginx
  least_time header | last_byte [inflight];
  ```
- 默认：—
- 上下文：`upstream`

此指令出现在版本 1.7.10 中。

指定组应使用一种负载均衡方法，其中请求传递给平均响应时间最短且活动连接数最少的服务器，并考虑服务器权重。如果有多台此类服务器，则使用加权轮询均衡方法依次尝试它们。

如果指定 `header` 参数，则使用接收[响应头](#var_upstream_header_time)的时间。如果指定 `last_byte` 参数，则使用接收[完整响应](#var_upstream_response_time)的时间。如果指定 `inflight` 参数（1.11.6），也会考虑未完成的请求。

> 在 1.11.6 版本之前，默认会考虑未完成的请求。

> 在 1.31.0 版本之前，此指令仅作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

### queue

- 语法：
  ```nginx
  queue number [timeout=time];
  ```
- 默认：—
- 上下文：`upstream`

此指令出现在版本 1.5.12 中。

如果在处理请求时无法立即选择上游服务器，请求将被放入队列。该指令指定同时可在队列中的最大请求 `number`。如果队列已满，或在 `timeout` 参数指定的时间段内无法选择要传递请求的服务器，则向客户端返回 502（Bad Gateway）错误。

`timeout` 参数的默认值为 60 秒。

> 使用默认轮询方法以外的负载均衡方法时，必须在 `queue` 指令之前激活它们。  
>  
> 此指令作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

### random

- 语法：`random [two [method]];`
- 默认：—
- 上下文：`upstream`

此指令出现在版本 1.15.1 中。

指定组应使用一种负载均衡方法，其中请求传递给随机选择的服务器，并考虑服务器权重。

可选的 `two` 参数指示 nginx 随机选择[两台](https://homes.cs.washington.edu/~karlin/papers/balls.pdf)服务器，然后使用指定的 `method` 选择一台服务器。默认方法是 `least_conn`，它将请求传递给活动连接数最少的服务器。

`least_time` 方法将请求传递给平均响应时间最短且活动连接数最少的服务器。如果指定 `least_time=header`，则使用接收[响应头](#var_upstream_header_time)的时间。如果指定 `least_time=last_byte`，则使用接收[完整响应](#var_upstream_response_time)的时间。

> `least_time` 方法作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

### resolver

- 语法：
  ```nginx
  resolver address ... [valid=time] [ipv4=on|off] [ipv6=on|off] [status_zone=zone];
  ```
- 默认：—
- 上下文：`upstream`

此指令出现在版本 1.27.3 中。

配置用于将上游服务器名称解析为地址的名称服务器，例如：

```nginx
resolver 127.0.0.1 [::1]:5353;
```

地址可以指定为域名或 IP 地址，可带端口。如果未指定端口，则使用端口 53。名称服务器按轮询方式查询。

默认情况下，nginx 在解析时会同时查找 IPv4 和 IPv6 地址。如果不希望查找 IPv4 或 IPv6 地址，可以指定 `ipv4=off`（1.23.1）或 `ipv6=off` 参数。

默认情况下，nginx 使用响应的 TTL 值缓存答案。可选的 `valid` 参数允许覆盖它：

```nginx
resolver 127.0.0.1 [::1]:5353 valid=30s;
```

> 为防止 DNS 欺骗，建议在适当保护的可信本地网络中配置 DNS 服务器。

可选的 `status_zone` 参数（1.17.5）启用对指定 `zone` 中 DNS 服务器请求和响应统计信息的[收集]。该参数作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

> 从 1.17.5 版本到 1.27.3 版本之前，此指令仅作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

### resolver_timeout

- 语法：`resolver_timeout time;`
- 默认：`resolver_timeout 30s;`
- 上下文：`upstream`

此指令出现在版本 1.27.3 中。

设置名称解析超时，例如：

```nginx
resolver_timeout 5s;
```

> 从 1.17.5 版本到 1.27.3 版本之前，此指令仅作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

### sticky

- 语法：
  ```nginx
  sticky cookie name [expires=time] [domain=domain] [httponly] [samesite=strict|lax|none|$variable] [secure] [path=path];
  sticky route $variable ...;
  sticky learn create=$variable lookup=$variable zone=name:size [timeout=time] [header] [sync];
  ```
- 默认：—
- 上下文：`upstream`

此指令出现在版本 1.5.7 中。

启用会话粘性，使来自同一客户端的请求传递给服务器组中的同一台服务器。有三种方法可用：

#### cookie

当使用 `cookie` 方法时，有关指定服务器的信息通过 nginx 生成的 HTTP cookie 传递：

```nginx
upstream backend {
    server backend1.example.com;
    server backend2.example.com;

    sticky cookie srv_id expires=1h domain=.example.com path=/;
}
```

来自尚未绑定到特定服务器的客户端的请求将传递给由配置的均衡方法选择的服务器。带有此 cookie 的进一步请求将传递给指定服务器。如果指定服务器无法处理请求，则像客户端尚未绑定一样选择新服务器。

> 由于负载均衡方法在考虑已绑定请求时总是尝试均匀分配负载，活动绑定请求数较多的服务器获得新的未绑定请求的可能性较小。

第一个参数设置要设置或检查的 cookie 名称。cookie 值是 IP 地址和端口（或 UNIX 域套接字路径）的 MD5 哈希的十六进制表示。但是，如果指定了 [server](#server) 指令的 `route` 参数，则 cookie 值将是 `route` 参数的值：

```nginx
upstream backend {
    server backend1.example.com route=a;
    server backend2.example.com route=b;

    sticky cookie srv_id expires=1h domain=.example.com path=/;
}
```

在这种情况下，`srv_id` cookie 的值将是 `a` 或 `b`。

附加参数如下：

- `expires=time`  
  设置浏览器应保留 cookie 的 `time`。特殊值 `max` 将使 cookie 在 `31 Dec 2037 23:55:55 GMT` 过期。如果未指定此参数，则 cookie 将在浏览器会话结束时过期。

- `domain=domain`  
  定义设置 cookie 的 `domain`。参数值可以包含变量（1.11.5）。

- `httponly`  
  向 cookie 添加 `HttpOnly` 属性（1.7.11）。

- `samesite=strict | lax | none | $variable`  
  向 cookie 添加 `SameSite`（1.19.4）属性，值为以下之一：`Strict`、`Lax`、`None`，或使用变量（1.23.3）。在后一种情况下，如果变量值为空，则不会向 cookie 添加 `SameSite` 属性；如果值解析为 `Strict`、`Lax` 或 `None`，则分配相应值；否则分配 `Strict` 值。

- `secure`  
  向 cookie 添加 `Secure` 属性（1.7.11）。

- `path=path`  
  定义设置 cookie 的 `path`。

如果省略任何参数，则不会设置相应的 cookie 字段。

#### route

当使用 `route` 方法时，被代理服务器在收到第一个请求时向客户端分配一个路由。来自此客户端的所有后续请求将在 cookie 或 URI 中携带路由信息。此信息与 [server](#server) 指令的 `route` 参数比较，以识别请求应代理到的服务器。如果未指定 `route` 参数，则路由名将是 IP 地址和端口（或 UNIX 域套接字路径）的 MD5 哈希的十六进制表示。如果指定服务器无法处理请求，则由配置的均衡方法选择新服务器，就像请求中没有路由信息一样。

`route` 方法的参数指定可能包含路由信息的变量。第一个非空变量用于查找匹配的服务器。

示例：

```nginx
map $cookie_jsessionid $route_cookie {
    ~.+\.(?P<route>\w+)$ $route;
}

map $request_uri $route_uri {
    ~jsessionid=.+\.(?P<route>\w+)$ $route;
}

upstream backend {
    server backend1.example.com route=a;
    server backend2.example.com route=b;

    sticky route $route_cookie $route_uri;
}
```

这里，如果请求中存在 `JSESSIONID` cookie，则从该 cookie 获取路由。否则，使用来自 URI 的路由。

#### learn

当使用 `learn` 方法（1.7.1）时，nginx 分析上游服务器响应，并学习通常通过 HTTP cookie 传递的服务器发起的会话。

```nginx
upstream backend {
   server backend1.example.com:8080;
   server backend2.example.com:8081;

   sticky learn
          create=$upstream_cookie_examplecookie
          lookup=$cookie_examplecookie
          zone=client_sessions:1m;
}
```

在示例中，上游服务器通过在响应中设置 cookie `EXAMPLECOOKIE` 创建会话。带有此 cookie 的进一步请求将传递给同一服务器。如果服务器无法处理请求，则像客户端尚未绑定一样选择新服务器。

`create` 和 `lookup` 参数分别指定指示如何创建新会话和搜索现有会话的变量。两个参数都可以多次指定，在这种情况下使用第一个非空变量。

会话存储在共享内存区中，其 `name` 和 `size` 由 `zone` 参数配置。在 64 位平台上，一兆字节的区可以存储约 4000 个会话。在 `timeout` 参数指定的时间内未访问的会话将从区中移除。默认情况下，`timeout` 设置为 10 分钟。

`header` 参数（1.13.1）允许在收到上游服务器响应头后立即创建会话。

`sync` 参数（1.13.8）启用共享内存区的[同步](../stream/ngx_stream_zone_sync_module.html#zone_sync)。该参数作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

> 在 1.29.6 版本之前，此指令仅作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

## 嵌入变量

`ngx_http_upstream_module` 模块支持以下嵌入变量：

- `$upstream_addr`  
  保存上游服务器的 IP 地址和端口，或 UNIX 域套接字路径。如果请求处理期间联系了多个服务器，则其地址用逗号分隔，例如 `192.168.1.1:80, 192.168.1.2:80, unix:/tmp/sock`。如果发生从一个服务器组到另一个服务器组的内部重定向，由 `X-Accel-Redirect` 或 [error_page](ngx_http_core_module.html#error_page) 发起，则来自不同组的服务器地址用冒号分隔，例如 `192.168.1.1:80, 192.168.1.2:80, unix:/tmp/sock : 192.168.10.1:80, 192.168.10.2:80`。如果无法选择服务器，则该变量保存服务器组名称。

- `$upstream_bytes_received`  
  从上游服务器接收的字节数（1.11.4）。来自多个连接的值用逗号和冒号分隔，类似 `$upstream_addr` 变量中的地址。

- `$upstream_bytes_sent`  
  发送到上游服务器的字节数（1.15.8）。来自多个连接的值用逗号和冒号分隔，类似 `$upstream_addr` 变量中的地址。

- `$upstream_cache_status`  
  保存访问响应缓存的状态（0.8.3）。状态可以是 `MISS`、`BYPASS`、`EXPIRED`、`STALE`、`UPDATING`、`REVALIDATED` 或 `HIT`。

- `$upstream_connect_time`  
  保存与上游服务器建立连接所花费的时间（1.9.1）；时间以秒为单位，毫秒分辨率。对于 SSL，包括握手时间。多个连接的时间用逗号和冒号分隔，类似 `$upstream_addr` 变量中的地址。

- `$upstream_cookie_<name>`  
  上游服务器在 `Set-Cookie` 响应头字段中发送的指定 `name` 的 cookie（1.7.1）。仅保存最后一个服务器响应中的 cookie。

- `$upstream_header_time`  
  保存从上游服务器接收响应头所花费的时间（1.7.10）；时间以秒为单位，毫秒分辨率。多个响应的时间用逗号和冒号分隔，类似 `$upstream_addr` 变量中的地址。

- `$upstream_http_<name>`  
  保存服务器响应头字段。例如，`Server` 响应头字段可通过 `$upstream_http_server` 变量获取。将头字段名称转换为变量名称的规则与以 `$http_` 前缀开头的变量相同。仅保存最后一个服务器响应中的头字段。

- `$upstream_last_addr`  
  保存最后选择的上游服务器的 IP 地址或 UNIX 域套接字路径（1.29.3）。  
  > 此变量作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

- `$upstream_last_server_name`  
  保存最后选择的上游服务器名称（1.25.3）；允许通过 SNI 传递它：  
  ```nginx
  proxy_ssl_server_name on;
  proxy_ssl_name        $upstream_last_server_name;
  ```  
  > 此变量作为我们的[商业订阅](https://www.f5.com/products/nginx)的一部分提供。

- `$upstream_queue_time`  
  保存请求在上游[队列](#queue)中花费的时间（1.13.9）；时间以秒为单位，毫秒分辨率。多个响应的时间用逗号和冒号分隔，类似 `$upstream_addr` 变量中的地址。

- `$upstream_response_length`  
  保存从上游服务器获得的响应长度（0.7.27）；长度以字节为单位。多个响应的长度用逗号和冒号分隔，类似 `$upstream_addr` 变量中的地址。

- `$upstream_response_time`  
  保存从上游服务器接收响应所花费的时间；时间以秒为单位，毫秒分辨率。多个响应的时间用逗号和冒号分隔，类似 `$upstream_addr` 变量中的地址。

- `$upstream_status`  
  保存从上游服务器获得的响应状态码。多个响应的状态码用逗号和冒号分隔，类似 `$upstream_addr` 变量中的地址。如果无法选择服务器，则该变量保存 502（Bad Gateway）状态码。

- `$upstream_trailer_<name>`  
  保存从上游服务器获得的响应末尾字段（1.13.10）。