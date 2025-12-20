### ```os```
- ```os.walk()``` 
    递归遍历目录
    ```python
    import os

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
    ```
    ```Iterator[tuple[AnyStr@walk, list[AnyStr@walk], list[AnyStr@walk]]]```
    迭代器返回的三元组均为字符串或字符串列表，搭配 ```os.path.join()``` 拼接路径

- ```os.path.join()``` 
    拼接路径
    ```python
    import os

    os.path.join('路径1','路径2','路径N')
    ```
    在非空参数间添加路径分隔符号。
    路径可为目录或文件名，可为仅最后一个生效的绝对路径

- ```os.path.relpath(path, startPath)```
    计算基于起始路径的相对路径

### ```frontmatter```
- <https://python-frontmatter.readthedocs.io/en/latest/>
- ```frontmatter.load()```
    从文件名、文件中加载到对象 ```Post```
- ```frontmatter.loads()```
    加载字符串到对象 ```Post```

- ```post.content``` 或 ```post```
    访问元数据外的内容
- ```post.metadata```
    获取元数据字典
- ```post['元数据字段名']```
    从元数据字典中检索字段


### ```re``` 
- <https://docs.python.org/zh-cn/3/library/re.html#>

- ```re.compile(pattern, flags=0)```
    将正则表达式保存到对象中复用
- ```flags```
    - ```re.DOTALL```
    使 ```.``` 匹配包含 ```\n``` 在内的任意字符

- ```re.search()```
    在字符串的任意位置匹配模式，返回第一个匹配的 ```Match``` 或 ```None```

- ```Match.group([group1, ...])```
    单个参数返回字符串，多个参数返回元组
    参数 ```0``` 应用所有子分组的匹配，其他数字则返回对应子分组的匹配

- 正则表达式
    - ```*?``` ```+?``` ```??```
        在默认贪婪的匹配符后的 ```?``` 转为非贪婪模式
### 备忘
- ```with open(filepath, 'r', encoding='utf-8') as f:```
    设置文件路径、模式、编码后读取文件，作用域结束后自动关闭

- ```if not container:```
    在布尔上下文快速判断字典、列表、元组等容器是否为空