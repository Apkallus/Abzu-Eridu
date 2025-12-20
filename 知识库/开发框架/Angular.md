- DomSanitizer 服务的```bypassSecurityTrustHtml```[方法](https://v6.angular.cn/api/platform-browser/DomSanitizer#bypasssecuritytrusthtml)：
    ```typescript
    this.searchValue = this.sanitizer.bypassSecurityTrustHtml(queryParam)
    ```
    > 绕过安全检查，并信任给定的值是一个安全的 HTML。