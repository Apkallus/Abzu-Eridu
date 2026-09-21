# npm

https://docs.npmjs.com/

## CLI

### Commands

#### npm install

https://docs.npmjs.com/cli/v12/commands/npm-install

```sh
npm install [<package-spec> ...]

aliases: add, i, in, ins, inst, insta, instal, isnt, isnta, isntal, isntall
```

This command installs a package and any packages that it depends on. 

A `package` is:
4. a `<name>@<version>` that is published on the registry (see registry) with (c)

In global mode (ie, with `-g` or `--global` appended to the command), it installs the current package context (ie, the current working directory) as a global package.


排障
- `npm install -g` 全局安装模块后，执行时出现模块找不到

    ```log
    Error: Cannot find module
    Require stack:
    ```
    - 在对应工具目录下执行本地安装
    
    - `npm root -g` 查看 npm 全局模块安装目录，并设置为 node.js 的模块目录环境变量
        ```sh
        npm root -g
        export NODE_PATH="$(npm root -g):$NODE_PATH"
        ```
        - 设置模块目录变量后，预期可成功执行

#### npm root

```sh
npm root
```

Print the effective node_modules folder to standard out.

使用 `-g` or `--global` 查看全局模块安装目录

