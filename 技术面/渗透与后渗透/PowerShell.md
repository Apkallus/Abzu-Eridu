powershell
- 万能工具
- 模块化脚本

脚本
- 受限制策略，禁止执行未签名脚本，仅允许交互式命令
- 无限制或远程签名策略，允许执行脚本
	- 然而组策略强制执行导致修改策略很困难
- 支持base64编码的Unicode字符串脚本导入
	- 工具：
		- gem install rbbk组合工具中的 iconv 与 b64
		- linux中的powershell为pswh
- web导入
	- Invoke-WebRequest 下载脚本
		- -UseBasicParsing 不尝试解析
		- 或加载后使用base64解码再Unicode解码
	- Invoke-Expression 运行脚本
- powersploit工具集
	- 当前github项目已存档
	- windows amsi恶意软件扫描接口阻止脚本执行
		- 禁用 amsi
		- 混淆脚本
- powershell empire c2
	- 确保使用的80与443端口未被占用
	- launcher.bat 应对 amsi阻止
		- 禁用 amsi
		- 提取base64字符串后远程加载脚本解码再运行
	- winrm 提权
		- 概念：使用相同账户凭证，运行 winrm 的环境具有高完整性级别
		- evil-winrm 连接 
	- 查看保存的账户凭证
		- 使用模块 credentials/mimikatz/logonpasswords*
		- 得到明文凭证与ntlm哈希
	- 持久化
		- 关闭windows实时保护
		- 使用 wmi 模块设置持久化
		- 重启后获得反向shell
atips
- Python的服务器功能
