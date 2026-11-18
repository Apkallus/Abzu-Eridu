https://learn.microsoft.com/zh-cn/windows/console/console-structures

# 控制台 API 结构

## INPUT_RECORD 结构

描述控制台输入缓冲区中的输入事件。 可以使用 [**ReadConsoleInput 或 PeekConsoleInput**] 函数从输入缓冲区读取这些记录，或使用 [**WriteConsoleInput**] 函数写入输入缓冲区。

```C
typedef struct _INPUT_RECORD {
  WORD  EventType;
  union {
    KEY_EVENT_RECORD          KeyEvent;
    MOUSE_EVENT_RECORD        MouseEvent;
    WINDOW_BUFFER_SIZE_RECORD WindowBufferSizeEvent;
    MENU_EVENT_RECORD         MenuEvent;
    FOCUS_EVENT_RECORD        FocusEvent;
  } Event;
} INPUT_RECORD;
```

### 成员

- `EventType`  
    输入事件类型和 `事件成员中` 存储的事件记录的句柄。

## KEY_EVENT_RECORD 结构

描述控制台 `INPUT_RECORD` 结构中的键盘输入事件。

```C
typedef struct _KEY_EVENT_RECORD {
  BOOL  bKeyDown;
  WORD  wRepeatCount;
  WORD  wVirtualKeyCode;
  WORD  wVirtualScanCode;
  union {
    WCHAR UnicodeChar;
    CHAR  AsciiChar;
  } uChar;
  DWORD dwControlKeyState;
} KEY_EVENT_RECORD;
```

### 成员

**bKeyDown** 如果按下键，则此成员为 **TRUE**。 否则，此成员为 **FALSE** （密钥已释放）。

**wRepeatCount** 重复计数，指示正在按住键。 例如，当某个键被按住时，你可能会得到 5 个事件，此成员等于 1、一个此成员等于 5 的事件，或者此成员大于或等于 1 的多个事件。

**wVirtualKeyCode** 一个 [虚拟密钥代码] ，用于以独立于设备的方式标识给定密钥。

**wVirtualScanCode** 表示键盘硬件生成的设备依赖值的给定键的虚拟扫描代码。

**uChar** 以下成员的联合。

**UnicodeChar** 已翻译的 Unicode 字符。

**AsciiChar** 已转换的 ASCII 字符。

**dwControlKeyState** 控制键的状态。 此成员可以是以下一个或多个值。


## WINDOW_BUFFER_SIZE_RECORD 结构 

描述主机屏幕缓冲区大小的变化。

```C
typedef struct _WINDOW_BUFFER_SIZE_RECORD {
  COORD dwSize;
} WINDOW_BUFFER_SIZE_RECORD;
```

### 成员

**dwSize**[**COORD**] 结构，包含控制台屏幕缓冲区的大小，以字符单元格列和行为单位。

### 注解

当控制台处于窗口感知模式（**ENABLE\_WINDOW\_INPUT**）时，缓冲区大小事件将放置在输入缓冲区中。
