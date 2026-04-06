- Forged Review
    - 描述： 以其他用户身份发布产品评论或编辑任何用户的现有评论。
    - 查看商品评论的请求
        ```GET /rest/products/1/reviews HTTP/1.1```
        响应
        ```json
        {
            "status": "success",
            "data": [{
                    "message": "One of my favorites!",
                    "author": "admin@juice-sh.op",
                    "product": 1,
                    "likesCount": 0,
                    "likedBy": [],
                    "_id": "doqP6F8YcHdLEKLFT"
                }
            ]
        }
        ```
    - 发布商品评论的请求
        ```PUT /rest/products/1/reviews HTTP/1.1```
        ```json
        {
            "message": "aaaaaaaaaaaaaaaaaaaa",
            "author": "admin@juice-sh.op"
        }
        ```
    - 尝试修改 ```PUT``` 请求中的消息体的作者字符串，成功发布评论从 ```GET```中看到此消息以其他作者的身份发布

- 代码挑战：
    ```typescript
    export function updateProductReviews () {
	  return (req: Request, res: Response, next: NextFunction) => {
	    const user = security.authenticatedUsers.from(req)
	    db.reviewsCollection.update(
	      { _id: req.body.id },
	      { $set: { message: req.body.message } },
	      { multi: true }
	    ).then(
	      (result: { modified: number, original: Array<{ author: any }> }) => {
	        res.json(result)
	      }, (err: unknown) => {
	        res.status(500).json(err)
	      })
	  }
	}
    ```
    - 查找数据库信息
        ```typescript
        db.collection.update(
            { query }, // 查询条件
            { update }, // 更新操作（如 $set）
            { multi: true } // 是否更新多条（默认 false）
        )
        ```
    - 漏洞在于检索了用户但弃置而未匹配，并且直接使用请求输入的```id```进行匹配，导致账户与评论未正确关联
        ```typescript
        const user = security.authenticatedUsers.from(req)
        { _id: req.body.id }
        ```
    - 修复：使用对用户的检索而不是仅使用请求体的```id```
        ```typescript
        const user = security.authenticatedUsers.from(req)
        {
            _id: req.body.id,
            author: user.data.email
        }
        ```
    > 根据 HTTP 请求中的身份验证令牌检索到的用户在服务器端设置作者，这是正确的做法。这可以防止用户随意在请求中附带任何他们喜欢的作者电子邮件。