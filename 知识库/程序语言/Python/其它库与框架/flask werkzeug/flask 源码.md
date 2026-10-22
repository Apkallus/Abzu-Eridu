https://github.com/pallets/flask

# flask

https://github.com/pallets/flask/tree/main/src/flask

[社区 0.11 旧版](https://tedboy.github.io/flask/index.html)
- 文档-源码 型，快速切换

## helpers.py

https://github.com/pallets/flask/blob/main/src/flask/helpers.py


### send_from_directory —— github 最新版

```py
def send_from_directory(
    directory: os.PathLike[str] | str,
    path: os.PathLike[str] | str,
    **kwargs: t.Any,
) -> Response:
    """使用 :func:`send_file` 从目录中发送文件。

    .. code-block:: python

        @app.route("/uploads/<path:name>")
        def download_file(name):
            return send_from_directory(
                app.config['UPLOAD_FOLDER'], name, as_attachment=True
            )

    这是一种从文件夹（例如静态文件或上传文件）安全地提供文件的方式。
    它使用 :func:`~werkzeug.security.safe_join` 来确保来自客户端的路径
    不会被恶意构造以指向指定目录之外。

    如果最终路径没有指向一个现有的常规文件，
    则抛出 404 :exc:`~werkzeug.exceptions.NotFound` 错误。

    :param directory: ``path`` 必须位于其中的目录，
        相对于当前应用程序的根路径。该值*绝不能*由客户端提供，
        否则将变得不安全。
    :param path: 要发送的文件路径，相对于 ``directory``。
    :param kwargs: 传递给 :func:`send_file` 的参数。

    .. versionchanged:: 2.0
        ``path`` 取代了 ``filename`` 参数。

    .. versionadded:: 2.0
        实现已移至 Werkzeug。现在它只是一个包装器，用于
        传递一些 Flask 特有的参数。

    .. versionadded:: 0.5
    """
    return werkzeug.utils.send_from_directory(  # type: ignore[return-value]
        directory, path, **_prepare_send_file_kwargs(**kwargs)
    )
```

#### send_from_directory 0.11 旧版

```py
def send_from_directory(directory, filename, **options):
    """使用 :func:`send_file` 从给定目录发送文件。这是一种安全的方式，
    可快速公开上传文件夹或类似位置中的静态文件。

    示例用法::

        @app.route('/uploads/<path:filename>')
        def download_file(filename):
            return send_from_directory(app.config['UPLOAD_FOLDER'],
                                       filename, as_attachment=True)

    .. admonition:: 发送文件与性能

       强烈建议在 Web 服务器中启用 ``X-Sendfile`` 支持，或者（如果
       无需身份验证）让 Web 服务器自行提供给定路径的文件，而无需
       调用 Web 应用程序，以提高性能。

    .. versionadded:: 0.5

    :param directory: 存储所有文件的目录。
    :param filename: 相对于该目录要下载的文件名。
    :param options: 可选的关键字参数，直接转发给 :func:`send_file`。
    """
    filename = safe_join(directory, filename)
    if not os.path.isabs(filename):
        filename = os.path.join(current_app.root_path, filename)
    try:
        if not os.path.isfile(filename):
            raise NotFound()
    except (TypeError, ValueError):
        raise BadRequest()
    options.setdefault('conditional', True)
    return send_file(filename, **options)
```

## 旧版

### safe_join 0.11 

```py
def safe_join(directory, filename):
    """Safely join `directory` and `filename`.

    Example usage::

        @app.route('/wiki/<path:filename>')
        def wiki_page(filename):
            filename = safe_join(app.config['WIKI_FOLDER'], filename)
            with open(filename, 'rb') as fd:
                content = fd.read()  # Read and process the file content...

    :param directory: the base directory.
    :param filename: the untrusted filename relative to that directory.
    :raises: :class:`~werkzeug.exceptions.NotFound` if the resulting path
             would fall out of `directory`.
    """
    filename = posixpath.normpath(filename)
    for sep in _os_alt_seps:
        if sep in filename:
            raise NotFound()
    if os.path.isabs(filename) or \
       filename == '..' or \
       filename.startswith('../'):
        raise NotFound()
    return os.path.join(directory, filename)
```

> 新版移动到 werkzeug