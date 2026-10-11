https://www.chromium.org/developers/

## For Developers

### Design Documents

#### Network Settings

https://www.chromium.org/developers/design-documents/network-settings/

##### Command-line options for proxy settings

###### --proxy-bypass-list —— 不使用代理的主机列表

```sh
--proxy-bypass-list=(<trailing_domain>|<ip-address>)[:<port>][;...]
```

示例
```sh
--proxy-server="foopy:8080" --proxy-bypass-list="*.google.com;*foo.com;127.0.0.1:8080"

# 设置 burp 为代理，本地流量使用代理，排除一批浏览器流量
--proxy-server="http://127.0.0.1:8080" --proxy-bypass-list="<-loopback>;*.google.com;*.googleapis.com;darkreader.org"
```