https://palletsprojects.com/projects/itsdangerous/

## url_safe.py

https://github.com/pallets/itsdangerous/blob/672971d6/src/itsdangerous/url_safe.py

```py
class URLSafeSerializerMixin(Serializer[str]):
    """
    与常规序列化器混用时，它会尝试用 zlib 压缩字符串，以便在需要时缩短其长度；同时还会对字符串进行 base64 编码，使其能够安全地放入 URL。
    """

    def dump_payload(self, obj: t.Any) -> bytes:
        json = super().dump_payload(obj)
        is_compressed = False
        compressed = zlib.compress(json)

        if len(compressed) < (len(json) - 1):
            json = compressed
            is_compressed = True

        base64d = base64_encode(json)

        if is_compressed:
            base64d = b"." + base64d

        return base64d
```
- flask cookie 压缩编码
    1. json = min(zlib 压缩后, 原始长度)
    2. base64 编码
    3. 若 zlib 压缩，则在开头添加 `.`