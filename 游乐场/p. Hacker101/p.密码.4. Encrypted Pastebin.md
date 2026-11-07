## 步骤

侦察
- 访问首页
    ```http
    GET / HTTP/2
    Host: id.ctf.hacker101.com
    ```
    - 响应与文本翻译
        ```
        我们开发出了互联网上最安全的文本分享平台。您的数据采用军事级128位AES加密进行保护，且加密密钥绝不会存储在我们的数据库中，因此任何黑客都无法未经授权访问您的信息。
        ```
        ```html
        <form method="POST">
            Title: <input type="text" name="title">
            <br>
            <textarea rows="40" cols="80" name="body">
        </textarea>
            <br>
            <input type="submit" value="Post">
        </form>
        <img src="tracking.gif">
        ```
        - 信息
            - 128位AES加密
            - 加密密钥不在数据库内

- 使用文本分享功能
    ```http
    POST / HTTP/2
    Host: id.ctf.hacker101.com

    title=title_fooooooooo&body=body_barrrrrrrrr
    ```
    - 响应 302
        ```http
        HTTP/2 302 Found
        Location: https://id.ctf.hacker101.com/?post=poniVKofdQQd-7S13D1ArHfkbAAy3B-hnuxKJIzj-E!Jm4gok!cxbSAoywSdxxewdaqGZt4-ilOwyli-oppQt3V9dgN2jPV!mlHis38k2vFuPWIJWkJ7tbg!1hiN!ATUoGMthYmaLoL4J2MTxipbgi8xCzYgOcE6UG8JBvOX2t2EBZmvk!zbsMQY76uZxhLSTrFZE4CYXBp-0LcQaHeSjg~~
        ```

- 追踪重定向，响应
    ```html
    <html>

    <head>
        <title>
            title_fooooooooo -- Encrypted Pastebin
        </title>
    </head>

    <body>
        <h1>
            title_fooooooooo
        </h1>
        <pre>
        body_barrrrrrrrr
        </pre>
        <img src="tracking.gif">
    </body>

    </html>
    ```
    - 标题反射到 `title` 与 `h1` 两处
    - 文本位于 `pre`

测试
- 使用单包攻击，获取一批 post 参数
    ```log
    post=r4sxReeXmVx0aWPOaif-1heDqC!d-ghQduSI!m0MdzOhP8GCnFYnjylbkXE9z7n-zLDTK1YWcpisTvN5g-0SWRpZVLSlqGaljq29lhu6XgzzAKINi9UTf7rAUuWF8OPPs76iavBwnCAI0rcdCKD6hHgbfVwxYWfMGa4JEwA5SEhuG6K8YyEWCaH5wDC-!VGmW6VFVvZXPZglhPoUpH8JUA~~

    post=wurLS67FX34w6oQScCVy10VXElFMF3D1EOvAaPijIenkomxOd4MiTXeBxavvkB-N!p1OOzmOjWVxrtSpjmKRZN!J90qBhH6kFAE2UPl!Jlxzv53T5pO02k2mxP9RSWEXaca-xujwNpgzXiqgSuc03qqwVgaFJBZlNEJ!MTL0ZKjJWLqs3S-O2ZZB4JDwGd0tVF48bNvlkJ!QSo66SK8i9g~~

    post=8fdraNYrUeOAqiN58mOFzxwHnOjnqRHg9quQ!fKTi04zqnT!4DCKz8PZcFQDIVPICGsPZ2WTvD4iMs18yzEY3EYUJeBqmbdMyUF5V1KGDCYkB7VpnGVJTi-dysObPDSl0rETxXQNR4-HUnvFMLBAGJJZMPpvgpnkHJiN!KK9Lcd480QUBrvnPA6OJw9vzXrJ9mB717KoeEpLNIShCYh-FQ~~

    post=FdgMb54lVMZvCVGeIG6JXxHKtbX9TtlIj1jsBPhYwxSgRMxLKWewRXtFhD3cSCSDd-i-wgJGmn0aJLU2-v-Hp344QlFgVgQnPdI-XYdVozCnWZaHhdFf-eQxpw6rjcN0HdhTRt0O2F2oPqg5u8OFmDi4XS0Bo-3T7g2tw4D1h8w-xX2zVt8fYastObrrmJX-RLOgeOo2!3zQ9VhCIUGVsA~~

    post=2Bab8W4EmGP17f4nAW!efs4pFV-Gc39!NBenI02d5YEwVf072h-hS2l8mvqDB7GkwT!C1j0BEHI7x7XCZ6WUCHjri38!WcdY0LTea5sEXdioE2yp3AlMK3zGDA5z24u3DY!Xh3jqCj6x2jcHkLvk0iGFTDwg24SIUmlfjijepDovJnfKP9!XaFZXksH!cfOwMh39aRpc7owSXLlDrHGgjA~~

    post=UccrRhoUfNCE!FCMPfjN8-yhr8Xcvd5o328hE-xOAyKyPTKY!CPpZgAK3DSHxEGh0Cz15SmlL6K3yL3hY46yGTZ6AHBuxaD5mXvGolqN842W3TOkqARM-KKqD3AlrfNdQkHKnWkRgNGrQrHONazvbU71IXzL9kSHnuVWgd2dbRkSIDuizcw6Fih!UWjZ-971clAWdVw0IMt18acSV04Lqw~~

    post=38HlnK1DHPF9zK7PaY45mKiRPG9gFv6jR4DvMk17GIxkn73rIjqMQbzhYCQnqiW8U92-!9aDbQcSR4PkaLTZI7beRlspzlATQ8fXtzFoV5igLg2NOvZiQTWb4g1pUwOQ6T6FYtQmFgHB3YU0e2UBcNBEyvbgBNAUzuSmItub3xhQN-4ygI7zC4i3x1!dyPTbwtxaxMiT9JEPyF3r9AbIsg~~

    post=iEVnSJwMhUMABP95I5!R9sDKiR6iqQqFsBeFjNJKvBlbYlA8GubfdfYK8divSlQ64lKt0!gFmUto0gwbCChmEPk9jXNIaUZ24QAe1tu6-IaFp4sCzLpzIy9rtq3oIgfIZ8LqI8ta-3S!grNgV3QqQbD-H75-EPDWhbiFtlOGtiS3gANPGbACOmkzmIHR!ltkCaI5WYCNU9tTh5-gzf0xsg~~

    post=QQ62ftzpou07-iTjFr!hU7fECPCr!MOvigimca7oQ51r7AqIuNeK3I756t0Z7EH5FMf9JI6s0pqvmZfIgT-NyJ2fg86F4cmXK5LSDhRDaGNDh9sjGsNbR3WcrcK6RcnwMBaxZJkI8p0dQi4SLCScigRx!u1nMHv2HmJr9zG6PpTp14Qih0a8Wku5p7e6Op4y9vCVC!SBHJKoUGqy47M8yA~~

    post=U3V5OfH43L!Iopes4K2lOuGfG6Ct3iVQhykBykFG7Vu73ajUC65SEgJfH8-pdxpMMEaM23ioYI2uMwHQHHWeEbmQ9kan0b4okfkor9P6FYxMONyi847ycoQXAfVTeNlVnpTOZMqXl1OxjdW0uluI-Opqgg-ymbwGkDp-F7iGffSH0bACnANPvcJoF0gh2eQiqcOGZXrQlsjShlviZBLA-g~~
    ```

移除查询参数
- 请求
    ```http
    GET /?post HTTP/2
    Host: id.ctf.hacker101.com
    ```
    - 响应
        ```log
        ^FLAG^7c0bc8f6cf87f4bf904264b1de7d666bbc8638c530ea0bdff8a68f4b65c24403$FLAG$
        Traceback (most recent call last):
        File "./main.py", line 69, in index
            post = json.loads(decryptLink(postCt).decode('utf8'))
        File "./common.py", line 48, in decryptLink
            cipher = AES.new(staticKey, AES.MODE_CBC, iv)
        File "/usr/local/lib/python2.7/site-packages/Crypto/Cipher/AES.py", line 95, in new
            return AESCipher(key, *args, **kwargs)
        File "/usr/local/lib/python2.7/site-packages/Crypto/Cipher/AES.py", line 59, in __init__
            blockalgo.BlockAlgo.__init__(self, _AES, key, *args, **kwargs)
        File "/usr/local/lib/python2.7/site-packages/Crypto/Cipher/blockalgo.py", line 141, in __init__
            self._cipher = factory.new(key, *args, **kwargs)
        ValueError: IV must be 16 bytes long
        ```
    - 移除/修改查询参数得到详细错误信息
    - 制造各种错误逐步获取信息
    - hard 模式下，flag 点数8
    - 信息记录到功能端点中

Host 头注入测试
- 设置
    ```http
    POST / HTTP/2
    Host: id.ctf.hacker101.com
    §X-Forwarded-Host§: test
    ```
    - 载荷 
        ```http
        X-Forwarded-Host: test
        ```
    - 响应
        ```http
        HTTP/2 302 Found
        Location: https://test/?post=jJ9mwVyIP0HDSbzcDTS2dGnhIs9L48ZhWnZ2WEb-v7BvTRC6lbKZMhSRpT8z!10wOD17L3w6rD6E6danx3KVP4choC4qaJQ8SiNmWLj690LwQkx3XeTNz2JctaYYC78jKLiRjerMKO!prlNCPqBFNkgQ7J-e0nZr2bxWciBDfpd-BQrzvxZADH!OEFtSNynn41kDMx-e74x2bOYb3rQ-GA~~

        <p>You should be redirected automatically to target URL: <a href="?post=jJ9mwVyIP0HDSbzcDTS2dGnhIs9L48ZhWnZ2WEb-v7BvTRC6lbKZMhSRpT8z!10wOD17L3w6rD6E6danx3KVP4choC4qaJQ8SiNmWLj690LwQkx3XeTNz2JctaYYC78jKLiRjerMKO!prlNCPqBFNkgQ7J-e0nZr2bxWciBDfpd-BQrzvxZADH!OEFtSNynn41kDMx-e74x2bOYb3rQ-GA~~">?post=jJ9mwVyIP0HDSbzcDTS2dGnhIs9L48ZhWnZ2WEb-v7BvTRC6lbKZMhSRpT8z!10wOD17L3w6rD6E6danx3KVP4choC4qaJQ8SiNmWLj690LwQkx3XeTNz2JctaYYC78jKLiRjerMKO!prlNCPqBFNkgQ7J-e0nZr2bxWciBDfpd-BQrzvxZADH!OEFtSNynn41kDMx-e74x2bOYb3rQ-GA~~</a>.  If not click the link.
        ```
        - 在 `Location` 头部反射，不出现在响应体。似乎无关

> [!WARNING] 挑战保留，直到回顾二进制的 AES-CBC 主题

## 功能端点

端点
- `/`
    - 方法
        - GET 得到文本分享表单
        - POST 提交文本分享
            - `title`
            - `body`
    - 参数
        - `/?post=参数`
            访问特定文本分享

post
- `./main.py`

    ```py
    69: post = json.loads(decryptLink(postCt).decode('utf8'))
    ```
- `./common.py`

    ```py
    11  b64d = lambda x: base64.decodestring(x.replace('~', '=').replace('!', '/').replace('-', '+'))
    22  raise PaddingException()
    46  data = b64d(data)
    48  cipher = AES.new(staticKey, AES.MODE_CBC, iv)
    49  return unpad(cipher.decrypt(data))
    ```
    - 拥有3组 base64 字符编码
        - 对应的 hackvertor 还原标签
            `<@replace('-','+')><@replace('!','/')><@replace('~','=')></@replace></@replace></@replace>`

    - 使用 `AES.MODE_CBC`

- `/usr/local/lib/python2.7/site-packages/Crypto/Cipher/AES.py`
- 异常日志
    ```log
    ValueError: IV must be 16 bytes long
    ValueError: Input strings must be a multiple of 16 in length
    Error: Incorrect padding
    ```


## 待测试

侦察
- [x] 路径与文件
    - 无
- [x] HTTP 方法
    - 无

储存型
- [x] XSS
    - 无
- [x] 服务器端模板注入
    - 无

反射
- [x] Host 注入
    - 反射在 `Location`，但似乎无关


参数
- post 参数 `/?post`
    - [x] 修改参数返回详细错误信息 
    - [ ] AES-CBC 
    - [ ] 模糊测试
- [ ] 暴破其他可能的参数 `/?参数`