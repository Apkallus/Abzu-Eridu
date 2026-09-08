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

## 记录

长时间记录
- burp 的组织器保留有趣的请求响应，也有笔记功能

过程
- 查看并更新检查表


过程记录
- 步骤
    - 详细内容
    - 或分离侦察与探测

- 功能端点
    - 已发现功能端点
    - 或包含参数信息与探测状态
    
- 待测试
    - 标记之后测试项目

- 文件
    - 获得的源码与配置文件

tips
- 由于现代 web app 使用大量 js，以及重定向，点击链接以查看最终访问地址

## 检查表

URL 查询参数或 REST 风格路径参数
- 服务器端注入
    - SQL 注入
        - 额外，猜测编号映射的资源，暴破资源名
- 访问控制
    - 不安全的对象访问
- 错误信息
    - 设置无效或移除参数

存储型内容（在所有反射/渲染位置查看）
- 存储型 XSS
- 服务器端模板注入

登录表单
- SQL 注入

功能端点
- 访问控制
    - 修改 HTTP 方法
    - Host 头注入
    - IP 头部覆盖
    - 请求走私

反射
- 反射型 XSS
- Host 头注入