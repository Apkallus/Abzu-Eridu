<https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/concepts.html>


## 使用实例元数据管理 EC2 实例

> 虽然您只能从实例本身中访问实例元数据和用户数据，但并未使用身份验证或加密方法对数据进行保护。任何可以直接访问实例的人以及可能在实例上运行的任何软件都可以查看其元数据。因此，您不应将敏感数据（例如密码或长期保存的加密密钥）存储为用户数据。

### 实例元数据类别

- `iam/security-credentials/role-name`
    - 如果存在与实例关联的 IAM 角色，则 role-name 为角色的名称，并且 role-name 包含与角色关联的临时安全凭证 (有关更多信息，请参阅 从实例元数据中检索安全凭证)。如果没有，则不显示。


## 使用实例元数据服务访问实例元数据

<https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html>

查看使用示例

- 获取实例元数据的可用版本
    ```log
    [ec2-user ~]$ curl http://169.254.169.254/
    1.0
    2007-01-19
    2016-04-19
    latest
    ```
    - 访问固定端点则列出版本

- 获取顶级元数据项
    ```log
    [ec2-user ~]$ curl http://169.254.169.254/latest/meta-data/    
    ami-id
    events/
    hostname
    iam/
    ```