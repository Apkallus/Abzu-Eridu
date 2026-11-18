https://docs.python.org/zh-cn/3/library/gc.html

# gc --- 垃圾回收器接口

此模块提供可选的垃圾回收器的接口，提供的功能包括：关闭收集器、调整收集频率、设置调试选项。

由于 Python 使用了带有引用计数的回收器，如果程序不会产生循环引用，可关闭回收器。
 
# gc.enable()

```py
gc.enable()
```

启用自动垃圾回收

## gc.disable()

```py
gc.disable()
```

停用自动垃圾回收

# gc.get_threshold()

```py
gc.get_threshold()
```

将当前回收阈值以形为 `(threshold0, threshold1, threshold2)` 的元组返回。


## gc.set_threshold()

```py
gc.set_threshold(threshold0[, threshold1[, threshold2]])
```

设置垃圾回收阈值（收集频率）。将 `threshold0` 设为零会禁用回收。

垃圾回收器把所有对象分类为三代，其依据是对象在多少次垃圾回收后幸存。

##  gc.freeze()

```py
gc.freeze()
```

冻结由垃圾回收器追踪的所有对象；将它们移至永久代并在所有未来的回收操作中忽略它们。

## gc.collect()

```py
gc.collect(generation=2)
```

不带参数时，将运行完全的回收。 可选的参数 `generation` 是一个指定要回收哪一代 (从 0 到 2) 的整数值。 

每当运行完整收集或最高代 (2) 收集时，为多个内置类型所维护的空闲列表会被清空。