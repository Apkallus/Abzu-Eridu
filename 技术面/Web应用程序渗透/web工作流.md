平台项目
- 排除提供方类型：
    - 金融
    - 军工
    - 监控
    - 奢侈品
- 偏好资产类型
    - Open Scope 开放范围
    - Close Scope 封闭范围：
        - Other Asset：
            - Any/Other 广泛的资产
            - 有时提供包含详细 IP 范围的文档链接
        - CIDR：专用网段

- 状态
    - 更新：或许新增有趣的资产类别，查看详细描述

对于开放或广泛类别但未列出 CIDR 范围的项目，使用普通侦察确认是否存在专用网段
- https://www.netify.ai/resources/applications/ 缺失部分信息
- https://networksdb.io/search/org/hackerone 缺失部分信息

hackerone 邮箱别名 
- `[username]@wearehackerone.com`

HTTP 自定义头
- `X-Bug-Bounty: Hackerone-<username>`
    - 在 burp - tools - proxy - http match and replace rules 添加 http 请求头：match 留空，replace 填入自定义头部
    - 勾选“仅添加到范围内项目”


使用组织名搜索 ASN：
- https://asnlookup.com/
- https://networksdb.io/
- https://radar.cloudflare.com/
使用 ASN 搜索网段：https://bgp.he.net/
在互联网注册机构使用通配符搜索组织名：https://whois.arin.net/
使用 CIDR 网段搜索路由可见 ASN 或前缀。即使网段本身不可达，但若处于可达的更短前缀网段内，仍可被访问。
- https://bgp.he.net/super-lg/
- https://stat.ripe.net/ 
- https://gins.garr.it/LG/

扫描类型：
- fast: 
    - TCP 默认的1000个常用端口扫描
    - UDP -F 100个端口快速扫描
- find: 特定 -sn 主机发现，并使用 -R 进行反向 DNS 解析
- deep: 全端口 -Pn TCP 扫描
- 使用 -F 的常见端口设置各种参数以对防火墙过滤进行探测

目录结构：`日期/类型/小时-分钟__目标`

自动化与定时任务
python 中分为多个功能，或分为多个脚本
- 设置 nmap 参数并执行
    - 输出 XML 格式用来解析数据
    - 根据日期设置文件夹，当天的输出归到此文件夹中
    - 文件名设置为当前日期+扫描范围，以直观显示概要
- 解析 XML 格式，提取有效内容后导出到CSV
- 将 CSV 导入到 Gephi 查看

使用 hping3 设置 ttl 查看伪造响应的来源
nmap 的空闲扫描使用 S 与 SA 包，而 O 检测时使用 S 包，当目标放行 S 而过滤 SA 时：检测到 IPID 递增，然而无法使用 sI 的空闲扫描。曾经出现社区的 S 包空闲扫描补丁，但未成功合并到主版本

TCP 无单主机发包速率限制时，在 RIPE 网段发现防火墙/入侵检测系统的伪造大量端口响应：一旦触发伪造，后续对目标IP的扫描无论速率如何均得到伪造响应。然而并未对网段其他 IP 进行响应伪造。对网段未开放端口的 IP 扫描，即使速率很高仍未触发伪造

IP/CIDR：
- IP 之间并不构成关联，IP 节点显示所有域名、开放端口/服务

域名
- 从父域延申到所有子域
- 域节点显示所有 Web 应用程序

应用程序
- 各种功能关联到 IP（仅限源 IP）、域名

burp 的组织器保留有趣的请求响应，也有笔记功能

由于现代 web app 使用大量 js，以及重定向，点击链接以查看最终访问地址

