- ```atob()```与```btoa()``` [方法](https://mdn.org.cn/en-US/docs/Web/API/Window/atob)：
    ```typescript
    const routes: Routes = [
	  {
	    path: atob('c2NvcmUtYm9hcmQ='),
	    component: ScoreBoardComponent
	  }
    ]
    ```
    > Window 接口的 atob() 方法解码使用 Base64 编码的数据字符串。使用 Window.btoa() 方法编码和传输可能导致通信问题的数据，然后传输它并使用 atob() 方法再次解码数据。