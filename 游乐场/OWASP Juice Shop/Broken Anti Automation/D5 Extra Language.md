---
title: Extra Language
description: 查看项目页面确定隐藏的资源，获取信息。并结合应用程序已知路径或命名规则推测对应的隐藏内容访问方式
---

- 描述：首先，你应该弄清楚语言在用户界面中是如何从技术上发生变化的。
    找回那个从未投入生产的语言文件。

- 加载语言文件时访问
    ```/assets/i18n/en.json```
- 提示：调查在线实际可用的语言。
- 查看示例解决方案
- 在 OWASP Juice Shop 项目页面
    ```https://owasp.org/www-project-juice-shop/```
    其侧边栏对应多个源
    - 访问
        ```https://crowdin.com/project/owasp-juice-shop```
        语言项目页面可直接看到对应的语言
    - 访问
        ```https://github.com/juice-shop/juice-shop/blob/master/CONTRIBUTING.md#i18n-contributions```
        Github 的语言贡献页面也可发现 crowdin 的语言项目地址
- 访问语言项目地址后找到星际迷航语言 ```Klingon```
    点击进入语言详情页面 ```https://crowdin.com/project/owasp-juice-shop/tlh-AA```
    找到对应结构的语言字符串 ```tlh-AA```
    访问 ```/assets/i18n/tlh_AA.json``` 得到目标语言 JSON 并通过挑战