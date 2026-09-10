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

## dockerfile

### FROM

```dockerfile
FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]
```
    
`FROM` 指令用于初始化一个新的构建阶段，并为后续所有指令设置基础镜像。因此，一个有效的 Dockerfile 必须以 `FROM` 指令开头。该指令指定的镜像可以是任何有效的镜像。

### WORKDIR

```dockerfile
WORKDIR /path/to/workdir
```

`WORKDIR` 指令用于设置 Dockerfile 中后续 `RUN`、`CMD`、`ENTRYPOINT`、`COPY` 和 `ADD` 指令的工作目录。如果指定的 `WORKDIR` 不存在，即使它不会被后续任何 Dockerfile 指令使用，也会被自动创建。

### RUN

`RUN` 指令将执行任何命令，在当前镜像之上创建一个新层。新增的层将在 Dockerfile 的下一步中使用。`RUN` 有两种形式：

```dockerfile
# Shell form:
RUN [OPTIONS] <command> ...
# Exec form:
RUN [OPTIONS] [ "<command>", ... ]
```

### ADD

`ADD` 指令有两种形式。当路径中包含空格时，必须使用后一种形式。

```dockerfile
ADD [OPTIONS] <src> ... <dest>
ADD [OPTIONS] ["<src>", ... "<dest>"]
```

`ADD` 指令用于从 `<src>` 复制新文件或目录，并将其添加到镜像文件系统中的 `<dest>` 路径。文件或目录可以从构建上下文、远程 URL 或 Git 仓库复制。

`ADD` 与 `COPY` 指令功能相似，但用途略有不同。详细了解 [`ADD` 与 `COPY` 的区别](https://docs.docker.com/build/building/best-practices/#add-or-copy)。


### COPY

`COPY` 指令有两种形式。后一种形式适用于包含空格的路径。

```dockerfile
COPY [OPTIONS] <src> ... <dest>
COPY [OPTIONS] ["<src>", ... "<dest>"]
```

`COPY` 指令用于从 `<src>` 复制新文件或目录，并将其添加到镜像文件系统中的 `<dest>` 路径。文件或目录可以从构建上下文、构建阶段、命名上下文或镜像中复制。

