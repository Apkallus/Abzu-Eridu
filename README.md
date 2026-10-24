# Abzu-Eridu

markdown

emoji:
- 🌟 核心资源
- ♾️ 持续使用的资源
- 📌 当前
- 📅 之后
- 🔍 待查看
- ❓ 未定
- ⏸️ 搁置
- 🎯 兴趣点
- 🖇️ 关联到兴趣点
- ⚔️ 载荷工具
- 🛠️ 普通工具
- 🥷 混淆工具

文件目录名：
- `o` 进行中
- `x` 终止
- `p` 暂停，待恢复
- `__` 描述
- 格式
    - `p.暂停标记.原序号. 原文件名`
        - 恢复并完成后删除开头标记
    - 文件标记传递到目录

文件内标记
- `v`

类型：
- 二进制利用
- 网络渗透
- web 应用程序渗透
- 专项：
    - 云渗透


## 资源池

导航中的导航
- [awesome-hacking](https://github.com/hack-with-github/awesome-hacking)

### 文档与靶场

- Web 应用程序渗透测试
    - [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-topics) 🌟 ♾️
        - 主题文档 + 靶机 + 研究文章
    - [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
        - 基础小节文档 + 与文档同一页面的教学挑战
- 二进制漏洞
    - [pwn.college](https://pwn.college/) 🌟 ♾️
        - 模块文档 + 模块视频 + 靶机（+ ASU 直播公开视频）
    - [ost2.fyi](https://ost2.fyi/) 
    - [Malwareunicorn.org](https://malwareunicorn.org/#/) ❓
        - 恶意代码逆向

### 文档

- 速查手册、载荷示例
    - [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) ♾️
    - [HackTricks wiki](https://book.hacktricks.wiki/) 📌
        - 实战化攻防技巧百科，覆盖渗透全流程各类服务与场景。
    - [Hacker Recipes](https://www.thehacker.recipes/) 📌
        - 按“配方”组织的攻击路径手册，侧重红队与内网渗透流程。
    - [OWASP 速查表系列](https://cheatsheetseries.owasp.org/)
        - 开发/防御向的 Web 安全最佳实践速查文档。
    - [OWASP Community](https://owasp.org/www-community/)
        - 社区维护的 Web 安全知识与漏洞分类参考库。

        - 按漏洞分类的常用 payload 与技巧合集。
    - [二进制挑战文档](https://guyinatuxedo.github.io/index.html)

- 漏洞库
    - Exploit-DB
- 攻防框架
    - [OWASP WSTG Web 安全测试指南](https://owasp.org/www-project-web-security-testing-guide/) ♾️
        - Web 应用程序黑盒测试框架与细节

    - [PTES 渗透测试执行标准](http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines) 📌
    - ~~[OWASP 移动安全测试指南](https://github.com/OWASP/mastg)~~
    - [OWASP 固件安全测试方法](https://github.com/scriptingxss/owasp-fstm)
    - MITRE ATT&CK
    - NIST SP 800-115 
    - OSSTMM v3

### 靶场

- web应用程序
    - [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)
        - 本地靶场，单应用集成多挑战，前后端都基于 JavaScript 开发。
    - [Hacker101 CTF](https://ctf.hacker101.com/)

    - OWASP Node.js Goat
    - PentesterLab
    - OWASP Damn Vulnerable Serverless
    - [Damn Vulnerable GraphQL Application](https://github.com/digininja/DVWA)
    
    

- 综合
    - [Root Me](https://www.root-me.org/?lang=en) ♾️
    - [picoCTF -> CyLab Security Academy](https://cylabacademy.org) ♾️
    - [hackropole](https://hackropole.fr/en/) 本地 docker 靶场 ♾️

    - http://vulnstack.qiyuanxuetang.net/vuln/
    - https://github.com/zhuifengshaonianhanlu/pikachu

    - [thehackerslabs](https://labs.thehackerslabs.com/) 本地靶场 ⏸️
        - 三分之一靶机使用会员
    - [RingZer0 Team Online CTF](https://ringzer0ctf.com/) 本地/在线靶场 ⏸️
        - 部分挑战缺乏分类
    - [echoctf](https://echoctf.red) openvpn 网络靶场 ⏸️
     
- 网络主机
    - [VulnHub](https://www.vulnhub.com/) 本地靶场
    - [Metasploitable3](https://github.com/rapid7/metasploitable3) 本地靶机 
    - [vulhub](https://github.com/vulhub/vulhub) docker 本地靶场
    - [hackmyvm.eu](https://hackmyvm.eu/) 本地靶场
    - [PwnTillDawn Online](https://online.pwntilldawn.com/) openvpn 网络靶场 ⏸️       

- 系统与二进制
    - [Exploit Education](https://exploit.education/)
    - OverTheWire 
    - ropemporium
    - https://crackmes.one/
    - https://pwnable.tw/challenge/
    - https://pwnable.kr/index.php
    - https://pwnable.xyz/

- 密码
    - [Cryptopals](https://cryptopals.com/) ❓
    - https://mysterytwister.org/
    
- 集群：
    - [vulnerable-AD](https://github.com/safebuffer/vulnerable-AD)
    - [BadBlood](https://github.com/davidprowe/BadBlood)
    - [GOAD](https://github.com/Orange-Cyberdefense/GOAD) 
    - NetExec
        - lab https://github.com/Pennyw0rth/NetExec-Lab
        - 工具 https://github.com/Pennyw0rth/NetExec
            - 使用说明 https://www.netexec.wiki/
    - https://github.com/madhuakula/kubernetes-goat

- 云
    - [导航](https://github.com/iknowjason/Awesome-CloudSec-Labs)
    - http://flaws.cloud/ 与 http://flaws2.cloud 
    - [wiz](https://www.wiz.io/ctf) 云复合靶场

- 开源情报侦察
    - [gralhix](https://gralhix.com/list-of-osint-exercises/)
    - [diverctf](https://diverctf.org/en.html)
    - [Bellingcat](https://challenge.bellingcat.com/) 

### 图书/可用

逆向
- Rootkits and Bootkits
- 《恶意代码分析实战 Practical Malware Analysis》
- 《逆向工程实战 Practical Reverse Engineering》
- https://www.ghidrabook.com/





- 《深入解析Windows操作系统 第7版》(Windows Internals, Part 1/2)

- Security Engineering: A Guide to Building Dependable Distributed Systems 3rd Edition, by Ross Anderson (Author)   
    <https://www.cl.cam.ac.uk/archive/rja14/book.html>

- 《Ethical Hacking: A Hands-on Introduction to Breaking In》 - Daniel G. Graham

- 《From Day Zero to Zero Day》- Eugene Lim

- 《Penetration Testing Azure for Ethical Hackers》 - David Okeyode, Karl Fosaaen

- 《网络渗透测试的艺术》（The Art of Network Penetration Testing）- Royce Davis

- A Bug Hunter's Diary

#### 教科书

汇编
- The Art of 64-Bit Assembly, Volume 1
- Modern X86 Assembly Language Programming
- [Reverse Engineering for Beginners](https://beginners.re/)

elf
- Learning Linux Binary Analysis
- Linkers and Loaders

操作系统
- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)
- linux 编程接口

专项
- Game Hacking: Developing Autonomous Bots for Online Games 
- Practical IoT Hacking

### 开发文档

- [MDN Web 文档](https://developer.mozilla.org/en-US/docs/Web) （不同于 MDN 开发者教程）
- [sqlcourse](http://www.sqlcourse.com/)
- [Microsoft Learn](https://learn.microsoft.com/zh-cn/security/)
    
### 公开课

- [pwn.college CSE 598: 应用漏洞研究](https://pwn.college/cse598-avr-f2024/) 公开课程 ❓
    - XNU 内核与 ARM64 架构
    - 当前公开课直播 Youtube 视频为 2024 fall 

- [MIT 6.S081 操作系统工程](https://pdos.csail.mit.edu/6.S081/2025/index.html) ❓
    操作系统的设计与实现，以及其作为系统编程基础的作用

- [MIT 6.858: Computer System Security](https://css.csail.mit.edu/6.858/2022/)

- [RPISEC Modern Binary Exploitation](https://github.com/RPISEC/MBE) ❓
    二进制漏洞利用课程的材料，旨在教授漏洞研究、逆向工程和二进制漏洞利用方面的技能。

## 线路

1. 操作系统
    1. `《C语言程序设计》 何钦铭、颜晖` 慕课
        - 慕课 [C语言程序设计 - 翁恺](https://www.icourse163.org/course/0809ZJU007A-199001)
        - 教材验证码的 [PTA 编程题目集](https://pintia.cn/problem-sets)
        - 学习方式：教材 + 慕课 + 在线编程题，三者结合作为第一门编程语言的学习足够充分。

    2. `《深入理解计算机系统》 Randal E. Bryant / David O'Hallaron` 公开课
        - 公开课[主页](https://csapp.cs.cmu.edu/3e/home.html) 包含：自动 lab、代码、网络旁注
        - 公开课对应 [CMU 的页面](https://www.cs.cmu.edu/~213/schedule.html) 可查看最新 pdf 或 ppt
        - 公开课视频 [B站](https://www.bilibili.com/video/BV1iW411d7hd/)，缺最后一个视频
        - 学习者发布的家庭作业答案 [dreamanddead](https://dreamanddead.github.io/CSAPP-3e-Solutions/) 与 [PaladinChendi](https://github.com/PaladinChendi/CSAPP)，在尽力后查看
        - 学习方式：教材与章节内练习1次 + 公开课视频 + 教材与章节内练习第二次 + 章节后家庭作业与 lab    
            - 作者提到学习这本书的方式是多次阅读，并且其组织教材结构的抽象化模型聚焦方法在知识学习上很有启发性。  
            - 值得再次重温，网络旁注的扩展部分也有不少内容。

2. 网络
    1. `《Python编程导论》 John V. Guttag` 公开课
        - 公开课页面 [MIT ocw 6.100L](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/pages/material-by-lecture/) 包含视频、代码、题目
        - 教材作者在 [Github 公布的教材代码](https://github.com/guttag/Intro-to-Computation-and-Programming)
        - 公开课视频 [B站](https://www.bilibili.com/video/BV1rr421G7nM)
        - 学习方法：图书 + 公开课视频与题目。视频包含大量基本代码讲解。
            - 公开课仅对应教材的前半部分。中文翻译版是旧版，新版代码间作者的 Github 仓库。    
            - 第一次接触到了橡皮鸭调试法，虽然之后我与 LLM 进行争论。 
            - 聚焦于基础语法，信息密度低，有些瞌睡。

    2. `《Python for Everybody》 Charles Severance` 公开课程
        - 公开课程[主页](https://www.py4e.com/)，包含在线可下载教材、视频与自动题目
        - 公开课程B站视频 [CS自学社区](https://www.bilibili.com/video/BV1vGbAeYEpz) 与 [中英字幕课程](https://www.bilibili.com/video/BV1b7LwzCEPo)
        - 学习方法：在线课程教材 + 视频 + 自动题目。视频有多个版本，且其中也包含代码讲解。  
            - 不深入但还是覆盖了一些正则表达式、网络编程、数据库的内容。

    3. `《计算机网络 自顶向下方法》 James F·Kurose / Keith W. Ross` 公开课程
        - 公开课程[主页](https://gaia.cs.umass.edu/kurose_ross/index.php)  
            - 其中 [wireshark lab](https://gaia.cs.umass.edu/kurose_ross/wireshark.php)、[编程作业](https://gaia.cs.umass.edu/kurose_ross/programming.php) 在图书的对应章节中列出
            - 包含 [视频/幻灯片/章内小节知识检测](https://gaia.cs.umass.edu/kurose_ross/lectures.php) 、[交互式章末习题](https://gaia.cs.umass.edu/kurose_ross/interactive/) 
        - 教材对应的[出版社页面](https://media.pearsoncmg.com/ph/esm/ecs_kurose_compnetwork_8/cw/content/self-assessment-mc/self-assessment-mc.php)包含 互动式动画、选择题/判断题
        - 公开课视频 [B站](https://www.bilibili.com/video/BV1mb4y1d7K7/)，在课程页面查看教材作者之后新增的视频
        - 学习方法：教材紧密结合课程网站的各项资源。    
            - 作者的课程网站包含大量内容，且随新版发布更新。  
            - 英文第八版的泄露习题答案可被搜索下载，但不完全对应中文习题。

    - `《Wireshark数据包分析实战》 Chris Sanders`
        - 作者在 [Github 发布的捕获数据包](https://github.com/chrissanders/packets)
        - 命令行数据捕获内容暂略

3. Web 应用程序渗透
    - [MDN Web开发者教程](https://developer.mozilla.org/en-US/docs/Learn_web_development)
        - 包含教程、讲解与挑战，其合作伙伴 Scrimba 拥有对应的交互式教程
            - 教程扩展部分不在侧边栏中，使用对应模块介绍页的链接进入

    - `《黑客攻防技术宝典：Web实战篇（The Web Application Hacker’s Handbook）》 Dafydd Stuttard / Marcus Pinto`
        - 拥有知识架构以及部分过时的内容，但结合作者的 PortSwigger Academy 仍值得阅读。
    - [PortSwigger Web Security Academy](https://portswigger.net/web-security)  Web 文档与 lab
        - 包含
            - [主题文档与对应 lab](https://portswigger.net/web-security/all-topics) 
            - [研究文章](https://portswigger.net/research)
            - [Burp 工具文档](https://portswigger.net/burp/documentation/contents)  
            - 各种速查表 

        - 按主题组织的高质量资料，值得反复查看。

    2. [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) Web lab
        - 项目拥有挑战的对应指南 [Pwning OWASP Juice Shop](https://pwning.owasp-juice.shop/companion-guide/latest/index.html)，不包含知识文档
        - 综合型靶机，在按主题分类的 PortSwigger 后拥有连贯视角，有一些新奇的挑战。 
            - 然而由于其性质，无法与 OWASP WSTG 指南一起构建实践框架。

    3. [OWASP Web 安全测试指南](https://owasp.org/www-project-web-security-testing-guide/) 文档
        - 项目主页的排版：标题缺少锚点，并且目录为静态侧边栏。
            - 直接查看 [Github 文档](https://github.com/OWASP/wstg/tree/master/document)。并且可在 LLM 中直接使用文档的md代码翻译。   
            - 附录部分的工具、推荐文档等内容也值得查看。  
            - Github 项目中拥有对应的 Checklist 检查清单。

    4. [OWASP WebGoat](https://owasp.org/www-project-webgoat/) Web lab
        - 基于 Java，挑战与小节文档在同一页面而非独立环境，教学型SQL，项目 wiki 的文档缺乏信息。    
            - 材料质量不一，但一些内容仍值得查看。    
            模块中介绍 ZAP 的使用，[ZAP 工具文档](https://www.zaproxy.org/docs/) 。 
            - [cycubix 的解决方案](https://docs.cycubix.com/application-security-series/web-application-security-essentials/solutions)，[IYS 的解决方案](https://inventyourshit.com/labs/webgoat/)

4. 二进制
    1. [pwn.college CSE 365：网络安全导论](https://pwn.college/cse365-f2025/) 公开课程  
        CSE 365 还包括对 pwn.college 平台本身的介绍：
        - 拥有定制的 GPT5 “sensai”。    
        - 模块视频 + 文档 + CTF 型靶机
            - 视频与幻灯片的部分概念不存在于文档中。    
            - 拥有练习模式，获取管理员权限调试   
        - 公开课进行 Twitch 直播，Youtube 拥有往期视频。（B站拥有 LLM 翻译）
        - 往期课程无首页链接但可修改URL访问： `cse365-f2025` `cse365-s2025` `cse365-f2024`。或使用导航栏的搜索功能

        - 使用大部分的基础与橙带道场内容
        - 当前公开课直播 Youtube 视频为 2024 fall，略过
        
        
    2. [pwn.college CSE 466：计算机系统安全](https://pwn.college/cse466-f2025/) 公开课程  
        - 在 CSE 365 后，几乎所有知识均来自于讲座视频、推荐阅读材料与公开课直播视频。同时进行讲座视频与挑战，并记录关键概念与工具技巧。
        - 使用拥有 root 权限的练习模式进行调试很必要

        - 使用所有的黄带与绿带道场内容
        - 当前公开课直播 Youtube 视频为 2025 fall
        - 每个讲师风格与涵盖内容不同，或许应当查看往期不同讲师的公开课程直播视频


    3. [pwn.college CSE 598：高级软件漏洞利用](https://pwn.college/cse598-se-s2025/) 公开课程 

        - 使用所有的蓝带道场内容，以及额外的两个 Windows 模块
            - 略过两个 Windows 模块中旧版的 office hours 答疑以及课程直播视频
        - 当前公开课直播 Youtube 视频为 2025 spring 

    4. `《计算机安全导论：深度实践》`杜文亮 
        - 项目资源页面：[SEED](https://www.handsonsecurity.net/resources.html)
            - 图书章节的对应实验环境（并非常规 lab）、幻灯片、无答案的问题集
            - 中文版对应英文版的第1/2版过渡，英文版出到第3版
                - 中文版图书以及最新版二进制实验主要使用32位架构
            - 内容：
                - 软件安全部分：简要的核心概念。
                - web 安全部分：陈旧且简略。
                - 网络安全部分：包含基础概念、工具命令与代码模板，作为本书的核心。
                - 实验粗糙，仅阅读说明。略过问题集
            - 重点是网络安全部分，之后或许返回查看代码模板，或许查看英文第三版新章节

- ⚠️ 中断 ⚠️
      
    - 《渗透测试高手》（Advanced Penetration Testing）-  Wil Allsopp 
        - 从钓鱼到C2开始，缺乏前期侦察

    - 《渗透测试实战 第三版》（The Hacker Playbook 3）-  Peter Kim 
        - 简略的工具介绍

5. 网络渗透 & 后渗透

    1. metasploit 攻击框架系列 
        - 工具 https://github.com/rapid7/metasploit-framework
        - 教程 https://www.offsec.com/metasploit-unleashed/introduction/
        - 文档 
            - https://docs.rapid7.com/metasploit/
            - https://docs.metasploit.com/
        - 图书 `Metasploit: The Penetration Tester’s Guide, 2nd Edition`
            - 无专用靶场，主要使用陈旧的 metasploitable3，除 MSSQL 外无配置说明
            - 内容
                - 代码示例为32位架构
                - 对渗透测试各阶段进行简要介绍，以及过程中在 MSF 对应的模块与少量额外工具
                - 略过：10无线
            - 若尝试在某阶段使用 MSF 则结合其他材料进行特定章节阅读
        - 靶机 https://github.com/rapid7/metasploitable3
            - 并非开箱即用：陈旧的靶机与设置文档，链接失效，缺失环境设置说明
        - 模块与漏洞仓库 https://www.rapid7.com/db

    2. 《灰帽黑客 第六版》（Gray Hat Hacking）- HARPER
        - 部分实验基于无法使用的云 [lab](https://github.com/GrayHatHacking/GHHv6)
        - 内容：
            - 前两部分包含简要的编程与系统概念，简略的工具介绍，对渗透测试与红队的概述。
            - 之后为核心内容，但仍然简略。
            - 略过章节：IDA Pro、威胁狩猎、虚拟机部分
        - 或需使用扩展阅读与同主题材料再次阅读

    3. 《Network Security Assessment (3rd Edition)》 – Chris McNab
        - [图书代码示例](https://resources.oreilly.com/examples/9780596006112/)
        - 内容：
            - 前3章提供概念速览，之后为核心的网络渗透部分
                - 或需创建类似第3章的文档索引页以导航到各主题
                - 部分协议/工具/命令示例已过时，提取框架概念

6. 📌 Web 应用程序渗透  
    
    1. 新材料与 OWASP WSTG 、PortSwigger、《黑客攻防技术宝典：Web实战篇》 一起，并发回顾/阅读/归档  
        - 图书材料：
            - 《Bug Bounty Bootcamp》 - Vickie Li
                
            - 《Web Application Security: Exploitation and Countermeasures for Modern Web Applications》- Andrew Hoffman
                - 暂略第三部分：防御

            - 《Web Hacking Arsenal: A Practical Guide to Modern Web Pentesting》 - Rafay Baloch
                - 虽然出版日期相对较新，然而侦察章节列举的工具大多停止更新

        - 分析：    
            - 各材料的内容结构近似且相互引用，并发阅读过程中能够简单发现过时/错误描述。选定拥有清晰结构的书为初始骨架，读完一章/小节后查看其他材料的同主题章节。此时，WSTG 这类零散的百科类文档可被整合到/重构骨架。
                - 各材料仍拥有作者独特的见解/工具集/工作流

            - 之后或需尝试使用各种自动化工具以快速进行初始探测，结合 lab 记录的步骤确认可自动化的部分，类似 portswigger 的原型污染主题同时介绍手动与自动步骤

            - 研究文档本身即可直接作为或提取内容到主题，类似 portswigger 发布研究后创建对应主题材料

    2. [hacker101](https://www.hacker101.com/)
        - 小型靶场 [hacker101 ctf](https://ctf.hacker101.com/) 
        - [各种资源导航](https://www.hacker101.com/resources)
        - [教学视频](https://www.hacker101.com/videos)
        - 分析
            - 在过程中构造速查/检查表，快速映射注入点与探测项到对应主题
            - portswigger 这类拥有教学文档的专项靶场中，能够高效学习并实践主题内容，过程中对特定主题构建“侦察-探测-利用”的工作流；而 hacker101 这类模拟场景、主题未知的复合靶场仅当基于主题文档并构建完整循环工作流时有效。
                - 当前所有 web 靶场均可用（浏览器利用、移动应用渗透、云渗透归为独立主题）

    3. 📌 进行一批靶场内的 web 主题挑战 
        - [picoCTF -> CyLab Security Academy](https://cylabacademy.org)
            - [综述文档](https://primer.cylabacademy.org/)
            - [资源](https://learn.cylabacademy.org/resources)
                - 视频
                - 主题简略文档
            - [挑战库](https://learn.cylabacademy.org/library)
                - 综合挑战库，包含web应用、加密、逆向工程、取证、二进制、LLM
                - 仅包含根主题，缺乏子主题分类
                - 挑战较新，使用现代技术栈。运行在 AWS EC2，每个挑战使用单独 docker
                - 挑战拥有 hint
            - 使用方式：
                - 学习路径并不涵盖所有挑战，也并非按照主题与子主题组织。直接在挑战库中按主题索引，当前专注于 web应用主题，按照难度进行
            - [解决方案](https://picoctfsolutions.com/)
                - 包含提示、代码、常用工具
        - [Root Me](https://www.root-me.org/?lang=en)
            - 资源
                - [陈旧文档](https://repository.root-me.org/)
            - 综合靶场，包含编程、网络、web应用、加密、取证、程序应用
                - 挑战持续更新，但频率下降，最早的挑战发布于几十年前。使用多用户服务器，部分挑战开启容器后重定向到对应端口
                - 挑战页面或拥有关联文档资源，以及在完成后解锁的其他挑战者的解决方案
            - 使用方式：
                - 中文缺失文档，使用 en
                - 主题使用挑战名称进行分类，但不完全。当前专注于 web应用主题，按照难度进行

        - [hackropole](https://hackropole.fr/en/)
            - 在线追踪进度，使用本地 docker 靶机的综合靶场，包含加密、取证、硬件、二进制、逆向、web
                - 作为年度 CTF 归档靶场，使用流行技术栈且持续更新。
                - 提供文件的挑战均为代码审计型，需实际查看组件版本对应的更新日志、文档、源码，部分挑战设置巧妙或难度较高
                - 挑战页面拥有解决方案，且 docker 型靶机在黑盒缺乏思路时转为白盒。靶场说明中标注挑战无需暴破
                - 仅包含根主题，缺乏子主题分类

        - [yeswehack dojo](https://dojo-yeswehack.com/)
            - dojo 
                - （部分）按主题分类（但分类错误）的模块化代码片段教程（后半部分模块均拆分自 2024 年的一个 CTF 挑战）
                    - 代码审计型精炼示例：简要阐述概念后，展示普通输入与几个载荷输入
                    - 针对代码片段的可视化交互型练习：在代码片段中固定输入点、实时显示输入在其中的状态。包含 hint 与解决方案
                    - 拥有盲注练习，但设置速率限制。每个载荷提交请求均触发几十个可视化组件的请求。仅对前几个字符进行概念测试
                    - 类似 owasp webgoat，拥有一些亮点但总体质量较低
                - 每月发布1个挑战，往期挑战进入存档并在[博客中发布解题思路](https://www.yeswehack.com/blog/dojo)
            - [博客主题文章](https://www.yeswehack.com/blog/learn-bug-bounty)
            - [docker 脆弱代码片段](https://github.com/yeswehack/vulnerable-code-snippets)
            - [工具](https://www.yeswehack.com/researchers/tools)
                - 其中 Dom Explorer、PP Finder（原型污染） 或可用
        
        - 分析
            - 进度
                - picoCTF、Root Me、hackropole 三个大型综合靶场
                    - 已尝试尽力做 Web 主题1星挑战（但仍不够尽力）。
                - yeswehack dojo 作为 Web 专项靶场
                    - 教程片段很少，已完成。
                    - 几十个每月挑战存档作为类2星以上挑战

            - hacker101 与 hackropole 均遇到 AES-ECB 密码学挑战，此时逐渐过渡到二进制类型
                - web 靶场低频率维持
                - 回顾 pwn.college CSE 365 网络安全基础中作为衔接的前几个模块：Linux 命令、权限模型、Web 基础。
                    - 此时尚不包含二进制利用且主题材料尚未建立，查阅并归档到 man/规范/指南中
                - 对之后的二进制主题使用与之前 Web 主题类似的：并发回顾/阅读/归档过程

- 二进制

    - foo

- TBD 📅

    - [pwn.college CSE 598 ASOW - Fall 2026](https://pwn.college/cse598-asow-f2026/)

    - 《API 攻防》（Hacking APIs） — Corey Ball

    - 二进制
        - 并发阅读
            - The Art of Software Security Assessment
            - pwn.college
            - 《黑客之道：漏洞发掘的艺术（Hacking: The Art of Exploitation）》
            - Exploiting Software: How to Break Code 
            - The Shellcoder's Handbook: Discovering and Exploiting Security Holes 
            
            - CTF Wiki
            - https://guyinatuxedo.github.io/index.html
        
        - 靶场
            - https://exploit.education/

        - 反汇编
            - 《二进制分析实战 Practical Binary Analysis》

        - 内核
            - A Guide to Kernel Exploitation: Attacking the Core

        - 发现
            - Fuzzing: Brute Force Vulnerability Discovery


    - 基于 AWS 的云渗透

    - 《攻击网络协议》（Attacking Network Protocols） — James Forshaw

    - 《OSINT TECHNIQUES ELEVENTH EDITION》- Michael Bazzell  &  Jason Edison 

    - 《网络渗透测试的艺术》（The Art of Network Penetration Testing）- Royce Davis 
        - 对应靶场 https://github.com/R3dy/capsulecorp-pentest



