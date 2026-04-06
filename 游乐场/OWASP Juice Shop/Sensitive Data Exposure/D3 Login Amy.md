- Login Amy
    - 描述：使用艾米原始的用户凭证登录。（这可能需要暴力破解 93.83 billion trillion trillion centuries，但幸运的是她没有读到“One Important Final Note”）
    - 在挑战 User Credentials 的 SQL 注入得到的所有用户信息中搜索
        ```json
        "email": "amy@juice-sh.op",
        "password": "030f05e45e30710c3ad3c32f00de0473"
        ```
        - 搜索引擎查询 MD5 哈希[逆向站点](https://md5.gromweb.com/?md5=030f05e45e30710c3ad3c32f00de0473)得到
            ```K1f.....................```
        - 使用明文密码登录
    - 示例解决方案，作为信息搜集的方法：
        - 搜索引擎搜索 ```93.83 billion trillion trillion centuries``` 或 ```One Important Final Note```
        - 得到页面 ```https://www.grc.com/haystack.htm```
        - 其中示例密码为 
            ```
            D0g.....................
            PrXyc.N(n4k77#L!eVdAfp9
            ```
        - ```One Important Final Note```:
            ```
            使用“D0g.....................”的例子不应字面理解，因为如果每个人都用简单的点来填充密码，攻击者很快就会在猜测中添加点，从而绕过对未知填充的全面搜索。
            相反，你应该自己制定个性化的填充策略。你可以在前面添加一些填充，和/或在短语中穿插，和/或在末尾添加更多。
            你可以在开头放一些字符，中间填充，然后在末尾放更多字符。
            还可以通过使用简单的、容易记住的字符图案，如“<->”或“[*]”或“^-^”等，来混合填充字符。但一定要自己发明！
            ```
        - 挑战描述对应 ```One Important Final Note``` 可知，Amy 使用了示例密码
        - Amy 是动画  ```飞出个未来 Futurama``` 中的角色
        > 她实际上做了一个非常类似的填充技巧，只是用她丈夫的名字 Kif 写成 K1f，而不是示例中的 D0g！她甚至懒得改变填充长度！