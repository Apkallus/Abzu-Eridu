# VSCode 

- [官网下载](https://code.visualstudio.com/Download)

旧版 linux 安装

    ```sh
    sudo apt install --only-upgrade snapd -y
    sudo systemctl restart snapd snapd.socket
    sudo snap install --classic code # 安装 vscode
    ```

## 使用

- 终端可移动到标签页

## 排障

- 若代码无补全或说明信息，尝试切换语言的解析器

- 若提示无法访问浏览器粘贴板，在浏览器中设置权限或关闭跟踪保护。在搜索栏左侧的盾形图标

## 网页版

- 在资源栏按下右键，包含上传与下载功能
- 若右键菜单仅显示“粘贴”，按下 `Esc` 后显示菜单

## 设置

设置，在 `Settings` 中搜索或编辑 `settings.json`
- 字体大小，字体发虚时微调
    ```json
    {
        "editor.fontSiz": 18,
        "markdown.preview.fontSize": 18,
        "terminal.integrated.fontSize": 16,
    }
    ```
- 字体集 `Font Family` 设置中英文等宽字体
    - ['JetBrains Maple Mono Regular'](https://github.com/SpaceTimee/Fusion-JetBrainsMapleMono)
- `Window: Zoom Level` 缩放设置，但通常仅调整字体大小
- `workbench.colorCustomization` 配置文件调整终端配色方案（但无语法高亮）  
    - [终端配色项目 github](https://glitchbone.github.io/vscode-base16-term/#/) 

## 扩展

VSCode扩展
- 若添加语言扩展，根据其 `功能-编程语言` 的支持或许使 md 的对应代码块自动应用高亮
- VSCode界面的中文支持：
    Chinese (Simplified) (简体中文) Language Pack for Visual Studio Code
- Remote Development 远程桌面，用于 WSL
- md 预览与预览模式编辑，使用 vscode 右上角自带预览或编辑
- md 表格：
    Markdown Table - Takumi Ishii
    - 从 csv 格式转换为表格： 
        在设置中 `markdowntable.showMenu.csvToTable` 开启此功能
        选中逗号分隔的 csv 格式内容后右键转换为表格
    - 添加新表格行：
        在列表末尾按 `Tab` 键
- 文件模板：
    File Template - rhangai
    1. 创建 ./vscode/templates 文件夹
    2. 将模板文件放入此文件夹中
    3. 在资源管理器栏的新建文件的预期路径，右键 - Create from template
    4. 在顶部弹窗中点击选择模板文件，之后输入新文件名并按下回车
- 编码：
    - URL Encode
        在文件名中包含空格时，需编码为 URL 格式。
        安装后右键菜单新增 URL 编码解码功能。
- 测试服务器：
    - Live Server - Ritwick Dey
        本地开启服务器，可模拟 CSRF
        - 设置中开启 `CORS`
            `"liveServer.settings.cors": true,`
- `Rainbow CSV` CSV 高亮与格式转换


## SSH 设置

物理机 vscode 客户端连接虚拟机 SSH 服务器 
- [vscode 文档](https://code.visualstudio.com/docs/remote/ssh)。
- [教程](https://umatechnology.org/how-to-enable-ssh-in-vmware-workstation/)

步骤
- 物理机 vscode 安装 `Remote - SSH` 插件
- 虚拟机
    - 终端命令
        ```sh
        # 安装 ssh 服务器
        sudo apt-get install openssh-server

        # 启用 ssh 服务
        sudo systemctl enable --now ssh
        sudo systemctl status ssh

        # 若 UFW 启用则允许 ssh 服务连接
        sudo ufw status
        sudo ufw allow ssh
        ```

- 在物理机测试虚拟机的连接 
    - 连接虚拟机
        `ssh 虚拟机用户名@主机名` 

    - 显示确认提示后输入 yes
        `Are you sure you want to continue connecting (yes/no/[fingerprint])? yes`

    - 输入密码后连接到虚拟机

- 使用物理机 ssh 密钥
    - 物理机创建密钥
        `ssh-keygen -f key -N '密码'`
        - key 为私钥
        - key.pub 为公钥
    - 查看公钥
        `type key.pub`
    - 复制物理机公钥到虚拟机 ssh 授权配置文件
        `echo '公钥内容' >> ./.ssh/authorized_keys`
    - 使用 ssh 私钥连接虚拟机
        `ssh -i key 虚拟机用户名@主机名`
- 设置虚拟机的服务器 ssh 配置文件 
    `/etc/ssh/sshd_config`

    ```log
    # 开启公钥验证
    PubkeyAuthentication yes
    # 关闭密码登录
    PasswordAuthentication no
    # 关闭 root 登录
    PermitRootLogin no
    ```
    - 重启 ssh 服务以应用修改
        `sudo systemctl restart ssh`

- 设置物理机的客户端 ssh 配置文件
    - vscode 的远程资源管理器中打开 ssh 配置文件并设置参数
        `~/.ssh/config`
        - `HostName 主机名`
        - `User 用户名`
        - `IdentityFile 私钥文件`
- 此时物理机 vscode 的 ssh 客户端成功连接到虚拟机 ssh 服务器
- 之后在 vmware 中手动启动并在后台运行，或使用 vmrun 命令行工具指定虚拟机后台运行

## 快捷键功能

终端面板
- ``Ctrl + ` `` 打开终端
- `Ctrl + J` 打开面板（终端作为面板的一部分）

搜索与替换
- `Ctrl + F` 搜索后点击搜索框左侧的 `>` 箭头以展开“替换”功能面板。也适用于跨文件搜索的 `Ctrl + Shift + F` 

专注模式
- `Ctrl + K => Z`
    `Ctrl + K` 组合键后按下 `Z` 进入隐藏其他界面的专注模式（Zen）

markdown 预览
- `Ctrl + V => K`