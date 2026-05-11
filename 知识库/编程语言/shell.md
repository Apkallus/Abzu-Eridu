### exec

- `exec /程序` 替换当前进程到对应程序
- `exec 3</` 将根目录重定向到 fd 3
    - `exec {fdn}</; echo $fdn` 将根目录重定向到自动分配的空闲 fd，并使用 `echo` 查看对应 fd，`fdn` 为普通变量名


### mapfile & readarray

```
mapfile [-n count] [-O origin] [-s count] [-t] [-u fd] [-C callback] [-c quantum] [array]
readarray [-n count] [-O origin] [-s count] [-t] [-u fd] [-C callback] [-c quantum] [array]
```

从标准输入读取行到索引数组变量array中，如果提供-u选项，则从文件描述符fd读取。变量MAPFILE是默认的数组。如果提供选项，则具有以下含义：
- `-t`
    删除每行读取后的换行符。

示例：
- `mapfile -t BIN_FILES  < <(file /challenge/* | grep ELF)`


### 语法

- `"${BIN_FILES[@]}"` 
    展开数组元素