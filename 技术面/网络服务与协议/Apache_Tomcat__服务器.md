如果我们能够通过 Tomcat 的管理功能，就可以使用 HTTP PUT 方法将我们的 payload 部署到易受攻击的系统上。

工具
- MSF
    - `msf auxiliary(tomcat_mgr_login)` 爆破凭证
    - `use exploit/multi/http/tomcat_mgr_deploy` 利用 Apache 的 HTTP PUT 功能，使用我们通过暴力破解登录发现的合法用户名和密码将我们的 payload 放置到系统上
        - 若无法写入 root 文件夹，因为我们是从受限用户帐户运行的，而此文件夹需要 root 级别的权限。通常，Apache 在 Apache 用户帐户下运行，该帐户有时称为 `apache`，但也可能是 `httpd` 或 `www-data` 等名称。