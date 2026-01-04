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

[cycubix 的解决方案](https://docs.cycubix.com/application-security-series/web-application-security-essentials/solutions)


:warning: 已知容器内文档渲染有误(XXE 10. Blind XXE)，与 Github 仓库的文档内容不同。

暂略：
- General - Writing new lesson  
    跳过

- Developer Tools - 6  
    :x: 无法通过
    响应 404，似乎运行错误
    在开发者工具的网络标签中查看 POST 请求体的参数值
    
- Crypto Basics - 6  
    :x: 无法通过 
    使用密钥对模数进行签名

- SQL Injection (mitigation) - 9  
    :x: 无法通过
    响应 404，似乎运行错误

- SQL Injection (mitigation) - 10  
    :x: 无法通过
    响应 404，似乎运行错误

- JWT tokens - 13
    使用提示得到刷新令牌端点，但除爆破外如何发现？


