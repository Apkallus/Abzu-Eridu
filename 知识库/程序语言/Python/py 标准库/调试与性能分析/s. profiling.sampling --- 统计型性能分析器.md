https://docs.python.org/zh-cn/3.15/library/profiling.sampling.html

# profiling.sampling --- 统计型性能分析器

```sh
# 使用 cpu 模式，提高采样率，采样时间 60s，使用火焰图
python -m profiling.sampling run --mode=cpu -r 20khz -d 60 --flamegraph -o a.html testa.py
```

其中的 `EMBEDDED_DATA` JSON 保存数据

## 命令

### run 命令

run 命令 会启动脚本Python 或模块 ，并从头开始对其进行性能分析:

```sh
python -m profiling.sampling run script.py
python -m profiling.sampling run -m mypackage.module
```

## 模式选项

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

