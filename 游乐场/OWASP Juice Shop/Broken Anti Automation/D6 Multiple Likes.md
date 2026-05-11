---
title: Multiple Likes
description: 测试请求的竞态条件，burp的多个页面同时发送或使用增强攻击器扩展设置内容后同时发送
---

- 描述；Like any review at least three times as the same user.
- 竞态条件
    - 点击 like 时发送的请求为
    ```POST /rest/products/reviews HTTP/1.1```
    ```{"id":"x5Mn7bHYmD4BiZLbY"}```
    - 使用 Burp 开启3个相同标签并放入一组中，选择最后一比特同时发送。
    - 或使用burp的增强攻击器扩展，在gate中加入多个重复请求后释放

- 示例解决方案仅使用脚本连续发送3次，此方法对竞态条件的测试较弱