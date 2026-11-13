https://docs.python.org/zh-cn/3/library/random.html

# random --- 生成伪随机数

该模块实现了各种分布的伪随机数生成器。

对于整数，可从一个范围中进行均匀选择。对于序列，可均匀选择一个随机元素、生成列表的随机排列、以及进行无重复的随机抽样。

## 整数用函数

### random.randrange()

```py
random.randrange(stop)
random.randrange(start, stop[, step])
```

返回从 `range(start, stop, step)` 随机选择的一个元素。

### random.randint()

```py
random.randint(a, b)
```

返回随机整数 `N` 满足 `a <= N <= b`。相当于 `randrange(a, b+1)`。

## 序列用函数

### random.choice(seq) - 序列随机取一个元素

```py
random.choice(seq)
```

从非空序列 `seq` 返回一个随机元素。如果 `seq` 为空，则引发 `IndexError`。

### random.choices() - 批量随机取元素

```py
random.choices(population, weights=None, *, cum_weights=None, k=1)
```

从 `population` 中有重复地随机选取元素，返回大小为 `k` 的元素列表。如果 `population` 为空，则引发 `IndexError`.

## 实值分布

以下函数生成特定的实值分布。如常用数学实践中所使用的那样，函数形参以分布方程中的相应变量命名，大多数这些方程都可以在任何统计学教材中找到。

### random.random()

```py
random.random()
```

返回 `0.0 <= X < 1.0` 范围内的下一个随机浮点数。


## 替代生成器


### class random.Random()

```py
class random.Random([seed])
```

该类实现了 `random` 模块所用的默认伪随机数生成器。