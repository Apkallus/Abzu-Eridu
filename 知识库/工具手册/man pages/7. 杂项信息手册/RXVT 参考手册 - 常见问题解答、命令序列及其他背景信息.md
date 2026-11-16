https://man.archlinux.org/man/urxvt.7.en

# RXVT REFERENCE - FAQ, command sequences and other background information

```sh
# set a new font set
printf '\33]50;%s\007' 9x15,xft:Kochi" Mincho"
# change the locale and tell rxvt-unicode about it
export LC_CTYPE=ja_JP.EUC-JP; printf "\33]701;$LC_CTYPE\007"
# set window title
printf '\33]2;%s\007' "new window title"
```

### DEC Private Modes

`"ESC [ ? Pm h"`
    DEC Private Mode Set (DECSET)
`"ESC [ ? Pm l"`
    DEC Private Mode Reset (DECRST)

`"Pm = 1049"` (X11 XTerm 1047 + 1048)

- `h` 使用备用屏幕缓冲区-如果切换到备用屏幕缓冲区时，请清除它

- `l` 使用普通屏幕缓冲区