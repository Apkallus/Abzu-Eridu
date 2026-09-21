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

## 核心工具

速查/载荷表
- [PayloadsAllTheThings](https://swisskyrepo.github.io/PayloadsAllTheThings/)

代码格式化
- [beautifier.io](https://beautifier.io/)
- [beautifytools](https://beautifytools.com/xml-beautifier.php)
- burp 的格式化复制有时将破坏格式（丢失缩进），普通复制或效果更佳

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
- [md5.gromweb](https://md5.gromweb.com/)
    - 仅限 MD5

解除混淆
- [webcrack](https://github.com/j4k0xb/webcrack)
    - 使用 npm 按照或使用[在线版](https://webcrack.netlify.app/)

DNS 重绑定测试
- [taviso/rbndr](https://lock.cmpxchg8b.com/rebinder.html)

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
    - 代码审查
    - 载荷构造
    - 收集已知文件名，之后分析命名风格
        - 前后缀
        - 可能的功能


------------
``````md
<!-- 记录格式 -->

## 侦察

访问首页
- 响应
    - 功能端点
    - 信息端点
    - 静态资源端点
    - 兴趣点

功能端点a
- 访问功能端点请求
    - 响应
        - 分析
        
- 使用功能请求
    - 响应
        - 分析
            - 参数设置
            - 功能作用
            - 与其他端点的联系
            - 兴趣点

信息端点a
- 请求
    - 响应
        - 分析
            - 信息结构与类型分析
            - 兴趣点


## 功能探测

普通功能a
- 请求
    - 响应
        - 端点与参数
        - 兴趣点
- 提交普通表单
- 提交异常表单
- 测试表单

功能b
- 触发页面代码或表单
    - 端点与参数
    - 兴趣点
- 关联 JS 代码
- 汇点渲染
- 探测
    - 普通测试
    - 构造载荷

访问`端点c`，响应
- 响应内容
    - 分析

## 功能端点摘要

主页
- 功能
    - 功能描述
    - 与其他端点的关联
- 参数 GET/POST
    - 参数格式/类型/功能
- 测试
    - 发现
        - 内容
            - 使用上下文特化字典
            - 使用侦察得到的列表
            - 使用已知命名风格
            - 是否携带凭证
        - 类型
            - [ ] 单文件/目录暴破
            - [ ] 路径遍历
            - [ ] 模糊测试
    - 参数挖掘
        - [ ] HTTP 方法测试
        - [ ] 请求头测试
        - [ ] URL 查询参数测试
        - [ ] POST 请求体参数测试
- 探测
    - 发现a
        - [ ] 测试a

端点a
- 功能与参数
    - GET 功能a
        - 参数a
        - 参数b
            - [ ] 参数测试
    - POST 功能b
    - POST 功能c
    - PUT 功能d

- 探测

特异目录
- 探测
    - [ ] 目录暴破

## 兴趣点

重定向模式
- 示例端点

会话 cookie 功能
- 设置 cookie
    - cookie a
    - cookie b
- 移除测试
- cookie 作用分析

获取信息的端点a
- 响应
    ```pa
    代码片段
    ```
    - 分析

访问失败的端点b
- 响应
    ```pa
    响应片段
    ```
    - 分析
        - 当前权限
        - [ ] 状态变更后的再次访问

侦察端点/参数/片段
- 获取的用户名列表
- 获取的特异数据

## 错误信息

泄露
- 代码片段
- 版本
- 参数与格式

## 文件

`文件名`
```
文件数据
```
- 分析
- [ ] 测试
- 载荷构造

``````
------------

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

## 检查表

侦察：
- 信息结构与类型
    - 例如提取用户名/邮件/id列表
- 端点、文件名、参数、类型
- 凭证暴破触点
- 端点（缺乏参数 400）
- 客户端保存状态的逻辑缺陷
- 新发现功能后递归侦察与探测

输入参数:
- 位置
    - URL 查询参数
    - 请求体参数
        - 资源
        - 登录
        - 功能
    - REST 风格路径参数
    - cookie 
    - Host 头与覆盖头
    - HTTP 方法
    - IP 覆盖头
    - 参数挖掘
- 类型
    - 服务器端注入
        - SQL 注入
            - 额外，猜测编号映射的资源，暴破资源名
        - 操作系统命令注入
    - 客户端
        - 反射型 XSS
    - 访问控制
        - 不安全的对象访问
    - 请求走私
    - 错误信息
        - 设置类型不匹配或移除参数
        - 设置类型匹配但错误的参数
    - HOST 头注入
    - 服务器端请求伪造
    - 逻辑漏洞
        - 客户端返回数据，服务器不保存状态

存储型内容
- 反射
    - 存储型 XSS
- 渲染
    - 服务器端模板注入

资源或令牌序列分析
- 分析命名风格，推测可能资源名称（分隔符/驼峰）
- 编码
- hash
    - hash 明文/盐值分析
- JWT
- 递增，特异序号

URL 带外
- 探测
- 泄露文件内容
- 加载文件执行
- GET 服务器端请求伪造

逻辑
- 用户a设置、读取用户b的信息
    - 识别关联的有效参数，移除噪音参数