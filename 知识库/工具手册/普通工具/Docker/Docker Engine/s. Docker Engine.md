https://docs.docker.com/engine/

# Docker Engine

## Networking

### 端口发布与映射

https://docs.docker.com/engine/network/port-publishing/

Docker 守护进程默认阻止对 IPv4/6 的未发布端口的访问。Docker 使用防火墙规则执行网络地址转换（NAT）、端口地址转换（PAT）和伪装。

例如，`docker run -p 8080:80 [...]` 会在 Docker 主机任意地址上的端口 8080 与容器的端口 80 之间创建映射。容器发出的连接将使用 Docker 主机的 IP 地址进行伪装。

#### 发布端口

使用 `docker create` 或 `docker run` 创建或运行容器时，桥接网络上容器的所有端口都可以从 Docker 主机以及连接到同一网络的其他容器访问。这些端口不能从主机外部访问；在默认配置下，也不能从其他网络中的容器访问。

使用 `--publish` 或 `-p` 标志可使端口在主机外部以及其他桥接网络中的容器中可用。这会在主机中创建一条防火墙规则，将容器端口映射到 Docker 主机上的端口，以供外部世界访问。示例：

```
-p [HostIP:]HostPort:ContainerPort[/tcp|/udp]   

-p 8080:80
# 将主机端口 `8080` 映射到容器 TCP 端口 `80`

-p 192.168.1.100:8080:80
# 将主机 IP `192.168.1.100` 的端口 `8080` 映射到容器 TCP 端口 `80`\

-p 8080:80/udp
# 将主机端口 `8080` 映射到容器中的 UDP 端口 `80`

-p 8080:80/tcp -p 8080:80/udp
# 将主机 TCP 端口 `8080` 映射到容器 TCP 端口 `80`，并将主机 UDP 端口 `8080` 映射到容器 UDP 端口 `80`
```

> [!IMPORTANT]
>
> 发布容器端口默认是不安全的。这意味着，当你发布容器端口后，它不仅可供 Docker 主机访问，也可供外部世界访问。
>
> 如果在发布标志中包含 localhost IP 地址（`127.0.0.1` 或 `::1`），则只有 Docker 主机可以访问已发布的容器端口。
>
> ```console
> $ docker run -p 127.0.0.1:8080:80 -p '[::1]:8080:80' nginx
> ```


如果端口映射中未指定主机 IP、桥接网络仅支持 IPv4，且 `--userland-proxy=true`（默认值），则主机 IPv6 地址上的端口将映射到容器的 IPv4 地址。
> 满足3个条件时，主机 IPv6 映射到容器 IPv4