---
title: Forged Coupon
description: 获得尽可能多的字符串序列，并根据上下文进行分类，对序列模式进行分析。查看依赖项并根据字符类型推测混淆/加密库，实际安装对应库进行解密与生成。查看字符串序列的各种可能来源及其所使用的代码库，此处为优惠券 bot，对工作流程与代码进行分析，在此过程中可能获得更多序列；或者继续探索代码的历史提交变更记录，根据演变推测当前代码使用的 API 或库的内容
---

- 描述：Forge a coupon code that gives you a discount of at least 80%.
- 关联挑战 Forgotten Sales Backup 获取的优惠券代码备份
    ```
    n<MibgC7sn
    mNYS#gC7sn
    o*IVigC7sn
    k#pDlgC7sn
    o*I]pgC7sn
    n(XRvgC7sn
    n(XLtgC7sn
    k#*AfgC7sn
    q:<IqgC7sn
    pEw8ogC7sn
    pes[BgC7sn
    l}6D$gC7ss
    ```
    - 十二个优惠券对应十二个月

- 使用优惠券的请求为
    ```PUT /rest/basket/3/coupon/n%3CMibgC7sn HTTP/1.1```
:x: 未彻底完成，值得之后仔细尝试
- 查看示例解决方案
    - 方向一：根据已知优惠券列表，推测前半为 id 后半为折扣。
    对后半内容进行爆破，直到得到目标折扣兑换券
        - 在方向三查看发送优惠券的bot的日志后，将折扣字符范围缩小到后两位
    - 方向二：由依赖项推测可能的加密/混淆库
    在几个候选库中根据其使用的字符最终剩下 z85 库
        > 使用 ```z85 -d "n<Mibh.u)v"``` 解密此代码返回 JAN17-50
        使用当前月份有效的代码进行 80%或更高折扣的加密，
        例如 ```z85 -e JAN17-80``` ，生成 ```n<Mibh.v0y```
    - 方向三：Juice Shop 在社交媒体使用自动化 bot 在消息中发送优惠券
    搜索得到对应代码库 
    https://github.com/juice-shop/juicy-coupon-bot
    访问 Actions 对应的优惠券工作流
    https://github.com/juice-shop/juicy-coupon-bot/actions/workflows/coupon-distribution.yml
    查看详细 Job，其中 Distribute coupons 步骤包含发放优惠券的细节
    1. 从 API 中得到月份 10%~40% 的4个优惠券
    2. 从中随机选择折扣
    3. 使用选择的折扣更新推送信息
    - 阅读代码，定位 API 的文件
        https://github.com/juice-shop/juicy-coupon-bot/blob/master/lib/currentCoupons.ts
        ```typescript
        export default async (apiEndpoint: string = 'https://5j4d1u7jhf.execute-api.eu-west-1.amazonaws.com/default/JuicyCouponFunc', apiKey: string = process.env.AWS_API_KEY ?? ''): Promise<{ expiryDate: string, discountCodes: Record<string, string> }> => {
            try {
                const res = await fetch(apiEndpoint, {
                method: 'GET',
                headers: {
                    'X-API-Key': apiKey
                }
                })
        ```
        - 从名称 ```currentCoupons.ts``` 以及提交历史 ```Commits on Mar 10, 2025``` 判断，存在旧版优惠券码的代码
        - 浏览上层目录的提交历史
        https://github.com/juice-shop/juicy-coupon-bot/commits/master/lib
        - 定位到最初修改使用 AWS API 的提交
        https://github.com/juice-shop/juicy-coupon-bot/commit/fde2003535598ad3c4edc17ad9ffcdc9c589d3c5#diff-635f0f1089881865008dc19f80d8e65e32dfcece88a9df48b711f850b5808d99
        使用 API 之前的实现为
        ```typescript
        const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

        function toMMMYY (date) {
        const month = date.getMonth()
        const year = date.getFullYear()
        return months[month] + year.toString().substring(2, 4)
        }

        module.exports = (discount, date = new Date()) => {
        const coupon = toMMMYY(date) + '-' + discount
        return z85.encode(coupon)
        ```
        - 确定了对 z85 库的使用以及构建方式
        - 使用并修改旧版 bot 或使用 z85 库手动生成优惠券