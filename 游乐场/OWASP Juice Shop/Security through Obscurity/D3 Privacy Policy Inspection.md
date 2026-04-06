- Privacy Policy Inspection
    - 描述：证明你确实阅读了我们的隐私政策。
    - 提示：
        > 1. 只有访问特殊URL才能确认你已经仔细阅读。
        > 2. 你首先应该明显解决“阅读我们的隐私政策”的挑战。
        > 3. 使用鼠标光标来不失去当前阅读的段落是没问题的。
        > 4. 如果你发现政策中有些特别热的部分，你可能想将它们熔合在一起，类似于你可能已经发现的在“应用一些高级密码分析来找到真正的复活节彩蛋”中的内容。
    - 在隐私政策页面 ```http://127.0.0.1:3000/#/privacy-security/privacy-policy```
        部分内容在光标移动是拥有特殊视觉效果，
        对应 HTML 为
        ```html
        <span _ngcontent-ng-c1032439724="" class="hot">http://127.0.0.1</span>
        ```
        在浏览器开发者工具栏中搜索类 ```.hot```，所有对应字段为
        ```
        http://127.0.0.1
        We may also
        instruct you
        to refuse all
        reasonably necessary
        responsibility
        ```
    - 示例解决方案：将收集到的单词作为路径访问
        > 将这些内容组合到 URL http://localhost:3000/we/may/also/instruct/you/to/refuse/all/reasonably/necessary/responsibility
        （如果需要，添加服务器端口）中，通过访问它来解决这个问题。