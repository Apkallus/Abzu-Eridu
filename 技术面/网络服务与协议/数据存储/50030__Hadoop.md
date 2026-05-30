
## Apache Hadoop

概念：
- Hadoop是一个开源框架，支持使用计算机集群进行大型数据集的分布式存储和处理。存储由Hadoop分布式文件系统（HDFS）处理，处理通过YARN使用MapReduce和其他应用程序（例如Apache Storm、Flink和Spark）执行。

工具：
- Nmap脚本查询MapReduce和HDFS服务（包括默认端口详情）

    | 脚本名称                             | 端口    | 用途                       |
    | -------------------------------- | ----- | ------------------------ |
    | `hadoop-jobtracker-info`         | 50030 | 从MapReduce作业和任务跟踪器服务检索信息 |
    | `hadoop-tasktracker-info`        | 50060 |                          |
    | `hadoop-namenode-info`           | 50070 | 从HDFS名称节点检索信息            |
    | `hadoop-datanode-info`           | 50075 | 从HDFS数据节点检索信息            |
    | `hadoop-secondary-namenode-info` | 50090 | 从HDFS辅助名称节点检索信息          |

- 轻量级Python和Go HDFS客户端

已知缺陷：
- Hadoop默认无认证运行。配置HDFS、YARN和MapReduce服务使用Kerberos。NVD列出了Hadoop认证绕过和身份冒充。
