后渗透：在获得初始访问目标作为立足点后
- 对本地和域进行
	- 侦查
	- 提权
	- 持久化
- 使用工具，如powershell、二进制文件识别漏洞
	- 服务
	- 权限
	- 配置

侦查
- 用户侦查
	- whoami /user 查看权限与suid
		- suid 格式
			S-1-5-21-3262898812-2511208411-1049563518-1111
			- 域suid：最后一个横杠前的全部字符串
			- 用户id：最后一个横杠后的字符串
				- 低于1000为特权用户
	- whoami /fqdn
		- dn 完全限定名格式
			CN=target,CN=Users,DC=ghh,DC=local
			- CN：从左到右为具体到不具体
				Users容器中的target
			- DC：从左到右的每个字段加点'.'以构建完整域名 
				ghh.local
	- whoami /group 查看组
		- 类型
			- 周知组拥有相同suid，例 everyone
			- 别名组通常为特权组
			- group组为本地组或活动目录组
	- whoami /priv 查看特权
			
			
	- seatbelt 工具查找信息
		- 导航到工具目录后使用Python建立简易服务器
		- 目标机器运行powershell后从Python服务器下载seatbelt模块
				
- 系统侦查
	- 概念：查看防护与权限状态，以及提权移动路径
	- powershell系统侦查
		- amsi
			- 读取amsi提供方的注册表子项并获取所有id
			- 使用获取的id在CLSID注册表中查看其名称、属性、路径
		- 日志策略
			- 查看是否存在日志策略
			- 若存在则尝试降级到PS2.0
				- 已安装2.0版本 ps
				- 拥有v2版 .net 组件
		- Get-ComputerInfo 查看操作系统基本信息
	- seatbelt 系统侦查
	- 若启用 uac 用户账户控制，运行二进制文件时将弹出提示，而攻击者的c2无法接收提示

ad 域
- PS侦查 
	- GetCurrentDomain() 获取域信息
	- 使用 whoami /fqdn 的用户信息到 ldap 中查询域中用户信息详情
	- 在搜索器中搜索域的组织单元ou信息
	- 使用有趣的组织单元信息到 ldap 中查看组权限详情
	- 在搜索器中搜索有趣的组，以获得组的成员信息
- 使用 powersploit 的 powerview 侦查
- 使用 bloodhound 的 sharphound 侦查

提权
- 本地提权
	- winpeas 工具分析系统漏洞
	- sharpup 工具分析系统漏洞
		- 如，可修改的服务二进制文件添加用户到管理员组，之后重启服务、注销登录或runas等方法启动新会话
- 域提权
	- 服务账户的描述中包含口令
	- Rubeus 工具执行kerberos的侦查与利用
		- SPN 标识映射服务与账户，在TGS票据授予服务中获取此票据，导出为ntlm哈希，破解后得到服务口令
		- AS-REP 预身份验证使用相同方式破解
	- 获取用户凭证后，查看用户组信息以及访问控制权限
	- 使用管理员凭证登录后，Rubeus 使用凭证添加tgt票据
		 
	- 使用 BetterSafetyKatz 对 krbtgt 账户进行 dcsync 攻击，得到sid与aes256_hmac 哈希
	- 在黄金票据攻击中使用之前的 sid与hmac哈希以伪造域管理员票据
- 域权限维持
	- AdminSDHolder 每小时将权限传播到域的其他组
		- 加载。powerview 使用域同步账户查看AdminSDHolder对象权限
		- 向 AdminSDHolder 对象添加访问控制权限到用户
	- sidhistory 域迁移功能：存储原账户sid或组sid
		- 使用域管理员令牌访问dc
			- 安装 dsinternals powershell 模块并导入
			- 停止ntds服务以解除数据库文件的锁定
			- Add-ADDBSidHistory 添加域管理员的sid到目标用户并指定ntds.dit 路径
			- 几秒后重启ntds服务
