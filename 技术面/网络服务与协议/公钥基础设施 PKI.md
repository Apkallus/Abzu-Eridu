数字签名
- 私钥签名，公钥验证

公钥证书 X.509 标准
- 独特序列号
- 认证机构信息
- 证书有效时间
- 主体拥有者信息
- 主体公钥
- 认证机构签名及签名算法
- 作为中间CA的扩展选项

X.509 
- 二进制数据
- 使用base64编码后保存在 pem 文件中

	
创建 CA
- 创建目录与文件作为 CA信息
- 创建公私钥并生成自签名证书
    `openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -keyout ca.key -out ca.crt`

主体获取CA签名的证书
- 主体创建公私钥并使用公钥生成签名请求
    - `openssl req -newkey rsa:2048 -sha256 -keyout server.key -out server.csr`

CA使用签名请求文件与CA证书生成主体证书，再使用CA私钥签名
- `openssl ca -config myCA_openssl.cnf -policy policy_anything -md sha256 -days 3650 -in server.csr -out server.crt -batch -cert ca.crt -keyfile ca.key`

主体使用证书
- 将证书追加到公私钥文件后，使用此证书
    - apache 服务器
        - 配置文件 /etc/apache2/sites-available
            - SSLCertificateFile 证书路径
            - SSLCertificateKeyFile 私钥路径
- 浏览器导入CA证书
    - Trust this CA to identify websites

CA链
- 根 CA 自签名
- 中间CA由根CA签名
- 验证
    1. 使用根CA验证中间CA
    2. 使用中间CA验证主体

创建中间CA
- 与主体获取Ca签名大致相同，唯一区别在于根 CA使用 -extensions 选项
	
	
主体使用中间ca证书
- 证书顺序为主体+中间CA


攻击面
- 攻破证书认证机构，得到CA颁发证书
- 窃取CA私钥，对证书进行签名
- 对签名使用的hash算法进行碰撞攻击，一个签名证书对应多个域
- 使用特殊字符编码，对名称进行确认时产生与目标形似的字符

证书类型
- DV域名验证
	- 电子邮件，发送到注册邮箱验证
	- http，设置服务器文件到独特数据
	- dns，设置ns服务器的cname记录到独特数据
- OV机构验证
- EV扩展验证
	- 浏览器使用独特EV列表与展示方式


openssl 命令
- s_client 开启客户端
	- -showcerts 显示证书
	- -connect 连接服务器
	- -CAfile 使用CA证书
- x509 格式转换
	- -in 输入文件.pem 
	- -outform 输出格式
	- -text 纯文本
    - -noout 无编码版本
    
- req
	- -x509 生成自签名公钥证书，否则为签发请求
	- -newkey 公私钥算法与长度
	- -days 过期时长
	- -keyout 私钥导出文件
	- -out 公钥签名证书导出文件
	- -sha256 签名算法
    - -subj 设置主体信息
    - -passout pass:密码设置
	- -new 创建签名请求
		- -key 导入公私钥
		- -out 导出签名请求文件
		
- genrsa 生成公私钥
	- -aes128 是否使用密码保护
	- -out 公私钥导出文件
- ca
	- -in 导入签名请求
	- -out 导出证书文件
	- -md 签名算法
	- -cert 导入CA签名证书
	- -keyfile 导入CA公私钥
	- -config 使用非默认配置文件
	- -extensions 设置中间CA扩展选项
- s_server 开启服务器
	- -cert 使用证书
	- -accept 监听端口
- verify 验证证书
	- -CAfile 使用CA证书
	- -untreated 待验证证书链
- 配置文件 /usr/lib/ssl/openssl.cnf
	- policy
		- policy_match 请求主体与CA的域匹配
		- policy_anything 无域匹配限制


## 资料

https://seedsecuritylabs.org/Labs_20.04/Files_cn/Crypto_PKI_cn.pdf