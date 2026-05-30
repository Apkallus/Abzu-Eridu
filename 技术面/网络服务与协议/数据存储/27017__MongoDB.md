
## MongoDB

概念：
- MongoDB是一个跨平台的面向文档的数据库。默认情况下，服务器监听TCP端口27017，并在无认证的情况下运行。

Shodan提供了在线暴露实例的详细信息。

Nmap通过`mongodb-databases`和`mongodb-info`脚本查询可用服务

Metasploit支持对需要认证的暴露MongoDB实例进行暴力破解密码（通过`mongodb_login`）。获得服务访问权限后，使用已知缺陷执行命令，并使用NoSQLMap克隆可用数据库。
