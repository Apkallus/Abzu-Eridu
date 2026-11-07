https://jinja.palletsprojects.com/en/stable/templates/

## 变量

模板中的 `foo.bar` 与 `foo["bar"]` 均尝试访问属性与条目这2类
- 属性 `getattr(foo, 'bar')`
    - 对应仅访问属性的过滤器 `attr()`
- 条目 `foo.__getitem__('bar')`
- 区别在于： `.` 优先属性，`[]` 优先条目


## 过滤器

过滤器修改变量。过滤器与变量之间用管道符号（`|`）分隔，并且可以在括号中带有可选参数。多个过滤器可以链式调用。一个过滤器的输出会应用到下一个过滤器。

例如，`{{ name|striptags|title }}` 将从变量 `name` 中移除所有 HTML 标签，并将输出转换为标题大小写（`title(striptags(name))`）。

接受参数的过滤器在参数周围有括号，就像函数调用一样。例如：`{{ listx|join(', ') }}` 将用逗号连接列表（`str.join(', ', listx)`）。

下面的[内置过滤器列表]描述了所有内置过滤器。