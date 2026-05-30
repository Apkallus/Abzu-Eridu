
## Apple文件协议

概念：
- Apple文件协议（AFP）特别提供Apple OS X主机之间的文件服务。使用URL（例如`afp://server/share`）访问内容，服务运行在TCP端口548上。

工具：
- Nmap脚本

    | 名称               | 描述                |
    | ---------------- | ----------------- |
    | `afp-ls`         | 列出可用的AFP卷和文件      |
    | `afp-path-vuln`  | 列出所有AFP卷和文件^[a]   |
    | `afp-serverinfo` | 显示AFP服务器信息        |
    | `afp-showmount`  | 列出可用的AFP共享及各自的ACL |


- Metasploit `afp_login`
- Hydra

Apple OS X实现存在多个信息泄露、目录遍历和命令执行漏洞。


