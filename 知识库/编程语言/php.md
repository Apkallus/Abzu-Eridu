## 配置

https://www.php.net/manual/en/ini.core.php

- `cgi.fix_pathinfo` `bool`

    为 CGI 提供真正的 `PATH_INFO`/`PATH_TRANSLATED` 支持。PHP 之前的行为是将 `PATH_TRANSLATED` 设置为 `SCRIPT_FILENAME`，并且不解析 `PATH_INFO` 是什么。关于 `PATH_INFO` 的更多信息，请参阅 CGI 规范。将此选项设置为 1 将使 PHP CGI 修复其路径以符合规范。设置为 0 将使 PHP 恢复之前的行为。此选项默认开启。您应修改您的脚本以使用 `SCRIPT_FILENAME` 而非 `PATH_TRANSLATED`。

    > 即，此处默认设置：当路径文件不存在时的向前回溯的文件查找行为

## 语法

### 文件系统

#### move_uploaded_file()

```php
function move_uploaded_file(string $from, string $to): bool
```

当 from 文件有效时，上传到 to 路径


#### unlink()

```php
function unlink(string $filename, ?resource $context = null): bool
```

删除 filename 文件