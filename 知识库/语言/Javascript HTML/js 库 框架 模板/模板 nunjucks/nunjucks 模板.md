https://mozilla.github.io/nunjucks/cn/templating.html

# 模板

## 内置的过滤器

### ♾️ dump (object)

在一个对象上调用JSON.stringify，并将结果输出到模板上。这在调试时很有用：

> 调试导出数据

```py
{{ foo | dump }}
```