- Bonus Payload
    - 关联挑战 XSS - DOM XSS
    - 描述：使用提供的攻击向量进行 DOM XSS
        ```html
        <iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>
        ```
    - 与 DOM XSS 相同，在搜索功能中使用提供的攻击向量。本次的攻击向量中加载了 soundcloud 中 Juice Shop 的歌曲。然而 Firefox 禁止加载子框架，但可在 chrome 中加载。
        - Firefox 默认使用更严格的同源策略
            - 在 Firefox 中打开 about:config 页面，搜索 security.fileuri.strict_origin_policy 首选项并将其设置为 true。
- 编程挑战
    - 与 DOM XSS 相同，漏洞在于绕过了angular框架的验证
        ```typescript
        this.searchValue = this.sanitizer.bypassSecurityTrustHtml(queryParam)
        ```