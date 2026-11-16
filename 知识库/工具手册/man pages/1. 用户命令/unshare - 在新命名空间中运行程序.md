https://www.man7.org/linux/man-pages/man1/unshare.1.html

# `unshare` - 在新命名空间中运行程序

## 概要

```sh
unshare [options] [program [arguments]]
```

## 描述

`unshare` 命令创建新的命名空间（如下文所述命令行选项所指定），然后执行指定的 `program`。如果未给出 `program`，则运行 `${SHELL}`。如果未设置 `SHELL`，则使用用户 `passwd(5)` 条目中的 shell。如果那里也未定义 shell，则使用 `/bin/sh` 作为后备。

默认情况下，新命名空间仅在拥有成员进程期间持续存在。即使没有成员进程，也可以通过将 `/proc/pid/ns/type` 文件 bind mount 到文件系统路径来使新命名空间持久化。以这种方式持久化的命名空间随后可以在 `program` 终止后通过 `nsenter(1)` 进入（PID 命名空间除外，它需要永久运行的 init 进程）。一旦不再需要持久命名空间，可以通过使用 `umount(8)` 移除 bind mount 来取消持久化。更多细节参见 **示例** 一节。

自 util-linux 版本 2.36 起，`unshare` 使用 `/proc/[pid]/ns/pid_for_children` 和 `/proc/[pid]/ns/time_for_children` 文件来实现持久 PID 和 TIME 命名空间。此更改需要 Linux 内核 4.17 或更高版本。

可以使用 `unshare` 创建以下类型的命名空间：

- **mount 命名空间**  
    挂载和卸载文件系统不会影响系统的其余部分，除非文件系统被显式标记为共享（使用 `mount --make-shared`；关于 `shared` 标志，参见 `/proc/self/mountinfo` 或 `findmnt -o+PROPAGATION`）。更多细节参见 `mount_namespaces(7)`。

    自 util-linux 版本 2.27 起，`unshare` 在新 mount 命名空间中自动将传播设置为 `private`，以确保新命名空间真正不共享。可以通过选项 `--propagation unchanged` 禁用此功能。注意 `private` 是内核默认值。

- **UTS 命名空间**  
    设置主机名或域名不会影响系统的其余部分。更多细节参见 `uts_namespaces(7)`。

- **IPC 命名空间**  
    进程将拥有独立的 POSIX 消息队列以及 System V 消息队列、信号量集和共享内存段命名空间。更多细节参见 `ipc_namespaces(7)`。

- **network 命名空间**  
    进程将拥有独立的 IPv4 和 IPv6 协议栈、IP 路由表、防火墙规则、`/proc/net` 和 `/sys/class/net` 目录树、套接字等。更多细节参见 `network_namespaces(7)`。

- **PID 命名空间**  
    子进程将拥有与父进程不同的 PID 到进程映射集合。更多细节参见 `pid_namespaces(7)`。

- **cgroup 命名空间**  
    进程将拥有 `/proc/self/cgroup` 的虚拟化视图，新的 cgroup 挂载将以命名空间 cgroup 根为根。更多细节参见 `cgroup_namespaces(7)`。

- **user 命名空间**  
    进程将拥有不同的 UID、GID 和能力集合。更多细节参见 `user_namespaces(7)`。

- **time 命名空间**  
    进程可以拥有 `CLOCK_MONOTONIC` 和/或 `CLOCK_BOOTTIME` 的不同视图，可以使用 `/proc/self/timens_offsets` 进行更改。更多细节参见 `time_namespaces(7)`。

## 选项

- `-i`, `--ipc[=file]`  
    创建新的 IPC 命名空间。如果指定了 `file`，则通过在 `file` 处创建 bind mount 使命名空间持久化。

- `-m`, `--mount[=file]`  
    创建新的 mount 命名空间。如果指定了 `file`，则通过在 `file` 处创建 bind mount 使命名空间持久化。注意 `file` 必须位于传播类型不是 `shared` 的挂载上（否则会产生错误）。当不确定当前设置时，使用命令 `findmnt -o+PROPAGATION`。另请参见下面的示例。

- `-n`, `--net[=file]`  
    创建新的 network 命名空间。如果指定了 `file`，则通过在 `file` 处创建 bind mount 使命名空间持久化。

- `-p`, `--pid[=file]`  
    创建新的 PID 命名空间。如果指定了 `file`，则通过在 `file` 处创建 bind mount 使命名空间持久化。（如果未同时指定 `--fork` 选项，则创建持久 PID 命名空间将失败。）

    另请参见 `--fork` 和 `--mount-proc` 选项。

- `-u`, `--uts[=file]`  
    创建新的 UTS 命名空间。如果指定了 `file`，则通过在 `file` 处创建 bind mount 使命名空间持久化。

- `-U`, `--user[=file]`  
    创建新的 user 命名空间。如果指定了 `file`，则通过在 `file` 处创建 bind mount 使命名空间持久化。

- `-C`, `--cgroup[=file]`  
    创建新的 cgroup 命名空间。如果指定了 `file`，则通过在 `file` 处创建 bind mount 使命名空间持久化。

- `-T`, `--time[=file]`  
    创建新的 time 命名空间。如果指定了 `file`，则通过在 `file` 处创建 bind mount 使命名空间持久化。可以使用 `--monotonic` 和 `--boottime` 选项指定 time 命名空间中的相应偏移。

- `-f`, `--fork`  
    将指定的 `program` 作为 `unshare` 的子进程 fork，而不是直接运行它。这在创建新 PID 命名空间时很有用。注意当 `unshare` 等待子进程时，它会忽略 `SIGINT` 和 `SIGTERM`，并且不向子进程转发任何信号。有必要向子进程发送信号。

- `--forward-signals`  
    将父 `unshare` 进程收到的 `SIGTERM` 和 `SIGINT` 信号转发给子进程。未指定此选项时，`unshare` 在等待子进程退出时忽略这些信号（自 util-linux 2.36 起的默认行为）。这允许父进程在子进程处理信号时保持存活。

    当父 `unshare` 进程将收到 `SIGTERM` 或 `SIGINT` 信号（例如在系统重新启动期间或来自进程管理器）时，如果你希望通知子进程优雅关闭请求以便其执行清理操作，此选项很有用。如果你的子进程有信号处理函数（如 shell trap 处理函数），启用此选项允许它们执行。

    此选项隐含 `--fork`。

- `--keep-caps`  
    当给出 `--user` 选项时，确保在 user 命名空间中授予的能力保留在子进程中。

- `--kill-child[=signame]`  
    当 `unshare` 终止时，将 `signame` 发送给 fork 出的子进程。与 `--pid` 结合使用，可以轻松可靠地杀死 `unshare` 下的整个进程树。如果未给出，`signame` 默认为 `SIGKILL`。此选项隐含 `--fork`。

- `--mount-proc[=mountpoint]`  
    在运行程序之前，将 proc 文件系统挂载到 `mountpoint`（默认为 `/proc`）。这在创建新 PID 命名空间时很有用。它还隐含创建新的 mount 命名空间，因为否则 `/proc` 挂载会扰乱系统上的现有程序。新的 proc 文件系统显式挂载为私有（使用 `MS_PRIVATE|MS_REC`）。

- `--mount-binfmt[=mountpoint]`  
    在运行程序之前，将 binfmt_misc 文件系统挂载到 `mountpoint`（默认为 `/proc/sys/fs/binfmt_misc`）。它还隐含创建新的 mount 命名空间，因为否则 binfmt_misc 挂载会扰乱系统上的现有程序。新的 binfmt_misc 文件系统显式挂载为私有（使用 `MS_PRIVATE|MS_REC`）。

- `--map-user uid|name`  
    仅在当前有效用户 ID 已映射到 `uid` 之后运行程序。如果多次指定此选项，则最后一次出现优先。此选项隐含 `--user`。

- `--map-users inneruid:outeruid:count|auto|subids|all`  
    仅在从 `outeruid` 开始、大小为 `count` 的用户 ID 块已映射到从 `inneruid` 开始的用户 ID 块之后运行程序。如果 `unshare` 以非特权方式运行，则使用 `newuidmap(1)` 创建此映射。

    由 `--map-user` 指定的映射（包括便利选项 `--map-root-user` 和 `--map-current-user`，它们展开为 `--map-user`）优先：它首先应用，如果此处请求的块与它重叠（在 `outeruid` 或 `inneruid` 一侧），则从此块中移除一个 "hole"，使两个映射不冲突。该 hole 丢弃块中最高的用户 ID，因此它映射的 ID 比 `count` 少一个，并且块围绕 `--map-user` 所声明的 ID 拆分，而不是包含它。结果，你期望此块映射的用户 ID（例如基于 `id -u` 的范围的第一个 ID）可能改为解析为 `--map-user` 设置的 ID，而块中最高的 `outeruid` 可能未被映射。

    多次使用 `--map-users` 以映射多个用户 ID 块。特殊值 `auto` 将有效用户从 `/etc/subuid` 拥有的第一个用户 ID 块映射到从用户 ID 0 开始的块。特殊值 `subids` 将同一块进行恒等映射。特殊值 `all` 将为父命名空间中可用的每个用户 ID 创建直通映射。此选项隐含 `--user`。

    在 util-linux 版本 2.39 之前，此选项期望一个逗号分隔的参数，形式为 `outeruid,inneruid,count`，但该格式现已弃用，以与 `/proc/[pid]/uid_map` 和 `X-mount.idmap` 挂载选项中使用的顺序保持一致。

- `--map-group gid|name`  
    仅在当前有效组 ID 已映射到 `gid` 之后运行程序。如果多次指定此选项，则最后一次出现优先。此选项隐含 `--setgroups=deny` 和 `--user`。

- `--map-groups innergid:outergid:count|auto|subids|all`  
    仅在从 `outergid` 开始、大小为 `count` 的组 ID 块已映射到从 `innergid` 开始的组 ID 块之后运行程序。如果 `unshare` 以非特权方式运行，则使用 `newgidmap(1)` 创建此映射。

    由 `--map-group` 指定的映射（包括便利选项 `--map-root-user` 和 `--map-current-user`，它们展开为 `--map-group`）优先：它首先应用，如果此处请求的块与它重叠（在 `outergid` 或 `innergid` 一侧），则从此块中移除一个 "hole"，使两个映射不冲突。该 hole 丢弃块中最高的组 ID，因此它映射的 ID 比 `count` 少一个，并且块围绕 `--map-group` 所声明的 ID 拆分，而不是包含它。结果，你期望此块映射的组 ID（例如基于 `id -g` 的范围的第一个 ID）可能改为解析为 `--map-group` 设置的 ID，而块中最高的 `outergid` 可能未被映射。

    多次使用 `--map-groups` 以映射多个组 ID 块。特殊值 `auto` 将有效用户从 `/etc/subgid` 拥有的第一个用户 ID 块映射到从组 ID 0 开始的块。特殊值 `subids` 将同一块进行恒等映射。特殊值 `all` 将为父命名空间中可用的每个组 ID 创建直通映射。此选项隐含 `--user`。

    在 util-linux 版本 2.39 之前，此选项期望一个逗号分隔的参数，形式为 `outergid,innergid,count`，但该格式现已弃用，以与 `/proc/[pid]/gid_map` 和 `X-mount.idmap` 挂载选项中使用的顺序保持一致。

- `--map-auto`  
    将有效用户从 `/etc/subuid` 拥有的第一个用户 ID 块映射到从用户 ID 0 开始的块。以相同方式，还将有效组从 `/etc/subgid` 拥有的第一个组 ID 块映射到从组 ID 0 开始的块。此选项旨在处理第一块从属用户和组 ID 可以映射整个用户和组 ID 空间的常见情况。此选项等效于指定 `--map-users=auto` 和 `--map-groups=auto`。

- `--map-subids`  
    将有效用户从 `/etc/subuid` 拥有的第一个用户 ID 块进行恒等映射。以相同方式，还将有效组从 `/etc/subgid` 拥有的第一个组 ID 块进行恒等映射。此选项等效于指定 `--map-users=subids` 和 `--map-groups=subids`。

- `-r`, `--map-root-user`  
    仅在当前有效用户和组 ID 已映射到新创建的 user 命名空间中的超级用户 UID 和 GID 之后运行程序。这使得即使以非特权方式运行，也可以方便地获得管理新创建命名空间各个方面所需的能力（例如在网络命名空间中配置接口或在 mount 命名空间中挂载文件系统）。作为便利功能，它不支持更复杂的用例，例如映射多个 UID 和 GID 范围。此选项隐含 `--setgroups=deny` 和 `--user`。此选项等效于 `--map-user=0 --map-group=0`。

- `-c`, `--map-current-user`  
    仅在当前有效用户和组 ID 已映射到新创建的 user 命名空间中的相同 UID 和 GID 之后运行程序。此选项隐含 `--setgroups=deny` 和 `--user`。此选项等效于 `--map-user=$(id -ru) --map-group=$(id -rg)`。

- `--owner uid:gid`  
    创建 user 命名空间时设置所有者用户和组。这些决定父命名空间中哪个用户在子命名空间中拥有 CAP_SYS_ADMIN，并且可以 `setns(2)` 进入其中。此选项允许特权用户代表非特权用户创建命名空间，使用其特权映射 ID 和/或将命名空间 bind mount 到文件系统。它隐含 `--user`。

- `--propagation private|shared|slave|unchanged`  
    递归设置新 mount 命名空间中的挂载传播标志。默认将传播设置为 `private`。可以使用参数 `unchanged` 禁用此功能。当未请求 mount 命名空间（`--mount`）时，该选项被静默忽略。

- `--setgroups allow|deny`  
    允许或拒绝 user 命名空间中的 `setgroups(2)` 系统调用。

    要能够调用 `setgroups(2)`，调用进程必须至少具有 `CAP_SETGID`。但自 Linux 3.19 起，进一步限制适用：内核仅在设置了 GID 映射（`/proc/pid/gid_map`）后才授予调用 `setgroups(2)` 的权限。当启用 `setgroups(2)` 时（即 `allow`，默认值），GID 映射可由 root 写入；当永久禁用 `setgroups(2)` 时（使用 `deny`），GID 映射变为可由非特权进程写入。

- `-R`, `--root dir`  
    以根目录设置为 `dir` 运行命令。

- `-w`, `--wd dir`  
    将工作目录更改为 `dir`。

- `-S`, `--setuid uid`  
    设置将在进入的命名空间中使用的用户 ID。

- `-G`, `--setgid gid`  
    设置将在进入的命名空间中使用的组 ID，并丢弃补充组。

- `-l`, `--load-interp string`  
    在命名空间中加载 binfmt_misc 定义（隐含 `--mount-binfmt`）。`string` 参数为 `:name:type:offset:magic:mask:interpreter:flags`。关于新二进制类型注册的更多细节，参见 <https://www.kernel.org/doc/Documentation/admin-guide/binfmt-misc.rst>。要在使用 `--root` 参数时管理 flags 中的 F 标志，binfmt_misc 被挂载两次：一次在 chroot 之前，从调用者文件系统加载解释器；一次在之后，使其可从 chroot 用户空间使用。

- `--monotonic offset`  
    设置将在进入的 time 命名空间中使用的 `CLOCK_MONOTONIC` 偏移。此选项要求使用 `--time` 取消共享 time 命名空间。

- `--boottime offset`  
    设置将在进入的 time 命名空间中使用的 `CLOCK_BOOTTIME` 偏移。此选项要求使用 `--time` 取消共享 time 命名空间。

- `--clear-env`  
    不将调用进程的环境变量传递给取消共享的进程。

- `--whitelist-env list`  
    清除所有环境变量，但逗号分隔的 `list` 中指定的变量除外。

- `-h`, `--help`  
    显示帮助文本并退出。

- `-V`, `--version`  
    显示版本并退出。

## 环境

- `SHELL`  
    未指定 `program` 时要运行的默认 shell。如果未设置 `SHELL`，则使用用户 `passwd(5)` 条目中的 shell。如果那里也未定义 shell，则使用 `/bin/sh` 作为后备。

## 注意事项

在 user 命名空间中作为 root 挂载的 proc 和 sysfs 文件系统必须受到限制，以便较低特权的用户无法获取较高特权用户已设为不可用的敏感文件的更多访问权限。简而言之，proc 和 sysfs 的规则尽可能接近 bind mount。

## 示例

以下命令创建一个 PID 命名空间，使用 `--fork` 确保执行的命令在子进程中执行（作为命名空间中的第一个进程，其 PID 为 1）。`--mount-proc` 选项确保同时创建新的 mount 命名空间，并挂载新的 `proc(5)` 文件系统，其中包含与新 PID 命名空间对应的信息。当 `readlink(1)` 命令终止时，新命名空间自动拆除。

```console
# unshare --fork --pid --mount-proc readlink /proc/self
1
```

作为非特权用户，创建一个新的 user 命名空间，其中用户的凭据映射到命名空间内的 root ID：

```console
$ id -u; id -g
1000
1000
$ unshare --user --map-root-user \
        sh -c 'whoami; cat /proc/self/uid_map /proc/self/gid_map'
root
         0       1000          1
         0       1000          1
```

作为非特权用户，创建一个 user 命名空间，其中前 65536 个 ID 全部映射，并且用户的凭据映射到命名空间内的 root ID。该映射由 `subuid(5)` 和 `subgid(5)` 中分配的从属 ID 确定。通过创建一个用户 ID 为 1、组 ID 为 1 的文件来演示此映射。为简洁起见，仅显示用户 ID 映射：

```console
$ id -u
1000
$ cat /etc/subuid
1000:100000:65536
$ unshare --user --map-auto --map-root-user
# id -u
0
# cat /proc/self/uid_map
         0       1000          1
         1     100000      65535
# touch file; chown 1:1 file
# ls -ln --time-style=+ file
-rw-r--r-- 1 1 1 0  file
# exit
$ ls -ln --time-style=+ file
-rw-r--r-- 1 100000 100000 0  file
```

以下命令中的第一个创建一个新的持久 UTS 命名空间，并修改该命名空间中可见的主机名。然后使用 `nsenter(1)` 进入该命名空间以显示修改后的主机名；此步骤表明，即使 `unshare` 命令终止后命名空间没有成员进程，UTS 命名空间仍然存在。然后通过移除 bind mount 销毁该命名空间。

```console
# touch /root/uts-ns
# unshare --uts=/root/uts-ns hostname FOO
# nsenter --uts=/root/uts-ns hostname
FOO
# umount /root/uts-ns
```

以下命令建立一个由 bind mount `/root/namespaces/mnt` 引用的持久 mount 命名空间。为确保该 bind mount 的创建成功，父目录（`/root/namespaces`）被设为传播类型不是 `shared` 的 bind mount。

```console
# mount --bind /root/namespaces /root/namespaces
# mount --make-private /root/namespaces
# touch /root/namespaces/mnt
# unshare --mount=/root/namespaces/mnt
```

以下命令演示在创建 PID 命名空间时使用 `--kill-child` 选项，以确保当 `unshare` 被杀死时，PID 命名空间内的所有进程都被杀死。

```console
# set +m                # 不打印作业状态消息

# unshare --pid --fork --mount-proc --kill-child -- \
       bash --norc -c '(sleep 555 &) && (ps a &) && sleep 999' &
[1] 53456
#     PID TTY      STAT   TIME COMMAND
      1 pts/3    S+     0:00 sleep 999
      3 pts/3    S+     0:00 sleep 555
      5 pts/3    R+     0:00 ps a

# ps h -o 'comm' $!     # 显示后台作业是 unshare(1)
unshare
# kill $!               # 杀死 unshare(1)
# pidof sleep
```

`pidof(1)` 命令不打印任何输出，因为 `sleep` 进程已被杀死。更准确地说，当命名空间中 PID 为 1 的 `sleep` 进程（即命名空间的 init 进程）被杀死时，这导致命名空间中的所有其他进程被杀死。相反，未使用 `--kill-child` 选项的类似命令序列表明，当 `unshare` 终止时，PID 命名空间中的进程不会被杀死：

```console
# unshare --pid --fork --mount-proc -- \
       bash --norc -c '(sleep 555 &) && (ps a &) && sleep 999' &
[1] 53479
#     PID TTY      STAT   TIME COMMAND
      1 pts/3    S+     0:00 sleep 999
      3 pts/3    S+     0:00 sleep 555
      5 pts/3    R+     0:00 ps a

# kill $!
# pidof sleep
53482 53480
```

以下示例演示创建一个 time 命名空间，其中 boottime 时钟设置为几年前的时间点：

```console
# uptime -p             # 显示初始 time 命名空间中的运行时间
up 21 hours, 30 minutes
# unshare --time --fork --boottime 300000000 uptime -p
up 9 years, 28 weeks, 1 day, 2 hours, 50 minutes
```

以下示例执行 chroot 进入目录 `/chroot/powerpc/jessie`，并安装解释器 `/bin/qemu-ppc-static` 以执行 powerpc 二进制文件。

```console
$  unshare --map-root-user --fork --pid --load-interp=":qemu-ppc:M::\\x7fELF\\x01\\x02\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x14:\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\x00\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xfe\\xff\\xff:/bin/qemu-ppc-static:OCF" --root=/chroot/powerpc/jessie /bin/bash -l
```

load-interp 参数可以按以下方式理解：

- `qemu-ppc`  
    是在 `/proc/sys/fs/binfmt_misc` 下创建的新文件的名称，用于注册解释器

- `M`  
    为给定类型的魔数定义解释器

- `\\x7fELF\\x01\\x02\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x1`  
    是用于识别要解释的文件的魔数（在此情况下为 PPC32 的 ELF 头）

- `\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\x00\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xfe\\xff\\xff`  
    要应用于魔数的掩码

- `/bin/qemu-ppc-static`  
    要与文件一起使用的解释器

- `OCF`  
    文件由内核使用文件自身的凭据和安全令牌打开，并在我们注册时立即加载。

## 作者

Mikhail Gusarov <dottedmag@dottedmag.net>，Karel Zak <kzak@redhat.com>

## 另请参见

`newuidmap(1)`、`newgidmap(1)`、`nsenter(1)`、`lsns(8)`、`clone(2)`、`unshare(2)`、`namespaces(7)`、`mount(8)`

## 报告缺陷

关于缺陷报告，请使用问题跟踪器 <https://github.com/util-linux/util-linux/issues>。

## 可用性

`unshare` 命令是 util-linux 包的一部分，可从 Linux 内核存档 <https://www.kernel.org/pub/linux/utils/util-linux/> 下载。本页是 `util-linux`（一个 Linux 实用程序的随机集合）项目的一部分。项目信息可在 ⟨<https://www.kernel.org/pub/linux/utils/util-linux/>⟩ 找到。如果对本手册页有缺陷报告，请发送至 `util-linux@vger.kernel.org`。本页获取自项目上游 Git 仓库 ⟨git://git.kernel.org/pub/scm/utils/util-linux/util-linux.git⟩，日期为 2026-08-04。（当时在仓库中找到的最近提交日期为 2026-08-03。）如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
util-linux 2.43.devel-1062-f... 2026-08-03                     UNSHARE(1)
```