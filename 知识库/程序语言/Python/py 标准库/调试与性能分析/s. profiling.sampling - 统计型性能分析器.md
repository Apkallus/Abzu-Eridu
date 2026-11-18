https://docs.python.org/zh-cn/3/library/profiling.sampling.html

# profiling.sampling --- 统计型性能分析器

```sh
# 使用 cpu 模式，提高采样率，采样时间 60s，使用火焰图
python3 -m profiling.sampling run --mode=cpu -r 20khz -d 30 --flamegraph -o profile.html script.py

# 使用 cpu 模式，提高采样率，采样时间 30s，终端文本输出
python3 -m profiling.sampling run --mode=cpu -r 20khz -d 30 --binary -o profile script.py
# 查看二进制文件
python3 -m profiling.sampling replay profile
```

其中的 `EMBEDDED_DATA` JSON 保存数据

## 命令

### run 命令

run 命令 会启动脚本Python 或模块 ，并从头开始对其进行性能分析:

```sh
python -m profiling.sampling run script.py
python -m profiling.sampling run -m mypackage.module
```

### replay 命令

replay 命令可将二进制性能分析文件转换为其他输出格式:

```sh
# Convert binary to pstats (default, prints to stdout)
python -m profiling.sampling replay profile.bin

# Convert binary to flame graph
python -m profiling.sampling replay --flamegraph -o output.html profile.bin

# Convert binary to gecko format for Firefox Profiler
python -m profiling.sampling replay --gecko -o profile.json profile.bin

# Convert binary to heatmap
python -m profiling.sampling replay --heatmap -o my_heatmap profile.bin
```

## 输出选项

- `--pstats`  
    生成 pstats 统计信息。这是默认行为。当输出到 stdout 时，结果将以文本表格形式呈现；若使用 `-o`，则生成二进制 pstats 文件。
    > 仅包含代码行号
    > 文件字符解析异常，存在无法解析为 utf-8 的字符
    
- `--flamegraph`  
    生成独立的 HTML 火焰图。

- `--heatmap`  
    生成包含行级样本计数的 HTML 热力图。

- `-o <path>, --output <path>`  
    输出文件或目录路径。

## 采样配置

### 采样率与持续时间

两个最基本的参数是采样率和持续时间。二者共同决定了在一次分析过程中将采集多少个样本。

`--sampling-rate` 选项（`-r`）用于设置样本采集频率。默认值为 1 kHz（每秒采集 1,000 个样本）:

```sh
python -m profiling.sampling run -r 20khz script.py
```

`--duration` 选项（`-d`）用于设置性能分析的持续时间（以秒为单位）。默认情况下，性能分析会一直持续，直到目标进程退出或被中断

```sh
python -m profiling.sampling run -d 60 script.py
```

## 分析模式

采样分析器支持四种模式，用于控制记录哪些样本。模式决定了分析器测量哪些指标：累计经过时间、CPU 执行时间、持有全局解释器锁所花费的时间，或异常处理时间。

### CPU 模式

CPU 模式（`--mode=cpu`）仅在线程实际在某个 CPU 核心上执行时才会记录样本:

```sh
python -m profiling.sampling run --mode=cpu script.py
```

在线程处于休眠状态、被 I/O 阻塞或等待锁时采集的样本会被丢弃。由此生成的性能剖面图会显示 CPU 周期被消耗于何处，同时过滤掉空闲时间。

> 日常使用模式，尤其对于拥有时间延迟。或需提高默认采样率

## 基于操作码的性能分析

--opcodes 选项可启用指令级性能分析，用于捕获每个采样点正在执行的 Python 字节码指令:

```sh
python -m profiling.sampling run --opcodes --flamegraph script.py
```

该功能可让开发者了解 Python 字节码的执行情况，包括自适应特化优化。


## 输出格式

### pstats

pstats 格式（`--pstats`）会生成一种与确定性分析器所生成结果类似的文本表格。这是默认的输出格式:

```sh
python -m profiling.sampling run script.py
python -m profiling.sampling run --pstats script.py
```

使用 `--no-summary` 同时抑制图例部分和摘要部分。

pstats 格式支持多种用于控制显示方式的选项。`--sort` 选项用于确定用于对结果进行排序的列`

`--limit` 选项将输出限制为前 N 条记录

`--no-summary` 选项会抑制统计表之前的标题摘要。

### 折叠堆栈格式

折叠堆栈格式（`--collapsed`）会为每个唯一的调用堆栈生成一行，并记录该堆栈被采样的次数:

```sh
python -m profiling.sampling run --collapsed script.py
```

### 二进制格式

二进制格式（`--binary`）可生成紧凑的二进制文件，从而高效存储分析数据:

```sh
python -m profiling.sampling run --binary -o profile.bin script.py
python -m profiling.sampling attach --binary -o profile.bin 12345
```

> 当直接使用默认的 pstats 文本解析异常时，输出为二进制格式，再使用 replay 查看

`--compression` 选项用于控制数据压缩

若要分析二进制配置文件，请使用 `replay command` 将其转换为其他格式，例如火焰图或 `pstats` 输出格式。