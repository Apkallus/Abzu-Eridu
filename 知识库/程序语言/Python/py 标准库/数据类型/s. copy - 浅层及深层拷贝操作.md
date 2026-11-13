https://docs.python.org/zh-cn/3/library/copy.html

# copy --- 浅层及深层拷贝操作

Python 的赋值语句不复制对象，而是创建目标和对象的绑定关系。对于自身可变，或包含可变项的集合，有时要生成副本用于改变操作，而不必改变原始对象。本模块提供了通用的浅层复制和深层复制操作，（如下所述）。


- 
    ```py
    copy.copy(obj)
    ```
    返回 `obj` 的浅拷贝。

- 
    ```py
    copy.deepcopy(obj[, memo])
    ```
    返回 `obj` 的深拷贝。

- 
    ```py
    copy.replace(obj, /, **changes)
    ```
    新建一个与 `obj` 类型相同的对象，使用来自 `changes` 的值替换字段。