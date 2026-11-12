# 7. 简单语句

https://docs.python.org/zh-cn/3/reference/simple_stmts.html

简单语句由一个单独的逻辑行构成。 多条简单语句可以存在于同一行内并以分号 `;` 分隔。

## 7.11. import 语句

模块名后使用 `as` 时，直接把 `as` 后的名称与导入模块绑定。

```py
import foo                 # foo 被导入并且被局部绑定
import foo.bar.baz         # foo, foo.bar 和 foo.bar.baz 被导入，foo 被局部绑定
import foo.bar.baz as fbb  # foo, foo.bar 和 foo.bar.baz 被导入，foo.bar.baz 被绑定为 fbb
from foo.bar import baz    # foo, foo.bar 和 foo.bar.baz 被导入，foo.bar.baz 被绑定为 baz
from foo import attr       # foo 被导入并且 foo.attr 被绑定为 attr
```