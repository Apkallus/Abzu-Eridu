# dockerfile

https://docs.docker.com/reference/dockerfile/

## FROM

```dockerfile
FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]
```
    
`FROM` 指令用于初始化一个新的构建阶段，并为后续所有指令设置基础镜像。因此，一个有效的 Dockerfile 必须以 `FROM` 指令开头。该指令指定的镜像可以是任何有效的镜像。

## WORKDIR

```dockerfile
WORKDIR /path/to/workdir
```

`WORKDIR` 指令用于设置 Dockerfile 中后续 `RUN`、`CMD`、`ENTRYPOINT`、`COPY` 和 `ADD` 指令的工作目录。如果指定的 `WORKDIR` 不存在，即使它不会被后续任何 Dockerfile 指令使用，也会被自动创建。

## RUN —— 构建容器时执行命令

`RUN` 指令将执行任何命令，在当前镜像之上创建一个新层。新增的层将在 Dockerfile 的下一步中使用。`RUN` 有两种形式：

```dockerfile
# Shell form:
RUN [OPTIONS] <command> ...
# Exec form:
RUN [OPTIONS] [ "<command>", ... ]
```

## ADD

`ADD` 指令有两种形式。当路径中包含空格时，必须使用后一种形式。

```dockerfile
ADD [OPTIONS] <src> ... <dest>
ADD [OPTIONS] ["<src>", ... "<dest>"]
```

`ADD` 指令用于从 `<src>` 复制新文件或目录，并将其添加到镜像文件系统中的 `<dest>` 路径。文件或目录可以从构建上下文、远程 URL 或 Git 仓库复制。

`ADD` 与 `COPY` 指令功能相似，但用途略有不同。详细了解 [`ADD` 与 `COPY` 的区别](https://docs.docker.com/build/building/best-practices/#add-or-copy)。


## COPY

`COPY` 指令有两种形式。后一种形式适用于包含空格的路径。

```dockerfile
COPY [OPTIONS] <src> ... <dest>
COPY [OPTIONS] ["<src>", ... "<dest>"]
```

`COPY` 指令用于从 `<src>` 复制新文件或目录，并将其添加到镜像文件系统中的 `<dest>` 路径。文件或目录可以从构建上下文、构建阶段、命名上下文或镜像中复制。


## USER —— 用户设置

```dockerfile
USER <user>[:<group>]
```

或

```dockerfile
USER <UID>[:<GID>]
```

`USER` 指令设置用户名（或 UID）以及可选的用户组（或 GID），以用作当前阶段剩余部分的默认用户和组。指定的用户用于 `RUN` 指令，并在运行时运行相关的 `ENTRYPOINT` 和 `CMD` 命令。

> **备注**
> 注意，当为用户指定组时，用户将*仅*具有指定的组成员身份。任何其他已配置的组成员身份都将被忽略。

> **警告**
> 当用户没有主组时，镜像（或下一条指令）将以 `root` 组运行。
>
> 在 Windows 上，如果用户不是内置账户，则必须先创建用户。这可以通过在 Dockerfile 中调用 `net user` 命令来完成。

```dockerfile
FROM microsoft/windowsservercore
# 在容器中创建 Windows 用户
RUN net user /add patrick
# 为后续命令设置它
USER patrick
```

### CMD —— 启动容器时执行命令

`CMD` 指令用于设置从镜像启动容器时默认执行的命令。

您可以使用 [Shell 或 Exec 形式] 来指定 `CMD` 指令：

-   `CMD ["executable","param1","param2"]`（Exec 形式）
-   `CMD ["param1","param2"]`（Exec 形式，作为 `ENTRYPOINT` 的默认参数）
-   `CMD command param1 param2`（Shell 形式）

Dockerfile 中只能包含一条 `CMD` 指令。如果定义了多条 `CMD`，仅最后一条生效。

`CMD` 的主要用途是为运行中的容器提供默认值。这些默认值可以包含可执行文件；若省略可执行文件，则必须同时指定 `ENTRYPOINT` 指令。

如果您希望容器每次运行时都执行相同的可执行程序，建议将 `ENTRYPOINT` 与 `CMD` 配合使用。请参阅 `[ENTRYPOINT]`。当用户在 `docker run` 命令中指定参数时，这些参数将覆盖 `CMD` 中指定的默认值，但默认的 `ENTRYPOINT` 仍会被保留并使用。

如果 `CMD` 仅用于为 `ENTRYPOINT` 指令提供默认参数，则 `CMD` 和 `ENTRYPOINT` 均应采用 [Exec 形式] 进行定义。

> **注意**
>
> 请勿混淆 `RUN` 与 `CMD`。`RUN` 会在构建阶段实际执行命令并提交结果；而 `CMD` 在构建时不会执行任何操作，它仅用于声明镜像的预期运行命令。
