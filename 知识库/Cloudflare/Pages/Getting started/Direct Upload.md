# Direct Upload

最后更新于 2026 年 4 月 21 日

Direct Upload 使你能够将预构建的资产上传到 Pages，并将其部署到 Cloudflare 全球网络。如果你希望[集成自己的构建平台](https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/)或从本地计算机上传，应选择 Direct Upload 而非 Git 集成。

本指南将指导你如何使用 Wrangler 或拖放方法上传资产。

> **你无法稍后切换到 Git 集成**
>
> 如果你选择 Direct Upload，则之后无法切换到 [Git 集成](https://developers.cloudflare.com/pages/get-started/git-integration/)。你将不得不创建一个使用 Git 集成的新项目才能使用自动部署。

## 先决条件

在使用 Direct Upload 部署项目之前，请运行适当的[构建命令](https://developers.cloudflare.com/pages/configuration/build-configuration/#framework-presets)来构建你的项目。

## 上传方法

准备好预构建资产后，有两种方式可以开始上传：

- [Wrangler](#wrangler-cli)。
- [拖放](#drag-and-drop)。

> **注意**
>
> 在 Direct Upload 项目中，你可以在使用 Wrangler 或拖放创建部署之间切换。对于现有的 Git 集成项目，你可以使用 [`wrangler deploy`](https://developers.cloudflare.com/workers/wrangler/commands/general/#deploy) 手动创建部署。但是，你不能在仪表板上对现有的 Git 集成项目使用拖放功能。

## 支持的文件类型

以下是每种 Direct Upload 选项支持的文件类型：

- Wrangler：单个资产文件夹。（不支持 Zip 文件。）
- 拖放：Zip 文件或单个资产文件夹。

## Wrangler CLI

### 设置 Wrangler

首先，安装 [`npm`](https://docs.npmjs.com/getting-started)。然后[安装 Wrangler，即开发者平台 CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/)。

#### 创建项目

使用 [`wrangler login` 命令](https://developers.cloudflare.com/workers/wrangler/commands/general/#login)登录 Wrangler。然后运行 [`pages project create` 命令](https://developers.cloudflare.com/workers/wrangler/commands/pages/#pages-project-create)：

```sh
npx wrangler pages project create
```

然后系统将提示你指定项目名称。你的项目将托管在 `<PROJECT_NAME>.pages.dev`（如果你的项目名称已被占用，则为你项目名称加上几个随机字符）。系统还会提示你指定生产分支。

后续部署将复用这两个值（保存在你的 `node_modules/.cache/wrangler` 文件夹中）。

#### 部署你的资产

至此，你已创建了一个空项目，现在可以为你的首次部署以及生产环境中的所有后续部署部署资产。为此，请运行 [`wrangler pages deploy`](https://developers.cloudflare.com/workers/wrangler/commands/general/#deploy) 命令：

```sh
npx wrangler pages deploy <BUILD_OUTPUT_DIRECTORY>
```

在[框架预设下的构建目录](https://developers.cloudflare.com/pages/configuration/build-configuration/#framework-presets)中找到适合你项目的构建输出目录。

你的生产部署将可在 `<PROJECT_NAME>.pages.dev` 上访问。

> **注意**
>
> 在使用 `wrangler pages deploy` 命令之前，你需要确保自己位于项目内。如果不是，你也可以传入项目路径。

要将资产部署到预览环境，请运行：

```sh
npx wrangler pages deploy <OUTPUT_DIRECTORY> --branch=<BRANCH_NAME>
```

对于你创建的每个分支，你都可以在 `<BRANCH_NAME>.<PROJECT_NAME>.pages.dev` 上获得一个分支别名。

> **注意**
>
> 如果你处于 Git 工作区中，Wrangler 会自动为你拉取分支信息。否则，你需要在此命令中指定你的分支。

如果你想简化项目创建和资产部署步骤，你也可以使用 deploy 命令同时创建和部署资产。如果你首先执行此命令，仍会提示你指定项目名称和生产分支。如上所述，这些值仍将为后续部署缓存。如果缓存已存在而你希望创建新项目，则需要运行 [`create` 命令](#create-your-project)。

#### 其他有用的命令

如果你想使用 Wrangler 获取 Direct Upload 的所有可用项目列表，请使用 [`pages project list`](https://developers.cloudflare.com/workers/wrangler/commands/pages/#pages-project-list)：

```sh
npx wrangler pages project list
```

要以 JSON 格式获取输出以便程序化使用或编写脚本，请使用 `--json` 标志：

```sh
npx wrangler pages project list --json
```

如果你想使用 Wrangler 获取特定项目的所有唯一预览 URL 列表，请使用 [`pages deployment list`](https://developers.cloudflare.com/workers/wrangler/commands/pages/#pages-deployment-list)：

```sh
npx wrangler pages deployment list
```

有关如何将 Wrangler 与 GitHub Actions、Circle CI 和 Travis CI 等持续集成工具结合使用以实现持续部署的分步说明，请参阅[将 Direct Upload 与持续集成结合使用](https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/)。

## 拖放

#### 使用拖放部署你的项目

要使用拖放进行部署：

1. 在 Cloudflare 仪表板中，转到 **Workers & Pages** 页面。

   [转到 **Workers & Pages** ↗](https://dash.cloudflare.com/?to=/:account/workers-and-pages)

2. 选择 **Create application** > **Get started** > **Drag and drop your files**。

3. 在提供的字段中输入你的项目名称，然后拖放你的资产。

4. 选择 **Deploy site**。

你的项目将从 `<PROJECT_NAME>.pages.dev` 提供服务。接下来，将你的构建输出目录拖放到上传框中。你的文件成功上传后，选择 **Save and Deploy** 并继续到你新部署的项目。

#### 创建新部署

项目创建后，选择 **Create a new deployment** 以开始你的站点的新版本。接下来，选择你的新部署将用于生产环境还是预览环境。如果选择预览，你可以创建新的部署分支或输入现有分支。

## 故障排除

### 限制

| 上传方法 | 文件限制 | 文件大小 |
| --- | --- | --- |
| Wrangler | 20,000 个文件 | 25 MiB |
| 拖放 | 1,000 个文件 | 25 MiB |

如果使用拖放方法，当资产过大因而上传失败时，资产旁边会出现一个红色警告符号。在这种情况下，你可以选择删除该资产，但无法替换它。要替换它，你必须重新上传整个项目。

### 生产分支配置

如果你的项目是 [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/) 项目，你将无法配置生产分支控制。要更新你的生产分支，你需要手动调用 API 中的 [Update Project](https://developers.cloudflare.com/api/resources/pages/subresources/projects/methods/edit/) 端点。

```bash
curl --request PATCH \
"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project_name}" \
--header "Authorization: Bearer <API_TOKEN>" \
--header "Content-Type: application/json" \
--data "{\"production_branch\": \"main\"}"
```

### Functions

从 Cloudflare 仪表板进行的拖放部署目前不支持编译 [Pages Functions](https://developers.cloudflare.com/pages/functions/) 的 `functions` 文件夹。要部署 `functions` 文件夹，你必须使用 Wrangler。使用 Wrangler 部署项目时，如果运行命令的位置存在 `functions` 文件夹，该 `functions` 文件夹将随项目一起上传。

但是，请注意，`_worker.js` 文件同时受 Wrangler 和从仪表板进行的拖放部署支持。