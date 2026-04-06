- Forged Feedback
    - 描述：用另一个用户的名字发表一些反馈。
    - 提交表单，查看 POST 内容
        ```json
        {
            "UserId": 19,
            "captchaId": 4,
            "captcha": "38",
            "comment": "test (***a@juice-sh.op)",
            "rating": 2
        }
        ```
    - 访问反馈功能，其表达的 HTML 代码
        ```html
        <input _ngcontent-ng-c4118930637="" hidden="" type="text" id="userId" ngdefaultcontrol="" class="ng-untouched ng-pristine ng-valid">
        ```
        此功能使用隐藏表单提交用户id
    - 修改 ```"UserId": 19``` 为其他数字作为其他用户发表反馈
        或修改 HTML 表单界面