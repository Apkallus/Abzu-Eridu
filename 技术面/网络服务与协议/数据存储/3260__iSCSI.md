

## iSCSI

概念：
- iSCSI通过TCP端口3260暴露，提供对存储阵列的网络访问。

工具：
- Nmap通过`iscsi-info`和`iscsi-brute`脚本探测和攻击暴露的iSCSI服务

如果在测试期间发现iSCSI服务，配置挂载卷并访问数据。
