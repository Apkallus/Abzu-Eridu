---
title: Video XSS
description: 分析前端页面自动生成的代码，定位到对应的路径生成库，而已知的前端框架集成了此库。得到此库的默认路径生成信息与路径名后继续推测可能的路径，分析常见或可能的开发目录构建方式探测或爆破路径
---

- 描述：Embed an XSS payload ```</script><script>alert(`xss`)</script>``` into our promo video.

- 搜索 ```Juice Shop promo video```无法得到相关信息
- 查看示例解决方案
    - > 作者在 v8.5.0 通过个人账户发布了一条关于新促销视频的推文，公开剧透 URL http://localhost:3000/promotion
    - 推文的视频链接为 
    http://juice-shop-staging.herokuapp.com/promotion
    可从 URL 地址反推到本地应用程序 URL
    - 但实际上只是 OWASP 的介绍视频，与 Juice Shop 无关

- 访问此地址加载的媒体
    ```GET /video HTTP/1.1```
    响应为
    ```
    Content-Location: /assets/public/videos/owasp_promo.mp4
    Content-Type: video/mp4
    ```
    - 访问此地址 ```/assets/public/videos/owasp_promo.mp4``` 可获得视频
    - 访问上层目录，无索引
- 查看 HTML 元素
    得到字幕脚本
    ```html
    <script id="subtitle" type="text/vtt" data-label="English" data-lang="en">WEBVTT

    00:00:01.396 --> 00:00:03.219
    OWASP is a non profit

    00:00:03.219 --> 00:00:06.564
    that stands for the Open Web Application Security Project!
    </script>
    ```
    - 得到字幕类型为 vtt
    > 一个幸运的猜测是视频旁边应该有一个相应的 .vtt 文件。
    - 尝试访问字幕文件 ```GET /assets/public/videos/owasp_promo.vtt HTTP/1.1```
        响应为字幕文本

- 关联挑战 Arbitrary File Write 的 zip 文件上传
    文件上传端点 ```http://127.0.0.1:3000/#/complain```
    文件覆盖路径 ```../../assets/public/videos/owasp_promo.vtt```
    - 失败，未能覆盖目标字幕文件，但此处应当已经遍历到根目录
    > 这可能意味着存在一个更深层的目录结构，其中 assets/ 位于其中。



- > 你可以从 http://localhost:3000/main.js 以及你在浏览器开发者工具的"源"标签页中找到的其他几个 JavaScript 文件中，通过它们都以 "use strict";(self.webpackChunkfrontend=self.webpackChunkfrontend||[]) 开头这一事实，获取一个可能的基目录 frontend/ 的提示，其中 frontend 是 Angular 项目名称。
    - 对开头的分析指向 - Webpack 自动生成
    - 对 Webpack 与 Angular 框架的分析得到
    > 1. Webpack 的集成和运行时代码生成由 Angular CLI 自动管理
    > 2. webpackChunk 后的 frontend 是 Webpack 配置中的 output.chunkLoadingGlobal 值，Angular CLI 默认使用项目名称（或 frontend 作为占位符）生成。
    > 3. 常规路径：Angular 构建后最终的静态资源位于 /dist/frontend（项目名 frontend 时）

- > 无论是通过密集的暴力破解、幸运的猜测还是大量的谷歌搜索，你最终可能会找到一个路径前缀为 frontend/dist/frontend/ ，而服务器上存在 assets/ 的路径。因此，你需要处理的路径是 frontend/dist/frontend/assets/
    - 反推：前端项目位于 /frontend 目录下，在其中使用 Angular 框架生成路径得到 /frontend/dist/frontend
    - 或者在尝试 /frontend 与 /dist/frontend 均无效的时候推测还存在更深的目录

    1. 你可以轻易找到许多 Angular 示例，其中一些 dist/ 文件夹参与了应用程序打包
    2. 通过 Google 你可能会偶然发现 https://vorozco.com/blog/2019/2019-09-11-Packagin-Angular-8-Apps-War.html，其中提到他们的包文件夹是 <directory>src/main/frontend/dist/frontend</directory> 。
    3. 你可以创建一个可能涉及的包名列表，然后针对这些包创建不同的 Zip Slip 有效载荷，逐步添加一个甚至两个额外的递归，进入更深层的目录级别。
    4. 只要你的列表中包含 frontend 和 dist ，最终你会在深度为 3 的层面上得到 frontend/dist/frontend 的正确排列。

- 提供的载荷关闭上下文中加载字幕的脚本标签后，在新脚本标签中执行代码