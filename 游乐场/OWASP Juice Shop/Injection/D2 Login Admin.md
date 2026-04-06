- Login Admin
    - 描述：使用管理员用户账号登录。
    - 在 Sensitive Data Exposure - Exposed credentials 挑战获得测试账户凭证，然后在 Broken Access Control - Admin Section 挑战访问管理页面后。
    得到管理用户账号的邮箱
    ```admin@juice-sh.op```
		- 或者根据“关于我们”-“客户反馈”展示的邮件地址进行推测
    - 在 Security Misconfiguration - Error Handling 挑战，确认了登录功能存在 SQL 注入漏洞
    - 尝试对登录功能进行 SQL 注入，设置攻击向量为
    ```admin@juice-sh.op'==```
    登录了目标管理员账户
    - 示例解决方案的其他方法：
        > 1. 使用 Email ```' or 1=1--``` 和任何密码登录，该密码将验证 Users 表中的第一个条目，该条目恰好是管理员
        > 2. 或者，通过 SQL 注入获取所有用户凭证列表来收集用户数据，并在彩虹表中查找管理员密码哈希后，使用 Email ```admin@juice-sh.op``` 和密码登录
    - 或者，```' or 1=1 ORDER BY 1 LIMIT 1 OFFSET 1 --``` 按顺序登录账户，直到登录管理员账户
        - 若使用此方法遍历，则可解决多个登录其他用户账户的挑战
- 代码挑战
    ```typescript
    export function login () {
	  function afterLogin (user: { data: User, bid: number }, res: Response, next: NextFunction) {
	    BasketModel.findOrCreate({ where: { UserId: user.data.id } })
	      .then(([basket]: [BasketModel, boolean]) => {
	        const token = security.authorize(user)
	        user.bid = basket.id // keep track of original basket
	        security.authenticatedUsers.put(token, user)
	        res.json({ authentication: { token, bid: basket.id, umail: user.data.email } })
	      }).catch((error: Error) => {
	        next(error)
	      })
	  }
	 
	  return (req: Request, res: Response, next: NextFunction) => {
	    models.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email || ''}' AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`, { model: UserModel, plain: true })
	      .then((authenticatedUser) => {
	        const user = utils.queryResultToJson(authenticatedUser)
	        if (user.data?.id && user.data.totpSecret !== '') {
	          res.status(401).json({
	            status: 'totp_token_required',
	            data: {
	              tmpToken: security.authorize({
	                userId: user.data.id,
	                type: 'password_valid_needs_second_factor_token'
	              })
	            }
	          })
	        } else if (user.data?.id) {
	          afterLogin(user, res, next)
	        } else {
	          res.status(401).send(res.__('Invalid email or password.'))
	        }
	      }).catch((error: Error) => {
	        next(error)
	      })
	  }
    ```
    - 漏洞在于对 SQL 并未使用占位符进行预处理而是直接拼接到语句中，使得输入可作为查询结构
        ```typescript
        models.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email || ''}' AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`, {
            model: UserModel,
            plain: true
        })
        ```
    - 修复为，对输入使用预处理语句，其中数据库密码存储的最佳实践为密码的散列值而不是明文
        ```typescript
        models.sequelize.query(`SELECT * FROM Users WHERE email = $1 AND password = $2 AND deletedAt IS NULL`, {
            bind: [req.body.email, security.hash(req.body.password)],
            model: models.User,
            plain: true
        })
        ```
        > 使用 Sequelize 的内置绑定（或替换）机制相当于创建一个预处理语句。这可以防止恶意用户输入通过篡改查询语法，因为它们在条件参数插入之前就已经“固定不变”了。