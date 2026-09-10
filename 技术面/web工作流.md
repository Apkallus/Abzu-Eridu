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

暴破字典
- > [!note] 待添加

代码格式化
- [beautifier.io](https://beautifier.io/)
- burp 的格式化复制有时将破坏格式（丢失缩进），普通复制或效果更佳

SQL 自动化
- [sqlmap](https://github.com/sqlmapproject/sqlmap/wiki/Usage)

文件元数据
- [exiftool](https://exiftool.sourceforge.net/exiftool_pod.html)

hash
- [md5.gromweb](https://md5.gromweb.com/)

## 记录

长时间记录
- burp 的组织器保留有趣的请求响应，也有笔记功能

过程
- 查看并更新检查表
- 手动测试时，后台继续目录暴破/扫描


过程记录
- 侦察与探测
    - 详细内容

- 功能端点
    - 已发现功能端点
    - 参数格式与限制
    - 当前测试状态

- 错误信息
    - 版本揭示
    - 代码片段

- 文件
    - 获得的源码与配置文件
    - 收集已知文件名，之后分析命名风格
        - 前后缀
        - 可能的功能


```md
<!-- 记录格式 -->
## 侦察与探测

访问首页
- 请求
    - 响应
        - 分析
- 测试
    - 响应
        - 分析

## 功能端点

`/`
- 参数 GET/POST
    - 索引
    - 开关变量
    - 信息
- 功能
- 测试
    - [x] 已测试
    - [ ] 待测试
- 探测
        
## 错误信息

## 文件
```

tips
- 由于现代 web app 使用大量 js，以及重定向，点击链接以查看最终访问地址
- URL 的 `http[s]` 方案：拥有仅 `http` 或 `https` 可行的场景，两种方案均需测试

## 检查表

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
    - 隐藏参数与头部挖掘
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
        - 设置无效或移除参数
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
- 分析命名风格，推测可能资源名称
- 编码
- hash
- JWT
- 递增，特异序号

URL 带外
- 探测
- 泄露文件内容
- 加载文件执行
- GET 服务器端请求伪造

响应
- 凭证触点
- 端点（存在、缺乏参数、不存在、作为注入点触发异常）
- 数据类型
    - 客户端保存状态的逻辑缺陷