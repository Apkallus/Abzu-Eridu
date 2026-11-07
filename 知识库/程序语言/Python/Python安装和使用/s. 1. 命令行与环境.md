# 1. 命令行与环境

https://docs.python.org/zh-cn/3/using/cmdline.html

为获取各种设置信息，CPython 解释器会扫描命令行与环境。

## 1.1. 命令行

调用 Python 时，可以指定下列任意选项：

```sh
python [-bBdEhiIOPqRsSuvVWx?] [-c command | -m module-name | script | - ] [args]
```

最常见的用例是启动时执行脚本：

```py
python myscript.py
```

### 1.1.1. 接口选项

- `-c <command>`  
    执行 `command` 中的 Python 代码。`command` 可以是一条语句，也可以是用换行符分隔的多条语句，其中，前导空白字符与普通模块代码中的作用一样。

- `-m <module-name>`  
    使用标准导入机制位置模块并将其内容作为 `__main__` 模块来执行。
    
    该参数是 `模块` 名称，请勿输入文件扩展名 (`.py`)。
    
- `<script>`  
    执行 `script` 中的 Python 代码