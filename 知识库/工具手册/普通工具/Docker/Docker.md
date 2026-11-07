# docker

`docker run -d -p 127.0.0.1:3000:3000 getting-started`
[文档](https://docs.docker.com/get-started/workshop/02_our_app/)

- `docker run`
	运行容器，并指定镜像的名称
- `-p HOST:CONTAINER`
	用于在主机和容器之间创建端口映射，其中 HOST 是主机上的地址， CONTAINER 是容器上的端口

- `-ps`
	显示正在运行的容器。要查看所有容器，使用 --all （或 -a ）标志
- `docker exec [OPTIONS] CONTAINER COMMAND [ARG...]` 
	运行中的容器中执行新命令，[文档](https://docs.docker.com/reference/cli/docker/container/exec/)
	- `-i, --interactive`
		即使未附加也保持 STDIN 打开
	- `-t, --tty`		
		分配伪终端
	- `-u, --user`
		Username or UID，使用 `-u root` 或 `-u 0`以root权限进入
	
	例，`docker exec -u root -it 容器名或ID /bin/bash`

## 使用

若容器设置本地配置文件映射，更新时仅需删除容器后映射相同配置文件（作为命令行参数，使用相同命令）。即可实现快速重新部署

### kali docker

[kali docker 镜像](https://www.kali.org/docs/containers/official-kalilinux-docker-images/)

[使用 Kali Linux Docker 镜像](https://www.kali.org/docs/containers/using-kali-docker-images/)

```sh
# 拉取最新镜像
docker pull docker.io/kalilinux/kali-rolling

# 运行容器，并分配伪终端
docker run --tty --interactive kalilinux/kali-rolling

# 设置 kali 仓库为清华源，容器初始无仓库源文件
touch /etc/apt/sources.list
echo -n 'deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main non-free contrib non-free-firmware' > /etc/apt/sources.list

# 使用默认项安装工具包
apt update && apt -y install kali-linux-headless

# 启动之前的容器
docker start 容器哈希

# 附加容器
docker attach 容器哈希
```
- 容器默认在同一子网，此时可直接访问挑战容器
	> [!warning] 遇到严重网络连接卡顿，似乎需使用其他网络配置

## 排障

```sh
docker compose down
docker compose up --pull always
```

## Manuals

### Docker Compose

#### How-tos

##### Networking

https://docs.docker.com/compose/how-tos/networking/


Compose 默认会为你处理网络，但在需要时也提供细粒度控制。本页解释默认网络如何工作，以及容器如何通过名称相互发现。还涵盖何时以及如何定义自定义网络、跨不同 Compose 项目连接服务、映射自定义主机名，以及调试连接问题。

###### 默认网络和服务发现

默认情况下，Compose 会为你的应用设置一个单一的[网络](https://docs.docker.com/reference/cli/docker/network/create/)。服务的每个容器都会加入该默认网络，既可被该网络上的其他容器访问，也可通过其服务名称被发现。此网络使用 `bridge` 驱动。要将服务连接到不同的 Compose 网络或外部网络，请参阅[指定自定义网络]。要更改服务使用主机网络栈的方式（`network_mode: host`），请参阅[更改网络模式]。

对于大多数开发设置，默认网络就足够了。当你运行 `docker compose up` 时，Compose 会创建一个名为 `<project-name>_default` 的网络，并将所有服务连接到它。每个服务都会向内部 DNS 服务器注册其名称，因此容器可以直接使用服务名称相互访问。无需 IP 地址或手动配置。

例如，假设你的应用位于名为 `myapp` 的目录中，并且你的 `compose.yaml` 如下所示：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:latest
    ports:
      - "8001:5432"
```

Compose 会自动将所有服务连接到默认网络，因此你无需在 Compose 文件中显式定义 `networks`。

当你运行 `docker compose up` 时，会发生以下情况：

1. 创建一个名为 `myapp_default` 的网络。
2. 使用 `web` 的配置创建一个容器。它以名称 `web` 加入 `myapp_default`。
3. 使用 `db` 的配置创建一个容器。它以名称 `db` 加入 `myapp_default`。

现在每个容器都可以查找服务名称 `web` 或 `db`，并获取相应容器的 IP 地址。`web` 服务可以通过 `postgres://db:5432` 连接到数据库。如果容器在本地运行，从主机机器可以通过 `postgres://localhost:8001` 访问同一个数据库。

> **提示**
>
> Docker 在每次容器启动时从网络子网动态分配容器 IP 地址，因此它们不会在重启或重新创建后持久保留。这意味着你应始终通过名称而非 IP 地址引用服务。当容器被重新创建时（例如配置更改后），它们会获得新的 IP 地址。服务名称保持稳定。

你的应用的网络名称基于“项目名称”，该名称取自其所在目录的名称。你可以使用 [`--project-name` 标志]或 [`COMPOSE_PROJECT_NAME` 环境变量]覆盖项目名称。

`HOST_PORT` 和 `CONTAINER_PORT` 用途不同。在上面的示例中，对于 `db`，`HOST_PORT` 是 `8001`，容器端口是 `5432`（Postgres 默认值）。网络化的服务间通信使用 `CONTAINER_PORT`。主机端口仅在从网络外部访问服务时使用。

