项目 docker 页面：
https://hub.docker.com/r/webgoat/webgoat


下载运行命令：
```sh
docker run -p 127.0.0.1:3000:8080 -p 127.0.0.1:9090:9090 -e TZ=Asia/Shanghai webgoat/webgoat
```
> 重要提示：请选择正确的时区，确保 Docker 容器与宿主机的时区一致。这对某些练习中使用的 JWT 令牌的有效性至关重要。

端口：
WebGoat 3000
WebWolf 9090

拦截代理服务器通常是 8080 端口，将 WebGoat 端口改为 3000

> http://:8080/WebGoat to start using WebGoat...
访问 WebGoat 对应主机的 `loaclhost:3000/WebGoat` 

在“HTTP Proxies”部分的介绍中，设置 Zap 的过滤器：

> Then in the URL Inc Regex box type:
> `.*WebGoat.*`
> And in the URL Exc Regex box type:
> `.*lesson.*.mvc.*`


> WebGoat 中的一个练习只能用 Burp 解决，还不能用 OWAP ZAP 解决。

爆破时设置单线程避免报错