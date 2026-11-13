https://docs.python.org/zh-cn/3/library/itertools.html

# itertools --- 为高效循环创建迭代器的函数

## Itertool 函数

### itertools.cycle(iterable)

创建一个迭代器，从可迭代对象中返回元素，并保存每个元素的副本。当可迭代对象耗尽时，返回保存副本中的元素。无限重复。

```py
for i in itertools.cycle(range(1, 7)):
    pass
```

### itertools.batched()

```py
itertools.batched(iterable, n, *, strict=False)
```
 
按照固定长度 `n`，分割可迭代对象。最后一个批次可能短于 `n`。

如果 `strict` 为真值，将在最终的批次短于 `n` 时引发 `ValueError`。

```py
# 列表推导式手动切割
tmp_list = [color_list[i:i+step] for i in range(0, color_list_len, step)]
# 等效调用
tmp_list = list(batched(color_list, step))
```


### itertools.starmap()

```py
itertools.starmap(function, iterable)
```

创建一个迭代器，它使用从 iterable 获取的参数来计算 function。 当参数形参已被“预先 zip”为元组时可代替 map() 来使用。

```py
def starmap(function, iterable):
    # starmap(pow, [(2,5), (3,2), (10,3)]) → 32 9 1000
    for args in iterable:
        yield function(*args)
```