https://github.com/leev/ngx_http_geoip2_module

# 描述

`ngx_http_geoip2_module` - 根据客户端 IP（默认）或指定变量（支持 IPv4 和 IPv6），使用 MaxMind GeoIP2 数据库中的值创建变量。

该模块现在支持 nginx `stream`，并且可以像 `http` 模块一样使用。

## 安装

首先按照 [libmaxminddb](https://github.com/maxmind/libmaxminddb) 的 [README.md 文件](https://github.com/maxmind/libmaxminddb/blob/main/README.md#installing-from-a-tarball) 中的说明安装 [libmaxminddb](https://github.com/maxmind/libmaxminddb)。

#### 下载 nginx 源码

```sh
wget http://nginx.org/download/nginx-VERSION.tar.gz
tar zxvf nginx-VERSION.tar.gz
cd nginx-VERSION
```

##### 作为动态模块构建（nginx 1.9.11+）：

```sh
./configure --with-compat --add-dynamic-module=/path/to/ngx_http_geoip2_module
make modules
```

这将生成 `objs/ngx_http_geoip2_module.so`。如需，可手动将其复制到 nginx 模块路径。

将以下行添加到 `nginx.conf`：

```nginx
load_module modules/ngx_http_geoip2_module.so;
```

##### 作为静态模块构建：

```sh
./configure --add-module=/path/to/ngx_http_geoip2_module
make
make install
```

##### 如果需要 stream 支持，请确保编译时包含 stream：

```sh
./configure --add-dynamic-module=/path/to/ngx_http_geoip2_module --with-stream
```

或

```sh
./configure --add-module=/path/to/ngx_http_geoip2_module --with-stream
```

## 下载 MaxMind GeoLite2 数据库（可选）

免费的 GeoLite2 数据库可从 [MaxMind 网站](http://dev.maxmind.com/geoip/geoip2/geolite2/) 获取（需要注册）。

## 示例用法：

```nginx
http {
    ...
    geoip2 /etc/maxmind-country.mmdb {
        auto_reload 5m;
        $geoip2_metadata_country_build metadata build_epoch;
        $geoip2_data_country_code default=US source=$variable_with_ip country iso_code;
        $geoip2_data_country_name country names en;
    }

    geoip2 /etc/maxmind-city.mmdb {
        $geoip2_data_city_name default=London city names en;
    }
    ....

    fastcgi_param COUNTRY_CODE $geoip2_data_country_code;
    fastcgi_param COUNTRY_NAME $geoip2_data_country_name;
    fastcgi_param CITY_NAME    $geoip2_data_city_name;
    ....
}

stream {
    ...
    geoip2 /etc/maxmind-country.mmdb {
        $geoip2_data_country_code default=US source=$remote_addr country iso_code;
    }
    ...
}
```

##### 元数据：

获取有关 GeoIP 数据库的元数据。

```text
$variable_name metadata <field>
```

可用字段：

- `build_epoch`：MaxMind 数据库的构建时间戳。
- `last_check`：最后一次检查数据库是否更改的时间（使用 `auto_reload` 时）
- `last_change`：最后一次重新加载数据库的时间（使用 `auto_reload` 时）

##### 自动重载（默认：禁用）：

启用 `auto_reload` 后，nginx 将按指定间隔检查数据库的修改时间，并在其发生变化时重新加载。

```nginx
auto_reload <interval>
```

##### GeoIP：

```text
$variable_name [default=<value] [source=$variable_with_ip] path ...
```

如果未指定 `default`，则变量在未找到时将为空。

如果未指定 `source`，将使用 `$remote_addr` 执行查找。

要找到所需数据的路径（例如 `country names en`），请使用 [mmdblookup 工具](https://maxmind.github.io/libmaxminddb/mmdblookup.html)：

```console
$ mmdblookup --file /usr/share/GeoIP/GeoIP2-Country.mmdb --ip 8.8.8.8
```

```log
  {
    "country":
      {
        "geoname_id":
          6252001 <uint32>
        "iso_code":
          "US" <utf8_string>
        "names":
          {
            "de":
              "USA" <utf8_string>
            "en":
              "United States" <utf8_string>
          }
      }
  }
```

```console
$ mmdblookup --file /usr/share/GeoIP/GeoIP2-Country.mmdb --ip 8.8.8.8 country names en
```

```log
  "United States" <utf8_string>
```

这相当于：

```text
$country_name "default=United States" source=$remote_addr country names en
```

##### 附加命令：

这些命令与原始 `ngx_http_geoip_module` 的作用相同，文档见：<http://nginx.org/en/docs/http/ngx_http_geoip_module.html#geoip_proxy>。

但是，如果在某个变量上提供 `source=$variable_with_ip` 选项，则这些设置将对该特定变量忽略。

```nginx
geoip2_proxy < cidr >
```

定义可信地址。当请求来自可信地址时，将改用 `X-Forwarded-For` 请求头字段中的地址。

```nginx
geoip2_proxy_recursive < on | off >
```

如果禁用递归搜索，则对于匹配某个可信地址的原始客户端地址，将改用 `X-Forwarded-For` 中发送的最后一个地址。如果启用递归搜索，则对于匹配某个可信地址的原始客户端地址，将改用 `X-Forwarded-For` 中发送的最后一个非可信地址。