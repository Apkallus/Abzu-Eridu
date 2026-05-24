资料
- windows 第七版
- windows 内核编程，作者 pavel


网络调试设置
- 两台windows虚拟机，安装一台后克隆
	- 调试器机
		- 安装windbg
	- 调试目标机
		- 管理员启用网络内核调试 
			- bcdedit.exe /debug on 
			- bcdedit.exe /dbgsettings net hostip:1.1.1.1 port:50000
			- 复制密钥到调试器机
			- 重启进入调试模式
- 在调试器机的网络调试功能输入目标机的ip端口与密钥
	- windbg.exe -k
	- 确保两台虚拟机可进行网络连接
	- 或需关闭防火墙

探索目标
- 并非立即分析windows内核，而是分析已知缺陷的内核驱动
- 追踪操作操作内存的函数，如 strcpy, memcpy, memmove. 以查找读写原语
	- 查看交叉引用，确认是否可控制参数寄存器
		- 即，追踪寄存器设置链是否可追溯到可控内存
	- 找到可控代码块后查找引用此代码的路径
- 编写代码与内核设备进行通信，对目标代码块的通信方式使用循环字符串
	- 调试器查看目标代码块中参数的值或指向内存中的控制状态

令牌窃取
- 使用高权限进程元数据结构中的令牌字段指针，覆盖低权限进程的对应字段
	- 系统进程始终拥有id4，且使用 SYSTEM 令牌的完全权限
	- 进程结构 EPROCESS 中的字段包含：
		- 进程id UniqueProcessld
		- 进程结构双向链表 ActiveProcessLinks
		- 令牌 Token
	- 内核符号 PsInitialSystemProcess 指向系统进程结构

内核基址查找
- EnumDeviceDrivers 函数定位每个驱动程序基址，得到迭代器
- GetDeviceDriverBaseNameA 使用每个驱动程序基址获取驱动程序名称，遍历迭代器时查看名称匹配ntoskrnl.exe则得到内核基址

计算PsInitialSystemProcess符号内核地址
- 在用户态加载ntoskrnl.exe后得到用户态中PsInitialSystemProcess符号地址，以计算符号相对偏移
- 使用内核基址与进程指针符号相对偏移得到PsInitialSystemProcess内核地址

提权
- 调试器得到EPROCESS结构中字段偏移
- 任意读得到令牌
- 提权
	- 遍历链表寻找与当前进程id匹配的进程结构
	- 任意写覆盖当前进程令牌
- 创建 shell 子进程
