# Abzu-Eridu

## 资源池

#### 文档与靶场

- Web 应用程序渗透测试
    - [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-topics) 
        - 主题文档 + 靶机 + 研究文章
    - [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
        - 基础小节文档 + 与文档同一页面的教学挑战
- 网络安全
    - [pwn.college](https://pwn.college/) 
        - 主题文档 + 靶机 + ASU 公开课

#### 渗透文档

- 速查手册
    - [HackTricks wiki](https://book.hacktricks.wiki/)
        - 综合黑客技术手册
    - [OWASP 速查表系列](https://cheatsheetseries.owasp.org/)
        - 应用程序预防与缓解速查表 
    - [OWASP Community](https://owasp.org/www-community/)
        - 应用程序攻击与漏洞文档
    - PayloadsAllTheThings
- 漏洞库
    - Exploit-DB
- 攻防框架
    - [PTES 渗透测试执行标准](http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines)
    - [OWASP 移动安全测试指南](https://owasp.org/www-project-mobile-security-testing-guide/)
    - [OWASP 固件安全测试方法](https://github.com/scriptingxss/owasp-fstm)
    - [OWASP Web 安全测试指南](https://owasp.org/www-project-web-security-testing-guide/)
        - 黑盒测试技术
    - MITRE ATT&CK

#### 渗透靶场

- web应用程序
    - [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)
        - 本地靶场，单应用集成多挑战，采用 Node.js、Express 和 Angular 编写，完全基于 JavaScript 开发的应用。
    - OWASP Node.js Goat
    - PentesterLab
    - OWASP Damn Vulnerable Serverless
    - Damn Vulnerable GraphQL Application
    

- 综合
    - [vulhub 基于 docker 的靶场](https://github.com/vulhub/vulhub)
        - 漏洞复现型本地综合靶场，基于 docker
    - [Root Me 在线靶场](https://www.root-me.org/)
        - 在线综合靶场
    - VulnHub
    - PwnTillDawn Online
    - [RingZer0 Team Online CTF](https://ringzer0ctf.com/)
        - 在线综合靶场
    - Hacker101 CTF
    - CTFlearn
    - picoCTF
     

- 系统与二进制
    - OverTheWire
    - ropemporium
    - [Exploit Education](https://exploit.education/)

#### 开发文档

- [MDN Web 文档](https://developer.mozilla.org/en-US/docs/Web) （不同于 MDN 开发者教程）
- [sqlcourse](http://www.sqlcourse.com/)

## :infinity: 线路

- 操作系统
    1. ```《C语言程序设计》 何钦铭、颜晖``` 慕课
        - 慕课 [C语言程序设计 - 翁恺](https://www.icourse163.org/course/0809ZJU007A-199001)
        - 教材验证码的 [PTA 编程题目集](https://pintia.cn/problem-sets)
        - 学习方式：教材 + 慕课 + 在线编程题，三者结合作为第一门编程语言的学习足够充分。

    2. ```《深入理解计算机系统》 Randal E. Bryant / David O'Hallaron``` 公开课
        - 公开课[主页](https://csapp.cs.cmu.edu/3e/home.html) 包含：自动 lab、代码、网络旁注
        - 公开课对应 [CMU 的页面](https://www.cs.cmu.edu/~213/schedule.html) 可查看最新 pdf 或 ppt
        - 公开课视频 [B站](https://www.bilibili.com/video/BV1iW411d7hd/)，缺最后一个视频
        - 学习者发布的家庭作业答案 [dreamanddead](https://dreamanddead.github.io/CSAPP-3e-Solutions/) 与 [PaladinChendi](https://github.com/PaladinChendi/CSAPP)，在尽力后查看
        - 学习方式：教材与章节内练习1次 + 公开课视频 + 教材与章节内练习第二次 + 章节后家庭作业与 lab    
            作者提到学习这本书的方式是多次阅读，并且其组织教材结构的抽象化模型聚焦方法在知识学习上很有启发性。  
            值得再次重温，网络旁注的扩展部分也有不少内容。

- 网络
    1. ```《Python编程导论》 John V. Guttag``` 公开课
        - 公开课页面 [MIT ocw 6.100L](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/pages/material-by-lecture/) 包含视频、代码、题目
        - 教材作者在 [Github 公布的教材代码](https://github.com/guttag/Intro-to-Computation-and-Programming)
        - 公开课视频 [B站](https://www.bilibili.com/video/BV1rr421G7nM)
        - 学习方法：图书 + 公开课视频与题目。视频包含大量基本代码讲解。
            公开课仅对应教材的前半部分。中文翻译版是旧版，新版代码间作者的 Github 仓库。    
            第一次接触到了橡皮鸭调试法，虽然之后我与 LLM 进行争论。 
            聚焦于基础语法，信息密度低，有些瞌睡。

    2. ```《Python for Everybody》 Charles Severance``` 公开课程
        - 公开课程[主页](https://www.py4e.com/)，包含在线可下载教材、视频与自动题目
        - 公开课程B站视频 [CS自学社区](https://www.bilibili.com/video/BV1vGbAeYEpz) 与 [中英字幕课程](https://www.bilibili.com/video/BV1b7LwzCEPo)
        - 学习方法：在线课程教材 + 视频 + 自动题目。视频有多个版本，且其中也包含代码讲解。  
            不深入但还是覆盖了一些正则表达式、网络编程、数据库的内容。

    - ```《计算机网络 自顶向下方法》 James F·Kurose / Keith W. Ross``` 公开课程
        - 公开课程[主页](https://gaia.cs.umass.edu/kurose_ross/index.php)  
            - 其中 [wireshark lab](https://gaia.cs.umass.edu/kurose_ross/wireshark.php)、[编程作业](https://gaia.cs.umass.edu/kurose_ross/programming.php) 在图书的对应章节中列出
            - 包含 [视频/幻灯片/章内小节知识检测](https://gaia.cs.umass.edu/kurose_ross/lectures.php) 、[交互式章末习题](https://gaia.cs.umass.edu/kurose_ross/interactive/) 
        - 教材对应的[出版社页面](https://media.pearsoncmg.com/ph/esm/ecs_kurose_compnetwork_8/cw/content/self-assessment-mc/self-assessment-mc.php)包含 互动式动画、选择题/判断题
        - 公开课视频 [B站](https://www.bilibili.com/video/BV1mb4y1d7K7/)，在课程页面查看教材作者之后新增的视频
        - 学习方法：教材紧密结合课程网站的各项资源。    
            作者的课程网站包含大量内容，且随新版发布更新。  
            英文第八版的泄露习题答案可被搜索下载，但不完全对应中文习题。

    - ```《Wireshark数据包分析实战》 Chris Sanders```
        - 作者在 [Github 发布的捕获数据包](https://github.com/chrissanders/packets)

- Web
    - MDN Web开发者教程 [前半部分](https://developer.mozilla.org/en-US/docs/Learn_web_development)
        - 包含教程、讲解与挑战，其合作伙伴 Scrimba 拥有对应的交互式教程
            教程扩展部分不在侧边栏中，使用对应模块介绍页的链接进入

- Web 应用程序渗透测试
    - ```《黑客攻防技术宝典：Web实战篇》 Dafydd Stuttard / Marcus Pinto```
        - 拥有知识架构以及部分过时的内容，但结合作者的 PortSwigger Academy 仍值得阅读。
    - [PortSwigger Web Security Academy](https://portswigger.net/web-security)  文档与 lab
        - 包含[主题文档与对应 lab](https://portswigger.net/web-security/all-topics) 还有[研究](https://portswigger.net/research)，以及 [Burp 工具文档](https://portswigger.net/burp/documentation/contents)。   
            除工具文档外，主题文档、lab也对应 Burp 的各种功能与插件的实际使用。 
            按主题组织的高质量资料，值得反复查看。
- Web
    - MDN Web开发者教程 [后半部分](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions)

- Web 应用程序渗透测试
    1. [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) 靶机
        - 项目拥有挑战的对应指南 [Pwning OWASP Juice Shop](https://pwning.owasp-juice.shop/companion-guide/latest/index.html)，不包含知识文档
        - 综合型靶机，在按主题分类的 PortSwigger 后拥有连贯视角，有一些新奇的挑战。 
            然而由于其性质，无法与 OWASP WSTG 指南一起构建实践框架。

    2. [OWASP Web 安全测试指南](https://owasp.org/www-project-web-security-testing-guide/) 文档
        - 项目主页的排版：标题缺少锚点，并且目录为静态侧边栏。
            直接查看 [Github 文档](https://github.com/OWASP/wstg/tree/master/document)。并且可在 LLM 中直接使用文档的md代码翻译。   
            附录部分的工具、推荐文档等内容也值得查看。  
            Github 项目中拥有对应的 Checklist 检查清单。

    - [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
        - 基于 Java，挑战与小节文档在同一页面而非独立环境，教学型SQL，项目 wiki 的文档缺乏信息。    
            材料质量不一，包含有争议的概念，但一些内容仍值得查看。    
            模块中介绍 ZAP 的使用，[ZAP 工具文档](https://www.zaproxy.org/docs/) 。 
            [cycubix 的解决方案](https://docs.cycubix.com/application-security-series/web-application-security-essentials/solutions)，[IYS 的解决方案](https://inventyourshit.com/labs/webgoat/)

- 网络安全
    1. [pwn.college CSE 365：网络安全导论](https://pwn.college/dojos)   
        CSE 365 还包括对 pwn.college 平台本身的介绍：
        - 拥有定制的 GPT5 “sensai”。    
        - 视频 + 文档 + CTF 型靶机，三者融合在模块化的小节中。
        - 各种内容持续更新  
        
        虽然B站拥有公开课程的LLM翻译视频，但还是使用最新材料。   


## 文档与靶场内容版权

### :book: 署名

- OWASP
    CC-BY-SA 4.0    
    <https://owasp.org/about/#licensing>

- HackTricks
    Attribution Share Adapt  
    <https://book.hacktricks.wiki/en/welcome/hacktricks-values-and-faq.html#license>

#### 署名 不发布解决方案

- pwn.college   
    <https://pwn.college/>
    
### :copyright: 版权声明许可

- MITRE    
    <https://attack.mitre.org/resources/legal-and-branding/terms-of-use/#license>   
    > © 2025 The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation.   

### :lock: 禁止

- PortSwigger   
    <https://portswigger.net/web-security/certification/terms-and-conditions/website-terms-of-use#7-use-of-website-content>

- Root-Me   
    <https://www.root-me.org/?page=structure&inc=page-mentions_legales&lang=en>
