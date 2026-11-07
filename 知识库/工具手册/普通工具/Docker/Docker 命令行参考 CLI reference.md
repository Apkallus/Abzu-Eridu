# CLI reference - docker

https://docs.docker.com/reference/cli/docker/

## docker image

https://docs.docker.com/reference/cli/docker/image/

### docker image pull —— Download an image from a registry

```sh
docker image pull [OPTIONS] NAME[:TAG|@DIGEST]

# 别名
docker pull
```

## docker compose

https://docs.docker.com/reference/cli/docker/compose/

### ♾️ docker compose up

https://docs.docker.com/reference/cli/docker/compose/up/

```sh
docker compose up [OPTIONS] [SERVICE...]
```

构建、（重新）创建、启动并附加到服务的容器。

除非它们已经在运行，此命令还会启动任何链接的服务。

`docker compose up` 命令会聚合每个容器的输出（就像 `docker compose logs --follow` 那样）。可以选择使用 `--attach` 标志来选择要附加的服务子集，或使用 `--no-attach` 排除某些服务，以防止输出被某些冗长服务淹没。

当命令退出时，所有容器都会停止。运行 `docker compose up --detach` 会在后台启动容器并让它们保持运行。

如果某个服务已有容器，并且该服务的配置或镜像在容器创建后发生了更改，`docker compose up` 会通过停止并重新创建容器来采纳这些更改（保留已挂载的卷）。要阻止 Compose 采纳更改，请使用 `--no-recreate` 标志。

如果要强制 Compose 停止并重新创建所有容器，请使用 `--force-recreate` 标志。

如果进程遇到错误，此命令的退出代码为 `1`。如果进程被 `SIGINT`（ctrl + C）或 `SIGTERM` 中断，容器会停止，退出代码为 `0`。

参数
- `--pull`
  Pull image before running (`"always"|"missing"|"never"`)
  > 排障用构建项 `--pull always` 


### docker compose down

https://docs.docker.com/reference/cli/docker/compose/down/

- 描述
  停止并移除容器、网络
- 用法

  ```console
  docker compose down [OPTIONS] [SERVICES]
  ```

> 构建失败时，排障用清理项

#### 描述

停止容器，并移除由 `up` 创建的容器、网络、卷和镜像。

默认情况下，仅移除以下内容：

- Compose 文件中定义的服务对应的容器。
- Compose 文件 `networks` 部分中定义的网络。
- 默认网络（如果使用了）。

定义为外部的网络和卷永远不会被移除。

默认情况下不会移除匿名卷。但是，由于匿名卷没有稳定的名称，后续的 `up` 不会自动挂载它们。对于需要在更新之间持久保存的数据，请使用显式路径作为绑定挂载或命名卷。

##### 启动前钩子容器

当 `pre_start` 生命周期钩子失败时，Compose 会保留其容器以供事后检查，而不是立即移除它。`compose down` 会在清理过程中自动移除这些保留的钩子容器，因此它们不会随着时间累积。

要列出运行 `down` 之前保留的钩子容器：

```console
$ docker ps -a --filter label=com.docker.compose.hook=pre_start
```

#### 选项

| 选项 | 默认值 | 描述 |
| --- | --- | --- |
| `--remove-orphans` |  | 移除未在 Compose 文件中定义的服务对应的容器 |
| `--rmi` |  | 移除服务使用的镜像。`"local"` 仅移除没有自定义标签的镜像（`"local"` 或 `"all"`） |
| `-t, --timeout` |  | 指定关闭超时时间（秒） |
| `-v, --volumes` |  | 移除 Compose 文件 `volumes` 部分中声明的命名卷以及附加到容器的匿名卷 |


## docker container
### docker container run

https://docs.docker.com/reference/cli/docker/container/run/

```sh
# Usage	
docker container run [OPTIONS] IMAGE [COMMAND] [ARG...]

# Aliases
docker run
```

`docker run` 命令在新容器中运行指定命令，必要时会自动拉取镜像并启动容器。

如需保留所有更改并重新启动已停止的容器，可使用 `docker start` 命令。

使用 `docker ps -a` 可以查看所有容器的列表，包括已停止的容器。


- `-t, --tty`
  分配伪终端（pseudo-TTY）
- `-i, --interactive`
  即使未附加也保持标准输入（STDIN）开启
  

### docker container start

https://docs.docker.com/reference/cli/docker/container/start/

```sh
# Usage	
docker container start [OPTIONS] CONTAINER [CONTAINER...]

# Aliases	
docker start
```

Start one or more stopped containers

### docker container attach

```sh
# Usage	
docker container attach [OPTIONS] CONTAINER

# Aliases
docker attach
```

连接终端与容器