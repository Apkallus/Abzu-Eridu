平台项目
- 偏好资产类型
    - Open Scope 开放范围
    - Close Scope 封闭范围：
        - Other Asset：
            - Any/Other 广泛的资产
            - 有时提供包含详细 IP 范围的文档链接
        - CIDR：专用网段

- 状态
    - 更新：或许新增有趣的资产类别，查看详细描述

邮箱别名 
- hackerone 
    `[username]@wearehackerone.com`
- intigriti
    `[yournickname]@intigriti.me`

HTTP 自定义头
- `X-Bug-Bounty: Hackerone-<username>`
    - 在 burp - tools - proxy - http match and replace rules 添加 http 请求头：match 留空，replace 填入自定义头部
    - 勾选“仅添加到范围内项目”


burp 的组织器保留有趣的请求响应，也有笔记功能

由于现代 web app 使用大量 js，以及重定向，点击链接以查看最终访问地址

