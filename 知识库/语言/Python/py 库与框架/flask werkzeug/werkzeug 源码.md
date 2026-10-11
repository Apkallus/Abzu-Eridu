# werkzeug

https://github.com/pallets/werkzeug/tree/main/src/werkzeug
- 与 flask github 库不同，werkzeug 拥有旧版代码

## security.py

https://github.com/pallets/werkzeug/blob/main/src/werkzeug/security.py

### safe_join

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
