- 调试标记文档
    https://code.djangoproject.com/wiki/TemplatePitfalls?version=10
    - 找到
        ```django
        {% debug %}
        ```

列出的所有对象中，框架的 settings 字段或为懒加载

```py
'settings': < LazySettings "None" >
```

- 模板载荷
    ```py
    {{settings}}
    ```
    - 服务器响应
        ```py
        <UserSettingsHolder>
        ```

    - 设置的懒加载导致无法直接打印所有属性，而仅为占位符

- 查看 django 的设置文档
    https://docs.djangoproject.com/en/6.1/ref/settings/#secret-key
    - 找到字段名称为 `SECRET_KEY`

- 查询设置的秘密字段
    ```py
    {{settings.SECRET_KEY}}
    ```
