[github](https://github.com/benoitc/gunicorn)


## 版本

### 22.0.0 —— 之前版本存在请求走私漏洞

github 版本 <https://github.com/benoitc/gunicorn/releases/tag/22.0.0>

ctf 思路 https://mizu.re/post/fcsc-2026-writeups#bubulle-corp-2

```md
Changes log

- 使用 `utime` 通知 worker 的存活状态
- 将安装配置迁移到 `pyproject.toml`
- 修复 HTTP 解析器中的大量安全漏洞（封堵若干请求走私向量）
- 一旦遇到不支持的请求帧格式，便不再尝试解析后续请求
- 对于 HTTP 版本低于 1.1 的请求，拒绝支持分块传输（该特性仅被用于漏洞利用）
- 当请求与已配置或传入的 `SCRIPT_NAME` 冲突时，现在会输出详细错误
- 不再检查 Trailer 字段中用于指示安全方案的头部
- 支持 Python 3.12

**重大变更（Breaking changes）**

- 最低版本要求为 Python 3.7
- HTTP 方法中有效字符的限制已限定为互联网标准所允许的范围
- 默认拒绝指定了不支持的传输编码（顺序）的请求（少见）
- 默认不再对 HTTP 方法进行大小写折叠（IANA 方法注册表中没有受此影响的方法）
- 默认不再接受包含井号（`#`）的 HTTP 方法（少见）
- 默认不再接受 HTTP 版本 < 1.0 或 >= 2.0（少见，仅支持 HTTP/1.1）
- 不再接受由多位数字组成，或包含前缀/后缀的 HTTP 版本
- 对于 Gunicorn 无法安全映射到变量的 HTTP 头部字段名，会像其他软件一样被静默丢弃
- 默认拒绝字段名为空的 HTTP 头部（无合法使用场景，常用于漏洞利用）
- 默认拒绝同时包含 `Transfer-Encoding` 和 `Content-Length` 的请求（此类消息可能表明试图进行请求走私）
- 不再允许空传输编码（据报告，在非常老旧且有问题的代理中曾出现）

**安全（SECURITY）**

- 修复 CVE-2024-1135
```

#### Commit 72238fc

<https://github.com/benoitc/gunicorn/commit/72238fcf8d29db62fdbb9d2481ced801e27fe139>

- 时间
    Dec 15, 2023

- 说明

    ```md
    符合 RFC 的请求行和头部解析

    - 统一 HEADER_RE 和 METH_RE
    - 在 obs-fold 处理期间将 CRLF 替换为 SP（参见 RFC 9112 第 5.2 节最后一段）
    - 停止剥离头部名称。
    - 在使用 obs-fold 的头部值中移除 OWS 中的 HTAB（参见 RFC 9112 第 5.2 节最后一段）
    - 使用 fullmatch 而非 search，后者在处理空字符串时存在问题。（参见 [GHSA-68xg-gqqm-vgj8](https://github.com/advisories/GHSA-68xg-gqqm-vgj8)）
    - 仅按空格拆分代理协议行。（参见代理协议第 2.1 节第 3 条）
    - 对方法和版本使用 fullmatch（感谢 Paul Dorn 注意到这一点。）
    - 将 str.strip() 调用替换为 str.strip(' \t')
    - 仅按 SP 拆分请求行。

    共同作者：Paul Dorn <pajod@users.noreply.github.com>
    ```

`gunicorn/http/message.py`
- 差异

    ```diff
    -   HEADER_RE = re.compile(r"[^!#$%&'*+\-.\^_`|~0-9a-zA-Z]")
    -   METH_RE = re.compile(r"[A-Z0-9$-_.]{3,20}")
    +   TOKEN_RE = re.compile(r"[!#$%&'*+\-.\^_`|~0-9a-zA-Z]+")

    ...

    -   if not METH_RE.match(bits[0]):
    +   if not TOKEN_RE.fullmatch(bits[0]):
            raise InvalidRequestMethod(bits[0])
    ```
    - 对 http 方法有效的检测中，旧版本仅需连续3个字符匹配

- 定义
    ```py
    def should_close(self):
        for (h, v) in self.headers:
            if h == "CONNECTION":
                v = v.lower().strip(" \t")
                if v == "close":
                    return True
                elif v == "keep-alive":
                    return False
                break
        return self.version <= (1, 0)
    ```
    - 持久连接头部匹配第一个后返回

### 与前一个版本的差异

<https://github.com/benoitc/gunicorn/compare/21.2.0...22.0.0#diff-7e884e24484c7ac02a634681dfd68ba4d1830cdf0204768b2fabbf84dd0adcd3L96>

- `gunicorn/http/message.py`

    ```diff
    -   name, value = name.strip(), [value.lstrip()]
    +   # this is still a dangerous place to do this
    +   #  but it is more correct than doing it before the pattern match:
    +   # after we entered Unicode wonderland, 8bits could case-shift into ASCII:
    +   # b"\xDF".decode("latin-1").upper().encode("ascii") == b"SS"
    +   name = name.upper()
    +   
    +   value = [value.lstrip(" \t")]
    ```
    - 头部名的空白符移除创造头部解析差异

## SCRIPT_NAME 头部 

https://github.com/benoitc/gunicorn/blob/ab9c8301cb9ae573ba597154ddeea16f0326fc15/gunicorn/http/wsgi.py#L117

最新版仍然存在

```py
script_name = os.environ.get("SCRIPT_NAME", "")

...

# set the path and script name
path_info = req.path
if script_name:
        path_info = path_info.split(script_name, 1)[1]
    environ['PATH_INFO'] = util.unquote_to_wsgi_str(path_info)
    environ['SCRIPT_NAME'] = script_name
```
   
读取 `SCRIPT_NAME` 头部，设置的值将在 `PATH_INFO` 被设置前被剥离。路由功能：在路径中指定将被移除的前缀路径。示例：
- 基准，URI 设置一个无效路径 `/不存在的目录a/`，得到 404
    - 添加头部 `SCRIPT_NAME: /不存在的目录a`，得到首页 `/`
        - `split()` 后索引1为 `/`
    - 添加头部 `SCRIPT_NAME: /任意b`，将触发 500 异常响应
        - `split()` 返回单元素列表，索引1抛出异常
- 设置 URI 与 `SCRIPT_NAME` 头部值相同 `/`，得到 308 重定向