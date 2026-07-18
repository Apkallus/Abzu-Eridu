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
    `sudo hping3 -S -p 32769 --ttl 5 -c 1 目标IP`
- S 包在低 TTL 立即得到 RA 响应
    - TTL 在光猫跳数 +1 后得到 RA 响应
    - 光猫的防火墙规则并不存在 RA 响应条目
    - 收到的 RA 包 TTL 为 63（64-1）
    - 最终推测伪造 RA 响应并非来自于光猫，而是光猫下一跳的 ISP 节点
- 查阅文档
    - [linux 内核的转发](https://elixir.bootlin.com/linux/v7.1.3/source/net/ipv4/ip_forward.c) 使用 [RFC 的 TTL 规则](https://www.freesoft.org/CIE/RFC/1812/110.htm)
        - 在 `ip_forward` 函数中，进行 TTL 检查与-1后，最终执行 forward
    - [netfilter hook 流程图](http://wiki.netfilter.org/wiki-nftables/index.php?title=Netfilter_hooks) 在转发 forward 之前仍有其他钩子 prerouting
        - 即使在普通系统中实现 TTL -1 前进行数据包过滤也没有任何障碍
    - [防火墙 REJECT 即支持 TCP RA 响应](https://git.netfilter.org/iptables/tree/extensions/libipt_REJECT.man)
        - 普通系统即可简单实现 TCP reset 响应


nmap 的空闲扫描使用 S 与 SA 包，而 O 检测时使用 S 包，当目标放行 S 而过滤 SA 时：检测到 IPID 递增，然而无法使用 sI 的空闲扫描。曾经出现社区的 S 包空闲扫描补丁，但未成功合并到主版本

sS 在 RIPE 网段发现防火墙/入侵检测系统的伪造大量端口响应：一旦触发伪造，后续对目标IP的扫描无论速率如何均得到伪造响应。然而并未对网段其他 IP 进行响应伪造。切换本机 ip 后恢复正常，此 IDS 仅对特定源 IP 生效
- 触发猜测
    - 任意网关内 ip 达到阈值，即内网单个 ip 速率触发。
        - 不会触发：进行单 ip 慢速，但高并发同时测试大量 ip
    - 互联网 ip 经过网关达到阈值，即外网 ip 速率触发。
        - 不会触发：无论深度/广度扫描，均保持总速率在阈值下
        - 操作：直接设置 max-rate，或设置任务并发数x单主机延迟
- ripe
    - 80p/s 100ms 无触发
    - 240p/s 100ms 无触发

sS 在 RIPE 网段的第二种伪造响应：扫描时触发伪造，但同一本机 ip 第二次测试时未得到伪造响应

Dstny 固定目标 IP 发现几十个开放端口，但不对应任何已知服务。几次切换本机 IP 仍得到相同结果
- 似乎不是 IDS 的伪造响应，用处不明。无视后继续扫描

连通测试
- 从本地 IP 对 CDN 全球节点测速
    - `steamcommunity 302`
- 从本地 IP 对云全球节点测速
    - `https://www.azurespeed.com/Azure/Latency`
- 使用 Looking glass 的从全球节点对本地 IP 进行路由追踪测试

未使用：
- Masscan 识别开放端口
- httpx 识别每个 IP 地址上的 Web 服务器
- Nmap 对这些端口进行有针对性的服务版本扫描

同一主机的 ipv4 与 ipv6 的防火墙策略或许不同，局域网 ip 与公网 ip 的防火墙策略或许不同

