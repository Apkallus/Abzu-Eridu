
## PostgreSQL

概念：
- PostgreSQL是一个对象关系数据库管理系统（ORDBMS），默认使用TCP端口5432为客户端提供服务。

指纹识别：
- Nmap

NVD中列出了大量导致命令执行和权限提升的已认证问题

### 暴力破解密码

工具：
- Metasploit的`postgres_login`模块测试可用服务是否存在弱凭证
- Nmap中的`pgsql-brute`脚本
- `psql`客户端

### 已认证的PostgreSQL攻击

用于PostgreSQL的已认证Metasploit模块

| 模块                    | 用途                                         |
| --------------------- | ------------------------------------------ |
| `postgres_sql`        | 执行任意SQL语句                                  |
| `postgres_hashdump`   | 提取用户名和密码哈希值                                |
| `postgres_schemadump` | 显示数据库模式                                    |
| `postgres_readfile`   | 导入本地文件并显示（例如 `/etc/passwd`）                |
| `postgres_payload`    | 通过`pg_largeobject`加载共享对象并创建UDF，在服务器端执行任意代码 |

使用Metasploit和Hashcat获取、准备和破解用户密码哈希。通过Metasploit使用`postgres_payload`模块执行命令。
