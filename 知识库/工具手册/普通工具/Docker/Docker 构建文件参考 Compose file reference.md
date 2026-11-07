# Compose file reference —— 构建文件规范

## Services

https://docs.docker.com/reference/compose-file/services/

服务是应用程序中计算资源的抽象定义，可以独立于其他组件进行扩展或替换。服务由一组容器支撑，平台根据副本要求和放置约束运行这些容器。由于服务由容器支撑，它们由 Docker 镜像和一组运行时参数定义。服务中的所有容器都使用这些参数以相同方式创建。

Compose 文件必须声明一个 `services` 顶层元素，它是一个映射，其键是服务名称的字符串表示，其值是服务定义。服务定义包含应用于每个服务容器的配置。

每个服务还可以包含一个 `build` 部分，用于定义如何为该服务创建 Docker 镜像。Compose 支持使用此服务定义构建 Docker 镜像。如果不使用，`build` 部分会被忽略，Compose 文件仍被视为有效。构建支持是 Compose 规范的可选方面，在 [Compose Build 规范](https://docs.docker.com/reference/compose-file/build/)文档中有详细描述。

每个服务定义运行其容器的运行时约束和要求。`deploy` 部分将这些约束分组，并让平台调整部署策略，以最佳方式匹配容器需求与可用资源。部署支持是 Compose 规范的可选方面，在 [Compose Deploy 规范](https://docs.docker.com/reference/compose-file/deploy/)文档中有详细描述。如果未实现，`deploy` 部分会被忽略，Compose 文件仍被视为有效。

---

高级示例

在以下示例中，`proxy` 服务使用 Nginx 镜像，将本地 Nginx 配置文件挂载到容器中，暴露端口 `80`，并依赖于 `backend` 服务。

`backend` 服务从位于 `backend` 目录中的 Dockerfile 构建镜像，并设置为在 `builder` 阶段构建。

```yaml
services:
  proxy:
    image: nginx
    volumes:
      - type: bind
        source: ./proxy/nginx.conf
        target: /etc/nginx/conf.d/default.conf
        read_only: true
    ports:
      - 80:80
    depends_on:
      - backend

  backend:
    build:
      context: backend
      target: builder
```

更多示例 Compose 文件，请浏览 [Awesome Compose 示例](https://github.com/docker/awesome-compose)。
