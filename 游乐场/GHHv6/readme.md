以下是针对本书中所有 AWS 实验的说明。第8章中另有 Azure 相关说明。

###### 云端环境搭建指南
1. 注册 AWS 账户  
   访问 https://aws.amazon.com 并注册一个新账户。

2. 这些实验环境设计用于 \*nix 系统。你可使用下载的 Kali Linux（https://www.kali.org/downloads/）安装版、你喜欢的任意 \*nix 发行版，或 Windows Subsystem for Linux（https://docs.microsoft.com/en-us/windows/wsl/install-win10）来运行。  
   另外，如果你希望完全在云端操作，登录账户后可打开 Amazon CloudShell。若采用此方式，请确保为其开启独立标签页，因为你需要从 Amazon AWS 控制台的其他页面复制/粘贴信息。

3. 安装以下工具：  
   AWS CLI（https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html）  
   Packer（https://learn.hashicorp.com/tutorials/packer/getting-started-install）  
   Terraform（https://learn.hashicorp.com/tutorials/terraform/install-cli）  
   Ansible（https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html）  
   jq（apt-get install jq 或 https://stedolan.github.io/jq/）

   若使用 Amazon CloudShell，请运行以下命令：
```
git clone https://github.com/GrayHatHacking/GHHv6.git
cd GHHv6/CloudSetup
bash install-cloud-tools.sh
. ~/.bash_profile
```
   若使用 Kali Linux，请运行以下命令：
```
git clone https://github.com/GrayHatHacking/GHHv6.git
sudo apt-get update
sudo apt-get install awscli packer software-properties-common ansible jq
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com buster main"
sudo apt-get update && sudo apt-get install terraform
```

4. 在 AWS 控制台中，进入“我的安全凭据”  
   ![我的安全凭据图片](https://github.com/GrayHatHacking/GHHv6/blob/main/CloudSetup/images/aws-signup-1.png)  
   转到访问密钥并点击“新建访问密钥”  
   ![新建访问密钥图片](https://github.com/GrayHatHacking/GHHv6/blob/main/CloudSetup/images/aws-signup-2.png)  
   下载密钥文件  
   ![下载密钥文件](https://github.com/GrayHatHacking/GHHv6/blob/main/CloudSetup/images/aws-signup-3.png)

5. 用编辑器打开该文件，然后打开终端窗口并输入：
   `aws configure`  
   ![AWS 配置图片](https://github.com/GrayHatHacking/GHHv6/blob/main/CloudSetup/images/aws-signup-4.png)  
   将文件中的访问密钥和私有密钥填入配置，区域选择 `us-east-1`。该区域包含我们将用到的所有 AWS 功能，是一个安全的默认选择。默认输出格式请选择 `json`。

6. 若你尚未执行此操作，请克隆本仓库：  
   `git clone https://github.com/GrayHatHacking/GHHv6.git`  
   进入 CloudSetup 目录并运行 `provision.sh` 脚本。这将为本书所有练习创建必要的角色和权限。脚本会新建一个名为 `ghh` 的用户和一个名为 `ghh` 的配置文件，以便所有示例无需修改即可运行。

7. 这些练习需要使用 SSH 密钥。若你尚未创建，请运行 `ssh-keygen` 生成一个新的密钥对。结果将在 `~/.ssh/` 目录下生成 `id_rsa` 和 `id_rsa.pub` 两个文件。这些文件将用于在 AWS 中生成密钥以便 SSH 连接，并使后续示例操作更加简便。

8. 在 AWS 中创建密钥对：  
   `aws ec2 import-key-pair --key-name ghh --public-key-material fileb://~/.ssh/id_rsa.pub --profile=ghh --region=us-east-1`

9. 运行 `build-images.sh` 为后续练习构建基础镜像。此过程可能需要几分钟到一小时。