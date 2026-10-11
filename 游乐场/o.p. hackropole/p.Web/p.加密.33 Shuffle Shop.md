You have just entered a castle…

Note: This challenge has been made for the finale of FCSC 2020.

```yaml
services:
  shuffle-shop:
    image: anssi/fcsc2020-web-shuffle-shop:latest
    ports:
      - "8000:80"

```




## 侦察、探测、代码审计

访问首页 `/`
- 响应
    ```http
    HTTP/1.1 200 OK
    Server: Apache/2.4.54 (Debian)
    X-Powered-By: PHP/7.4.33
    Set-Cookie: PHPSESSID=b9dbb37c8b69e7a079361fb130371c63; path=/
    Expires: Thu, 19 Nov 1981 08:52:00 GMT
    Set-Cookie: PHPSESSID=5806f52cd8fe89ae864e990692a3675c; path=/
    ```
    
    ```html
    <form action="shuffleshop.php">
        <input type="submit" value="Entrer" />
    </form>
    ```
    - 功能
    - 信息端点
    
    - 兴趣点
        - 特异注释

访问 `/shuffleshop.php`
- 响应
    ```html
    <script>
        // 兴趣点 `"Flag potion","price":100000`
        var potions = JSON.parse('[{"idx":0,"name":"Health potion","price":10,"color":"#ff0000"},{"idx":1,"name":"Stamina potion","price":10,"color":"#33cc33"},{"idx":2,"name":"Strengh potion","price":15,"color":"#996633"},{"idx":3,"name":"Clerverness potion","price":15,"color":"#99ffcc"},{"idx":9,"name":"Flag potion","price":100000,"color":"#ffff00"},{"idx":4,"name":"Breath potion","price":25,"color":"#00ffcc"},{"idx":5,"name":"Invisible potion","price":30,"color":"#ffffcc"},{"idx":6,"name":"Fly potion","price":59,"color":"#ff99ff"},{"idx":7,"name":"Love potion","price":99,"color":"#ff0066"},{"idx":8,"name":"Fire-protection potion","price":67,"color":"#ff6600"}]');
        var cart_enc = "";
        var p1 = 0,
            p2 = 1,
            p3 = 2;

        // 设置3个元素以显示3个药水信息
        function displayPotions() {
            document.getElementById('potion_name_1')
                .innerHTML = potions[p1]['name'];
            document.getElementById('potion_name_1')
                .style = "background-color:" + potions[p1]['color'];
            document.getElementById('potion_price_1')
                .innerHTML = potions[p1]['price'];
            document.getElementById('potion_buy_1')
                .onclick = function() {
                    addItem(potions[p1]['idx']);
                };

            ...
        }

        // 药水洗牌后显示药水信息，从 json 中随机选择药水
        function shuffleStand() {
            var max = potions.length;
            p1 = Math.floor(Math.random() * max);
            p2 = Math.floor(Math.random() * max);
            p3 = Math.floor(Math.random() * max);
            displayPotions();
        }

        // 端点 cart.php
        /// 参数 `add` `idx=`
        /// 使用硬币，成功时调用 `refreshCart`
        function addItem(idx) {
            var xhr_addItem = new XMLHttpRequest();
            xhr_addItem.open("GET", "cart.php?add&idx=" + idx, true);
            xhr_addItem.onload = function() {
                if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                    if (this.responseText === "not enough FCSC-coins")
                        alert("Le montant de votre panier ne peut pas dépasser la quantité de FCSC-coins que vous possédez !");
                    else if (this.responseText === "potion added")
                        refreshCart();
                }
            }
            xhr_addItem.send();
        }


        function refreshCart() {
            // 端点 cart.php
            /// 参数 refresh
            /// 成功时设置 `id=cart` 元素的 HTML 为响应文本
            var xhr_refreshCart = new XMLHttpRequest();
            xhr_refreshCart.open("GET", "cart.php?refresh", true);
            xhr_refreshCart.onload = function() {
                if (this.readyState === XMLHttpRequest.DONE && this.status === 200)
                    document.getElementById('cart')
                    .innerHTML = this.responseText;
            }

            // 端点 cart.php
            /// 参数 refreshEnc
            /// 成功时设置 JS 变量 `cart_enc` 的值为响应文本
            var xhr_refreshCartEnc = new XMLHttpRequest();
            xhr_refreshCartEnc.open("GET", "cart.php?refreshEnc", true);
            xhr_refreshCartEnc.onload = function() {
                if (this.readyState === XMLHttpRequest.DONE && this.status === 200)
                    cart_enc = this.responseText;
            }

            xhr_refreshCart.send();
            xhr_refreshCartEnc.send();
        }

        // 提交购物车
        /// 端点 cart.php
        /// 参数 `validate` `cart=cart_enc`
        function validateCart() {
            refreshCart();
            var xhr_validateCart = new XMLHttpRequest();
            xhr_validateCart.open("GET", "cart.php?validate&cart=" + cart_enc, true);
            xhr_validateCart.onload = function() {
                if (this.readyState == XMLHttpRequest.DONE && this.status === 200)
                    alert(this.responseText);
            }
            xhr_validateCart.send();
        }
    </script>
    ```

    ```html
    <table border="1|0">
        <tr align="center">
            <td>
                <div id="potion_name_1"></div>
                <div id="potion_price_1"></div>
            </td>
            <td>
                <div id="potion_name_2"></div>
                <div id="potion_price_2"></div>
            </td>
            <td>
                <div id="potion_name_3"></div>
                <div id="potion_price_3"></div>
            </td>
        </tr>
        <tr align="center">
            <td><input type="button" id="potion_buy_1" value="add" onclick></td>
            <td><input type="button" id="potion_buy_2" value="add"></td>
            <td><input type="button" id="potion_buy_3" value="add"></td>
        </tr>
    </table>

    <input type="button" onclick="shuffleStand()" value="Shuffle !"><br /><br />
    You have : 5000 FCSC-coins.<br />
    Your current cart : <br />
    <div id="cart" style="background-color:#996633" width="50px">
    </div><br /><br />
    <input type="button" value="Confirm cart" onclick="validateCart()" />
    <script>
        // 加载页面立即显示药水，并刷新一次
        displayPotions();
        refreshCart();
    </script>
    ```

- 查看浏览器 JS 请求1
    ```http
    GET /cart.php?refresh HTTP/1.1
    Host: 127.0.0.1:8000
    ```
    - 响应 
        ```json
        {
            "total": 0,
            "Health potion": 0,
            "Stamina potion": 0,
            "Strengh potion": 0,
            "Clerverness potion": 0,
            "Flag potion": 0,
            "Breath potion": 0,
            "Invisible potion": 0,
            "Fly potion": 0,
            "Love potion": 0,
            "Fire-protection potion": 0
        }
        ```

- 查看浏览器 JS 请求2
    ```http
    GET /cart.php?refreshEnc HTTP/1.1
    Host: 127.0.0.1:8000
    ```
    - 响应
        ```
        4861d347d2f39fa406fb3b08f52982fe85d2927560d60fcf9d3c02e25e4f6f35f2df39dd23ed5845714a65ffb50a46e65150d1dec636fa71795100b5f07d4d7b05014d5e28fe8398ebbd11fe6b435b464d3cacf1a1c0d4e5b773c33c3c0f76b186d8f97992c0e811e680b8a2e7296fc82230982213a37ee2600f3293d47df45ceaa228e31358c18a1bd4079e9123a8a9e1d2e9a9fea06c969cf7a944df14394cde8a8f32d3cfd3c63a9f3e236b7d550de3f52fb891a0ed8ec7bf1e8d5af638099efe9cde6992f140ffb1258723c03760
        ```

分析
- 药水购物应用
- `"Flag potion","price":100000` 似乎即为关键商品，
- 拥有硬币 `5000 FCSC-coins`

购买普通药水
- 添加到购物车
    ```http
    GET /cart.php?add&idx=0 HTTP/1.1
    ```
    - 响应
        ```
        potion added
        ```
- 添加操作自动触发浏览器普通刷新与加密刷新
    - 普通刷新
        ```http
        GET /cart.php?refresh HTTP/1.1
        ```
        - 响应
            ```json
            {"total":10,"Health potion":1...
            ```

    - 加密刷新
        ```http
        GET /cart.php?refreshEnc HTTP/1.1
        ```

- 提交购物车
    ```http
    GET /cart.php?validate&cart=3fc02ee86c92c5429c1753f560b9e67942a7e665b7f40ec8f7c7a52e866b3e5458a831353216845122eb26a951ac29eee049440c06e50aec529fb14bdbbe81d4e0af636931ea0d18f030c8a9453679a11fb40b1f3f7881835386e2113d8b77773c7e45712b14444d470cfe46c6f9b27a53d2da2e395063a67047ecc49dec5aba568c3df55964d7d3bab704e701831c3429e83a4493fd102cd9b49d2ada8b68d1a04cb37d89749b3254e1933360286b8fa0ca8a3aa1e227b75d2a0e3baa91aac35cc148da97c5cdd3cde4a35494765949 HTTP/1.1
    ```
    - 使用加密刷新序列

- 若尝试添加 flag 药水，则立即回显错误信息
    ```http
    GET /cart.php?add&idx=9 HTTP/1.1
    ```

    - 响应
        ```http
        not enough FCSC-coins
        ```



查看其他挑战者的解决方案，当前挑战为 ECB 型挑战
- ⚠️ 暂停直到回顾二进制密码主题时继续 ⚠️

## 端点功能

`/shuffleshop.php`
- 功能
    - 显示3个药水
    - 导航到刷新与提交


`cart.php`
- 功能

    - 添加药水到购物车，`shuffleshop.php` 点击药水的 `add` 按钮触发
        - 参数 
            - `add` 
            - `idx=`

        - 兴趣点
            - `idx`
                - 设置参数列表 `idx[]=`，添加药水 `Stamina potion`
                - 设置空参数值 `idx=`，添加药水 `Health potion`
                - 多个参数，最后一个有效
                - 设置非数字参数值 `idx=x`，添加药水 `Health potion`
                - 设置 flag 药水时显示硬币不足，似乎添加时立即检测，或许提交购物车时不检测

    
    - 刷新，获得浏览器显示数据 JSON
        - 参数 
            - `refresh`
        - 成功时设置 `id=cart` 元素的 HTML 为响应 JSON
        - 兴趣点
            - 空 cookie 时购物车内容为全0


    - 加密刷新，获得购物车加密序列
        - 参数 
            - `refreshEnc`
        - 成功时设置 JS 变量`cart_enc` 的值为响应购物车加密序列
        - 兴趣点
            - 相同购物车组合，总会获得相同加密序列
            - 加密序列在客户端保存，或包含结账信息


    - 提交购物车加密序列，`shuffleshop.php` 点击 `Confirm cart` 按钮触发
        - 参数 
            - `validate` 
            - `cart=cart_enc`
                - 使用加密刷新序列
                - 获得错误信息
                - 或仅提交加密序列而无额外验证
                
## 兴趣点

收集一批加密序列，从空购物车开始

```
// 空
4861d347d2f39fa406fb3b08f52982fe85d2927560d60fcf9d3c02e25e4f6f35f2df39dd23ed5845714a65ffb50a46e65150d1dec636fa71795100b5f07d4d7b05014d5e28fe8398ebbd11fe6b435b464d3cacf1a1c0d4e5b773c33c3c0f76b186d8f97992c0e811e680b8a2e7296fc82230982213a37ee2600f3293d47df45ceaa228e31358c18a1bd4079e9123a8a9e1d2e9a9fea06c969cf7a944df14394cde8a8f32d3cfd3c63a9f3e236b7d550de3f52fb891a0ed8ec7bf1e8d5af638099efe9cde6992f140ffb1258723c03760

// 添加 id=4
2aa79e98bd8d3ca7ae4248a763fce2c2d04f5ef584029a718b779a05967bae0b58a831353216845122eb26a951ac29eee049440c06e50aec529fb14bdbbe81d4e0af636931ea0d18f030c8a9453679a11fb40b1f3f7881835386e2113d8b77773c7e45712b14444d470cfe46c6f9b27a26a167f1943e2e38eb4aceb0068bfeb4568c3df55964d7d3bab704e701831c3429e83a4493fd102cd9b49d2ada8b68d1a04cb37d89749b3254e1933360286b8fa0ca8a3aa1e227b75d2a0e3baa91aac35cc148da97c5cdd3cde4a35494765949

// 添加 id=7
182f1028c694dc90271ca372d79b7a792e6a2ead8ffedc65d63bf0487d0dcf93945f3a84de7a5dec02e37b989ef5b34a86b776657b3fcb21f34c5cfca0fcf5b3438abca18111786fb9061c1329d144e0106d3e759e3cf6e24d9f4f4da883b77ef87de20cdd9d759d072403a624edff49b2a5c57fef1ff26a9402e46ed4093a3f8f63b9fd8a5abbd653896257224ef664f4b932d0ad4499dc1afe3a72cbc967e1fda642d12f7e1cbd4ab56e76e04ffb60d01256ad6714c58cdbf37c48a5550226fff09bf815380467ad30093ebf62c692

// 第二次添加 id=7
2a5bda20aa2429a9709648a2e93eabb72e6a2ead8ffedc65d63bf0487d0dcf93945f3a84de7a5dec02e37b989ef5b34a86b776657b3fcb21f34c5cfca0fcf5b3438abca18111786fb9061c1329d144e0106d3e759e3cf6e24d9f4f4da883b77ef87de20cdd9d759d072403a624edff49b2a5c57fef1ff26a9402e46ed4093a3f8f63b9fd8a5abbd653896257224ef664f4b932d0ad4499dc1afe3a72cbc967e1fda642d12f7e1cbd4ab56e76e04ffb60e583591424585a8d3320621fb931da3efff09bf815380467ad30093ebf62c692

// 第三次添加 id=7
88080791dfd4c26e8844af770b8f71c42e6a2ead8ffedc65d63bf0487d0dcf93945f3a84de7a5dec02e37b989ef5b34a86b776657b3fcb21f34c5cfca0fcf5b3438abca18111786fb9061c1329d144e0106d3e759e3cf6e24d9f4f4da883b77ef87de20cdd9d759d072403a624edff49b2a5c57fef1ff26a9402e46ed4093a3f8f63b9fd8a5abbd653896257224ef664f4b932d0ad4499dc1afe3a72cbc967e1fda642d12f7e1cbd4ab56e76e04ffb6060531b6b1cb84ab5e2d3b92ccb1cfc90fff09bf815380467ad30093ebf62c692

// 第二次添加 id=4
1ad659057186d37ea35f342cb57923fc2e6a2ead8ffedc65d63bf0487d0dcf93945f3a84de7a5dec02e37b989ef5b34a86b776657b3fcb21f34c5cfca0fcf5b3438abca18111786fb9061c1329d144e0106d3e759e3cf6e24d9f4f4da883b77ef87de20cdd9d759d072403a624edff49eb626dae008e7ea4cce6bba7d00f5b7b8f63b9fd8a5abbd653896257224ef664f4b932d0ad4499dc1afe3a72cbc967e1fda642d12f7e1cbd4ab56e76e04ffb6060531b6b1cb84ab5e2d3b92ccb1cfc90fff09bf815380467ad30093ebf62c692
```
- 分析
    - 每次添加不同 id 时，序列似乎完全变化
    - 连续添加相同 id 时，序列仅变化开头与接近结尾的一小部分
    - 或许在切换商品时重构，而当前商品数量递增时仅部分修改

## 错误信息

`/cart.php?validate&cart=`
- 单个字符
    ```http
    GET /cart.php?validate&cart=x HTTP/1.1
    ```
    ```html
    <br />
    <b>Warning</b>: hex2bin(): Hexadecimal input string must have an even length in <b>/var/www/html/libssl.php</b> on line <b>20</b><br />
    You should have the flag potion in your cart to win
    ```
    - 使用函数 `hex2bin()`
    - 文件 `/var/www/html/libssl.php`
    - 错误由于二进制字符串转换时，字符数量不足导致异常