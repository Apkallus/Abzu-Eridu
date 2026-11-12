## terminfo(5) - 终端能力数据库

https://github.com/ThomasDickey/ncurses-snapshots/

- `clear`  
    清除屏幕并将光标移到起始位置（P*）

- `civis`  
    使光标不可见

- `cup` 
    移到第 #1 行第 #2 列

- `sgr0`  
    关闭所有属性

- `rmso`  
    退出突出显示模式

- `setaf`  
    将前景色设为 #1，使用 ANSI 转义

- `setab`  
    将背景色设为 #1，使用 ANSI 转义

- `colornm`  
    给出颜色 #1 的名称

- `colors`  
    屏幕上的最大颜色数

- `pairs`  
    屏幕上的最大颜色对数

## console_codes(4) - Linux 控制台转义与控制序列

## tput - 初始化终端、使用其能力或查询 terminfo 数据库


```sh
# 闪烁的光标

# 隐藏光标
tput civis
# 收到退出信号信号前恢复光标
trap "tput cnorm" EXIT

# 循环交替：显示与隐藏光标
while true; do
    tput cnorm
    sleep 0.6
    tput civis
    sleep 0.6
done
```