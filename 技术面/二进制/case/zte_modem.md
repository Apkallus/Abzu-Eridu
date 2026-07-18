工具
- https://github.com/douniwan5788/zte_modem_tools#

文章
- https://blog.nkxingxh.top/archives/310/
- https://noviachen.github.io/posts/e320a5fc.html

使用 zte_modem_tools 以工厂模式临时开启光猫 telnet 端口，同时获取 telnet 临时管理权限用户名与密码

使用获取的临时 root 凭证访问光猫 telnet 端点
- 光猫配置 FTP 目录为根目录，使用 FTP 客户端或 Wget 下载文件

    ```sh
    # FTP 服务默认开启
    sendcmd 1 DB set FTPServerCfg 0 FtpEnable 1
    # FTP LAN 方向访问默认开启
    sendcmd 1 DB set FTPServerCfg 0 FtpLanEnable 1
    # 修改 FTP 目录从 /mnt 到根目录
    sendcmd 1 DB set FTPUser 0 Location /
    # FTP 用户权限默认 root
    sendcmd 1 DB set FTPUser 0 UserRight 3
    sendcmd 1 DB save
    reboot
    ```

- 光猫配置开启 LAN 方向的 Telnet 端口访问，并设置用户权限为 root

    ```sh
    # 启用 Telnet LAN 方向访问
    sendcmd 1 DB set TelnetCfg 0 Lan_Enable 1
    # 设置 Telnet 用户权限为 root
    sendcmd 1 DB set TelnetCfg 0 InitSecLvl 3
    # 设置 Telnet 最大用户数为2
    sendcmd 1 DB set TelnetCfg 0 Max_Con_Num 2
    # 开启 Telnet 端口
    sendcmd 1 DB set PortControl 3 PortEnable 1
    sendcmd 1 DB save
    reboot
    ```

下载 `db_user_cfg.xml` 并使用 `ztecfg.exe` 解密得到 telnet 固定管理权限凭证

```xml
<DM name="TS_UName" val="用户名"/>
<DM name="TS_UPwd" val="密码"/>
```

配置文件中
- `TelnetCfg` 为 telnet 项配置，包含令牌