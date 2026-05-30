## MySQL

概念：
- MySQL通常监听在基于Unix和Windows的服务器的TCP端口3306。

指纹识别工具：
- Nmap

NVD列出了MySQL中多个严重的、未经认证即可远程利用的漏洞

### 暴力破解密码

许多产品使用默认密码配置MySQL帐户

工具：
- Metasploit `mysql_login` 模块
- mysql客户端

### 已认证的MySQL攻击

查询漏洞数据库查看已知缺陷
搜索 MSF 的对应模块

#### 通过MySQL执行本地操作系统命令

如果能够将一个恶意共享库上传到MySQL可读的目录结构中（通过Web应用程序漏洞、FTP或其他方式），则可以通过MySQL加载该库作为用户定义函数（UDF）来实现操作系统命令执行。Bernardo Damele A. G.的`udfhac` GitHub仓库[^4]包含其共享库的源代码。可以在`sqlmap`[^5]的`udf/mysql/`目录下找到适用于Windows和Linux的32位和64位编译版本。

最初由Adam Palmer[^6]描述。


[^4]: 参见GitHub上的 [udfhac](http://bit.ly/2aDpqhd)。  
[^5]: 参见GitHub上的 [sqlmap](http://bit.ly/2aDoCbS)。  
[^6]: Adam Palmer, [“MySQL Root to System Root with lib_mysqludf_sys for Windows and Linux”](http://bit.ly/2aDp3D6), IO Digital Sec, 2013年8月13日。
