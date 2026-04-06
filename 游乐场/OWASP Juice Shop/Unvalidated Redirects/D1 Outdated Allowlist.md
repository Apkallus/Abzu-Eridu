- Outdated Allowlist
    - 说明：让我们将您重定向到我们不再推广的加密货币地址之一。
    - 提示：
        > 0. 一段时间前，Juice Shop 项目通过Bitcoin、Dash 和 Ether 接受捐赠。但它从未收到过任何捐赠，因此这些支付方式后来被取消了。
        > 1. 当从代码中删除对那些地址的引用时，开发人员有点粗心。
        > 2. 更具体地说，他们粗心的方式甚至使得 Angular 编译器无法自动清理他们留下的痕迹。
        > 3. 当然，仅仅直接访问任何加密货币链接并不能解决这个挑战。
    - 在 burp 代理历史记录中搜索 ```Bitcoin```
        - 其中 ```main.js``` 文件中包含加密货币数据与重定向地址
            ```javascript
            showBitcoinQrCode() {
                this.dialog.open(Yt, {
                    data: {
                        data: "bitcoin:1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm",
                        url: "./redirect?to=https://blockchain.info/address/1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm",
                        address: "1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm",
                        title: "TITLE_BITCOIN_ADDRESS"
                    }
                })
            }
            showDashQrCode() {
                this.dialog.open(Yt, {
                    data: {
                        data: "dash:Xr556RzuwX6hg5EGpkybbv5RanJoZN17kW",
                        url: "./redirect?to=https://explorer.dash.org/address/Xr556RzuwX6hg5EGpkybbv5RanJoZN17kW",
                        address: "Xr556RzuwX6hg5EGpkybbv5RanJoZN17kW",
                        title: "TITLE_DASH_ADDRESS"
                    }
                })
            }
            showEtherQrCode() {
                this.dialog.open(Yt, {
                    data: {
                        data: "0x0f933ab9fCAAA782D0279C300D73750e1311EAE6",
                        url: "./redirect?to=https://etherscan.io/address/0x0f933ab9fcaaa782d0279c300d73750e1311eae6",
                        address: "0x0f933ab9fCAAA782D0279C300D73750e1311EAE6",
                        title: "TITLE_ETHER_ADDRESS"
                    }
                })
            }
            ```
        - 访问重定向链接完成挑战
        
    - 示例解决方案：
        - 添加商品到购物车，继续流程，直到进入 My Payment Options 界面
        - 点击 Other payment options 选项卡展开 Donations 与 Merchandise 界面
        - ```http://127.0.0.1:3000/redirect?to=http://shop.spreadshirt.com/juiceshop```
        观察到大部分链接使用```redirect?to=```进行重定向
        - 在 ```main.js``` 中搜索 ```redirect?to=``` 找到加密货币的重定向链接

- 代码挑战
    ```typescript
    export const redirectAllowlist = new Set([
	  'https://github.com/juice-shop/juice-shop',
	  'https://blockchain.info/address/1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm',
	  'https://explorer.dash.org/address/Xr556RzuwX6hg5EGpkybbv5RanJoZN17kW',
	  'https://etherscan.io/address/0x0f933ab9fcaaa782d0279c300d73750e1311eae6',
	  'http://shop.spreadshirt.com/juiceshop',
	  'http://shop.spreadshirt.de/juiceshop',
	  'https://www.stickeryou.com/products/owasp-juice-shop/794',
	  'http://leanpub.com/juice-shop'
	])
	 
	export const isRedirectAllowed = (url: string) => {
	  let allowed = false
	  for (const allowedUrl of redirectAllowlist) {
	    allowed = allowed || url.includes(allowedUrl)
	  }
	  return allowed
	}
    ```
    - 使用重定向的功能被移除后，未将过时条目 URL 从重定向白名单中删除
        ```typescript
        'https://blockchain.info/address/1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm',
        'https://explorer.dash.org/address/Xr556RzuwX6hg5EGpkybbv5RanJoZN17kW',
        'https://etherscan.io/address/0x0f933ab9fcaaa782d0279c300d73750e1311eae6',
        ```
    - 修复：删除所有过时条目