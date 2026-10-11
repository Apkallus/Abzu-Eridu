# C3 CLI

最后更新于 2026 年 8 月 25 日

Cloudflare 提供了一个用于创建新的 Workers 和 Pages 项目的 CLI 命令——`npm create cloudflare`，由 [`create-cloudflare` 包](https://www.npmjs.com/package/create-cloudflare)提供支持。

## 创建新应用程序

打开终端窗口并运行：

```bash
npm create cloudflare@latest -- --platform=pages
```

其他包管理器：

```bash
yarn create cloudflare --platform=pages
pnpm create cloudflare@latest --platform=pages
```

运行此命令将提示你安装 [`create-cloudflare`](https://www.npmjs.com/package/create-cloudflare) 包，然后询问你希望创建的应用程序类型。

> **注意**
>
> 要创建 Pages 项目，你现在必须指定 `--platform=pages` 参数，否则 C3 将始终创建一个 Workers 项目。

## Web 框架

如果你选择 "Framework Starter" 选项，系统将提示你选择一个框架。目前支持以下框架：

- [Angular](https://developers.cloudflare.com/pages/framework-guides/deploy-an-angular-site/)
- [Astro](https://developers.cloudflare.com/pages/framework-guides/deploy-an-astro-site/)
- [Docusaurus](https://developers.cloudflare.com/pages/framework-guides/deploy-a-docusaurus-site/)
- [Gatsby](https://developers.cloudflare.com/pages/framework-guides/deploy-a-gatsby-site/)
- [Hono](https://developers.cloudflare.com/pages/framework-guides/deploy-a-hono-site/)
- [Next.js 静态导出](https://developers.cloudflare.com/pages/framework-guides/nextjs/deploy-a-static-nextjs-site/)
- [Nuxt](https://developers.cloudflare.com/pages/framework-guides/deploy-a-nuxt-site/)
- [Qwik](https://developers.cloudflare.com/pages/framework-guides/deploy-a-qwik-site/)
- [React](https://developers.cloudflare.com/pages/framework-guides/deploy-a-react-site/)
- [Redwood](https://developers.cloudflare.com/workers/framework-guides/web-apps/redwoodsdk/)
- [Remix](https://developers.cloudflare.com/pages/framework-guides/deploy-a-remix-site/)
- [SolidStart](https://developers.cloudflare.com/pages/framework-guides/deploy-a-solid-start-site/)
- [SvelteKit](https://developers.cloudflare.com/pages/framework-guides/deploy-a-svelte-kit-site/)
- [Vue](https://developers.cloudflare.com/pages/framework-guides/deploy-a-vue-site/)

当你使用框架时，`npm create cloudflare` 会直接使用框架自身的命令来生成新项目，这可能会提示额外的问题。这确保你创建的项目与框架的最新版本保持同步，并且通过 `npm create cloudflare` 创建项目时，你拥有与直接使用框架工具创建项目时相同的所有选项。

## 部署

项目配置完成后，系统会询问你是否要将项目部署到 Cloudflare。这是可选的。

如果你选择部署，系统会要求你登录 Cloudflare 账户（如果尚未登录），然后你的项目将被部署。

## 创建连接到 git 仓库的新 Pages 项目

要使用 `npm create cloudflare` 创建一个新项目，然后将其连接到你的 Github 或 Gitlab 账户上的 Git 仓库，请执行以下步骤：

1. 运行 `npm create cloudflare@latest`，并选择你想要的选项
2. 对于提示 "Do you want to deploy your application?"（是否要部署应用程序？）选择 `no`。这很重要——如果你选择 `yes` 并从终端部署应用程序（[直接上传](https://developers.cloudflare.com/pages/get-started/direct-upload/)），那么之后将无法将此 Pages 项目连接到 git 仓库。你将不得不创建一个新的 Cloudflare Pages 项目。
3. 使用 `npm create cloudflare@latest` 刚刚为你创建的应用程序，创建一个新的 git 仓库。
4. 按照 [Git 集成指南](https://developers.cloudflare.com/pages/get-started/git-integration/)中概述的步骤操作。

## CLI 参数

C3 通过一系列交互式提示收集任何必需的输入。你也可以通过命令行参数指定你的选择，这将跳过这些提示。要在 CI 等非交互式环境中使用 C3，你必须通过命令行指定所有必需的参数。

以下是 C3 调用的完整格式以及可能的 CLI 参数：

```bash
npm create cloudflare@latest -- --platform=pages [<DIRECTORY>] [OPTIONS] [-- <NESTED ARGS...>]
```

其他包管理器：

```bash
yarn create cloudflare --platform=pages [<DIRECTORY>] [OPTIONS] [-- <NESTED ARGS...>]
pnpm create cloudflare@latest --platform=pages [<DIRECTORY>] [OPTIONS] [-- <NESTED ARGS...>]
```

- `DIRECTORY` `string`（可选）
  - 应在其中创建应用程序的目录。应用程序名称取自目录名。

- `NESTED ARGS..` `string[]`（可选）
  - 传递给 C3 可能调用的任何第三方 CLI 的 CLI 参数（在 full-stack 应用程序的情况下）。

- `--category` `string`（可选）
  - 应创建的模板类型。
  - 此选项的可能值有：
    - `hello-world`：Hello World 示例
    - `web-framework`：Framework Starter
    - `demo`：Application Starter
    - `remote-template`：来自 GitHub 仓库的模板

- `--type` `string`（可选）
  - 应创建的应用程序类型。
  - 此选项的可能值有：
    - `hello-world`：一个基本的 "Hello World" Cloudflare Worker。
    - `hello-world-durable-object`：一个 [Durable Object](https://developers.cloudflare.com/durable-objects/) 以及一个用于与其通信的 Worker。
    - `common`：一个实现了常见路由/代理功能示例的 Cloudflare Worker。
    - `scheduled`：一个计划任务型 Cloudflare Worker（通过 [Cron Triggers](https://developers.cloudflare.com/workers/configuration/cron-triggers/) 触发）。
    - `queues`：一个既是 [Queues](https://developers.cloudflare.com/queues/) 消费者又是生产者的 Cloudflare Worker。
    - `openapi`：一个实现 OpenAPI REST 端点的 Worker。
    - `pre-existing`：从 Cloudflare dashboard 获取一个已初始化的 Worker。

- `--framework` `string`（可选）
  - 用于创建 Web 应用程序的框架类型（使用此选项时，`--type` 被忽略）。
  - 此选项的可能值有：
    - `angular`
    - `astro`
    - `docusaurus`
    - `gatsby`
    - `hono`
    - `next`
    - `nuxt`
    - `qwik`
    - `react`
    - `redwood`
    - `remix`
    - `solid`
    - `svelte`
    - `vue`

- `--template` `string`（可选）
  - 通过托管在 git 仓库中的外部模板创建新项目
  - 此选项的值可以指定为以下任何一种：
    - `user/repo`
    - `git@github.com:user/repo`
    - `https://github.com/user/repo`
    - `user/repo/some-template`（子目录）
    - `user/repo#canary`（分支）
    - `user/repo#1234abcd`（提交哈希）
    - `bitbucket:user/repo`（BitBucket）
    - `gitlab:user/repo`（GitLab）
  
  有关更多详细信息，请参见 `degit` [文档](https://github.com/Rich-Harris/degit)。
  
  模板至少必须包含以下内容：
  - `package.json`
  - [Wrangler 配置文件](https://developers.cloudflare.com/pages/functions/wrangler-configuration/)
  - `src/`，其中包含从 Wrangler 配置文件引用的 worker 脚本
  
  有关更多示例，请参见此仓库的 [templates 文件夹](https://github.com/cloudflare/workers-sdk/tree/main/packages/create-cloudflare/templates)。

- `--deploy` `boolean`（默认值：true）可选
  - 在创建后部署你的应用程序。

- `--lang` `string`（默认值：ts）可选
  - 模板的编程语言。
  - 此选项的可能值有：
    - `ts`
    - `js`
    - `python`

- `--ts` `boolean`（默认值：true）可选
  - 在应用程序中使用 TypeScript。已弃用。请改用 `--lang=ts`。

- `--git` `boolean`（默认值：true）可选
  - 为你的应用程序初始化本地 git 仓库。

- `--open` `boolean`（默认值：true）可选
  - 在浏览器中打开已部署的应用程序（如果应用程序未部署，此选项将被忽略）。

- `--existing-script` `string`（可选）
  - 要在本地克隆的现有 Cloudflare Workers 脚本的名称。使用此选项时，`--type` 被强制为 `pre-existing`。
  - 当指定 `--existing-script` 时，`deploy` 将被忽略。

- `-y`, `--accept-defaults` `boolean`（可选）
  - 使用所有默认 C3 选项，每个选项也可以通过指定来覆盖。

- `--auto-update` `boolean`（默认值：true）可选
  - 自动使用最新版本的 C3。

- `-v`, `--version` `boolean`（可选）
  - 显示版本号。

- `-h`, `--help` `boolean`（可选）
  - 显示帮助信息。

> **注意**
>
> 上述所有布尔选项都可以带值或不带值指定，例如 `--open` 和 `--open true` 效果相同；在选项名称前加上 `no-` 会将其取反，因此例如 `--no-open` 和 `--open false` 效果相同。

## 遥测

Cloudflare 收集匿名使用数据以随时间改进 `create-cloudflare`。请在我们的[数据政策](https://github.com/cloudflare/workers-sdk/blob/main/packages/create-cloudflare/telemetry.md)中阅读更多相关信息。

如果你不希望共享任何信息，可以选择退出。

```bash
npm create cloudflare@latest -- telemetry disable
```

其他包管理器：

```bash
yarn create cloudflare telemetry disable
pnpm create cloudflare@latest telemetry disable
```

或者，你可以设置一个环境变量：

```sh
export CREATE_CLOUDFLARE_TELEMETRY_DISABLED=1
```

你可以随时检查遥测收集的状态。

```bash
npm create cloudflare@latest -- telemetry status
```

其他包管理器：

```bash
yarn create cloudflare telemetry status
pnpm create cloudflare@latest telemetry status
```

你随时可以重新启用遥测收集。

```bash
npm create cloudflare@latest -- telemetry enable
```

其他包管理器：

```bash
yarn create cloudflare telemetry enable
pnpm create cloudflare@latest telemetry enable
```