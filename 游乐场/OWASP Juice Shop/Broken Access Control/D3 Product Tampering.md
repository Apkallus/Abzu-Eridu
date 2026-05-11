- Product Tampering
    - 描述：将 OWASP SSL Advanced Forensic Tool (O-Saft) 
    http://127.0.0.1:3000/#/search?q=OWASP%20SSL%20Advanced%20Forensic%20Tool%20(O-Saft)
    产品描述中的链接 href 更改为
    https://owasp.slack.com
    - 此商品的 id 为 9
    - 挑战 API-only XSS 发现了修改商品描述的端点
    - 原描述为
        ```GET /api/products/9 HTTP/1.1```
        ```"description":"O-Saft is an easy to use tool to show information about SSL certificate and tests the SSL connection according given list of ciphers and various SSL configurations. <a href=\"https://www.owasp.org/index.php/O-Saft\" target=\"_blank\">More...</a>"```
    - 使用 PUT 方法，提交修改后的描述链接地址
        ``````PUT /api/products/9 HTTP/1.1```
        ```"description":"O-Saft is an easy to use tool to show information about SSL certificate and tests the SSL connection according given list of ciphers and various SSL configurations. <a href=\"https://owasp.slack.com\" target=\"_blank\">More...</a>"```

- 代码挑战：
    ```typescript
    /** Authorization **/
	  /* Baskets: Unauthorized users are not allowed to access baskets */
	  app.use('/rest/basket', security.isAuthorized(), security.appendUserId())
	  /* BasketItems: API only accessible for authenticated users */
	  app.use('/api/BasketItems', security.isAuthorized())
	  app.use('/api/BasketItems/:id', security.isAuthorized())
	  /* Feedbacks: GET allowed for feedback carousel, POST allowed in order to provide feedback without being logged in */
	  app.use('/api/Feedbacks/:id', security.isAuthorized())
	  /* Users: Only POST is allowed in order to register a new user */
	  app.get('/api/Users', security.isAuthorized())
	  app.route('/api/Users/:id')
	    .get(security.isAuthorized())
	    .put(security.denyAll())
	    .delete(security.denyAll())
	  /* Products: Only GET is allowed in order to view products */
	  app.post('/api/Products', security.isAuthorized())
	  // app.put('/api/Products/:id', security.isAuthorized())
	  app.delete('/api/Products/:id', security.denyAll())
	  /* Challenges: GET list of challenges allowed. Everything else forbidden entirely */
	  app.post('/api/Challenges', security.denyAll())
	  app.use('/api/Challenges/:id', security.denyAll())
	  /* Hints: GET and PUT hints allowed. Everything else forbidden */
	  app.post('/api/Hints', security.denyAll())
	  app.route('/api/Hints/:id')
	    .get(security.denyAll())
	    .delete(security.denyAll())
	  /* Complaints: POST and GET allowed when logged in only */
	  app.get('/api/Complaints', security.isAuthorized())
	  app.post('/api/Complaints', security.isAuthorized())
	  app.use('/api/Complaints/:id', security.denyAll())
	  /* Recycles: POST and GET allowed when logged in only */
	  app.get('/api/Recycles', recycles.blockRecycleItems())
	  app.post('/api/Recycles', security.isAuthorized())
	  /* Challenge evaluation before finale takes over */
	  app.get('/api/Recycles/:id', recycles.getRecycleItem())
	  app.put('/api/Recycles/:id', security.denyAll())
	  app.delete('/api/Recycles/:id', security.denyAll())
	  /* SecurityQuestions: Only GET list of questions allowed. */
	  app.post('/api/SecurityQuestions', security.denyAll())
	  app.use('/api/SecurityQuestions/:id', security.denyAll())
	  /* SecurityAnswers: Only POST of answer allowed. */
	  app.get('/api/SecurityAnswers', security.denyAll())
	  app.use('/api/SecurityAnswers/:id', security.denyAll())
	  /* REST API */
	  app.use('/rest/user/authentication-details', security.isAuthorized())
	  app.use('/rest/basket/:id', security.isAuthorized())
	  app.use('/rest/basket/:id/order', security.isAuthorized())
	  app.post('/api/Users', verify.emptyUserRegistration())
	  /* Unauthorized users are not allowed to access B2B API */
	  app.use('/b2b/v2', security.isAuthorized())
	  /* Check if the quantity is available in stock and limit per user not exceeded, then add item to basket */
	  app.put('/api/BasketItems/:id', security.appendUserId(), basketItems.quantityCheckBeforeBasketItemUpdate())
	  app.post('/api/BasketItems', security.appendUserId(), basketItems.quantityCheckBeforeBasketItemAddition(), basketItems.addBasketItem())
	  /* Accounting users are allowed to check and update quantities */
	  app.delete('/api/Quantitys/:id', security.denyAll())
	  app.post('/api/Quantitys', security.denyAll())
	  app.use('/api/Quantitys/:id', security.isAccounting(), IpFilter(['123.456.789'], { mode: 'allow' }))
	  /* Feedbacks: Do not allow changes of existing feedback */
	  app.put('/api/Feedbacks/:id', security.denyAll())
	  /* PrivacyRequests: Only allowed for authenticated users */
	  app.use('/api/PrivacyRequests', security.isAuthorized())
	  app.use('/api/PrivacyRequests/:id', security.isAuthorized())
	  /* PaymentMethodRequests: Only allowed for authenticated users */
	  app.post('/api/Cards', security.appendUserId())
	  app.get('/api/Cards', security.appendUserId(), payment.getPaymentMethods())
	  app.put('/api/Cards/:id', security.denyAll())
	  app.delete('/api/Cards/:id', security.appendUserId(), payment.delPaymentMethodById())
	  app.get('/api/Cards/:id', security.appendUserId(), payment.getPaymentMethodById())
	  /* PrivacyRequests: Only POST allowed for authenticated users */
	  app.post('/api/PrivacyRequests', security.isAuthorized())
	  app.get('/api/PrivacyRequests', security.denyAll())
	  app.use('/api/PrivacyRequests/:id', security.denyAll())
	 
	  app.post('/api/Addresss', security.appendUserId())
	  app.get('/api/Addresss', security.appendUserId(), address.getAddress())
	  app.put('/api/Addresss/:id', security.appendUserId())
	  app.delete('/api/Addresss/:id', security.appendUserId(), address.delAddressById())
	  app.get('/api/Addresss/:id', security.appendUserId(), address.getAddressById())
	  app.get('/api/Deliverys', delivery.getDeliveryMethods())
	  app.get('/api/Deliverys/:id', delivery.getDeliveryMethod())
    ```
    > API 路由需要为特定的 HTTP 请求方法明确定义处理程序，如果它们希望覆盖“允许所有人访问所有内容”的默认行为。
    - 漏洞在于：对商品的路由未覆盖默认行为
        ```typescript
        // app.put('/api/Products/:id', security.isAuthorized())
        ```
    - 修复：覆盖默认行为，并禁止对商品内容进行修改
        ```typescript
        app.post('/api/Products', security.denyAll())
        app.put('/api/Products/:id', security.denyAll())
        ```
    > 对于产品API，禁用除GET以外的所有HTTP动词确实是实现安全访问控制唯一安全的方法。商店管理员无论如何都不应使用面向客户的Web界面来管理商店的库存。