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
- `re.sub(pattern, repl, string, count=0, flags=0)`  
    返回通过使用 repl 替换在 string 最左边非重叠出现的 pattern 而获得的字符串。 如果样式没有找到，则不加改变地返回 string。  
    可选参数 count 是要替换的模式的最大出现次数；count 必须是一个非负整数。 如果省略或为零，则将全部替换。
- ```re.search()```
    在字符串的任意位置匹配模式，返回第一个匹配的 ```Match``` 或 ```None```

- ```Match.group([group1, ...])```
    单个参数返回字符串，多个参数返回元组
    参数 ```0``` 应用所有子分组的匹配，其他数字则返回对应子分组的匹配

- 正则表达式
    - ```*?``` ```+?``` ```??```
        在默认贪婪的匹配符后的 ```?``` 转为非贪婪模式
    - `{m,n}`  
        对正则式进行 m 到 n 次匹配，在 m 和 n 之间取尽量多。  
        忽略 m 意为指定下界为 0，忽略 n 指定上界为无限次。

### zipfile

[文档](https://docs.python.org/zh-cn/3/library/zipfile.html)

- `ZipFile.write(filename, arcname=None, compress_type=None, compresslevel=None)`
    将名为 filename 的文件写入归档，给予的归档名为 arcname (默认情况下将与 filename 一致，但是不带驱动器盘符并会移除开头的路径分隔符)。
- `ZipFile.writestr(zinfo_or_arcname, data, compress_type=None, compresslevel=None)`
    将一个文件写入归档，内容为 data。 zinfo_or_arcname 可以是它在归档中将被给予的名称，或者是 ZipInfo 的实例。
    即，设置归档内文件名及其数据。

###  string

- `string.replace(old, new[, count])`  
    使用字串new替换字串old  
    count设置替换次数，若未指定则替换所有

### urllib

`urllib.request.urlopen(url, data=None, [timeout, ]*, context=None)`
打开 *url*，它可以是包含有效、正确编码的 URL 的字符串，也可以是 Request 对象。

```python
import urllib.request

url = 'https://www.example.com'
response = urllib.request.urlopen(url)
# 此处读取为字节序列，或需使用 decode('utf-8') 解码
content = response.read()

print(content)
```

### sys

- `sys.argv`
    一个列表，其中包含了被传递给 Python 脚本的命令行参数。 `argv[0]` 为脚本的名称（是否是完整的路径名取决于操作系统）。

### 备忘
- ```with open(filepath, 'r', encoding='utf-8') as f:```
    设置文件路径、模式、编码后读取文件，作用域结束后自动关闭
    - `x` 模式可避免覆盖文件

- ```if not container:```
    在布尔上下文快速判断字典、列表、元组等容器是否为空

- `'abcde'[1:]`
    提取子串

- `for i, value in enumerate(列表)`  
    `enumerate()` 函数返回下标与值，可用来遍历列表
    

## 参考

https://geek-docs.com/python