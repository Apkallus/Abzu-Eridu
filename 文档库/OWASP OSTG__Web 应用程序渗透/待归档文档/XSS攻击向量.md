- XSS 速查表
    - [PortSwigger Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
- 攻击向量
    - 元素的事件监听器
        ```html
        <svg onload=print()>
        ```
    - javascript 伪协议
        ```html
        <iframe src="javascript:alert(`xss`)">
        ```
- HTML 元素上下文
    - ```<code>``` 元素并不自动对文本段内容进行转义
    - ```<textarea>``` 如何？如果注入 ```</textarea>``` 如何？

- 绕过防护过滤
    - OWASP Juice Shop - XSS - D4 Server-side XSS Protection
        非迭代的仅删除一次 HTML 标记对