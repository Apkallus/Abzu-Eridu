# API

https://jinja.palletsprojects.com/en/stable/api/

## High Level API

### class jinja2.Environment() —— 环境

```py
class jinja2.Environment([options])
```

- `loader`
    The template loader for this environment.


#### get_template() —— 加载模板

```py
get_template(name, parent=None, globals=None)
```

通过名称加载模板，使用 `loader` 并返回一个[模板]。

## Loaders

### class jinja2.FileSystemLoader() —— 从文件系统中的目录加载模板

```py
class jinja2.FileSystemLoader(searchpath, encoding='utf-8', followlinks=False)
```

路径可以是相对路径或绝对路径。相对路径相对于当前工作目录。

```py
loader = FileSystemLoader("templates")
```

可以提供一个路径列表。系统将按顺序搜索这些目录，一旦找到第一个匹配的模板就会停止。

```py
loader = FileSystemLoader(["/override/templates", "/default/templates"])
```