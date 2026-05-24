- github 文件下载镜像
    - <https://github.akams.cn/>
    - <https://git.yylx.win/>

- 将远程仓库克隆到本地计算机，[MDN 开发者学习](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/development_environment#clone_the_repo_to_your_local_computer)：
    1. 创建仓库
    2. 点击绿色的 Code 按钮，在 Local-Clone-HTTPS 选项中复制 URL 地址
    3. 安装 Git
    4. 在当前目录克隆仓库
        ```sh
        git clone 复制的URL
        ```
    5. 进入仓库目录
        ```sh
        cd 仓库名
        ```
    
- 设置 Github HTTPS Git 令牌
    1. 点击头像-Settings，进入账户设置页面
    2. 点击 Developer Settings，选择 Personal access tokens - Token (classic)
    3. 点击 Generate new token 按钮后设置令牌
        - 过期时间
        - 仓库范围
        - 对于 Git 推送，至少设置仓库权限为 Contents 读写
    4. 复制并保存令牌
- 在 Git 中设置全局用户名与邮箱
    - 查看当前设置
        ```sh
        git config --global --list
        ```
    - 设置全局用户名与邮箱，对 commit 命令的设置
        ```sh
        git config --global user.email "you@example.com"
        git config --global user.name "Your Name"
        ```

    - [更改远程仓库的 URL](https://docs.github.com/zh/get-started/git-basics/managing-remote-repositories?changing-a-remote-repositorys-url=#changing-a-remote-repositorys-url)，对 push 命令的设置，以“令牌@主机名”格式的 URL 来自动使用令牌登录
        ```sh
        git remote set-url origin https://令牌@github.com/用户名/仓库名.git
        ```

- 修改并同步更改，[MDN 开发者学习](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/development_environment#modify_and_sync_changes)：
    1. 从远程仓库获取最新分支信息，并删除本地已不存在于远程的分支引用
        ```sh
        git fetch --prune origin
        ```
    1. 拉取仓库内容
        ```sh    
        git pull origin main
        ```
        origin 为远程仓库位置
        main 为分支
    2. 切换到新分支储存更改
        ```sh
        git checkout -b 自定义新分支名
        ```
        checkout 切换分支
        -b 创建新分支
    3. 设置 .gitignore 文件
    4. 添加除 .gitignore 文件规则外的所有修改文件到分支暂存区
        ```sh
        git add -A
        ```
    5. 检查当前分支位置以及修改状态
        ```sh
        git status
        ```
    6. 从暂存区推送到本地仓库
        ```sh
        git commit -m "提交信息"
        ```
    7. 从本地仓库推送到远程仓库，省略分支名为当前分支
        ```sh
        git push origin 分支名
        ```
    8. 在 Github 仓库页面查看与合并分支
- 其他命令
    - 查看本地分支
        ```sh
        git branch
        ```
    - ‌删除本地分支
        ```sh
        git branch -d 分支名
        ```
    - 查看当前远程仓库地址
        ```sh
        git remote -v
        ```
    - 当前分支首次推送时设置对应的上游分支，每个分支的设置独立
        ```sh
        git push --set-upstream origin branch_name
        ```
    - `git checkout` 
        - `git checkout <branch>`  
            切换分支
        - `git checkout <commit> <filename>` or `git checkout <filename>`  
            恢复文件的不同版本
    - `git log`  
        显示提交日志
    - `git show`  
        显示一个或多个对象（blob、树、标签和提交）。
    - `git-reset`
        重置当前HEAD到指定的状态。若遇到提交后的错误，使用此命令与提交 hash 重置 head 与暂存区

        - `git reset [<模式>] <提交>`：更改 `HEAD` 指向的提交。这使得它可以撤销各种 Git 操作，例如提交（commit）、合并（merge）、变基（rebase）和拉取（pull）。

        - 当你指定文件或目录，或者传入 `--patch` 选项时，`git reset` 会更新指定文件的暂存版本。

        - `git reset [<模式>] [<提交>]`  
        将当前分支的头部（HEAD）设置为指向 `<提交>`。根据 `<模式>` 的不同，也会更新工作目录和/或暂存区（索引），使其与 `<提交>` 的内容一致。`<提交>` 默认为 `HEAD`。在执行操作之前，`ORIG_HEAD` 会被设置为当前分支的顶端。

        `<模式>` （默认为 `--mixed`）：

        - **`--mixed`**  
        保持工作目录不变。更新暂存区以匹配新的 HEAD，因此没有任何内容会被暂存。  
        如果指定了 `-N`，则将已删除的路径标记为“意图添加”（intent-to-add，参见 `git-add[1]`）。

        - **`--soft`**  
        保持工作树文件和暂存区不变。  
        例如，如果你没有暂存的更改，可以使用 `git reset --soft HEAD~5` 然后 `git commit`，将最近 5 次提交合并为 1 次提交。即使工作树中存在更改（这些更改不会被触碰），该命令也能正常工作，但这种用法可能会导致困惑。

        - **`--hard`**  
        用 `<提交>` 中的版本覆盖所有文件和目录，并且可能会覆盖未跟踪的文件。不在 `<提交>` 中的已跟踪文件会被删除，以使工作树与 `<提交>` 完全一致。同时更新暂存区以匹配新的 HEAD，因此没有任何内容会被暂存。
