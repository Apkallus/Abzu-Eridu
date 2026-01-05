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
    2. 点击 Developer Settings，选择 Personal access tokens - Fine-grained tokens
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
    1. 获取并拉取仓库内容
        ```sh
        git fetch origin main
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
