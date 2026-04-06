---
title: Expired Coupon
description: 搜索关键字获得过期优惠代码。查看日期验证代码获取有效日期，修改本机时间为对应优惠代码的有效日期。查看语言使用函数的文档或在控制台中实际输入以了解用法
---

- 描述：Successfully redeem an expired campaign coupon code.
- 查看示例解决方案
    - 在 ```main.js``` 中搜索关键词 ```campaign```
        得到代码、有效日期、折扣幅度
        ```javascript
        WMNSDY2019: {
            validOn: 15519996e5,
            discount: 75
        }
        ```
        - 尝试使用将得到 ```Invalid coupon.``` 提示
    - 继续浏览，验证优惠代码有效性的 JavaScript 代码：
        UTC+0的0点时间戳 = 当前时间-当前时区偏移的毫秒数
        ```javascript
        applyCoupon() {
            this.campaignCoupon = this.couponControl.value, this.clientDate = new Date;
            const e = 60 * (this.clientDate.getTimezoneOffset() + 60) * 1e3;
            this.clientDate.setHours(0, 0, 0, 0), this.clientDate = this.clientDate.getTime() - e, sessionStorage.setItem("couponDetails", `${this.campaignCoupon}-${this.clientDate}`);
            const o = this.campaigns[this.couponControl.value];
            o ? this.clientDate === o.validOn ? this.showConfirmation(o.discount) : (this.couponConfirmation = void 0, this.translate.get("INVALID_COUPON")
        ```
        日期转换，将科学计数法数字转为普通毫秒时间戳，使用 Data 对象将毫秒时间戳转换为日期
        ```javascript
        let timestampStr = '15519996e5'; 
        let timestamp = Number(timestampStr);
        let date = new Date(timestamp); 
        ```
        得到 ```Mar 08 2019```