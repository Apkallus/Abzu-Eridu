## 平台

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

[地址信息](https://prepedu.com/zh-hant/blog/read-street-addresses-in-english)
- City
    市，省
- Street address
    街道地址：小区名，行政区划街道（Subdistrict），行政区划（District）
- Second address line
    详细地址

## 核心工具

速查载荷表
- [PayloadsAllTheThings](https://swisskyrepo.github.io/PayloadsAllTheThings/)

wiki
- [hacktricks](https://hacktricks.wiki/)

代码格式化
- [beautifier.io](https://beautifier.io/)
- burp 的格式化复制有时将破坏格式（丢失缩进），普通复制或效果更佳
- [formatter.org](https://formatter.org/python-formatter)
- [beautifytools](https://beautifytools.com/xml-beautifier.php)

SQL 自动化
- [sqlmap](https://github.com/sqlmapproject/sqlmap/wiki/Usage)

文件元数据
- [exiftool](https://exiftool.sourceforge.net/exiftool_pod.html)

hash
- hashcat 暴破工具
- [weakpass](https://weakpass.com/)
    - 各种字典下载
        - [rockyou](https://weakpass.com/wordlists/rockyou.txt)
    - 工具页面
        - 以 hashcat 格式提取 zip 文件的 hash ，且包含 hashcat 对应类型
        - hash 类型识别
        - hash 彩虹表功能不可用
- [md5.gromweb](https://md5.gromweb.com/)
    - 仅限 MD5

解除混淆
- [webcrack](https://github.com/j4k0xb/webcrack)
    - 使用 npm 安装或使用[在线版](https://webcrack.netlify.app/)

DNS 重绑定测试
- [taviso/rbndr](https://lock.cmpxchg8b.com/rebinder.html)

加密识别与解密
- [dcode.fr](https://www.dcode.fr/cipher-identifier)
- [payloadplayground.com](https://payloadplayground.com/tools/cipher-decoder)
- [待测试：ciphey](https://github.com/bee-san/ciphey)

编码识别与解码
- [hackvertor](https://github.com/hackvertor/hackvertor)
    - burp 拥有对应插件
- [待测试：CyberChef](https://gchq.github.io/CyberChef/)

`.js.map` SourceMap 还原
- [sourcemapper](https://github.com/denandz/sourcemapper)
    - 完整还原代码，包含 JS 注释。而工具 shuji 重组结构，且注释丢失。

本地 XSS lab
- 服务器
    - 在文件所在目录 `python -m http.server 5500`
    - vscode 插件 live server
- 协作服务器
    - `ncat -l 9999`

- 或之后使用 python 脚本配置详细条目

随机序列预测
- [v8_rand_buster](https://github.com/d0nutptr/v8_rand_buster)

正则表达式
- [regex-vis 可视化工具](https://regex-vis.com/)

wasm 
- 浏览器开发者工具栏
    - 查看文本格式
- [wabt](https://webassembly.github.io/wabt/demo/)
    - 文本 <=> 二进制相互转换
    - 未尝试：github 项目拥有反编译到 c 的工具 `wasm2c`
- 未尝试：[Ghidra 插件 ghidra-wasm-plugin](https://github.com/garrettgu10/ghidra-wasm-plugin)

HTTP 连通性测试
- [httpbin](https://httpbin.org/)
- [testserver](https://testserver.host/)

GraphQL 可视化工具
- [graphql-visualizer](http://nathanrandal.com/graphql-visualizer/) 
    - 丢失数据
- https://apis.guru/graphql-voyager/
    - 丢失数据

版本
- git diff 快速查看文件差异
- burp 比较器查看文件与字节差异

sha1 碰撞
- [alf.nu jpg 转 pdf](https://alf.nu/SHA1)

DOM XSS
- 待寻找 burp DOM 插件的替代

## 字典

字典载荷
- 模糊测试
    - 同时拥有 `../` 与 `..\` 两种类型，且包含无文件的目录载荷
        - 对应不同后端类型
        - 测试目录索引
    - 包含 SQLi 的通配符 `%`
    - [500 SecLists - Fuzzing](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/UnixAttacks.fuzzdb.txt) 
        - 可用，但长时间未更新

- api 字典
    - 拥有 `sessions`
    - 组合路径探测
        - [300 SecLists - api - api-endpoints.txt](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/api/api-endpoints.txt)

    - 单元素
        - [1万 SecLists - api - api-endpoints-res.txt](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/api/api-endpoints-res.txt)
        
    - 多元素
        - [1000 SecLists - api - objects](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/api/objects.txt)
      
      
- 用户名与密码
    - 用户名
        - [1万 SecLists - Usernames - names.txt](https://github.com/danielmiessler/SecLists/blob/master/Usernames/Names/names.txt)
    
    - 密码
        - 大型密码仅用来本地暴破
        - [10万 SecLists - Passwords - 100k-most-used-passwords-NCSC.tx](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt)


## 记录

长时间记录
- burp 的组织器保留有趣的请求响应，也有笔记功能

过程
- 查看并更新检查表
- 手动测试时，后台继续目录暴破/扫描


过程记录
- 侦察与探测
    - 记录关键请求、响应与尝试

- 功能端点
    - 已发现功能端点
    - 参数格式与限制
    - 当前测试状态
    - 与其他端点的关联（单独列出或包含在功能描述内）
    - 存在 XSS 时，标记源的参数中，而不是分散到各个汇

- 兴趣点
    - 摘录直接暴露的代码片段并分析
    - 模式记录

- 错误信息
    - 触发错误源
    - 版本揭示
    - 代码片段

- 文件
    - 泄露的源码与配置文件
    - 代码审计
    - 载荷构造
    - 收集已知文件名，之后分析命名风格
        - 前后缀
        - 可能的功能

## tips

- 现代 web app 使用大量 js，以及重定向
    - 点击链接以查看最终访问地址
    - 查看浏览器的 DOM，识别有趣的动态构建内容
    - 对于 ctf：查看使用的库版本，并对比官网的库文件，以查看设计者是否混淆代码到库文件中
- URL 的 `http[s]` 方案：拥有仅 `http` 或 `https` 可行的场景，两种方案均需测试
- HTTP/2 拥有头部大小写规范，大小写敏感的头部需使用 HTTP/1.1 协议
- 暴破字典包含登出功能导致 cookie 无效
- 除拦截响应并修改外，还可在浏览器开发者工具中设置断点，在执行前使用控制台设置任意值
- 暴破时注意 burp 的设置，例如 URL 编码功能或导致额外编码
- 功能相似的端点可能使用相同或相似的参数
- 组件交叉点的测试，如
    - SQL 数据库a查询中包含对数据库b的查询，双重 SQL
    - 服务器路径或参数中包含对其他服务器的资源引用
- 端点暴破时，额外进行一次 POST 方法暴破
- 路径规范化的末尾斜杠 `/` 重定向，或存在服务器端重定向缺陷。也需注意在端点访问时手动添加
- 服务器泄露文件路径后也尝试再浏览器中访问，分析文件的访问状态以及应用程序与本地路径的相对位置
- 执行顺序、迭代递归
    - 净化绕过
        - 冗余字符串，迭代净化拼接构造载荷
        - 嵌套模板对象，递归渲染绕过第一次净化
- 查看 github 版本 diff 快速识别硬编码凭据
- 猜测数据/状态回显时，后端的对应代码
    - 名称回显
        - 使用会话 cookie 内保存的名称
        - 在数据库查询对应的名称（储存型 SQLi）
    - 数量回显
        - 查询当前条目在数据库的数量（布尔型 SQLi）

- 模糊测试观测点
    - SQL 型载荷中：添加额外引号、注释、条件但与原响应相同，或响应有效的其他资源，或响应所有资源
        - 特殊符号被净化
        - 或存在 SQL 注入
    - 时间延迟载荷触发响应延迟
- 记录并分析过程中的各种状态触发的对应错误信息
    - 端点是否存在
    - 参数是否存在

- 批量参数探测可能失败，冗余参数直接导致失败
- 使用各种特殊符号，注释、通配
- 数字除进制、负数、巨大数外，还有科学计数法
- `明文+盐 = hash` => `盐+明文 = hash`
    - 拥有其中2个元素即得到另一个，得到明文与 hash 时暴破得到盐，明文与盐可互换

- 文件路径结构与网络查询结构在相对路径且无参数时很相似
- 识别版本后寻找特定[载荷](https://github.com/swisskyrepo/PayloadsAllTheThings)或字典

- 查询代码库，以 v8 功能示例
    - 当前组件文档 v8
    - 主调组件文件 node.js
    - 使用组件文档 edge
- 浏览代码库时
    - 文档：函数结构、参数、示例
    - 指南：功能介绍与导航
    - 头文件：函数声明与注释说明、结构类型说明
    - 源码：所有内容
    - 使用 llm 快速追踪函数调用

- 登录表单
    - 用户
        - 注册用户
        - 目标用户
    - 用户名：有效/无效
    - 密码：有效/无效

- JS 带外时尝试多种载荷，有时 `fetch` 或 `navigator.sendBeacon` 这类请求失败，而 `location` 与 `new Image().src` 成功

- 代码审计
    - 若分支判断使用不同函数，查阅文档以分析差异

- SQL 注入后的分支判断，尝试使得前后匹配
    - 尝试提取之前的值，各种表
    - 尝试设置注入值以完全覆盖，排序
    - 尝试控制之前的值，随机种子

- 寻找语言特异值，并查看特异计算结果
    - JS 
        `0 -0 NaN Infinity -Infinity`

- 当文档不足够详细时，源码的注释甚至可能包含更多信息

- 预测载荷的解码顺序，对载荷执行多重/多类编码，或使用编码不敏感的载荷

## 命令，之后重温二进制时合并

- 系统信息

    ```sh
    # 架构信息
    uname -a

    # 操作系统版本信息
    cat /etc/os-release

    # 内核编译信息
    cat /proc/version                 
    ```

- 用户权限

    ```sh
    # 当前用户
    whoami 

    # 用户组
    id

    # sudo 权限
    sudo -ll

    # 用户表
    cat /etc/passwd

    # 用户组
    cat /etc/group

    # 当前登录用户及其操作 
    w

    # 登录历史记录
    last
    ```

- 文件环境
    ```sh
    # 查看工作目录
    pwd

    # 查看环境变量
    env
    cat /proc/self/environ

    # 文件挂载
    cat /etc/fstab
    ```

- 网络

    ```sh
    # 主机
    cat /etc/hosts
    ```

- 进程

    ```sh
    # 进程信息
    ps aux

    # 服务状态
    service --status-all 
    ```

- 计划任务
    ```sh
    # 所有计划任务
    ls -al /etc/cron*
    ```

## 编码模式，之后合并

- deflate_compress
    - 格式：`.` + base64URL(deflate编码)

- JSFuck —— JS 动态代码构建
    - 格式：
        - 由字符集 `-~[]<>` 组成的运行时动态构建代码（`Function()`），末尾通常拥有 `()` 以实际执行
    - 解码：
        - 浏览器开发者工具中设置断点，逐步执行，浏览器将在运行时解码
        - 浏览器开发者工具中选中末尾调用符号 `()` 前的代码后，右键在控制台执行（或复制后在控制台/本地构造）。此时仅构建而不执行函数
    - 工具：
        - [JSFuck](https://jsfuck.com/)
        - [jscrew](https://www.jscrew.it/) 

## 特异文件、目录，之后合并

- apache
    ```log
    # 目录级配置文件
    .htaccess
    ```

- macOS
    ```log
    # 目录属性文件
    .DS_Store
    ```

- web
    ```log
    # web 目录
    /www/html/*

## 错误信息，之后合并

- PostgreSQL 
    ```log
    pq: syntax error at or near 
    ```


## 载荷构造

- 混淆
    - 编码
    - 动态代码构建
    - 大小写
    - 空白符
    - Unicode 空白、相近字符
    - 注释、成对引号
- 字段访问
    - 点 `.`
    - 索引 `[]`
- 参数
    - 列表型 `foo[]=bar`

## 版本依赖

应用目录下 `/package.json`
- `"devDependencies"`

## 代码审计

流程
- 从源到汇，追踪用户输入
- 查看过程中对输入的限制，如长度、字串
- 查看传递/拼接到函数或语句：
    - SQL 查询
    - 命令执行
        - `system` / `exec` / `shell_exec` / `passthru` / `popen` / `proc_open`
    - 文件读取
        - `readFileSync` / `file_get_contents` / `fopen` / `include` / `require`

条件判断或限制
- 参数
    - 类型转换
    - 重复参数到列表型参数 `a=1&a=2` `a[]=1` 元素精确匹配
        - 绕过单参数比较
    - 空值
    - 严格比较与宽松比较

- 数字：特异值、计算，及其字符串形式
    - 极值：最大最小数
    - 正负无穷：`Infinity` / `-Infinity`
    - 正负零：`0` / `-0`
    - NaN
    - null / undefined
    - 科学计数法：`1e3` / `0e1`
        - 绕过数字长度检查
        - 魔术哈希 `0e`，以0为底时数值为0

- 字符串
    - 大小写敏感
    - 编码解码顺序
        - 绕过检测
        - 保存下一阶段载荷
    - 被转义
    - 超长截断
    - Unicode 混淆

服务器配置与组件
- 配置
  - 工作目录
  - URL 转发
  - 本地文件
- 规则覆盖
- 组件解析差异
  - 分隔符
  - 前后缀去除
  - 检查-使用顺序


文档查询
- 教程，快速得到基础语法
- 参考，查看方法、函数细节
- 更新日志，快速得到旧版缺陷
- 规范

反混淆
- 不可见 Unicode 字符作为参数或值