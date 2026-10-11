https://nginx-wiki.getpagespeed.com/

## Configuration & patterns

### Examples

#### X-Accel (X-Sendfile) —— 代理内部重定向，返回匹配文件

https://github.com/GetPageSpeed/nginx-wiki/blob/master/docs/config/examples/x-accel.md

X-Accel 允许根据后端返回的头部，内部重定向到某个位置。这通常称为 **X-Sendfile**。

##### 工作原理

1. 后端处理身份验证、日志记录或其他逻辑
2. 后端发送带有内部 URI 的 `X-Accel-Redirect` 头
3. NGINX 提供文件服务，释放后端以处理其他请求
4. 最终用户直接从 NGINX 接收文件

---

##### 基本配置

###### 使用 `alias`

```nginx
# 当传入 URI /protected_files/myfile.tar.gz 时
# 将提供 /var/www/files/myfile.tar.gz
location /protected_files {
    internal;
    alias /var/www/files;
}
```

###### 使用 `root`

```nginx
# 当传入 URI /protected_files/myfile.tar.gz 时
# 将提供 /var/www/protected_files/myfile.tar.gz
location /protected_files {
    internal;
    root /var/www;
}
```

###### 代理到另一台服务器

```nginx
location /protected_files {
    internal;
    proxy_pass http://127.0.0.2;
}
```

> **`internal`**
>
> `internal` 指令阻止客户端直接访问此位置。只有内部重定向（如 X-Accel）才能到达它。

---

##### 特殊头

###### X-Accel-Redirect

设置 NGINX 要提供服务的 URI。

```http
X-Accel-Redirect: /protected_files/myfile.tar.gz
```

##### X-Accel-Buffering

控制此连接的代理缓冲。

- `yes`：允许响应缓存（默认）
- `no`：无缓冲响应（用于 Comet/流式传输）

```http
X-Accel-Buffering: no
```

###### X-Accel-Charset

设置文件的字符集。

```http
X-Accel-Charset: utf-8
```

###### X-Accel-Expires

设置文件在 NGINX 内部缓存中的过期时间。

- `off`：禁用缓存过期（默认）
- `<seconds>`：在 N 秒后过期

```http
X-Accel-Expires: 3600
```

###### X-Accel-Limit-Rate

设置此单个请求的速率限制。

- `off`：无限制（默认）
- `<bytes>`：限制为 N 字节/秒

```http
X-Accel-Limit-Rate: 1024
```

---

##### 示例：受保护的下载

###### NGINX 配置

```nginx
server {
    listen 80;
    server_name example.com;

    # 公共前端
    location / {
        proxy_pass http://backend;
    }

    # 受保护文件（仅内部）
    location /protected/ {
        internal;
        alias /var/www/downloads/;
    }
}
```

###### 后端响应（例如 PHP）

```php
<?php
// 验证用户是否有访问权限
if (!user_has_access($file)) {
    http_response_code(403);
    exit;
}

// 记录下载
log_download($user, $file);

// 让 NGINX 提供文件
header('X-Accel-Redirect: /protected/' . $file);
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename="' . basename($file) . '"');
exit;
?>
```