- Admin Section
    - 在 ```main.js``` 中搜索关键词 ```admin```，找到管理页面路由设置
        ```typescript
        qm = [{
            path: "administration",
            component: rr,
            canActivate: [ee]
        }]
        ```
    - 未登录状态访问 
    ```http://127.0.0.1:3000/#/administration``` 
    响应显示 ```403 You are not allowed to access this page!```
    - 使用 Sensitive Data Exposure - D2 Exposed credentials 获得的测试账户，成功进入管理页面

- 代码挑战
    - 在代码中找到管理功能路由
        ```typescript
        {
            path: 'administration',
            component: AdministrationComponent,
            canActivate: [AdminGuard]
	    }
        ```
    - 修复为：删除此路由
        ```typescript
        /* TODO: Externalize admin functions into separate application
        that is only accessible inside corporate network.
        */
        // {
        //   path: 'administration',
        //   component: AdministrationComponent,
        //   canActivate: [AdminGuard]
        // }
        ```
        > 尽管可以通过访问控制来尝试限制对网店管理功能的访问，但通过内部托管一个不暴露于互联网的独立管理后台应用程序来更严格地应用“关注点分离”模式，绝对更安全。