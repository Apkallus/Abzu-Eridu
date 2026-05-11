- Confidential Document
    - 描述: 访问机密文件
    - 提示：
        > 1. 分析并篡改在应用程序中直接提供文件的超链接。
        > 2. 你要找的文件没有任何保护。一旦找到它，你也可以访问它。
    - 访问服务器的搜索引擎索引文件
        ```http://127.0.0.1:3000/robots.txt```
        得到
        ```
        User-agent: *
        Disallow: /ftp
        ```
    - 从侧边栏进入“About Us”页面后，访问条款链接
        ```http://127.0.0.1:3000/ftp/legal.md```
    - 尝试访问发现的 ```/ftp```目录
    目录中包含各种 md 与配置备份文件
    - 其中 ```acquisitions.md``` 即为收购计划文件
        ```http://127.0.0.1:3000/ftp/acquisitions.md```

- 编程挑战
    ```TypeScript
    /* /ftp directory browsing and file download */
        app.use('/ftp', serveIndexMiddleware, serveIndex('ftp', { icons: true }))
        app.use('/ftp(?!/quarantine)/:file', servePublicFiles())
        app.use('/ftp/quarantine/:file', serveQuarantineFiles())
        
        app.use('/.well-known', serveIndexMiddleware, serveIndex('.well-known', { icons: true, view: 'details' }))
        app.use('/.well-known', express.static('.well-known'))
        
        /* /encryptionkeys directory browsing */
        app.use('/encryptionkeys', serveIndexMiddleware, serveIndex('encryptionkeys', { icons: true, view: 'details' }))
        app.use('/encryptionkeys/:file', serveKeyFiles())
        
        /* /logs directory browsing */
        app.use('/support/logs', serveIndexMiddleware, serveIndex('logs', { icons: true, view: 'details' }))
        app.use('/support/logs/:file', serveLogFiles())
        
        /* Swagger documentation for B2B v2 endpoints */
        app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument))
        
        app.use(express.static(path.resolve('frontend/dist/frontend')))
        app.use(cookieParser('kekse'))
    ```

    - 其中对 ```/ftp``` 的路由
        ```TypeScript
            app.use('/ftp', serveIndexMiddleware, serveIndex('ftp', { icons: true }))
            app.use('/ftp(?!/quarantine)/:file', servePublicFiles())
            app.use('/ftp/quarantine/:file', serveQuarantineFiles())
        ```
    - 修复为：全部删除。
    其他修复方案仅控制图标或目录的显示。
    - ```/ftp```目录中包含可公开文件、机密信息、设置备份。
    使用路由权限控制也不恰当，可公开文件应当移动到其他位置