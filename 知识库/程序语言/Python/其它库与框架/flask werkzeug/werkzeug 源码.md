# werkzeug

https://github.com/pallets/werkzeug/tree/main/src/werkzeug
- 与 flask github 库不同，werkzeug 拥有旧版代码

## security.py

https://github.com/pallets/werkzeug/blob/main/src/werkzeug/security.py

### safe_join —— 路径

```py
def safe_join(directory: str, *untrusted: str) -> str | None:
    """安全地将零个或多个不受信任的路径组件拼接到受信任的基础目录，
    以避免逃逸出基础目录。如果路径不安全，则返回 ``None``。

    假定不受信任的路径来自/用于 URL，例如用于提供文件。因此，
    它只应使用正斜杠 ``/`` 路径分隔符，并将使用该分隔符进行拼接。
    在 Windows 上，不允许使用反斜杠 ``\\`` 分隔符。

    这仅考虑路径名，不验证其是否存在、是否为符号链接，或文件/
    文件系统的其他属性。应用程序需要确保 ``directory`` 的内容
    是可信的。

    在 Windows 上，不允许使用特殊设备名，例如 ``CON`` 和 ``NUL``，
    因为这是用于通过 :func:`.send_from_directory` 提供文件的，
    而这些文件在读取时会挂起。

    允许 NTFS 备用数据流 (ADS)，例如 ``filename:stream``。
    :func:`.secure_filename` 在保存时会移除 ``:``。

    :param directory: 受信任的基础目录。
    :param untrusted: 相对于基础目录的不受信任路径组件。
    :return: 安全路径，否则返回 ``None``。

    .. versionchanged:: 3.1.9
        在 Windows 上，不允许带有空 ADS 流标记的特殊设备名。

    .. versionchanged:: 3.1.6
        在 Windows 上，不允许位于多段路径中的特殊设备名。

    .. versionchanged:: 3.1.5
        在 Windows 上，不允许更多特殊设备名，无论其扩展名或尾随空格如何。

    .. versionchanged:: 3.1.4
        在 Windows 上，不允许特殊设备名。
    """
    if not directory:
        # Ensure we end up with ./path if directory="" is given,
        # otherwise the first untrusted part could become trusted.
        directory = "."

    parts = [directory]

    for part in untrusted:
        if not part:
            continue

        part = posixpath.normpath(part)

        if (
            os.path.isabs(part)
            # ntpath.isabs doesn't catch this
            or part.startswith("/")
            or part == ".."
            or part.startswith("../")
            or any(sep in part for sep in _os_alt_seps)
            or (
                os.name == "nt"
                and any(
                    p.partition(":")[0].partition(".")[0].strip().upper()
                    in _windows_device_files
                    for p in part.split("/")
                )
            )
        ):
            return None

        parts.append(part)

    return posixpath.join(*parts)
```

> 旧版位于 flask


## middleware

### proxy_fix.py —— 中间件，解析代理头

https://github.com/pallets/werkzeug/blob/7868bef5/src/werkzeug/middleware/proxy_fix.py

```py
"""
X-Forwarded-For 代理修正
=========================

本模块提供一个中间件，根据应用前方的代理可能设置的
``X-Forwarded-`` 头来调整 WSGI environ。

当应用运行在代理服务器后面时，WSGI 可能将请求视为来自该服务器，
而不是真实客户端。代理会设置各种头来追踪请求实际来自何处。

仅当应用确实位于此类代理之后时，才应使用此中间件，并且应配置
其前方链式代理的数量。并非所有代理都会设置所有头。由于传入的
头可以被伪造，你必须设置每个头由多少个代理设置，以便中间件
知道该信任什么。

.. autoclass:: ProxyFix

:copyright: 2007 Pallets
:license: BSD-3-Clause
"""

from __future__ import annotations

import typing as t

from ..http import parse_list_header

if t.TYPE_CHECKING:
    from _typeshed.wsgi import StartResponse
    from _typeshed.wsgi import WSGIApplication
    from _typeshed.wsgi import WSGIEnvironment


class ProxyFix:
    """根据应用前方的代理可能设置的 ``X-Forwarded-`` 头调整 WSGI environ。

    -   ``X-Forwarded-For`` 设置 ``REMOTE_ADDR``。
    -   ``X-Forwarded-Proto`` 设置 ``wsgi.url_scheme``。
    -   ``X-Forwarded-Host`` 设置 ``HTTP_HOST``、``SERVER_NAME`` 和
        ``SERVER_PORT``。
    -   ``X-Forwarded-Port`` 设置 ``HTTP_HOST`` 和 ``SERVER_PORT``。
    -   ``X-Forwarded-Prefix`` 设置 ``SCRIPT_NAME``。

    你必须告诉中间件每个头由多少个代理设置，以便它知道哪些值可信。
    信任来自客户端而非代理的值会带来安全问题。

    头的原始值存储在 WSGI environ 的 ``werkzeug.proxy_fix.orig``
    字典中。

    :param app: 要包装的 WSGI 应用。
    :param x_for: 对 ``X-Forwarded-For`` 信任的值的数量。
    :param x_proto: 对 ``X-Forwarded-Proto`` 信任的值的数量。
    :param x_host: 对 ``X-Forwarded-Host`` 信任的值的数量。
    :param x_port: 对 ``X-Forwarded-Port`` 信任的值的数量。
    :param x_prefix: 对 ``X-Forwarded-Prefix`` 信任的值的数量。

    .. code-block:: python

        from werkzeug.middleware.proxy_fix import ProxyFix
        # 应用位于一个设置 -For 和 -Host 头的代理之后。
        app = ProxyFix(app, x_for=1, x_host=1)

    .. versionchanged:: 1.0
        移除了 ``num_proxies`` 参数和属性、``get_remote_addr`` 方法，以及
        environ 键 ``orig_remote_addr``、``orig_wsgi_url_scheme`` 和
        ``orig_http_host``。

    .. versionchanged:: 0.15
        所有头都支持多个值。每个头都配置为单独的可信代理数量。

    .. versionchanged:: 0.15
        原始 WSGI environ 值存储在 ``werkzeug.proxy_fix.orig`` 字典中。

    .. versionchanged:: 0.15
        支持 ``X-Forwarded-Port`` 和 ``X-Forwarded-Prefix``。

    .. versionchanged:: 0.15
        ``X-Forwarded-Host`` 和 ``X-Forwarded-Port`` 会修改
        ``SERVER_NAME`` 和 ``SERVER_PORT``。
    """

    def __init__(
        self,
        app: WSGIApplication,
        x_for: int = 1,
        x_proto: int = 1,
        x_host: int = 0,
        x_port: int = 0,
        x_prefix: int = 0,
    ) -> None:
        self.app = app
        self.x_for = x_for
        self.x_proto = x_proto
        self.x_host = x_host
        self.x_port = x_port
        self.x_prefix = x_prefix

    def _get_real_value(self, trusted: int, value: str | None) -> str | None:
        """根据配置的可信代理数量，从列表头中获取真实值。

        :param trusted: 头中要信任的值的数量。
        :param value: 要解析的逗号分隔列表头值。
        :return: 真实值；如果值的数量少于可信代理数量，则返回
            ``None``。

        .. versionchanged:: 1.0
            从 ``_get_trusted_comma`` 重命名。

        .. versionadded:: 0.15
        """
        if not (trusted and value):
            return None
        values = parse_list_header(value)
        if len(values) >= trusted:
            return values[-trusted]
        return None

    def __call__(
        self, environ: WSGIEnvironment, start_response: StartResponse
    ) -> t.Iterable[bytes]:
        """在调用被包装的应用之前，根据各种 ``Forwarded`` 头修改
        WSGI environ。将原始 environ 值存储在
        ``werkzeug.proxy_fix.orig_{key}`` 中。
        """
        environ_get = environ.get
        orig_remote_addr = environ_get("REMOTE_ADDR")
        orig_wsgi_url_scheme = environ_get("wsgi.url_scheme")
        orig_http_host = environ_get("HTTP_HOST")
        environ.update(
            {
                "werkzeug.proxy_fix.orig": {
                    "REMOTE_ADDR": orig_remote_addr,
                    "wsgi.url_scheme": orig_wsgi_url_scheme,
                    "HTTP_HOST": orig_http_host,
                    "SERVER_NAME": environ_get("SERVER_NAME"),
                    "SERVER_PORT": environ_get("SERVER_PORT"),
                    "SCRIPT_NAME": environ_get("SCRIPT_NAME"),
                }
            }
        )

        x_for = self._get_real_value(self.x_for, environ_get("HTTP_X_FORWARDED_FOR"))
        if x_for:
            environ["REMOTE_ADDR"] = x_for

        x_proto = self._get_real_value(
            self.x_proto, environ_get("HTTP_X_FORWARDED_PROTO")
        )
        if x_proto:
            environ["wsgi.url_scheme"] = x_proto

        x_host = self._get_real_value(self.x_host, environ_get("HTTP_X_FORWARDED_HOST"))
        if x_host:
            environ["HTTP_HOST"] = environ["SERVER_NAME"] = x_host
            # 通过 "]" 判断是否为不带端口的 IPv6 地址
            if ":" in x_host and not x_host.endswith("]"):
                environ["SERVER_NAME"], environ["SERVER_PORT"] = x_host.rsplit(":", 1)

        x_port = self._get_real_value(self.x_port, environ_get("HTTP_X_FORWARDED_PORT"))
        if x_port:
            host = environ.get("HTTP_HOST")
            if host:
                # 通过 "]" 判断是否为不带端口的 IPv6 地址
                if ":" in host and not host.endswith("]"):
                    host = host.rsplit(":", 1)[0]
                environ["HTTP_HOST"] = f"{host}:{x_port}"
            environ["SERVER_PORT"] = x_port

        x_prefix = self._get_real_value(
            self.x_prefix, environ_get("HTTP_X_FORWARDED_PREFIX")
        )
        if x_prefix:
            environ["SCRIPT_NAME"] = x_prefix

        return self.app(environ, start_response)
```
- 当中间件启用时，设置 X 头部到环境变量

## wrappers

### request.py

https://github.com/pallets/werkzeug/blob/7868bef5/src/werkzeug/wrappers/request.py

```py
class Request(_SansIORequest):
    def __init__(
            self,
            environ: WSGIEnvironment,
            populate_request: bool = True,
            shallow: bool = False,
        ) -> None:
            super().__init__(
                method=environ.get("REQUEST_METHOD", "GET"),
                scheme=environ.get("wsgi.url_scheme", "http"),
                server=_get_server(environ),
                root_path=_wsgi_decoding_dance(environ.get("SCRIPT_NAME") or ""),
                path=_wsgi_decoding_dance(environ.get("PATH_INFO") or ""),
                query_string=environ.get("QUERY_STRING", "").encode("latin1"),
                headers=EnvironHeaders(environ),
                remote_addr=environ.get("REMOTE_ADDR"),
            )
            self.environ = environ
            self.shallow = shallow
```
- 读取环境变量初始化


## serving.py —— 自带服务器

https://github.com/pallets/werkzeug/blob/7868bef5/src/werkzeug/serving.py

```py
class WSGIRequestHandler(BaseHTTPRequestHandler):
    """A request handler that implements WSGI dispatching."""

    server: BaseWSGIServer

    @property
    def server_version(self) -> str:  # type: ignore
        return self.server._server_version

    def make_environ(self) -> WSGIEnvironment:
        request_url = urlsplit(self.path)
        url_scheme = "http" if self.server.ssl_context is None else "https"

        if not self.client_address:
            self.client_address = ("<local>", 0)
        elif isinstance(self.client_address, str):
            self.client_address = (self.client_address, 0)

        # If there was no scheme but the path started with two slashes,
        # the first segment may have been incorrectly parsed as the
        # netloc, prepend it to the path again.
        if not request_url.scheme and request_url.netloc:
            path_info = f"/{request_url.netloc}{request_url.path}"
        else:
            path_info = request_url.path

        path_info = unquote(path_info)

        environ: WSGIEnvironment = {
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": url_scheme,
            "wsgi.input": self.rfile,
            "wsgi.errors": sys.stderr,
            "wsgi.multithread": self.server.multithread,
            "wsgi.multiprocess": self.server.multiprocess,
            "wsgi.run_once": False,
            "werkzeug.socket": self.connection,
            "SERVER_SOFTWARE": self.server_version,
            "REQUEST_METHOD": self.command,
            "SCRIPT_NAME": "",
            "PATH_INFO": _wsgi_encoding_dance(path_info),
            "QUERY_STRING": _wsgi_encoding_dance(request_url.query),
            # Non-standard, added by mod_wsgi, uWSGI
            "REQUEST_URI": _wsgi_encoding_dance(self.path),
            # Non-standard, added by gunicorn
            "RAW_URI": _wsgi_encoding_dance(self.path),
            "REMOTE_ADDR": self.address_string(),
            "REMOTE_PORT": self.port_integer(),
            "SERVER_NAME": self.server.server_address[0],
            "SERVER_PORT": str(self.server.server_address[1]),
            "SERVER_PROTOCOL": self.request_version,
        }
        ...

    def address_string(self) -> str:
            if getattr(self, "environ", None):
                return self.environ["REMOTE_ADDR"]  # type: ignore

            if not self.client_address:
                return "<local>"

            return self.client_address[0]

```
- 自带服务器设置环境变量