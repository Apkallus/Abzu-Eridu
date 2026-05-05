
## source/libio/bits/types/struct_FILE.h 文件结构

```c
/* 此结构体的标签名为 _IO_FILE，是为了保留历史遗留的 C++ 命名规范，
   以便接受 FILE* 类型参数的函数能够保持其命名。
   新代码中不应再使用该名称。 */
struct _IO_FILE
{
  int _flags;		/* 高16位是 _IO_MAGIC；其余位是标志位。 */

  /* 以下指针对应于 C++ 的 streambuf 协议。 */
  char *_IO_read_ptr;	/* 当前读指针 */
  char *_IO_read_end;	/* 获取区域的结束位置。 */
  char *_IO_read_base;	/* 放回+获取区域的起始位置。 */
  char *_IO_write_base;	/* 放入区域的起始位置。 */
  char *_IO_write_ptr;	/* 当前写指针。 */
  char *_IO_write_end;	/* 放入区域的结束位置。 */
  char *_IO_buf_base;	/* 保留区域的起始位置。 */
  char *_IO_buf_end;	/* 保留区域的结束位置。 */

  /* 以下字段用于支持回退和撤销操作。 */
  char *_IO_save_base;  /* 指向非当前获取区域的起始位置。 */
  char *_IO_backup_base;  /* 指向回退区域的第一个有效字符。 */
  char *_IO_save_end;   /* 指向非当前获取区域的结束位置。 */

  struct _IO_marker *_markers;

  struct _IO_FILE *_chain;

  int _fileno;
  int _flags2:24;
  /* 当 malloc 分配缓冲区失败时使用的后备缓冲区。 */
  char _short_backupbuf[1];
  __off_t _old_offset; /* 之前是 _offset，但大小太小。 */

  /* pbase() 的列数加1；0 表示未知。 */
  unsigned short _cur_column;
  signed char _vtable_offset;
  char _shortbuf[1];

  _IO_lock_t *_lock;
#ifdef _IO_USE_OLD_IO_FILE
};

struct _IO_FILE_complete
{
  struct _IO_FILE _file;           /* 基础 _IO_FILE 结构体 */
#endif
  __off64_t _offset;               /* 文件偏移量 */
  /* 宽字符流相关内容 */
  struct _IO_codecvt *_codecvt;    /* 编码转换对象 */
  struct _IO_wide_data *_wide_data; /* 宽字符流数据 */
  struct _IO_FILE *_freeres_list;  /* 可释放资源链表 */
  void *_freeres_buf;              /* 可释放资源缓冲区 */
  struct _IO_FILE **_prevchain;    /* 前向链表指针 */
  int _mode;                       /* 文件打开模式 */
#if __WORDSIZE == 64
  int _unused3;                    /* 64位系统下未使用的填充 */
#endif
  __uint64_t _total_written;       /* 已写入总字节数 */
#if __WORDSIZE == 32
  int _unused3;                    /* 32位系统下未使用的填充 */
#endif
  /* 确保我们不再陷入麻烦 */
  char _unused2[12 * sizeof (int) - 5 * sizeof (void *)];
};
```

## / libio / libio.h 文件结构

```c
/* _flags 字段的魔法数字和标志位。魔法数字主要是历史遗留，但为兼容性而保留。
   它占用 _flags 的高16位；低16位是实际的标志位。 */

#define _IO_MAGIC         0xFBAD0000 /* 魔法数字 */
#define _IO_MAGIC_MASK    0xFFFF0000
#define _IO_USER_BUF          0x0001 /* 关闭时不释放缓冲区。 */
#define _IO_UNBUFFERED        0x0002
#define _IO_NO_READS          0x0004 /* 不允许读取。 */
#define _IO_NO_WRITES         0x0008 /* 不允许写入。 */
#define _IO_EOF_SEEN          0x0010
#define _IO_ERR_SEEN          0x0020
#define _IO_DELETE_DONT_CLOSE 0x0040 /* 关闭时不要调用 close(_fileno)。 */
#define _IO_LINKED            0x0080 /* 在打开文件链表中。 */
#define _IO_IN_BACKUP         0x0100
#define _IO_LINE_BUF          0x0200
#define _IO_TIED_PUT_GET      0x0400 /* 读写指针同步移动。 */
#define _IO_CURRENTLY_PUTTING 0x0800
#define _IO_IS_APPENDING      0x1000
#define _IO_IS_FILEBUF        0x2000
                           /* 0x4000 不再使用，为兼容性保留。 */
#define _IO_USER_LOCK         0x8000


/* 宽字符流的额外数据。 */
struct _IO_wide_data
{
  wchar_t *_IO_read_ptr;	/* 当前读指针 */
  wchar_t *_IO_read_end;	/* 获取区域的结束位置 */
  wchar_t *_IO_read_base;	/* 放回+获取区域的起始位置 */
  wchar_t *_IO_write_base;	/* 放入区域的起始位置 */
  wchar_t *_IO_write_ptr;	/* 当前写指针 */
  wchar_t *_IO_write_end;	/* 放入区域的结束位置 */
  wchar_t *_IO_buf_base;	/* 保留区域的起始位置 */
  wchar_t *_IO_buf_end;		/* 保留区域的结束位置 */
  /* 以下字段用于支持回退和撤销操作 */
  wchar_t *_IO_save_base;	/* 指向非当前获取区域的起始位置 */
  wchar_t *_IO_backup_base;	/* 指向回退区域的第一个有效字符 */
  wchar_t *_IO_save_end;	/* 指向非当前获取区域的结束位置 */

  __mbstate_t _IO_state;
  __mbstate_t _IO_last_state;
  struct _IO_codecvt _codecvt;

  wchar_t _shortbuf[1];

  const struct _IO_jump_t *_wide_vtable;
};

```

## / libio / libioP.h 文件结构

```c
struct _IO_jump_t
{
    JUMP_FIELD(size_t, __dummy);
    JUMP_FIELD(size_t, __dummy2);
    JUMP_FIELD(_IO_finish_t, __finish);
    JUMP_FIELD(_IO_overflow_t, __overflow);
    JUMP_FIELD(_IO_underflow_t, __underflow);
    JUMP_FIELD(_IO_underflow_t, __uflow);
    JUMP_FIELD(_IO_pbackfail_t, __pbackfail);
    /* showmany */
    JUMP_FIELD(_IO_xsputn_t, __xsputn);
    JUMP_FIELD(_IO_xsgetn_t, __xsgetn);
    JUMP_FIELD(_IO_seekoff_t, __seekoff);
    JUMP_FIELD(_IO_seekpos_t, __seekpos);
    JUMP_FIELD(_IO_setbuf_t, __setbuf);
    JUMP_FIELD(_IO_sync_t, __sync);
    JUMP_FIELD(_IO_doallocate_t, __doallocate);
    JUMP_FIELD(_IO_read_t, __read);
    JUMP_FIELD(_IO_write_t, __write);
    JUMP_FIELD(_IO_seek_t, __seek);
    JUMP_FIELD(_IO_close_t, __close);
    JUMP_FIELD(_IO_stat_t, __stat);
    JUMP_FIELD(_IO_showmanyc_t, __showmanyc);
    JUMP_FIELD(_IO_imbue_t, __imbue);
};

/* 我们总是在 _IO_FILE 后面额外分配一个字。
   这个字包含一个指向所使用的函数跳转表的指针。
   这是为了与 C++ streambuf 兼容；该字可被篡改成指向虚函数表的指针。 */

struct _IO_FILE_plus
{
  FILE file;
  const struct _IO_jump_t *vtable;
};
```

##  / include / linux / msg.h 信息结构

```c
/* one msg_msg structure for each message */
struct msg_msg {
	struct list_head m_list;
	long m_type;
	size_t m_ts;		/* message text size */
	struct msg_msgseg *next;
	void *security;
	/* the actual message follows immediately */
};
```