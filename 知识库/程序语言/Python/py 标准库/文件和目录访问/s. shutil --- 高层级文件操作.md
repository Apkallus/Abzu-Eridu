https://docs.python.org/zh-cn/3/library/shutil.html

# shutil --- 高层级文件操作

## 查询输出终端的尺寸¶

### shutil.get_terminal_size()

```py
shutil.get_terminal_size(fallback=(columns, lines))
```

获取终端窗口的尺寸。

`os.get_terminal_size()` 的回退包装版

返回的值是一个 `os.terminal_size` 类型的具名元组。