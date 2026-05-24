## 1 渗透测试的绝对基础
- 渗透测试执行标准（PTES）的各阶段
- 参与前交互
- 情报收集
- 威胁建模
- 漏洞分析
- 漏洞利用
- 后渗透利用
- 报告编写
- 渗透测试的类型

## 2 Metasploit 基础
- 术语
  - 漏洞利用
  - 载荷
  - Shellcode
  - 模块
  - 监听器
- Metasploit 接口
  - MSFconsole
  - 资源脚本
  - Armitage 和 Cobalt Strike
- Metasploit 工具
  - MSFvenom
  - NASM Shell
  - Metasploit Pro
- 总结

## 3 情报收集
- 被动信息收集
  - Whois 查询
  - Netcraft
  - DNS 分析
- 主动信息收集
  - 使用 Nmap 进行端口扫描
  - 使用 Metasploit 进行端口扫描
  - 定向扫描
  - 扫描服务器消息块（SMB）
  - 寻找配置不当的 Microsoft SQL Server
  - 扫描 S3 存储桶
  - 扫描 SSH 服务器版本
  - 扫描 FTP 服务器
  - 扫描简单网络管理协议（SNMP）
  - 编写自定义扫描器
- 总结

## 4 漏洞分析

## 5 漏洞利用的乐趣
- 基础漏洞利用
  - 搜索漏洞利用
    - searchsploit
    - info
  - 选择漏洞利用
    - show payloads
    - show targets
    - set 和 unset
    - save
    - exploit
- 攻击 Windows 主机
- 攻击 Ubuntu 主机
- 总结

## 6 Meterpreter
- 攻击 Windows 虚拟机
- 使用 Nmap 进行端口扫描
- 暴力破解 MySQL 服务器认证
- 上传用户定义函数
- Meterpreter 基本命令
- 捕获屏幕截图
- 查找平台信息
- 捕获键盘输入
- 提取密码哈希
- 哈希传递

- Mimikatz 和 Kiwi
- 权限提升
- 横向移动技术
- 令牌伪造
- DCSync 和黄金票据攻击
- 其他有用的 Meterpreter 命令
  - 启用远程桌面服务
  - 查看目标上的所有流量
  - 信息收集（Scraping a System）
- 建立持久化
- 使用 Railgun 操作 Windows API
- 跳板（Pivoting）到其他系统
- 总结

## 7 规避检测
- 使用 MSFvenom 创建独立二进制文件
- 使用 MSFvenom 进行编码
- 打包可执行文件
- 自定义可执行模板
- 隐蔽启动载荷
- 规避模块
- 开发自定义载荷
- 从 Python 文件生成可执行文件
- 总结

## 8 社会工程学
- 更新和配置社会工程师工具包（SET）
- 鱼叉式网络钓鱼攻击
  - 搭建邮件服务器
  - 发送恶意邮件
- 使用 Gophish 进行钓鱼
- Web 攻击
  - 用户名和密码收割
  - 标签绑架（Tabnabbing）
  - 绕过双因素认证
- 感染性媒体生成攻击
- 总结

## 9 客户端侧攻击
- 基于浏览器的漏洞利用
- 在 Metasploit 中查找漏洞利用
- 使用 AutoPwn2 自动化利用

## 10 无线攻击
- 连接无线网卡
- 监控 Wi-Fi 流量
- 取消认证和 DoS 攻击
- 捕获和破解握手包
- 邪恶双子攻击
- 使用 Metasploit 嗅探流量
- 使用 Wi-Fi Pineapple 收集凭证
- 总结

## 11 辅助模块
- 探索辅助模块
- 搜索 HTTP 模块
- 创建辅助模块
  - 编写模块
  - 运行模块
  - 调试模块
- 总结

## 12 将漏洞移植到框架中
- 汇编语言基础
- EIP 和 ESP 寄存器
- JMP 指令集
- NOP 和 NOP 滑板
- 禁用保护机制
- 移植缓冲区溢出漏洞
  - 剥离现有漏洞利用代码
  - 配置漏洞利用定义
  - 测试基础漏洞利用
  - 实现框架特性
  - 添加随机化
  - 移除 NOP 滑板
  - 移除哑 shellcode
- 移植 SEH 覆盖漏洞利用
- 总结

## 13 构建自己的模块
- 在 MS SQL 上获得命令执行
- 启用管理员级存储过程
- 运行模块
- 探索模块代码
- 创建新模块
- 编辑现有模块
- 运行 Shell 漏洞利用
- 定义漏洞利用
- 上传 PowerShell 脚本
- 运行漏洞利用
- 总结

## 14 创建自己的漏洞利用
- 模糊测试的艺术
  - 下载测试应用程序
  - 编写模糊器
  - 测试模糊器
- 控制结构化异常处理（SEH）
- 绕过限制
- 获取返回地址
- 包含向后跳转和近跳转
- 添加载荷
- 坏字符和远程代码执行
- 总结

## 15 模拟渗透测试
- 参与前交互
- 情报收集
- 威胁建模
- 漏洞利用
  - 执行漏洞利用
  - 建立持久化
- 后渗透利用
  - 扫描 Linux 系统
  - 识别易受攻击的服务
  - 攻击 Apache Tomcat
  - 攻击不常见的服务
  - 清理痕迹
- 总结

## 16 云渗透测试
- 云安全基础
- 身份和访问管理
- 无服务器函数
- 存储
- Docker 容器
- 搭建云测试环境
- 容器接管
- 逃逸 Docker 容器
- Kubernetes
- 总结

## 附录 A：搭建实验环境
- x86 和 AMD64
- ARM 和 Apple Silicon
- 安装 Kali 元包

## 附录 B：速查表
- MSFconsole
- Meterpreter
- MSFvenom
- Meterpreter 后渗透利用
