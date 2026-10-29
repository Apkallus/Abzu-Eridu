# `capabilities` — Linux 能力概述

https://man7.org/linux/man-pages/man7/capabilities.7.html

## 描述

为了执行权限检查，传统 UNIX 实现将进程分为两类：*特权*进程（其有效用户 ID 为 0，称为超级用户或 root）和*非特权*进程（其有效 UID 非零）。特权进程绕过所有内核权限检查，而非特权进程则根据进程凭据（通常是：有效 UID、有效 GID 和补充组列表）接受完整的权限检查。

从 Linux 2.2 开始，Linux 将传统上与超级用户关联的特权划分为称为*能力*（capabilities）的独立单元，这些单元可以独立启用和禁用。能力是每线程属性。

### 能力列表

以下列表显示 Linux 上实现的能力，以及每种能力允许的操作或行为：

- `CAP_AUDIT_CONTROL`（自 Linux 2.6.11 起）：启用和禁用内核审计；更改审计过滤规则；检索审计状态和过滤规则。
- `CAP_AUDIT_READ`（自 Linux 3.16 起）：允许通过多播 netlink 套接字读取审计日志。
- `CAP_AUDIT_WRITE`（自 Linux 2.6.11 起）：将记录写入内核审计日志。
- `CAP_BLOCK_SUSPEND`（自 Linux 3.5 起）：使用可阻止系统挂起的功能（`[epoll(7)]` 的 `EPOLLWAKEUP`、`/proc/sys/wake_lock`）。
- `CAP_BPF`（自 Linux 5.8 起）：使用特权 BPF 操作；见 `[bpf(2)]` 和 `[bpf-helpers(7)]`。  
  此能力在 Linux 5.8 中添加，用于将 BPF 功能从过载的 `CAP_SYS_ADMIN` 能力中分离出来。
- `CAP_CHECKPOINT_RESTORE`（自 Linux 5.9 起）：  
  - 更新 `/proc/sys/kernel/ns_last_pid`（见 `[pid_namespaces(7)]`）；  
  - 使用 `[clone3(2)]` 的 `set_tid` 特性；  
  - 读取其他进程的 `/proc/pid/map_files` 中符号链接的内容。  
  
  此能力在 Linux 5.9 中添加，用于将检查点/恢复功能从过载的 `CAP_SYS_ADMIN` 能力中分离出来。
- `CAP_CHOWN`：对文件 UID 和 GID 进行任意更改（见 `[chown(2)]`）。
- `CAP_DAC_OVERRIDE`：绕过文件读、写和执行权限检查。（DAC 是“自主访问控制”的缩写。）
- `CAP_DAC_READ_SEARCH`：  
  - 绕过文件读权限检查以及目录读和执行权限检查；  
  - 调用 `[open_by_handle_at(2)]`；  
  - 使用 `[linkat(2)]` 的 `AT_EMPTY_PATH` 标志创建指向文件描述符所引用文件的链接。
- `CAP_FOWNER`：  
  - 绕过通常要求进程文件系统 UID 与文件 UID 匹配的操作的权限检查（例如 `[chmod(2)]`、`[utime(2)]`），但 `CAP_DAC_OVERRIDE` 和 `CAP_DAC_READ_SEARCH` 覆盖的操作除外；  
  - 在任意文件上设置 inode 标志（见 `[FS_IOC_SETFLAGS(2const)]`）；  
  - 在任意文件上设置访问控制列表（ACL）；  
  - 删除文件时忽略目录粘滞位；  
  - 修改任意用户拥有的粘滞目录上的 `user` 扩展属性；  
  - 在 `[open(2)]` 和 `[fcntl(2)]` 中为任意文件指定 `O_NOATIME`。
- `CAP_FSETID`：  
  - 文件被修改时不清除设置用户 ID 和设置组 ID 模式位；  
  - 为 GID 与文件系统或调用进程的任何补充 GID 不匹配的文件设置设置组 ID 位。
- `CAP_IPC_LOCK`：  
  - 锁定内存（`[mlock(2)]`、`[mlockall(2)]`、`[mmap(2)]`、`[shmctl(2)]`）；  
  - 使用大页分配内存（`[memfd_create(2)]`、`[mmap(2)]`、`[shmctl(2)]`）。
- `CAP_IPC_OWNER`：绕过对 System V IPC 对象操作的权限检查。
- `CAP_KILL`：绕过发送信号的权限检查（见 `[kill(2)]`）。这包括使用 `[ioctl(2)]` 的 `KDSIGACCEPT` 操作。
- `CAP_LEASE`（自 Linux 2.4 起）：在任意文件上建立租约（见 `[fcntl(2)]`）。
- `CAP_LINUX_IMMUTABLE`：设置 `FS_APPEND_FL` 和 `FS_IMMUTABLE_FL` inode 标志（见 `[FS_IOC_SETFLAGS(2const)]`）。
- `CAP_MAC_ADMIN`（自 Linux 2.6.25 起）：允许 MAC 配置或状态更改。为 Smack Linux 安全模块（LSM）实现。
- `CAP_MAC_OVERRIDE`（自 Linux 2.6.25 起）：覆盖强制访问控制（MAC）。为 Smack LSM 实现。
- `CAP_MKNOD`（自 Linux 2.4 起）：使用 `[mknod(2)]` 创建特殊文件。
- `CAP_NET_ADMIN`：执行各种网络相关操作：  
  - 接口配置；  
  - IP 防火墙、伪装和记账管理；  
  - 修改路由表；  
  - 为透明代理绑定到任意地址；  
  - 设置服务类型（TOS）；  
  - 清除驱动程序统计信息；  
  - 设置混杂模式；  
  - 启用多播；  
  - 使用 `[setsockopt(2)]` 设置以下套接字选项：`SO_DEBUG`、`SO_MARK`、`SO_PRIORITY`（用于 0 到 6 范围之外的优先级）、`SO_RCVBUFFORCE` 和 `SO_SNDBUFFORCE`。
- `CAP_NET_BIND_SERVICE`：将套接字绑定到 Internet 域特权端口（端口号小于 1024）。
- `CAP_NET_BROADCAST`：（未使用）进行套接字广播并监听多播。
- `CAP_NET_RAW`：  
  - 使用 RAW 和 PACKET 套接字；  
  - 为透明代理绑定到任意地址。
- `CAP_PERFMON`（自 Linux 5.8 起）：使用各种性能监控机制，包括：  
  - 调用 `[perf_event_open(2)]`；  
  - 使用具有性能影响的各种 BPF 操作。  
  
  此能力在 Linux 5.8 中添加，用于将性能监控功能从过载的 `CAP_SYS_ADMIN` 能力中分离出来。另见内核源文件 `Documentation/admin-guide/perf-security.rst`。
- `CAP_SETGID`：  
  - 对进程 GID 和补充 GID 列表进行任意操作；  
  - 通过 UNIX 域套接字传递套接字凭据时伪造 GID；  
  - 在用户命名空间中写入组 ID 映射（见 `[user_namespaces(7)]`）。
- `CAP_SETFCAP`（自 Linux 2.6.24 起）：在文件上设置任意能力。  
  自 Linux 5.12 起，在新用户命名空间中映射用户 ID 0 也需要此能力；详情见 `[user_namespaces(7)]`。
- `CAP_SETPCAP`：  
  如果支持文件能力（即自 Linux 2.6.24 起）：将调用线程边界集中的任意能力添加到其可继承集；从边界集中删除能力（通过 `[prctl(2)]` 的 `PR_CAPBSET_DROP`）；更改 `securebits` 标志。  
  
  如果不支持文件能力（即 Linux 2.6.24 之前）：在调用者的许可能力集中向任何其他进程授予或移除任意能力。（当内核配置为支持文件能力时，`CAP_SETPCAP` 的此属性不可用，因为对于此类内核，`CAP_SETPCAP` 具有完全不同的语义。）
- `CAP_SETUID`：  
  - 对进程 UID 进行任意操作（`[setuid(2)]`、`[setreuid(2)]`、`[setresuid(2)]`、`[setfsuid(2)]`）；  
  - 通过 UNIX 域套接字传递套接字凭据时伪造 UID；  
  - 在用户命名空间中写入用户 ID 映射（见 `[user_namespaces(7)]`）。
- `CAP_SYS_ADMIN`：  
  *注意*：此能力过载；见下文*给内核开发者的说明*。  
  - 执行一系列系统管理操作，包括：`[quotactl(2)]`、`[mount(2)]`、`[umount(2)]`、`[pivot_root(2)]`、`[swapon(2)]`、`[swapoff(2)]`、`[sethostname(2)]` 和 `[setdomainname(2)]`；  
  - 执行特权 `[syslog(2)]` 操作（自 Linux 2.6.37 起，应使用 `CAP_SYSLOG` 允许此类操作）；  
  - 执行 `VM86_REQUEST_IRQ` `vm86(2)` 命令；  
  - 访问由 `CAP_CHECKPOINT_RESTORE` 管理的相同检查点/恢复功能（但访问该功能首选后者这一更弱的能力）；  
  - 执行由 `CAP_BPF` 管理的相同 BPF 操作（但访问该功能首选后者这一更弱的能力）；  
  - 使用由 `CAP_PERFMON` 管理的相同性能监控机制（但访问该功能首选后者这一更弱的能力）；  
  - 对任意 System V IPC 对象执行 `IPC_SET` 和 `IPC_RMID` 操作；  
  - 覆盖 `RLIMIT_NPROC` 资源限制；  
  - 对 `trusted` 和 `security` 扩展属性执行操作（见 `[xattr(7)]`）；  
  - 使用 `[lookup_dcookie(2)]`；  
  - 使用 `[ioprio_set(2)]` 分配 `IOPRIO_CLASS_RT` 和（Linux 2.6.25 之前）`IOPRIO_CLASS_IDLE` I/O 调度类；  
  - 通过 UNIX 域套接字传递套接字凭据时伪造 PID；  
  - 在打开文件的系统调用（例如 `[accept(2)]`、`[execve(2)]`、`[open(2)]`、`[pipe(2)]`）中超过 `/proc/sys/fs/file-max`（系统范围的打开文件数限制）；  
  - 使用 `[clone(2)]` 和 `[unshare(2)]` 创建新命名空间的 `CLONE_*` 标志（但自 Linux 3.8 起，创建用户命名空间不需要任何能力）；  
  - 访问特权 `perf` 事件信息；  
  - 调用 `[setns(2)]`（需要*目标*命名空间中的 `CAP_SYS_ADMIN`）；  
  - 调用 `[fanotify_init(2)]`；  
  - 执行特权 `KEYCTL_CHOWN` 和 `KEYCTL_SETPERM` `[keyctl(2)]` 操作；  
  - 执行 `[madvise(2)]` 的 `MADV_HWPOISON` 操作；  
  - 使用 `TIOCSTI ioctl(2)` 向调用者控制终端以外的终端输入队列插入字符；  
  - 使用已过时的 `[nfsservctl(2)]` 系统调用；  
  - 使用已过时的 `[bdflush(2)]` 系统调用；  
  - 执行各种特权块设备 `[ioctl(2)]` 操作；  
  - 执行各种特权文件系统 `[ioctl(2)]` 操作；  
  - 对 `/dev/random` 设备执行特权 `[ioctl(2)]` 操作（见 `[random(4)]`）；  
  - 安装 `[seccomp(2)]` 过滤器而无需先设置 `no_new_privs` 线程属性；  
  - 修改设备控制组的允许/拒绝规则；  
  - 使用 `[ptrace(2)]` 的 `PTRACE_SECCOMP_GET_FILTER` 操作转储被跟踪者的 seccomp 过滤器；  
  - 使用 `[ptrace(2)]` 的 `PTRACE_SETOPTIONS` 操作暂停被跟踪者的 seccomp 保护（即 `PTRACE_O_SUSPEND_SECCOMP` 标志）；  
  - 对许多设备驱动程序执行管理操作；  
  - 通过写入 `/proc/pid/autogroup` 修改自动组 nice 值（见 `[sched(7)]`）。
- `CAP_SYS_BOOT`：使用 `[reboot(2)]` 和 `[kexec_load(2)]`。
- `CAP_SYS_CHROOT`：  
  - 使用 `[chroot(2)]`；  
  - 使用 `[setns(2)]` 更改挂载命名空间。
- `CAP_SYS_MODULE`：  
  - 加载和卸载内核模块（见 `[init_module(2)]` 和 `[delete_module(2)]`）；  
  - Linux 2.6.25 之前：从系统范围的能力边界集中删除能力。
- `CAP_SYS_NICE`：  
  - 降低进程 nice 值（`[nice(2)]`、`[setpriority(2)]`）并更改任意进程的 nice 值；  
  - 为调用进程设置实时调度策略，并为任意进程设置调度策略和优先级（`[sched_setscheduler(2)]`、`[sched_setparam(2)]`、`[sched_setattr(2)]`）；  
  - 为任意进程设置 CPU 亲和性（`[sched_setaffinity(2)]`）；  
  - 为任意进程设置 I/O 调度类和优先级（`[ioprio_set(2)]`）；  
  - 对任意进程应用 `[migrate_pages(2)]` 并允许进程迁移到任意节点；  
  - 对任意进程应用 `[move_pages(2)]`；  
  - 将 `MPOL_MF_MOVE_ALL` 标志与 `[mbind(2)]` 和 `[move_pages(2)]` 一起使用。
- `CAP_SYS_PACCT`：使用 `[acct(2)]`。
- `CAP_SYS_PTRACE`：  
  - 使用 `[ptrace(2)]` 跟踪任意进程；  
  - 通过 `/proc` 检查其他进程的敏感信息（例如读取 `/proc/pid/maps`、`/proc/pid/mem`，或读取符号链接 `/proc/pid/exe`、`/proc/pid/fd/*`）；  
  - 对任意进程应用 `[get_robust_list(2)]`；  
  - 使用 `[process_vm_readv(2)]` 和 `[process_vm_writev(2)]` 在任意进程的内存中传输数据；  
  - 使用 `[kcmp(2)]` 检查进程；  
  - 执行其他特权进程检查和调试操作。（参见 `ptrace_may_access()` 内核函数的用法。）
- `CAP_SYS_RAWIO`：  
  - 执行 I/O 端口操作（`[iopl(2)]` 和 `[ioperm(2)]`）；  
  - 访问 `/proc/kcore`；  
  - 使用 `FIBMAP ioctl(2)` 操作；  
  - 打开用于访问 x86 模型特定寄存器（MSR，见 `[msr(4)]`）的设备；  
  - 更新 `/proc/sys/vm/mmap_min_addr`；  
  - 在低于 `/proc/sys/vm/mmap_min_addr` 指定值的地址创建内存映射；  
  - 映射 `/proc/bus/pci` 中的文件；  
  - 打开 `/dev/mem` 和 `/dev/kmem`；  
  - 执行各种 SCSI 设备命令；  
  - 对 `[hpsa(4)]` 和 `[cciss(4)]` 设备执行某些操作；  
  - 对其他设备执行一系列设备特定操作。
- `CAP_SYS_RESOURCE`：  
  - 使用 ext2 文件系统上的保留空间；  
  - 进行控制 ext3 日志的 `[ioctl(2)]` 调用；  
  - 覆盖磁盘配额限制；  
  - 增加资源限制（见 `[setrlimit(2)]`）；  
  - 覆盖 `RLIMIT_NPROC` 资源限制；  
  - 在分配控制台时覆盖最大控制台数；  
  - 覆盖最大 keymap 数；  
  - 允许来自实时时钟的超过 64Hz 的中断；  
  - 将 System V 消息队列的 `msg_qbytes` 限制提高到 `/proc/sys/kernel/msgmnb` 中的限制之上（见 `[msgop(2)]` 和 `[msgctl(2)]`）；  
  - 允许在通过 UNIX 域套接字向另一进程传递文件描述符时绕过关于“在途”文件描述符数量的 `RLIMIT_NOFILE` 资源限制（见 `[unix(7)]`）；  
  - 使用 `F_SETPIPE_SZ` `[fcntl(2)]` 命令设置管道容量时覆盖 `/proc/sys/fs/pipe-size-max` 限制；  
  - 使用 `F_SETPIPE_SZ` 将管道容量提高到 `/proc/sys/fs/pipe-max-size` 指定的限制之上；  
  - 创建 POSIX 消息队列时覆盖 `/proc/sys/fs/mqueue/queues_max`、`/proc/sys/fs/mqueue/msg_max` 和 `/proc/sys/fs/mqueue/msgsize_max` 限制（见 `[mq_overview(7)]`）；  
  - 使用 `[prctl(2)]` 的 `PR_SET_MM` 操作；  
  - 将 `/proc/pid/oom_score_adj` 设置为低于具有 `CAP_SYS_RESOURCE` 的进程最后设置的值。
- `CAP_SYS_TIME`：设置系统时钟（`[settimeofday(2)]`、`[stime(2)]`、`[adjtimex(2)]`）；设置实时（硬件）时钟。
- `CAP_SYS_TTY_CONFIG`：使用 `[vhangup(2)]`；对虚拟终端使用各种特权 `[ioctl(2)]` 操作。
- `CAP_SYSLOG`（自 Linux 2.6.37 起）：  
  - 执行特权 `[syslog(2)]` 操作。哪些操作需要特权，见 `[syslog(2)]`。  
  - 当 `/proc/sys/kernel/kptr_restrict` 的值为 1 时，查看通过 `/proc` 和其他接口暴露的内核地址。（参见 `[proc(5)]` 中关于 `kptr_restrict` 的讨论。）
- `CAP_WAKE_ALARM`（自 Linux 3.0 起）：触发将唤醒系统的操作（设置 `CLOCK_REALTIME_ALARM` 和 `CLOCK_BOOTTIME_ALARM` 定时器）。

### 过去和当前的实现

能力的完整实现要求：

- 对于所有特权操作，内核必须检查线程的有效集中是否具有所需能力。
- 内核必须提供允许更改和检索线程能力集的系统调用。
- 文件系统必须支持将能力附加到可执行文件，以便进程在执行该文件时获得这些能力。

在 Linux 2.6.24 之前，只满足前两项要求；自 Linux 2.6.24 起，三项要求均已满足。

### 给内核开发者的说明

添加应由能力管理的新内核特性时，请考虑以下几点。

- 能力的目标是将超级用户的权力划分为若干部分，这样，如果一个具有一种或多种能力的程序被攻破，其对系统造成损害的能力将小于以 root 特权运行的同一程序。
- 你可以选择为新特性创建新能力，或将特性与现有能力之一关联。为了将能力集合保持在可管理的大小，后一种选择更可取，除非有令人信服的理由采用前一种选择。（还有一个技术限制：能力集的大小目前限制为 64 位。）
- 要确定哪个现有能力最适合与你的新特性关联，请回顾上面的能力列表，以找到最适合新特性的“归类槽”。一种方法是确定是否存在其他需要能力且将始终与新特性一起使用的特性。如果新特性在没有这些其他特性的情况下毫无用处，则应使用与其他特性相同的能力。
- 如果可能避免，*不要*选择 `CAP_SYS_ADMIN`！现有能力检查的很大一部分都与该能力关联（见上面的部分列表）。它可以被合理地称为“新的 root”，因为一方面它授予广泛的权力，另一方面其广泛范围意味着许多特权程序需要此能力。不要让问题变得更糟。唯一应与 `CAP_SYS_ADMIN` 关联的新特性是那些与该归类槽中现有用途*密切*匹配的特性。
- 如果你已确定确实有必要为你的特性创建新能力，不要将其制定或命名为“一次性”能力。例如，添加高度特定的 `CAP_SYS_PACCT` 可能是一个错误。相反，尝试将新能力识别并命名为更广泛的归类槽，以便其他相关的未来用例可能适合其中。

### 线程能力集

每个线程具有以下能力集，其中包含上述能力的零个或多个：

- *Permitted*（许可集）：  
  这是线程可以假定的有效能力的限制超集。它也是没有在其有效集中具有 `CAP_SETPCAP` 能力的线程可以添加到可继承集的能力的限制超集。  
  
  如果线程从许可集中删除某个能力，它永远无法重新获得该能力（除非它 `[execve(2)]` 一个设置用户 ID 为 root 的程序，或一个其关联文件能力授予该能力的程序）。
- *Inheritable*（可继承集）：  
  这是一组在 `[execve(2)]` 期间保留的能力。可继承能力在执行任何程序时保持可继承，并且当执行在文件可继承集中设置了对应位的程序时，可继承能力会被添加到许可集。  
  
  由于在非 root 用户下运行时，可继承能力通常不会在 `[execve(2)]` 期间保留，因此希望以提升的能力运行辅助程序的应用程序应考虑使用下面描述的环境能力。
- *Effective*（有效集）：  
  这是内核用于对线程执行权限检查的能力集。
- *Bounding*（边界集）（自 Linux 2.6.25 起为每线程）：  
  能力边界集是一种机制，可用于限制在 `[execve(2)]` 期间获得的能力。  
  
  自 Linux 2.6.25 起，这是每线程能力集。在较旧的内核中，能力边界集是系统上所有线程共享的系统范围属性。  
  
  更多详情见下文*能力边界集*。
- *Ambient*（环境集）（自 Linux 4.3 起）：  
  这是一组在非特权程序的 `[execve(2)]` 期间保留的能力。环境能力集遵循以下不变式：如果某个能力不同时在许可集和可继承集中，则它永远不能成为环境能力。  
  
  可以使用 `[prctl(2)]` 直接修改环境能力集。如果对应的许可能力或可继承能力被降低，环境能力会自动降低。  
  
  执行由于设置用户 ID 或设置组 ID 位而更改 UID 或 GID 的程序，或执行设置了任何文件能力的程序，将清除环境集。调用 `[execve(2)]` 时，环境能力会被添加到许可集并分配到有效集。如果环境能力导致进程的许可能力和有效能力在 `[execve(2)]` 期间增加，这不会触发 `[ld.so(8)]` 中描述的安全执行模式。

通过 `[fork(2)]` 创建的子进程继承其父进程能力集的副本。关于 `[execve(2)]` 如何影响能力的详情，见下文*execve() 期间能力的转换*。

使用 `[capset(2)]`，线程可以操作自己的能力集；见下文*以编程方式调整能力集*。

自 Linux 3.2 起，文件 `/proc/sys/kernel/cap_last_cap` 暴露正在运行的内核支持的最高能力的数值；这可用于确定能力集中可以设置的最高位。

### 文件能力

自 Linux 2.6.24 起，内核支持使用 `[setcap(8)]` 将能力集与可执行文件关联。文件能力集存储在名为 `security.capability` 的扩展属性中（见 `[setxattr(2)]` 和 `[xattr(7)]`）。写入此扩展属性需要 `CAP_SETFCAP` 能力。文件能力集与线程的能力集一起，决定线程在 `[execve(2)]` 之后的能力。

三个文件能力集是：

- *Permitted*（许可集，以前称为 *forced*）：  
  无论线程的可继承能力如何，这些能力都会自动许可给线程。
- *Inheritable*（可继承集，以前称为 *allowed*）：  
  此集与线程的可继承集进行 AND 运算，以确定在 `[execve(2)]` 之后线程许可集中启用哪些可继承能力。
- *Effective*（有效集）：  
  这不是一个集，而只是一个单独的位。如果设置了此位，则在 `[execve(2)]` 期间，线程的所有新许可能力也会在有效集中提升。如果未设置此位，则在 `[execve(2)]` 之后，新许可能力都不会进入新的有效集。  
  
  启用文件有效能力位意味着，任何导致线程在 `[execve(2)]` 期间获得对应许可能力的文件许可能力或可继承能力（见下文*execve() 期间能力的转换*），也将在线程的有效集中获得该能力。因此，在为文件分配能力（`[setcap(8)]`、`[cap_set_file(3)]`、`[cap_set_fd(3)]`）时，如果我们为任何能力指定有效标志为启用，则还必须为所有其他对应许可标志或可继承标志已启用的能力指定有效标志为启用。

### 文件能力扩展属性版本控制

为了允许扩展，内核支持一种在用于实现文件能力的 `security.capability` 扩展属性中编码版本号的方案。这些版本号是实现的内部版本号，不直接对用户空间应用程序可见。迄今为止，支持以下版本：

- `VFS_CAP_REVISION_1`：  
  这是最初的文件能力实现，支持文件能力的 32 位掩码。
- `VFS_CAP_REVISION_2`（自 Linux 2.6.25 起）：  
  此版本允许大小为 64 位的文件能力掩码，并且随着支持的能力数量增长到超过 32 个，这一版本是必要的。内核透明地继续支持执行具有 32 位版本 1 能力掩码的文件，但当向以前没有能力的文件添加能力，或修改现有文件的能力时，它会自动使用版本 2 方案（或如下所述的版本 3 方案）。
- `VFS_CAP_REVISION_3`（自 Linux 4.14 起）：  
  提供版本 3 文件能力以支持命名空间文件能力（如下所述）。  
  
  与版本 2 文件能力一样，版本 3 能力掩码的大小为 64 位。但此外，命名空间的 root 用户 ID 被编码在 `security.capability` 扩展属性中。（命名空间的 root 用户 ID 是该命名空间内的用户 ID 0 在初始用户命名空间中映射到的值。）  
  
  版本 3 文件能力设计为与版本 2 能力共存；也就是说，在现代 Linux 系统上，可能有些文件具有版本 2 能力，而其他文件具有版本 3 能力。

在 Linux 4.14 之前，可以附加到文件的唯一一种文件能力扩展属性是 `VFS_CAP_REVISION_2` 属性。自 Linux 4.14 起，附加到文件的 `security.capability` 扩展属性的版本取决于创建该属性时的环境。

从 Linux 4.14 开始，如果以下两个条件都成立，则会自动创建（或转换为）版本 3（`VFS_CAP_REVISION_3`）的 `security.capability` 扩展属性：

- 写入属性的线程位于非初始用户命名空间中。（更准确地说：该线程位于底层文件系统挂载来源的用户命名空间以外的用户命名空间中。）
- 该线程对文件 inode 具有 `CAP_SETFCAP` 能力，这意味着 (a) 该线程在其自己的用户命名空间中具有 `CAP_SETFCAP` 能力；并且 (b) 文件 inode 的 UID 和 GID 在写入者的用户命名空间中具有映射。

创建 `VFS_CAP_REVISION_3` 的 `security.capability` 扩展属性时，创建线程的用户命名空间的 root 用户 ID 会被保存到扩展属性中。

相比之下，从位于底层文件系统挂载所在命名空间（通常意味着初始用户命名空间）的特权（`CAP_SETFCAP`）线程创建或修改 `security.capability` 扩展属性，会自动创建版本 2（`VFS_CAP_REVISION_2`）属性。

请注意，版本 3 `security.capability` 扩展属性的创建是自动的。也就是说，当用户空间应用程序以版本 2 格式写入（`[setxattr(2)]`）`security.capability` 属性时，如果该属性是在上述环境中创建的，内核将自动创建版本 3 属性。相应地，当位于由该 root 用户 ID（或该用户命名空间的后代）创建的用户命名空间内的进程检索（`[getxattr(2)]`）版本 3 `security.capability` 属性时，返回的属性会（自动）简化为看起来像版本 2 属性（即返回值是版本 2 属性的大小，不包含 root 用户 ID）。这些自动转换意味着无需更改用户空间工具（例如 `setcap` 和 `getcap`），即可使用这些工具创建和检索版本 3 `security.capability` 属性。

请注意，文件可以关联版本 2 或版本 3 的 `security.capability` 扩展属性，但不能同时关联两者：创建或修改 `security.capability` 扩展属性将根据创建或修改该扩展属性时的环境自动修改版本。

### execve() 期间能力的转换

在 `[execve(2)]` 期间，内核使用以下算法计算进程的新能力：

```text
P'(ambient)     = (file is privileged) ? 0 : P(ambient)

P'(permitted)   = (P(inheritable) & F(inheritable)) |
                  (F(permitted) & P(bounding)) | P'(ambient)

P'(effective)   = F(effective) ? P'(permitted) : P'(ambient)

P'(inheritable) = P(inheritable)    [i.e., unchanged]

P'(bounding)    = P(bounding)       [i.e., unchanged]
```

其中：

```text
P()    denotes the value of a thread capability set before the
       execve(2)

P'()   denotes the value of a thread capability set after the
       execve(2)

F()    denotes a file capability set
```

注意与上述能力转换规则有关的以下细节：

- 环境能力集仅自 Linux 4.3 起存在。在确定 `[execve(2)]` 期间环境集的转换时，特权文件是指具有能力或设置了设置用户 ID 或设置组 ID 位的文件。
- 在 Linux 2.6.25 之前，边界集是系统上所有线程共享的系统范围属性。该系统范围值用于在 `[execve(2)]` 期间计算新的许可集，方式与上面针对 `P(bounding)` 所示相同。

*注意*：在上述能力转换期间，文件能力可能因与忽略设置用户 ID 和设置组 ID 位相同的原因而被忽略（视为空）；见 `[execve(2)]`。如果内核使用 `no_file_caps` 选项启动，文件能力同样会被忽略。

*注意*：根据上述规则，如果具有非零用户 ID 的进程执行 `[execve(2)]`，则其许可集和有效集中存在的任何能力都将被清除。关于用户 ID 为零的进程执行 `[execve(2)]` 时能力的处理，见下文*能力与 root 执行程序*。

### 对能力迟钝二进制程序的安全检查

能力迟钝（capability-dumb）二进制程序是指已标记为具有文件能力，但尚未转换为使用 `[libcap(3)]` API 来操作其能力的应用程序。（换句话说，这是一个传统的设置用户 ID 为 root 的程序，已改为使用文件能力，但其代码尚未修改以理解能力。）对于此类应用程序，文件上设置了有效能力位，以便在执行文件时，文件许可能力自动在进程有效集中启用。内核将设置了有效能力位的文件识别为能力迟钝程序，以用于此处描述的检查。

执行能力迟钝二进制程序时，内核会在执行上述能力转换之后，检查进程是否获得了文件许可集中指定的所有许可能力。（这种情况*不*发生的典型原因是能力边界集屏蔽了文件许可集中的某些能力。）如果进程未获得完整的文件许可能力集，则 `[execve(2)]` 会失败并返回错误 `EPERM`。这防止了在能力迟钝应用程序以低于其所需特权执行时可能产生的安全风险。请注意，根据定义，应用程序本身无法识别此问题，因为它不使用 `[libcap(3)]` API。

### 能力与 root 执行程序

为了镜像传统 UNIX 语义，当 UID 为 0（root）的进程执行程序以及执行设置用户 ID 为 root 的程序时，内核会对文件能力进行特殊处理。

在执行由二进制文件的设置用户 ID 模式位触发的任何进程有效 ID 更改之后——例如，由于执行了设置用户 ID 为 root 的程序而将有效用户 ID 切换为 0（root）——内核按如下方式计算文件能力集：

1. 如果进程的真实或有效用户 ID 为 0（root），则忽略文件可继承集和许可集；相反，它们在概念上被视为全 1（即所有能力启用）。（此行为有一个例外，见下文*具有文件能力的设置用户 ID 为 root 的程序*。）
2. 如果进程的有效用户 ID 为 0（root）或文件有效位实际上已启用，则文件有效位在概念上定义为 1（启用）。

然后，这些文件能力集的概念值按上述方式用于计算 `[execve(2)]` 期间进程能力的转换。

因此，当具有非零 UID 的进程 `[execve(2)]` 一个未附加能力的设置用户 ID 为 root 的程序，或者当真实和有效 UID 均为零的进程 `[execve(2)]` 一个程序时，进程新许可能力的计算简化为：

```text
P'(permitted)   = P(inheritable) | P(bounding)

P'(effective)   = P'(permitted)
```

因此，进程在其许可能力集和有效能力集中获得所有能力，但被能力边界集屏蔽的能力除外。（在计算 `P'(permitted)` 时，`P'(ambient)` 项可以简化掉，因为根据定义它是 `P(inheritable)` 的真子集。）

本小节中描述的对用户 ID 0（root）的特殊处理可以使用下面描述的 `securebits` 机制禁用。

### 具有文件能力的设置用户 ID 为 root 的程序

上述*能力与 root 执行程序*中描述的行为有一个例外。如果 (a) 正在执行的二进制文件附加了能力，且 (b) 进程的真实用户 ID *不是* 0（root），且 (c) 进程的有效用户 ID *是* 0（root），则文件能力位会被尊重（即它们不会在概念上被视为全 1）。这种情况通常出现在执行同时具有文件能力的设置用户 ID 为 root 的程序时。执行此类程序时，进程只获得该程序授予的能力（即不是所有能力，这与执行没有任何关联文件能力的设置用户 ID 为 root 的程序时不同）。

请注意，可以为程序文件分配空能力集，因此可以创建一个设置用户 ID 为 root 的程序，该程序将执行它的进程的有效和保存设置用户 ID 更改为 0，但不授予该进程任何能力。

### 能力边界集

能力边界集是一种安全机制，可用于限制在 `[execve(2)]` 期间可以获得的能力。边界集按以下方式使用：

- 在 `[execve(2)]` 期间，能力边界集与文件许可能力集进行 AND 运算，此运算结果分配给线程的许可能力集。因此，能力边界集对可执行文件可能授予的许可能力设置了限制。
- （自 Linux 2.6.25 起）能力边界集充当线程可以使用 `[capset(2)]` 添加到其可继承集的能力的限制超集。这意味着，如果某个能力不在边界集中，则线程无法将此能力添加到其可继承集，即使它在其许可能力中，因此当它 `[execve(2)]` 一个在其可继承集中具有该能力的文件时，也无法在其许可集中保留该能力。

请注意，边界集屏蔽文件许可能力，但不屏蔽可继承能力。如果线程在其可继承集中维护某个不在其边界集中的能力，则它仍然可以通过执行在其可继承集中具有该能力的文件来在其许可集中获得该能力。

取决于内核版本，能力边界集要么是系统范围属性，要么是每进程属性。

#### 自 Linux 2.6.25 起的能力边界集

从 Linux 2.6.25 起，*能力边界集*是每线程属性。（下面描述的系统范围能力边界集不再存在。）

边界集在 `[fork(2)]` 时从线程的父进程继承，并在 `[execve(2)]` 期间保留。

线程可以使用 `[prctl(2)]` 的 `PR_CAPBSET_DROP` 操作从其能力边界集中删除能力，前提是它具有 `CAP_SETPCAP` 能力。一旦某个能力从边界集中删除，就无法再恢复到该集。线程可以使用 `[prctl(2)]` 的 `PR_CAPBSET_READ` 操作确定某个能力是否在其边界集中。

仅当文件能力编译到内核中时，才支持从边界集中删除能力。在 Linux 2.6.33 之前，文件能力是通过 `CONFIG_SECURITY_FILE_CAPABILITIES` 选项配置的可选特性。自 Linux 2.6.33 起，该配置选项已被移除，文件能力始终是内核的一部分。当文件能力编译到内核中时，`init` 进程（所有进程的祖先）以完整边界集开始。如果文件能力未编译到内核中，则 `init` 以完整边界集减去 `CAP_SETPCAP` 开始，因为当没有文件能力时，此能力具有不同含义。

从边界集中删除能力不会将其从线程的可继承集中删除。但是，它会阻止将来将该能力添加回线程的可继承集。

#### Linux 2.6.25 之前的能力边界集

在 Linux 2.6.25 之前，能力边界集是影响系统上所有线程的系统范围属性。边界集可通过文件 `/proc/sys/kernel/cap-bound` 访问。（令人困惑的是，此位掩码参数在 `/proc/sys/kernel/cap-bound` 中表示为有符号十进制数。）

只有 `init` 进程可以在能力边界集中设置能力；除此之外，超级用户（更准确地说：具有 `CAP_SYS_MODULE` 能力的进程）只能从此集中清除能力。

在标准系统上，能力边界集始终屏蔽 `CAP_SETPCAP` 能力。要移除此限制（危险！），请修改 `include/linux/capability.h` 中 `CAP_INIT_EFF_SET` 的定义并重新构建内核。

系统范围能力边界集特性在 Linux 2.2.11 中添加。

### 用户 ID 更改对能力的影响

为了保留 0 和非零用户 ID 之间转换的传统语义，内核在线程的真实、有效、保存设置和文件系统用户 ID 更改时（使用 `[setuid(2)]`、`[setresuid(2)]` 或类似调用），会对线程的能力集进行以下更改：

- 如果一个或多个真实、有效或保存设置用户 ID 以前为 0，并且由于 UID 更改，所有这些 ID 都具有非零值，则从许可、有效和环境能力集中清除所有能力。
- 如果有效用户 ID 从 0 更改为非零，则从有效集中清除所有能力。
- 如果有效用户 ID 从非零更改为 0，则将许可集复制到有效集。
- 如果文件系统用户 ID 从 0 更改为非零（见 `[setfsuid(2)]`），则从有效集中清除以下能力：`CAP_CHOWN`、`CAP_DAC_OVERRIDE`、`CAP_DAC_READ_SEARCH`、`CAP_FOWNER`、`CAP_FSETID`、`CAP_LINUX_IMMUTABLE`（自 Linux 2.6.30 起）、`CAP_MAC_OVERRIDE` 和 `CAP_MKNOD`（自 Linux 2.6.30 起）。如果文件系统 UID 从非零更改为 0，则这些能力中任何在许可集中启用的能力都会在有效集中启用。

如果一个线程的一个或多个用户 ID 值为 0，并且它希望在其所有用户 ID 重置为非零值时防止其许可能力集被清除，则可以使用下面描述的 `SECBIT_KEEP_CAPS` securebits 标志。

### 以编程方式调整能力集

线程可以使用 `[capget(2)]` 和 `[capset(2)]` 系统调用检索和更改其许可、有效和可继承能力集。然而，为此目的，首选使用 `libcap` 包中提供的 `[cap_get_proc(3)]` 和 `[cap_set_proc(3)]`。以下规则管理线程能力集的更改：

- 如果调用者没有 `CAP_SETPCAP` 能力，则可继承集必须是现有可继承集和许可集的组合的子集。
- （自 Linux 2.6.25 起）新的可继承集必须是现有可继承集和能力边界集的组合的子集。
- 新的许可集必须是现有许可集的子集（即，不可能获得线程当前没有的许可能力）。
- 新的有效集必须是新许可集的子集。

### securebits 标志：建立仅能力环境

从 Linux 2.6.26 开始，并且在启用了文件能力的内核中，Linux 实现了一组每线程 `securebits` 标志，可用于禁用对 UID 0（*root*）能力的特殊处理。这些标志如下：

- `SECBIT_KEEP_CAPS`：  
  设置此标志允许具有一个或多个 0 UID 的线程在将其所有 UID 切换为非零值时，在其许可集中保留能力。如果未设置此标志，则此类 UID 切换会导致线程失去所有许可能力。此标志在 `[execve(2)]` 时始终被清除。  
  
  请注意，即使设置了 `SECBIT_KEEP_CAPS` 标志，当线程将其有效 UID 切换为非零值时，其有效能力也会被清除。但是，如果线程设置了此标志且其有效 UID 已经非零，并且线程随后将所有其他 UID 切换为非零值，则有效能力不会被清除。  
  
  如果设置了 `SECBIT_NO_SETUID_FIXUP` 标志，则忽略 `SECBIT_KEEP_CAPS` 标志的设置。（后一个标志提供前一个标志效果的超集。）  
  
  此标志提供与较早的 `[prctl(2)]` `PR_SET_KEEPCAPS` 操作相同的功能。
- `SECBIT_NO_SETUID_FIXUP`：设置此标志会阻止内核在线程的有效和文件系统 UID 在零和非零值之间切换时调整进程的许可、有效和环境能力集。见上文*用户 ID 更改对能力的影响*。
- `SECBIT_NOROOT`：如果设置了此位，则当执行设置用户 ID 为 root 的程序时，或当有效或真实 UID 为 0 的进程调用 `[execve(2)]` 时，内核不授予能力。（见上文*能力与 root 执行程序*。）
- `SECBIT_NO_CAP_AMBIENT_RAISE`：设置此标志禁止通过 `[prctl(2)]` 的 `PR_CAP_AMBIENT_RAISE` 操作提升环境能力。

上述每个“基础”标志都有一个配套的“锁定”标志。设置任何“锁定”标志都是不可逆的，并具有阻止进一步更改相应“基础”标志的效果。锁定标志为：`SECBIT_KEEP_CAPS_LOCKED`、`SECBIT_NO_SETUID_FIXUP_LOCKED`、`SECBIT_NOROOT_LOCKED` 和 `SECBIT_NO_CAP_AMBIENT_RAISE_LOCKED`。

可以使用 `[prctl(2)]` 的 `PR_SET_SECUREBITS` 和 `PR_GET_SECUREBITS` 操作修改和检索 `securebits` 标志。修改这些标志需要 `CAP_SETPCAP` 能力。请注意，`SECBIT_*` 常量仅在包含 `<linux/securebits.h>` 头文件后可用。

`securebits` 标志由子进程继承。在 `[execve(2)]` 期间，所有标志都会保留，但 `SECBIT_KEEP_CAPS` 除外，它始终被清除。

应用程序可以使用以下调用将自身及其所有后代锁定在这样一种环境中：获得能力的唯一方式是执行具有关联文件能力的程序：

```c
prctl(PR_SET_SECUREBITS,
        /* SECBIT_KEEP_CAPS off */
        SECBIT_KEEP_CAPS_LOCKED |
        SECBIT_NO_SETUID_FIXUP |
        SECBIT_NO_SETUID_FIXUP_LOCKED |
        SECBIT_NOROOT |
        SECBIT_NOROOT_LOCKED);
        /* Setting/locking SECBIT_NO_CAP_AMBIENT_RAISE
           is not required */
```

### 每用户命名空间的“设置用户 ID 为 root”程序

如果设置用户 ID 程序的 UID 与创建用户命名空间的 UID 匹配，则当该命名空间或任何后代用户命名空间内的任何进程执行该程序时，它将在进程的许可集和有效集中授予能力。

`[execve(2)]` 期间进程能力转换的规则与上文*execve() 期间能力的转换*和*能力与 root 执行程序*中描述的完全相同，不同之处在于后一小节中的“root”是用户命名空间创建者的 UID。

### 命名空间文件能力

传统（即版本 2）文件能力仅将一组能力掩码与二进制可执行文件关联。当进程执行具有此类能力的二进制文件时，它会按照上文*execve() 期间能力的转换*中描述的规则获得关联能力（在其用户命名空间内）。

由于版本 2 文件能力无论执行进程位于哪个用户命名空间中都会向其授予能力，因此只有特权进程才被允许将能力与文件关联。这里，“特权”是指在其挂载文件系统的用户命名空间（通常是初始用户命名空间）中具有 `CAP_SETFCAP` 能力的进程。此限制使文件能力在某些用例中毫无用处。例如，在用户命名空间容器中，可能希望创建一个二进制文件，该文件仅向该容器内执行的进程授予能力，而不向容器外执行的进程授予能力。

Linux 4.14 添加了所谓的命名空间文件能力以支持此类用例。命名空间文件能力记录为版本 3（即 `VFS_CAP_REVISION_3`）的 `security.capability` 扩展属性。此类属性会在上文*文件能力扩展属性版本控制*中描述的环境中自动创建。创建版本 3 `security.capability` 扩展属性时，内核不仅记录扩展属性中的能力掩码，还记录命名空间 root 用户 ID。

与具有 `VFS_CAP_REVISION_2` 文件能力的二进制文件一样，具有 `VFS_CAP_REVISION_3` 文件能力的二进制文件会在 `execve()` 期间向进程授予能力。但是，只有当二进制文件由位于其 UID 0 映射到扩展属性中保存的 root 用户 ID 的用户命名空间中的进程执行时，或由位于此类命名空间后代的进程执行时，才会授予能力。

### 与用户命名空间的交互

关于能力与用户命名空间交互的更多信息，见 `[user_namespaces(7)]`。

## 标准

没有标准管理能力，但 Linux 能力实现基于已撤回的 POSIX.1e 草案标准 ⟨https://archive.org/details/posix_1003.1e-990310⟩。

## 注释

尝试使用 `[strace(1)]` 跟踪具有能力的二进制文件（或设置用户 ID 为 root 的二进制文件）时，你可能会发现 `-u <username>` 选项很有用。类似这样：

```console
$ sudo strace -o trace.log -u ceci ./myprivprog
```

从 Linux 2.5.27 到 Linux 2.6.26，能力是可选的內核组件，可以通过 `CONFIG_SECURITY_CAPABILITIES` 内核配置选项启用/禁用。

`/proc/pid/task/TID/status` 文件可用于查看线程的能力集。`/proc/pid/status` 文件显示进程主线程的能力集。在 Linux 3.8 之前，不存在的能力在这些集中显示为已启用（1）。自 Linux 3.8 起，所有不存在的能力（高于 `CAP_LAST_CAP`）显示为已禁用（0）。

`libcap` 包提供了一套用于设置和获取能力的例程，它比 `[capset(2)]` 和 `[capget(2)]` 提供的接口更舒适，且更不容易更改。此包还提供 `[setcap(8)]` 和 `[getcap(8)]` 程序。它可在 ⟨https://git.kernel.org/pub/scm/libs/libcap/libcap.git/refs/⟩ 找到。

在 Linux 2.6.24 之前，以及在 Linux 2.6.24 到 Linux 2.6.32 期间如果未启用文件能力，具有 `CAP_SETPCAP` 能力的线程可以操作除自身以外线程的能力。然而，这只是理论上的可能，因为在以下两种情况下，任何线程都从未拥有 `CAP_SETPCAP`：

- 在 2.6.25 之前的实现中，系统范围能力边界集 `/proc/sys/kernel/cap-bound` 始终屏蔽 `CAP_SETPCAP` 能力，如果不修改内核源代码并重新构建内核，则无法更改这一点。
- 如果文件能力被禁用（即内核 `CONFIG_SECURITY_FILE_CAPABILITIES` 选项被禁用），则 `init` 启动时其每进程边界集中已移除 `CAP_SETPCAP` 能力，并且该边界集由系统上创建的所有其他进程继承。

## 另请参见

`[capsh(1)]`、`[setpriv(1)]`、`[prctl(2)]`、`[setfsuid(2)]`、`[cap_clear(3)]`、`[cap_copy_ext(3)]`、`[cap_from_text(3)]`、`[cap_get_file(3)]`、`[cap_get_proc(3)]`、`[cap_init(3)]`、`[capgetp(3)]`、`[capsetp(3)]`、`[libcap(3)]`、`[proc(5)]`、`[credentials(7)]`、`[pthreads(7)]`、`[user_namespaces(7)]`、`[captest(8)]`、`[filecap(8)]`、`[getcap(8)]`、`[getpcaps(8)]`、`[netcap(8)]`、`[pscap(8)]`、`[setcap(8)]`

Linux 内核源代码树中的 `include/linux/capability.h`

## 版权说明

本页面是 *man-pages*（Linux 内核和 C 库用户空间接口文档）项目的一部分。有关该项目的信息可在 <https://www.kernel.org/doc/man-pages/> 找到。如果您对本手册页有错误报告，请参见 <https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/CONTRIBUTING>。本页面取自 2026-09-09 从 <https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/> 获取的 man-pages-6.19.tar.gz 压缩包。如果您发现此 HTML 版本页面存在渲染问题，或者您认为有更好或更新的页面来源，或者您对本版权说明（*不*属于原始手册页的一部分）中的信息有更正或改进，请发送邮件至 `man-pages@man7.org`。

Linux man-pages 6.19 2026-02-08 `Capabilities`(7)