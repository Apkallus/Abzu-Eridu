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

sS 在 RIPE 网段发现防火墙/入侵检测系统的伪造大量端口响应：一旦触发伪造，后续对目标IP的扫描无论速率如何均得到伪造响应。然而并未对网段其他 IP 进行响应伪造。
- 触发猜测
    - 任意网关内 ip 达到阈值，即内网单个 ip 速率触发。
        - 不会触发：进行单 ip 慢速，但高并发同时测试大量 ip
    - 互联网 ip 经过网关达到阈值，即外网 ip 速率触发。
        - 不会触发：无论深度/广度扫描，均保持总速率在阈值下
        - 操作：直接设置 max-rate，或设置任务并发数x单主机延迟
- ripe
    - 80p/s 100ms 无触发
    - 240p/s 100ms 无触发

连通测试
- 从本地 IP 对 CDN 全球节点测速
    - `steamcommunity 302`
- 从本地 IP 对云全球节点测速
    - `https://www.azurespeed.com/Azure/Latency`
- 使用 Looking glass 的从全球节点对本地 IP 进行路由追踪测试