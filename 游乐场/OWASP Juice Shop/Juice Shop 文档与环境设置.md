软件安装与设置记录在“综合环境设置”文件夹下，此处记录文档与特殊设置

- [OWASP Juice Shop 项目页面](https://owasp.org/www-project-juice-shop/)

- [Juice Shop 指南](https://pwning.owasp-juice.shop/companion-guide/latest/)
    - 特性:
        - 完全使用 JavaScript/TypeScript 编写的应用程序
        - RESTful API
        - 运行时自我恢复，使用cookie保存进度，也可使用备份与恢复功能
        - JavaScript 代码压缩/丑化，更难阅读

    - [架构描述](https://pwning.owasp-juice.shop/companion-guide/latest/introduction/architecture.html)：  
    ![架构图](./architecture-diagram.png)

    - [漏洞分类映射列表](https://pwning.owasp-juice.shop/companion-guide/latest/part1/categories.html)：  
    ![漏洞分类映射图](./categories.png)

    - 解决漏洞后可能有对应的代码挑战，寻找并修复对应代码

    - 解决挑战后的[漏洞避免措施](https://cheatsheetseries.owasp.org/)

    - [默认对容器禁用潜在危险挑战](https://pwning.owasp-juice.shop/companion-guide/latest/part1/challenges.html#_potentially_dangerous_challenges)
        > 要重新启用所有挑战，设置环境变量 NODE_ENV=unsafe ，或者在 YAML 配置文件中设置 safetyMode: disabled 

- [Docker 容器安装与命令](https://hub.docker.com/r/bkimminich/juice-shop#docker-container)：
    1. 安装 Docker
    2. 运行 ```docker pull bkimminich/juice-shop```
    3. 运行 ```docker run --rm -p 3000:3000 bkimminich/juice-shop```
    4. 浏览器访问 http://localhost:3000⁠，localhost 默认为127.0.0.1

    - Firefox 默认不代理本机地址，搜索到[CSDN博客](https://blog.csdn.net/HUC0723/article/details/119953560)或[Microsoft云开发文档](https://learn.microsoft.com/en-us/microsoft-cloud/dev/dev-proxy/how-to/intercept-localhost-requests)：
        > 若要将 Mozilla Firefox 配置为向系统代理发送 localhost 的 URL 请求，需要将 network.proxy.allow_hijacking_localhost 首选项设置为 true。 为此，请在 about:config Firefox 中打开页面，搜索 network.proxy.allow_hijacking_localhost 首选项并将其设置为 true。
        
    - 设置环境变量，开启容器的潜在危险挑战
    ```docker run --rm -p 3000:3000 -e NODE_ENV=unsafe bkimminich/juice-shop```



- 计划
    - 结合 OWASP Web 安全测试指南 与 PortSwigger Web Security Academy 的主题文档，在进行 OWASP Juice Shop 靶场的过程中构建 Web应用程序渗透测试的概念框架
    - 使用分类映射
    - 使用靶场~~教学模式~~/提示以及 [Juice Shop 指南的提示/解决方案](https://pwning.owasp-juice.shop/companion-guide/latest/part2/README.html)
    - 在计分板的设置中时常备份进度
    - 使用```beautifier.io```等代码格式化工具还原被压缩的代码以便于阅读
    - 对应用程序进行分析时应当构建功能结构表，并保存或记录感兴趣的消息

- 暂略
    - 暂时跳过所有加密货币相关内容
    - Cryptographic Issues - Weird Crypto
        使用 ```MD5```通过挑战，但[示例解决方案](https://pwning.owasp-juice.shop/companion-guide/latest/appendix/solutions.html#_inform_the_shop_about_an_algorithm_or_library_it_should_definitely_not_use_the_way_it_does)中拥有对其他挑战的不当加密的剧透，暂且忽略
    - Sensitive Data Exposure - NFT Takeover
        代码挑战的代码修复显示异常
    - Improper Input Validation - Mint the Honey Pot
        设置钱包与获取测试币
    - Sensitive Data Exposure - Reset Uvogin's Password :x:
        使用受限制网络进行信息搜集
        根据语言风格推测化名
        使用社交媒体搜索软件以及历史档案库站点搜集信息
        值得之后重试
    - Miscellaneous - Security Advisory
        定位了对应文件，但不知 ```a suitable checksum as proof```指什么，尝试提交对应 json 文件的哈希，但无法通过
    - Injection - SSTi
        > 请注意，当在 Docker 容器或 Heroku dyno 中运行 Juice Shop 时，此挑战不可用！无法以“安全”的方式实现此漏洞，而没有任何底层系统被攻破的风险。
    - Broken Access Control - SSRF    
        前置挑战 Injection - SSTi 无法在 Docker 运行
    - Security Misconfiguration - Login Support Team :x:
        下载加密文件，使用暴力破解脚本或工具测试弱密码
        使用哪些工具？如何操作文件？暂时略过，但在之后应当确保完成
        python 拥有对应的库
        如何根据已知密码规则修改爆破单词表？
    - Broken Anti Automation - Reset Morty's Password :x:
        对两个单词的大小写与数字的 leet 变体创建单词表
        之后尝试创建自己的单词表
    - Cryptographic Issues - Forged Coupon :x:
        值得再次分析
    - Sensitive Data Exposure - Leaked API Key :x:
        未提供解决方案，或许与自动优惠券机器人有关，但如何探查 API 密钥泄露？
    - XSS - Video XSS :x:
        对目录的探索值得继续分析
- 未归类
    - Improper Input Validation - Admin Registration
        注册时在提交的输入中添加账户角色属性设置，注册拥有管理员权限的账户
    - XSS - API-only XSS
        探索商品 URL 的方法，使用 api 更新或创建商品内容，其中商品描述部分可显示 HTML 元素，修改商品描述实现储存型 XSS
    - Improper Input Validation - Deluxe Fraud
        - 使用不同权限的账户浏览，此处使用非会员账户才可看到“成为会员”按钮
        - 拦截并修改参数值或名值对或提交空请求体
        - 修改或移除参数进入预期外行为，此处为扣款方式