azure
- 概念
	- 资产结构设置访问控制
		- 按照树状层级组织订阅模型，权限继承
	- azure 使用虚拟机，存在更多利用途径
	- azure 与 azure AD两个系统紧密集成
- 区别
	- 权限结构
		- aws api密钥编程访问与 iam 模型
		- azure ad 身份提供方的各种Oauth流
	- 开箱即用
		- aws 无，需手动构建
		- azure 自动管理系统，run-command 特性
	- 函数服务
		- aws 独立函数
		- azure 在同一应用程序的函数共享磁盘且无分割
- 实验环境 purplecloud

azure 宿主系统攻击
- 查找使用 azure 的租户
	- 使用 openidconnect 的周知端点查看是否在 azure
	- 访问 getuserrealm 端点查看租户类型
	- azure 账户通常为邮箱地址
		- 从社交平台、职业平台搜集邮箱信息，或姓名等信息构建探测邮件地址
	- 或使用当前域构建账户格式地址
- 对一批账户进行口令喷洒
	- 基于账户锁定，并非尝试密码爆破特定账户，而是对一批账户进行特定密码探测
	- 工具
		- maolspray, o365spray
	- o365spray
		- 枚举用户
		- 支持多种身份验证
		- 拥有口令喷洒功能
- 使用得到的凭证
	- 尝试登录
	- 查看虚拟机列表
	- 尝试执行命令或更改机器

控制平面
- 当拥有域控制器的凭证
- 查询身份元数据，得到 jwt 令牌
- 使用jwt令牌到 restful 端点
- 在域控制器安装 azure cli，并测试运行命令，从而实现远程命令执行
- 设置后门
	- 禁用windows 防御
	- 设置 MeterPreter 代理
	- 获得反向shell
