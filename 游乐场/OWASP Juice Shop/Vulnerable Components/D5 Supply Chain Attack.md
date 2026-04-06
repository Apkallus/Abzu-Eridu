---
title: Supply Chain Attack
description: 尝试确定已知漏洞时，除了 CVE 编号外也搜索对应版本，定位原发现报告以及官网修复公告。已知漏洞不一定拥有对应 CVE 编号
---

- 描述：通知开发团队 http://127.0.0.1:3000/#/contact  他们的一些凭证存在危险。（发送他们原始报告的URL或分配的CVE或其他标识符）
- 与挑战 Vulnerable Library 相似，只是改为查找开发依赖项的已知漏洞
- 将开发依赖项内容复制到 LLM 聚合查询，其中
    ```
    eslint-scope@3.7.2
    cross-spawn@~5.1
    phantomjs-prebuilt@~2
    karma-phantomjs-launcher@~1.0
    ···
    ```
- 但很难定位 ```eslint-scope@3.7.2``` 的CVE编号
    尝试对此版本使用搜索引擎，第一条即为原发现报告
    ```https://github.com/eslint/eslint-scope/issues/39```
    并且其中包含官网修复与公告
    - 此事件作为供应链攻击，似乎不对应任何 CVE 编号
    https://eslint.org/blog/2018/07/postmortem-for-malicious-package-publishes/
    > 2018 年 7 月 12 日，一名攻击者攻破了 ESLint 维护者的 npm 账号，并将 eslint-scope 和 eslint-config-eslint 软件包的恶意版本发布到 npm 注册中心。