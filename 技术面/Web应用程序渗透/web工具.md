# 工具

## 可被扫描的练习域名

nmap
- http://scanme.nmap.org/

portswigger
- http://portswigger-labs.net/
- https://ginandjuice.shop/

## 搜索引擎

- 常规搜索引擎：Bing、Google、Baidu、DuckDuckGo
- 历史快照：
    - [Internet Archive Wayback Machine](https://archive.org/web/)，“以数字形式构建互联网站点和其他文化文物的数字图书馆。”
    - [archive.ph](https://archive.ph)（也称为 archive.md）- 按需存档服务，创建永久快照
    - [CachedView](https://cachedview.com/) - 汇集来自多个来源的缓存页面，包括 Google 缓存历史数据、Wayback Machine 等
- 商业网络与安全搜索引擎
    - [Censys](https://censys.io) 索引互联网连接的基础设施，包括服务器、证书和开放服务。有限免费
    - [Shodan](https://www.shodan.io/)，搜索互联网连接设备和服务的服务。有限免费
- 几乎不使用的内容
    - [binsearch.info](https://binsearch.info/)，用于二进制 Usenet 新闻组的搜索引擎。
    - [Common Crawl](https://commoncrawl.org/)，“一个开放的 Web 爬取数据存储库，任何人都可以访问和分析。”

- 搜索模式数据库
    - [Google Hacking Database](https://www.exploit-db.com/google-hacking-database) 搜索模式参考

## 免费IPv6隧道

[tunnelbroker](https://tunnelbroker.net/)

## 公共反向 WHOIS 工具

- [ViewDNS.info](https://viewdns.info/reversewhois/)

## TSL 证书

- [crt.sh](https://crt.sh/)

## 网站截图

- [EyeWitness](https://github.com/RedSiege/EyeWitness)  提供部分服务器头信息，并尽可能识别默认凭证

## 自动化 GitHub 侦察工具

- [Gitrob](https://github.com/michenriksen/gitrob/)
- [TruffleHog](https://github.com/trufflesecurity/truffleHog/)

## 各种 API 密钥使用格式

[KeyHacks](https://github.com/streaak/keyhacks/)

## 开源情报工具

开源情报综合导航
- https://www.osintdirectory.com/

## 可视化工具

- [gephi](https://github.com/gephi/gephi)

## 信息泄露

[谷歌地图 API 扫描器](https://github.com/ozguralp/gmapsapiscanner/)

## 服务器指纹识别

默认错误页面信息汇总：
- https://0xdf.gitlab.io/cheatsheets/404


## 自动化网络扫描工具

- [Netcraft](https://toolbar.netcraft.com/site_report)，一个在线工具，用于扫描站点以获取信息，包括 Web 服务器详细信息。
- [Nikto](https://github.com/sullo/nikto)，一个开源的命令行扫描工具。
- [Nmap](https://nmap.org/)，一个开源的命令行工具，也有 GUI 版本 [Zenmap](https://nmap.org/zenmap/)。


## 集成web工具

- ZAP
- Burp Suite

## 通用模糊测试

- [ffuf](https://github.com/ffuf/ffuf)
- [Gobuster](https://github.com/OJ/gobuster) 

## 目录枚举

- [dirsearch](https://github.com/maurosoria/dirsearch)
- [feroxbuster](https://github.com/epi052/feroxbuster)

## 手动网络工具

HTTP 请求
-  `telnet`，

TLS 请求
- `openssl`。

下载
- `wget`
- `curl`

DNS
- `host`
- `dig`
- `nslookup`

## DNS 枚举

工具
- `amass`
- `subfinder`
- `dnsrecon`
- `fierce`

使用 Web 服务的正向 DNS 查询
- Netcraft [Search DNS](https://searchdns.netcraft.com/?host) 查询属于所选域的名称列表，例如 `example.com`。然后，他们将检查获得的名称是否与他们正在检查的目标相关。

使用 Web 服务的反向 DNS 查询
- [MxToolbox Reverse IP](https://mxtoolbox.com/ReverseLookup.aspx)
- [DNSstuff](https://www.dnsstuff.com/)（提供多种服务）
- [Net Square](https://web.archive.org/web/20190515092354/https://www.net-square.com/mspawn.html)（对域和 IP 地址进行多次查询，需要安装）


## 元文件中的信息泄露

www.robotstxt.org
- `https://example.com/robots.txt`

HTML 文档的 `HEAD` 部分内的 `META` 标签

securitytxt.org
- `https://example.com/security.txt` 
- `https://example.com/.well-known/security.txt`

humanstxt.org
- `https://example.com/humans.txt`

其他 RFC 和互联网草案建议在 `.well-known/` 目录中标准化使用文件。列表：
- [Wikipedia](https://en.wikipedia.org/wiki/List_of_/.well-known/_services_offered_by_webservers)
- [通过 IANA](https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml)

## 文件元数据


PDF 文件：
- `exiftool`
- `pdfinfo` 

Office 文档（DOCX、XLSX）：
- `exiftool`

## 框架的指纹识别工具

[WhatWeb](https://github.com/urbanadventurer/WhatWeb)
[wappalyzer](https://www.wappalyzer.com/)

## 爆破字典

- 综合字典 https://github.com/danielmiessler/SecLists
- 字典导航 https://github.com/gmelodie/awesome-wordlists

# 工具设置

## gephi - 可视化工具

工具
- 选项 
    - 其他
        - 字体 Consolas 16
- appearance
    - look and feel 黑色主题

- Gephi 默认设置
    - 可视化 - 默认背景
    - 预览 - 默认设置

文件 - 新建项目
- 概览 - 底部 - 背景颜色图标
- 预览 - 左侧预览设置 - 预设置