# systemd, init - systemd 系统与服务管理器

## 概要

```sh
/usr/lib/systemd/systemd [OPTIONS...]

init [OPTIONS...]
```

## 描述

systemd 是 Linux 操作系统的系统与服务管理器。当作为启动时的第一个进程（即 PID 1）运行时，它充当 init 系统，负责启动并维护用户空间服务。对于已登录用户，会启动单独的实例来启动他们的服务。

`systemd` 通常不由用户直接调用，而是作为 `/sbin/init` 符号链接安装，并在早期启动期间启动。用户管理器实例通过 [`user@.service(5)`] 服务自动启动。

当作为系统实例运行时，systemd 解释配置文件 `system.conf` 以及 `system.conf.d` 目录中的文件；当作为用户实例运行时，systemd 解释配置文件 `user.conf` 以及 `user.conf.d` 目录中的文件。更多信息参见 [`systemd-system.conf(5)`]。

`systemd` 包含各种需要在启动过程中执行的任务的原生实现。例如，它设置主机名或配置回环网络设备。它还设置并挂载各种 API 文件系统，如 `/sys/`、`/proc/` 和 `/dev/`。

如果系统时钟看起来设置不正确，`systemd` 还会在早期启动期间重置它。参见下文“系统时钟纪元”一节。

请注意，systemd 提供的接口部分（但并非全部）受 **接口可移植性与稳定性承诺**[1] 覆盖。

`systemd` 的 D-Bus API 在 [`org.freedesktop.systemd1(5)`] 和 [`org.freedesktop.LogControl1(5)`] 中描述。

在容器或 initrd 环境中调用 systemd 的系统应分别实现 **容器接口**[2] 或 **initrd 接口**[3] 规范。

## 单元

systemd 在称为“单元”的各种实体之间提供依赖系统，共有 11 种不同类型。单元封装了与系统启动和维护相关的各种对象。大多数单元在单元配置文件中配置，其语法和基本选项集在 [`systemd.unit(5)`] 中描述；不过有些单元是从其他配置文件自动创建、从系统状态动态创建或在运行时以编程方式创建的。单元可以处于多种状态，如下表所述。注意，各种单元类型可能有许多附加子状态，这些子状态映射到此处描述的通用单元状态。

**表 1. 单元 ACTIVE 状态**

- `active`  
  已启动、已绑定、已插入……取决于单元类型。

- `inactive`  
  已停止、已解除绑定、已拔出……取决于单元类型。

- `failed`  
  类似于 `inactive`，但单元以某种方式失败（进程退出时返回错误码、崩溃、操作超时，或重启次数过多）。

- `activating`  
  正在从 `inactive` 变为 `active`。

- `deactivating`  
  正在从 `active` 变为 `inactive`。

- `maintenance`  
  单元处于 `inactive` 状态，并且正在执行维护操作。

- `reloading`  
  单元处于 `active` 状态，并且正在重新加载其配置。

- `refreshing`  
  单元处于 `active` 状态，并且正在其命名空间中激活新的挂载。

以下单元类型可用：

1. Service 单元，用于启动和控制守护进程及其组成的进程。详情参见 [`systemd.service(5)`]。

2. Socket 单元，封装系统中的本地 IPC 或网络套接字，适用于基于套接字的激活。套接字单元的详情参见 [`systemd.socket(5)`]，基于套接字的激活及其他激活形式的详情参见 [`daemon(7)`]。

3. Target 单元，用于对单元进行分组，或在启动期间提供众所周知的同步点，参见 [`systemd.target(5)`]。

4. Device 单元，在 systemd 中暴露内核设备，可用于实现基于设备的激活。详情参见 [`systemd.device(5)`]。

5. Mount 单元，控制文件系统中的挂载点，详情参见 [`systemd.mount(5)`]。

6. Automount 单元，提供自动挂载能力，用于按需挂载文件系统以及并行启动。参见 [`systemd.automount(5)`]。

7. Timer 单元，用于基于定时器触发其他单元的激活。详情参见 [`systemd.timer(5)`]。

8. Swap 单元与 mount 单元非常相似，封装操作系统的内存交换分区或文件。它们在 [`systemd.swap(5)`] 中描述。

9. Path 单元，可用于在文件系统对象发生变化或被修改时激活其他服务。参见 [`systemd.path(5)`]。

10. Slice 单元，可用于将管理系统进程的单元（如 service 和 scope 单元）分组到层次树中，以便进行资源管理。参见 [`systemd.slice(5)`]。

11. Scope 单元类似于 service 单元，但管理外部进程而不是启动它们。参见 [`systemd.scope(5)`]。

单元以其配置文件名命名。有些单元具有特殊语义。详细列表见 [`systemd.special(7)`]。

systemd 了解各种依赖关系，包括正负需求依赖（即 `Requires=` 和 `Conflicts=`）以及顺序依赖（`After=` 和 `Before=`）。注意：顺序依赖和需求依赖是正交的。如果两个单元之间仅存在需求依赖（例如 `foo.service` 需要 `bar.service`），但没有顺序依赖（例如 `foo.service` 在 `bar.service` 之后），并且两者都被请求启动，则它们将并行启动。常见的做法是在两个单元之间同时放置需求依赖和顺序依赖。另请注意，大多数依赖关系由 systemd 隐式创建和维护。在大多数情况下，应该不需要手动声明额外依赖，但可以这样做。

应用程序和单元（通过依赖关系）可以请求单元的状态更改。在 systemd 中，这些请求被封装为“作业”并维护在作业队列中。作业可能成功或失败，其执行根据为其调度的单元的顺序依赖关系进行排序。

启动时，systemd 激活 target 单元 `default.target`，其作业是通过依赖关系拉入启动时服务和其他启动时单元来激活它们。通常，单元名只是 `graphical.target`（用于进入 UI 的完整功能启动）或 `multi-user.target`（用于嵌入式或服务器环境中的受限仅控制台启动，或类似场景；是 `graphical.target` 的子集）的别名（符号链接）。不过，管理员可以自行决定将其配置为任何其他 target 单元的别名。关于这些 target 单元的详情参见 [`systemd.special(7)`]。

首次启动时，`systemd` 将根据预设策略启用或禁用单元。参见 [`systemd.preset(5)`] 以及 [`machine-id(5)`] 中的“首次启动语义”。

systemd 只在内存中保留最小数量的已加载单元。具体而言，只有满足以下至少一个条件的单元才会保留在内存中：

1. 处于 active、activating、deactivating 或 failed 状态（即除“inactive”之外的任何单元状态）

2. 有为其排队的作业

3. 是至少一个已加载到内存中的其他单元的依赖项

4. 仍有某种形式的资源被分配（例如，一个 service 单元处于 inactive 状态，但仍有忽略终止请求的进程残留）

5. 已通过 D-Bus 调用以编程方式固定到内存中

systemd 会在请求对单元进行操作时，自动且隐式地从磁盘加载尚未加载的单元。因此，在许多方面，单元是否已加载对客户端是不可见的。使用 `systemctl list-units --all` 全面列出当前已加载的所有单元。任何不满足上述条件的单元都会被立即卸载。注意，当单元从内存中卸载时，其记账数据也会被清除。不过，这些数据通常不会丢失，因为每当单元关闭时，都会生成一条 journal 日志记录，声明所消耗的资源。

systemd 生成的进程被放置在以它们所属单元命名的独立 Linux 控制组中，位于私有的 systemd 层次结构中。（关于控制组（简称“cgroups”）的更多信息，参见 **Control Groups v2**[4]。）systemd 利用这一点有效地跟踪进程。控制组信息由内核维护，可通过文件系统层次结构（位于 `/sys/fs/cgroup/` 下）或 [`systemd-cgls(1)`] 或 [`ps(1)`] 等工具访问（`ps xawf -eo pid,user,cgroup,args` 对于列出所有进程及其所属 systemd 单元特别有用）。

systemd 与各种既有的 Unix 功能兼容，例如 `/etc/fstab` 或 utmp 数据库。

systemd 具有最小事务系统：如果请求某个单元启动或关闭，它会将该单元及其所有依赖项添加到临时事务中。然后，它会验证事务是否一致（即所有单元的顺序是否无循环）。如果不一致，systemd 会尝试修复，并从事务中移除非必要作业以消除循环。此外，systemd 会尝试抑制事务中会停止正在运行服务的非必要作业。最后，它会检查事务中的作业是否与已排队的作业矛盾，并可选择此时中止事务。如果一切顺利且事务一致且影响最小化，则将其与所有已未完成的作业合并并添加到运行队列。实际上，这意味着在执行请求的操作之前，systemd 会验证其是否合理，尽可能修复，只有在确实无法工作时才失败。

注意，事务是独立于单元运行时状态生成的；因此，例如，如果对已启动的单元请求启动作业，它仍会生成事务并唤醒任何非活动依赖项（并根据定义的关系传播其他作业）。这是因为排队的作业在执行时会与目标单元的状态进行比较，当两者都满足时标记为成功并完成。然而，此作业还会因定义的关系拉入其他依赖项，从而导致（在我们的示例中）任何非活动单元的启动作业也被排队。

单元可以在启动和系统管理器重新加载时动态生成，例如基于其他配置文件或内核命令行上传递的参数。详情参见 [`systemd.generator(7)`]。

## 目录

### 系统单元目录

systemd 系统管理器从各种目录读取单元配置。希望安装单元文件的软件包应将其放置在 `pkg-config systemd --variable=systemdsystemunitdir` 返回的目录中。检查的其他目录是 `/usr/local/lib/systemd/system` 和 `/usr/lib/systemd/system`。用户配置始终优先。`pkg-config systemd --variable=systemdsystemconfdir` 返回系统配置目录的路径。软件包应仅使用 [`systemctl(1)`] 工具的 `enable` 和 `disable` 命令来更改这些目录的内容。完整目录列表在 [`systemd.unit(5)`] 中提供。

### 用户单元目录

类似的规则适用于用户单元目录。不过，这里遵循 **XDG Base Directory 规范**[5] 来查找单元。应用程序应将其单元文件放置在 `pkg-config systemd --variable=systemduserunitdir` 返回的目录中。全局配置在 `pkg-config systemd --variable=systemduserconfdir` 报告的目录中进行。[`systemctl(1)`] 工具的 `enable` 和 `disable` 命令可以处理全局（即对所有用户）和私有（对一个用户）的单元启用/禁用。完整目录列表在 [`systemd.unit(5)`] 中提供。

## 信号

该服务监听各种 UNIX 进程信号，可用于异步请求各种操作。信号处理在启动期间很早就启用，早于调用任何其他进程。然而，打算通过此机制请求这些操作的监督容器管理器或类似组件必须考虑到，此功能在最早的初始化阶段不可用。一旦信号处理程序启用，就会发出携带 `X_SYSTEMD_SIGNALS_LEVEL=2` 字段的 `sd_notify()` 通知消息，见下文。这可用于正确安排这些信号的提交。

**SIGTERM**

收到此信号后，systemd 系统管理器会序列化其状态，重新执行自身，并再次反序列化保存的状态。这大致相当于 `systemctl daemon-reexec`。

systemd 用户管理器在收到此信号时将启动 `exit.target` 单元。这大致相当于 `systemctl --user start exit.target --job-mode=replace-irreversibly`。

**SIGINT**

收到此信号后，systemd 系统管理器将启动 `ctrl-alt-del.target` 单元。这大致相当于 `systemctl start ctrl-alt-del.target --job-mode=replace-irreversibly`。如果此信号在 2 秒内收到超过 7 次，则会立即触发重启。注意，在控制台上按 Ctrl+Alt+Del 会触发此信号。因此，如果重启挂起，在 2 秒内按 Ctrl+Alt+Del 超过 7 次是触发立即重启的相对安全的方法。

systemd 用户管理器以与 `SIGTERM` 相同的方式处理此信号。

**SIGWINCH**

收到此信号时，systemd 系统管理器将启动 `kbrequest.target` 单元。这大致相当于 `systemctl start kbrequest.target`。

此信号被 systemd 用户管理器忽略。

**SIGPWR**

收到此信号时，systemd 管理器将启动 `sigpwr.target` 单元。这大致相当于 `systemctl start sigpwr.target`。

**SIGUSR1**

收到此信号时，systemd 管理器将尝试重新连接到 D-Bus 总线。

**SIGUSR2**

收到此信号时，systemd 管理器将以人类可读形式记录其完整状态。记录的数据与 `systemd-analyze dump` 打印的数据相同。

**SIGHUP**

重新加载完整的守护进程配置。这大致相当于 `systemctl daemon-reload`。

**SIGRTMIN+0**

进入默认模式，启动 `default.target` 单元。这大致相当于 `systemctl isolate default.target`。

**SIGRTMIN+1**

进入救援模式，启动 `rescue.target` 单元。这大致相当于 `systemctl isolate rescue.target`。

**SIGRTMIN+2**

进入紧急模式，启动 `emergency.service` 单元。这大致相当于 `systemctl isolate emergency.service`。

**SIGRTMIN+3**

停机，启动 `halt.target` 单元。这大致相当于 `systemctl start halt.target --job-mode=replace-irreversibly`。

**SIGRTMIN+4**

关机，启动 `poweroff.target` 单元。这大致相当于 `systemctl start poweroff.target --job-mode=replace-irreversibly`。

**SIGRTMIN+5**

重启机器，启动 `reboot.target` 单元。这大致相当于 `systemctl start reboot.target --job-mode=replace-irreversibly`。

**SIGRTMIN+6**

通过 kexec 重启机器，启动 `kexec.target` 单元。这大致相当于 `systemctl start kexec.target --job-mode=replace-irreversibly`。

**SIGRTMIN+7**

重启用户空间，启动 `soft-reboot.target` 单元。这大致相当于 `systemctl start soft-reboot.target --job-mode=replace-irreversibly`。

在版本 254 中添加。

**SIGRTMIN+13**

立即停机。

**SIGRTMIN+14**

立即关机。

**SIGRTMIN+15**

立即重启机器。

**SIGRTMIN+16**

通过 kexec 立即重启机器。

**SIGRTMIN+17**

立即重启用户空间。

在版本 254 中添加。

**SIGRTMIN+20**

启用控制台上的状态消息显示，由内核命令行上的 `systemd.show_status=1` 控制。

你可能想使用 `SetShowStatus()` 而不是 `SIGRTMIN+20`，以防止竞态条件。参见 [`org.freedesktop.systemd1(5)`]。

**SIGRTMIN+21**

禁用控制台上的状态消息显示，由内核命令行上的 `systemd.show_status=0` 控制。

你可能想使用 `SetShowStatus()` 而不是 `SIGRTMIN+21`，以防止竞态条件。参见 [`org.freedesktop.systemd1(5)`]。

**SIGRTMIN+22**

将服务管理器的日志级别设置为“debug”，方式等同于内核命令行上的 `systemd.log_level=debug`。

**SIGRTMIN+23**

将日志级别恢复为配置值。配置值按优先级顺序派生自：内核命令行上 `systemd.log-level=` 指定的值，或配置文件中 `LogLevel=` 指定的值，或内置默认值“info”。

在版本 239 中添加。

**SIGRTMIN+24**

立即退出管理器（仅适用于 `--user` 实例）。

在版本 195 中添加。

**SIGRTMIN+25**

收到此信号后，systemd 管理器将重新执行自身。这大致相当于 `systemctl daemon-reexec`，但会异步执行。

systemd 系统管理器以与 `SIGTERM` 相同的方式处理此信号。

在版本 250 中添加。

**SIGRTMIN+26**

将日志目标恢复为配置值。配置值按优先级顺序派生自：内核命令行上 `systemd.log-target=` 指定的值，或配置文件中 `LogTarget=` 指定的值，或内置默认值。

在版本 239 中添加。

**SIGRTMIN+27**、**SIGRTMIN+28**

在 `SIGRTMIN+27` 上将日志目标设置为“console”（或在 `SIGRTMIN+28` 上设置为“kmsg”），方式等同于内核命令行上的 `systemd.log_target=console`（或在 `SIGRTMIN+28` 上为 `systemd.log_target=kmsg`）。

在版本 239 中添加。

## 环境

系统管理器的环境块最初由内核设置。（具体而言，内核命令行上的“key=value”赋值会转换为 PID 1 的环境变量）。对于用户管理器，系统管理器按照 [`systemd.exec(5)`] 中“生成进程中的环境变量”一节所述设置环境。系统管理器中的 `DefaultEnvironment=` 设置适用于所有服务，包括 `user@.service`。可以通过 `user@.service` 的 `Environment=` 和 `EnvironmentFile=` 设置（参见 [`systemd.exec(5)`]）配置额外条目（如同任何其他服务）。此外，可以通过 [`systemd-system.conf(5)`] 和 [`systemd-user.conf(5)`] 中的 `ManagerEnvironment=` 设置设置额外的环境变量。

`systemd` 理解的部分变量：

`$SYSTEMD_LOG_LEVEL`  
发出消息的最大日志级别（日志级别更高即更不重要的消息将被抑制）。接受逗号分隔的值列表。值可以是（按重要性递减顺序）`emerg`、`alert`、`crit`、`err`、`warning`、`notice`、`info`、`debug` 之一，或 0...7 范围内的整数。更多信息参见 [`syslog(3)`]。每个值可选地以 `console`、`syslog`、`kmsg` 或 `journal` 之一为前缀，后跟冒号，以设置该特定日志目标的最大日志级别（例如 `SYSTEMD_LOG_LEVEL=debug,console:info` 指定以 debug 级别记录日志，但记录到控制台时除外，应为 info 级别）。注意，全局最大日志级别优先于任何按目标的最大日志级别。

可以用 `--log-level=` 覆盖。

`$SYSTEMD_LOG_COLOR`  
一个布尔值。如果为 true，写入 tty 的消息将根据优先级着色。

可以用 `--log-color=` 覆盖。

`$SYSTEMD_LOG_TIME`  
一个布尔值。如果为 true，控制台日志消息将带有时间戳前缀。

可以用 `--log-time=` 覆盖。

在版本 246 中添加。

`$SYSTEMD_LOG_LOCATION`  
一个布尔值。如果为 true，消息将带有消息来源源代码中的文件名和行号前缀。

可以用 `--log-location=` 覆盖。

`$SYSTEMD_LOG_TID`  
一个布尔值。如果为 true，消息将带有当前数字线程 ID（TID）前缀。

在版本 247 中添加。

`$SYSTEMD_LOG_TARGET`  
日志消息的目标。`console`（记录到附加的 tty）、`console-prefixed`（记录到附加的 tty，但带有编码日志级别和“facility”的前缀，参见 [`syslog(3)`]）、`kmsg`（记录到内核环形日志缓冲区）、`journal`（记录到 journal）、`journal-or-kmsg`（如果可用则记录到 journal，否则记录到 kmsg）、`auto`（自动确定适当的日志目标，默认值）、`null`（禁用日志输出）之一。

可以用 `--log-target=` 覆盖。

`$SYSTEMD_LOG_RATELIMIT_KMSG`  
是否对 kmsg 进行速率限制。接受布尔值。默认为“true”。如果禁用，systemd 将不会对写入 kmsg 的消息进行速率限制。

在版本 254 中添加。

`$XDG_CONFIG_HOME`、`$XDG_CONFIG_DIRS`、`$XDG_DATA_HOME`、`$XDG_DATA_DIRS`  
systemd 用户管理器根据 **XDG Base Directory 规范**[5] 使用这些变量来查找其配置。

`$SYSTEMD_UNIT_PATH`、`$SYSTEMD_GENERATOR_PATH`、`$SYSTEMD_ENVIRONMENT_GENERATOR_PATH`  
控制 systemd 在哪里查找单元文件和生成器。

这些变量可以包含路径列表，用冒号（`:`）分隔。设置时，如果列表以空组件结尾（`...:`），则此列表会前置到通常的路径集。否则，指定的列表将替换通常的路径集。

`$SYSTEMD_PAGER`、`$PAGER`  
未给出 `--no-pager` 时使用的分页器。如果设置了 `$SYSTEMD_PAGER`，则使用它；否则使用 `$PAGER`。如果既未设置 `$SYSTEMD_PAGER` 也未设置 `$PAGER`，则依次尝试一组众所周知的分页器实现，包括 [`less(1)`] 和 [`more(1)`]，直到找到一个。如果未发现分页器实现，则不调用分页器。将这些环境变量设置为空字符串或值“cat”等同于传递 `--no-pager`。

注意：如果未设置 `$SYSTEMD_PAGERSECURE`，则 `$SYSTEMD_PAGER` 和 `$PAGER` 只能用于禁用分页器（使用“cat”或“”），否则会被忽略。

`$SYSTEMD_LESS`  
覆盖传递给 `less` 的选项（默认“FRSXMK”）。

用户可能特别想更改两个选项：

`K`  
此选项指示分页器在按下 Ctrl+C 时立即退出。要允许 `less` 自行处理 Ctrl+C 以切换回分页器命令提示符，请取消设置此选项。

如果 `$SYSTEMD_LESS` 的值不包含“K”，并且调用的分页器是 `less`，则 Ctrl+C 将被可执行文件忽略，需要由分页器处理。

`X`  
此选项指示分页器不向终端发送 termcap 初始化和反初始化字符串。默认设置为允许命令输出在分页器退出后仍保持可见。不过，这会阻止某些分页器功能工作，特别是分页输出无法用鼠标滚动。

注意，设置常规的 `$LESS` 环境变量对 systemd 工具调用的 `less` 没有影响。

更多讨论参见 [`less(1)`]。

`$SYSTEMD_LESSCHARSET`  
覆盖传递给 `less` 的字符集（如果调用终端被确定为 UTF-8 兼容，默认为“utf-8”）。

注意，设置常规的 `$LESSCHARSET` 环境变量对 systemd 工具调用的 `less` 没有影响。

`$SYSTEMD_PAGERSECURE`  
像 [`less(1)`] 这样的常见分页器命令，除了“分页”（即滚动浏览输出）之外，还支持打开或写入其他文件以及运行任意 shell 命令。当以提升的权限调用命令时，例如在 [`sudo(8)`] 或 `pkexec(1)` 下，分页器会成为安全边界。必须注意仅使用功能严格受限的程序作为分页器，并且不允许打开或创建新文件或启动子进程等非预期的交互功能。可以如下所述启用分页器的“安全模式”，*如果分页器支持的话*（大多数分页器的编写方式并未考虑这一点）。建议在允许不受信任的用户以提升的权限执行命令时，显式启用“安全模式”或使用 `--no-pager` 或 `PAGER=cat` 完全禁用分页器。

此选项接受布尔参数。设置为 true 时，启用分页器的“安全模式”。在“安全模式”下，调用分页器时将设置 `LESSSECURE=1`，指示分页器禁用打开或创建新文件或启动新子进程的命令。目前只有 [`less(1)`] 已知理解此变量并实现“安全模式”。

设置为 false 时，不对分页器施加任何限制。设置 `SYSTEMD_PAGERSECURE=0` 或未将其从继承环境中移除可能允许用户调用任意命令。

当未设置 `$SYSTEMD_PAGERSECURE` 时，systemd 工具会尝试自动判断是否应启用“安全模式”以及分页器是否支持它。如果有效 UID 与登录会话的所有者不同（参见 [`geteuid(2)`] 和 [`sd_pid_get_owner_uid(3)`]），或在 [`sudo(8)`] 或类似工具下运行（设置了 `$SUDO_UID`[6]），则启用“安全模式”。在这些情况下，将设置 `SYSTEMD_PAGERSECURE=1`，并且完全不使用已知未实现“安全模式”的分页器。注意，此自动检测仅涵盖最常见的提权机制，旨在提供便利。建议显式设置 `$SYSTEMD_PAGERSECURE` 或禁用分页器。

注意，如果要尊重 `$SYSTEMD_PAGER` 或 `$PAGER` 变量（而非仅用于禁用分页器），还必须设置 `$SYSTEMD_PAGERSECURE`。

`$SYSTEMD_COLORS`  
接受布尔参数或特殊值。默认情况下（未设置），`systemd` 及相关工具将尽可能在其输出中使用颜色。如果 `$COLORTERM` 设置为“truecolor”或“24bit”，则启用 24 位颜色，否则启用 256 色，除非 `$NO_COLOR` 或 `$TERM` 指示颜色已禁用。

`true`  
与未设置相同，但忽略 `$NO_COLOR`。

`false`  
输出将变为单色。

“16”、“256”、“24bit”  
始终分别使用基础 16 种 ANSI 颜色、256 色或 24 位颜色。

“auto-16”、“auto-256”、“auto-24bit”  
使用给定数量的颜色，受 `$TERM` 以及控制台连接对象的约束。

`$SYSTEMD_URLIFY`  
值必须为布尔值。控制是否在输出中为支持此功能的终端模拟器生成可点击链接。可指定此项以覆盖 `systemd` 基于 `$TERM` 和其他条件所做的决定。

`$LISTEN_PID`、`$LISTEN_PIDFDID`、`$LISTEN_FDS`、`$LISTEN_FDNAMES`  
由 systemd 在基于套接字的激活期间为受监督进程设置。更多信息参见 [`sd_listen_fds(3)`]。

`$NOTIFY_SOCKET`  
由服务管理器为其服务设置，用于状态和就绪通知。服务管理器也使用它来通知堆栈上层的监督容器管理器或服务管理器其自身进度。更多信息参见 [`sd_notify(3)`] 及相关章节。

有关 systemd 及其各组件理解的其他环境变量，参见 **已知环境变量**[7]。

## 内核命令行

当作为系统实例运行时，systemd 解析下面列出的若干选项。这些选项可以作为内核命令行参数指定，具体从哪些来源解析取决于 systemd 执行的环境。如果在 Linux 容器内运行，这些选项从传递给 systemd 本身的命令行参数解析，与上面“选项”一节中列出的任何命令行选项并列。如果在 Linux 容器外运行，则这些参数从 `/proc/cmdline` 解析。

理解以下变量：

`systemd.unit=`、`rd.systemd.unit=`  
覆盖启动时要激活的单元。默认为 `default.target`。这可用于临时启动到不同的启动单元，例如 `rescue.target` 或 `emergency.service`。关于这些单元的详情参见 [`systemd.special(7)`]。带“rd.”前缀的选项仅在 initrd 中生效，不带前缀的选项仅在主系统中生效。

`systemd.dump_core`  
接受布尔参数，或不带参数指定时启用该选项。如果启用，systemd 管理器（PID 1）在崩溃时转储核心。否则不创建核心转储。默认启用。

在版本 233 中添加。

`systemd.crash_chvt`  
接受正整数或布尔参数。也可以不带参数指定，效果与正布尔值相同。如果指定正整数（范围 1–63），系统管理器（PID 1）将在崩溃时激活指定的虚拟终端。默认禁用，意味着不尝试此类切换。如果设置为启用，则使用内核消息写入的虚拟终端。

在版本 233 中添加。

`systemd.crash_shell`  
接受布尔参数，或不带参数指定时启用该选项。如果启用，系统管理器（PID 1）在崩溃时生成一个 shell。否则不生成 shell。出于安全原因默认禁用，因为该 shell 不受密码认证保护。

在版本 233 中添加。

`systemd.crash_action=`  
接受“freeze”、“reboot”或“poweroff”之一。默认为“freeze”。如果设置为“freeze”，系统管理器（PID 1）崩溃时系统将无限期挂起。如果设置为“reboot”，系统管理器（PID 1）崩溃时将在 10 秒延迟后自动重启机器。如果设置为“poweroff”，系统管理器（PID 1）崩溃时将立即关机。如果与 `systemd.crash_shell` 组合使用，则在 shell 退出后执行配置的崩溃动作。

在版本 256 中添加。

`systemd.confirm_spawn`  
接受布尔参数或应发出确认消息的虚拟控制台路径。也可以不带参数指定，效果与正布尔值相同。如果启用，系统管理器（PID 1）在使用 `/dev/console` 生成进程时请求确认。如果提供了路径或控制台名称（如“ttyS0”），则使用该路径指向或该名称描述的虚拟控制台。默认禁用。

在版本 233 中添加。

`systemd.service_watchdogs=`  
接受布尔参数。如果禁用，系统管理器（PID 1）将忽略所有服务运行时看门狗（`WatchdogSec=`）和紧急动作（例如 `OnFailure=` 或 `StartLimitAction=`）；参见 [`systemd.service(5)`]。默认启用，即看门狗和失败动作正常处理。硬件看门狗不受此选项影响。

在版本 237 中添加。

`systemd.show_status`  
接受布尔参数或常量 `error` 和 `auto`。也可以不带参数指定，效果与正布尔值相同。如果启用，systemd 管理器（PID 1）在启动期间在控制台上显示简洁的服务状态更新。使用 `error` 时，仅显示关于失败的消息，但启动其他方面保持安静。`auto` 的行为类似 `false`，直到启动出现显著延迟。默认启用，除非将 `quiet` 作为内核命令行选项传递，此时默认为 `error`。如果指定，将覆盖系统管理器配置文件选项 `ShowStatus=`，参见 [`systemd-system.conf(5)`]。

在版本 233 中添加。

`systemd.status_unit_format=`  
接受 `name`、`description` 或 `combined` 作为值。如果为 `name`，系统管理器将在状态消息中使用单元名称。如果为 `combined`，系统管理器将在状态消息中使用单元名称和描述。指定时，覆盖系统管理器配置文件选项 `StatusUnitFormat=`，参见 [`systemd-system.conf(5)`]。

在版本 243 中添加。

`systemd.log_color`、`systemd.log_level=`、`systemd.log_location`、`systemd.log_target=`、`systemd.log_time`、`systemd.log_tid`、`systemd.log_ratelimit_kmsg`  
控制日志输出，效果与上面描述的 `$SYSTEMD_LOG_COLOR`、`$SYSTEMD_LOG_LEVEL`、`$SYSTEMD_LOG_LOCATION`、`$SYSTEMD_LOG_TARGET`、`$SYSTEMD_LOG_TIME`、`$SYSTEMD_LOG_TID` 和 `$SYSTEMD_LOG_RATELIMIT_KMSG` 环境变量相同。`systemd.log_color`、`systemd.log_location`、`systemd.log_time`、`systemd.log_tid` 和 `systemd.log_ratelimit_kmsg` 可以不带参数指定，效果与正布尔值相同。

`systemd.default_standard_output=`、`systemd.default_standard_error=`  
控制服务和套接字的默认标准输出和错误输出。即控制 `StandardOutput=` 和 `StandardError=` 的默认值（详情参见 [`systemd.exec(5)`]）。接受 `inherit`、`null`、`tty`、`journal`、`journal+console`、`kmsg`、`kmsg+console` 之一。如果省略参数，`systemd.default-standard-output=` 默认为 `journal`，`systemd.default-standard-error=` 默认为 `inherit`。

`systemd.setenv=`  
接受形式为 `VARIABLE=VALUE` 的字符串参数。可用于设置要添加到 fork 子进程的默认环境变量。可多次使用以设置多个变量。

`systemd.machine_id=`  
接受 32 个字符的十六进制值，用于设置 machine-id。主要用于网络启动，其中每次启动都希望使用相同的 machine-id。

在版本 229 中添加。

`systemd.set_credential=`、`systemd.set_credential_binary=`  
设置系统凭据，然后可以使用 `ImportCredential=` 或 `LoadCredential=` 设置将其传播到系统服务，详情参见 [`systemd.exec(5)`]。接受一对凭据名称和值，用冒号分隔。`systemd.set_credential=` 参数期望凭据值为字面文本形式，`systemd.set_credential_binary=` 参数接受 Base64 编码的二进制数据。注意，内核命令行通常可由非特权程序在 `/proc/cmdline` 中访问。因此，此机制不适合传输敏感数据。仅将其用于不敏感的数据（例如公钥/证书，而非私钥），或用于测试/调试环境。

更多信息参见 **系统与服务凭据**[8] 文档。

在版本 251 中添加。

`systemd.import_credentials=`  
接受布尔参数。如果为 false，则禁用从内核命令行、DMI/SMBIOS OEM 字符串表、qemu_fw_cfg 子系统或 EFI 内核 stub 导入凭据。

在版本 251 中添加。

`systemd.credentials_boot_policy=`  
控制在什么条件下接受用“null”密钥加密的凭据（即包裹在 `systemd-creds` 信封中但既不提供机密性也不提供真实性的凭据，参见 [`systemd-creds(1)`]）。这为在机器拥有用于加密凭据的密钥之前（例如首次启动时或没有 TPM2 设备的系统上）配置凭据提供了回退。接受 `strict`、`tofu`、`relaxed` 或 `off` 之一：

- `strict` 从不接受“null”密钥，即始终坚持正确的加密。

- `tofu`（首次使用信任）在首次启动时或没有 TPM2 设备可用时接受“null”密钥。

- `relaxed` 在 SecureBoot 禁用或没有 TPM2 设备可用时接受“null”密钥。

- `off` 始终接受“null”密钥。

默认为 `relaxed`。注意，此策略仅适用于默认接受决定；它对使用主机密钥或 TPM2 设备加密的凭据没有影响，这些凭据始终被接受。

更多信息参见 **系统与服务凭据**[8] 文档。

在版本 262 中添加。

`quiet`  
关闭启动时的状态输出，类似于 `systemd.show_status=no`。注意，此选项也会被内核本身读取并禁用内核日志输出。因此，传递此选项会同时关闭系统管理器和内核的通常输出。

在版本 186 中添加。

`debug`  
打开调试输出。这等同于 `systemd.log_level=debug`。注意，此选项也会被内核本身读取并启用内核调试输出。因此，传递此选项会同时打开系统管理器和内核的调试输出。

在版本 205 中添加。

`emergency`、`rd.emergency`  
启动进入紧急模式。这些选项分别等同于 `systemd.unit=emergency.target` 或 `rd.systemd.unit=emergency.target`。它们最初是为与 SysV 兼容而提供的，但作为方便的快捷方式保留。

在版本 186 中添加。

`rescue`、`rd.rescue`、`single`、`1`  
启动进入救援模式。这些选项等同于 `systemd.unit=rescue.target` 或 `rd.systemd.unit=rescue.target`。它们最初是为与 SysV 兼容而提供的，但作为方便的快捷方式保留。

在版本 186 中添加。

`3`、`5`  
启动进入特定 target 的快捷方式：`3` 等同于 `systemd.unit=multi-user.target`，`5` 等同于 `systemd.unit=graphical.target`。这些选项最初是为与 SysV 兼容而提供的，但作为方便的快捷方式保留。

在版本 186 中添加。

`locale.LANG=`、`locale.LANGUAGE=`、`locale.LC_CTYPE=`、`locale.LC_NUMERIC=`、`locale.LC_TIME=`、`locale.LC_COLLATE=`、`locale.LC_MONETARY=`、`locale.LC_MESSAGES=`、`locale.LC_PAPER=`、`locale.LC_NAME=`、`locale.LC_ADDRESS=`、`locale.LC_TELEPHONE=`、`locale.LC_MEASUREMENT=`、`locale.LC_IDENTIFICATION=`  
设置要使用的系统区域设置。这会覆盖 `/etc/locale.conf` 中的设置。更多信息参见 [`locale.conf(5)`] 和 [`locale(7)`]。

在版本 186 中添加。

`systemd.minimum_uptime_sec=`  
接受以秒为单位的时间。指定系统关闭前的最低运行时间。更多信息参见 [`systemd-system.conf(5)`] 中描述的 `MinimumUptimeSec=` 设置。

在版本 261 中添加。

有关核心 OS 组件理解的其他内核命令行参数，请参阅 [`kernel-command-line(7)`]。

## 系统凭据

在初始化期间，服务管理器将从各种来源导入凭据到系统凭据集中，然后可以传播到服务中并由生成器使用：

- 服务管理器首次初始化时，将从 SMBIOS Type 11 供应商字符串 `io.systemd.credential:name=value` 和 `io.systemd.credential.binary:name=value` 读取系统凭据。

- 同时，它将从 QEMU “fw_cfg” 导入凭据。（注意，SMBIOS 机制通常更受青睐，因为它更快且更通用。）

- 凭据可以通过内核命令行使用 `systemd.set-credential=` 参数传递，见上文。

- 凭据可以通过 [`systemd-stub(7)`] 从 UEFI 环境传递。

- 当服务管理器在 initrd → 主机过渡期间被调用时，它将把 `/run/credentials/@initrd/` 中的所有文件作为系统凭据导入。

如下调用 [`systemd-creds(1)`] 查看传入系统的凭据列表：

```sh
# systemd-creds --system list
```

更多信息参见 **系统与服务凭据**[8] 文档。

作为 PID 1 运行时的服务管理器消费以下系统凭据：

`vmm.notify_socket`  
包含一个 `AF_VSOCK` 或 `AF_UNIX` 地址，用于在服务管理器完成启动时发送 `READY=1` 通知消息。更多信息参见 [`sd_notify(3)`] 和下一节。注意，如果 hypervisor 不支持 `AF_VSOCK` 上的 `SOCK_DGRAM`，则将改为尝试 `SOCK_SEQPACKET`。`AF_VSOCK` 的凭据负载应为形式为“vsock:CID:PORT”的字符串。可以使用“vsock-stream”、“vsock-dgram”和“vsock-seqpacket”代替“vsock”以强制使用相应的套接字类型。

此功能对于机器管理器或主机上的其他进程在虚拟机完成启动时通过 VSOCK 接收通知很有用。

在版本 254 中添加。

`system.machine_id`  
接受 128 位十六进制 ID，用于在文件尚未设置时初始化 `/etc/machine-id`。详情参见 [`machine-id(5)`]。

在版本 254 中添加。

有关 systemd 各其他组件消费的系统凭据列表，参见 [`systemd.system-credentials(7)`]。

## 就绪协议

服务管理器在管理器与其服务之间（即沿堆栈向下）以及管理器与堆栈上层的潜在监督者之间（后者可以是机器或容器管理器，或者对于每用户服务管理器而言是系统服务管理器实例）实现就绪通知协议。基本协议（及其建议的 API）在 [`sd_notify(3)`] 中描述。

服务管理器（包括 PID 1）用于向其自身监督者报告就绪状态的通知套接字通过通常的 `$NOTIFY_SOCKET` 环境变量设置（见上文）。由于这仅可直接为容器管理器和每用户服务管理器实例设置，因此提供了额外的配置机制，特别是用于 VM 环境：`vmm.notify_socket` 系统凭据（见上文）可以通过 SMBIOS Type 11 供应商字符串设置为合适的套接字（通常是 `AF_VSOCK` 套接字）。详情见上文。

服务管理器沿堆栈向上到监督者的通知协议支持若干扩展字段，允许监督者了解系统的特定属性并跟踪其启动进度。具体发送以下字段：

- 一旦确定系统的初始主机名，将发出 `X_SYSTEMD_HOSTNAME=...` 消息。注意，在后续运行时主机名可能会以编程方式再次更改，并且（目前）在这种情况下不会发出进一步通知。

  在版本 256 中添加。

- 一旦确定系统的机器 ID，将发出 `X_SYSTEMD_MACHINE_ID=...` 消息。详情参见 [`machine-id(5)`]。

  在版本 256 中添加。

- 一旦服务管理器安装上述各种 UNIX 进程信号处理程序，将发出 `X_SYSTEMD_SIGNALS_LEVEL=...` 消息。该字段的值是格式化为十进制字符串的无符号整数，表示服务管理器支持的 UNIX 进程信号功能级别。目前仅定义了一个功能级别：

  - `X_SYSTEMD_SIGNALS_LEVEL=2` 涵盖上述各种 UNIX 进程信号——它们是历史 SysV init 系统所支持信号的上位集合。

  在此消息发送之前发送给 PID 1 的信号可能尚未被正确处理。这些消息的消费者应将值解析为表示支持级别的无符号整数。目前仅定义了提到的级别 2，但以后可能会定义具有更高整数的附加级别，实现当前定义行为的超集。

  在版本 256 中添加。

- 每个 target 单元激活或停止激活时，将发出 `X_SYSTEMD_UNIT_ACTIVE=...` 和 `X_SYSTEMD_UNIT_INACTIVE=...` 消息。这对于跟踪启动进度和功能很有用。例如，一旦报告 `ssh-access.target` 单元已启动，通常即可使用 SSH 访问，详情参见 [`systemd.special(7)`]。

  在版本 256 中添加。

- 在系统关闭前不久将发出 `X_SYSTEMD_SHUTDOWN=...` 消息。值为“reboot”、“halt”、“poweroff”、“kexec”之一，表示正在执行的关闭类型。

  在版本 256 中添加。

- 在系统关闭前不久还将发出 `X_SYSTEMD_REBOOT_PARAMETER=...` 消息。其值为通过 `systemctl --reboot-argument=...` 配置的重启参数。

  在版本 256 中添加。

注意，这些扩展字段是在常规“READY=1”和“RELOADING=1”通知之外发送的。

## 选项

`systemd` 很少被直接调用，因为它很早就启动，并且在用户可能与之交互时已经在运行。通常使用 [`systemctl(1)`] 等工具向管理器发出命令。由于 `systemd` 通常不直接调用，下面列出的选项主要用于调试和特殊用途。

### 内省与调试选项

这些选项用于测试和内省，`systemd` 可以随时带这些选项调用：

`--dump-configuration-items`  
转储理解的单元配置项。这会输出单元定义文件中理解的配置项的简洁但完整列表。

`--dump-bus-properties`  
转储暴露的总线属性。这会输出 D-Bus 上暴露的属性的简洁但完整列表。

在版本 239 中添加。

`--test`  
确定初始启动事务（即启动时排队的作业列表），转储它并退出——而不实际执行任何确定的作业。此选项仅用于调试。注意，在常规服务管理器启动期间，可能会启动此操作未显示的附加单元，因为硬件、套接字、总线或其他类型的激活可能在事务执行时添加附加作业。使用 `--system` 请求系统服务管理器的初始事务（这也是隐含的默认值），与 `--user` 组合以改为请求每用户服务管理器的初始事务。

`--system`、`--user`  
与 `--test` 结合使用时，选择是为系统实例还是每用户实例计算初始事务。不带 `--test` 调用时这些选项没有效果，因为在常规（即非 `--test`）调用期间，服务管理器将通过检查其运行的 PID 是否为 1 来自动检测应以系统模式还是每用户模式运行。注意，不支持在服务管理器以 `--system` 模式运行但 PID 不是 1 的情况下启动和维护系统。

`-h`、`--help`  
打印简短帮助文本并退出。

`--version`  
打印简短版本字符串并退出。

### 复制内核命令行设置的选项

这些选项直接对应于上面“内核命令行”中列出的选项。对于系统管理器，两种形式可以等效使用，但建议在此上下文中使用上面列出的形式，因为它们具有适当的命名空间。当选项同时在内核命令行和普通命令行参数上指定时，后者具有更高优先级。

当 `systemd` 用作用户管理器时，内核命令行被忽略，仅理解下面描述的选项。不过，`systemd` 通常通过 [`user@.service(5)`] 服务以这种模式启动，该服务在所有用户之间共享。使用配置文件修改设置（参见 [`systemd-user.conf(5)`]）或环境变量可能更方便。关于环境块如何设置的讨论，参见上文“环境”一节。

`--unit=`  
设置启动时要激活的默认单元。如果未指定，默认为 `default.target`。参见上文 `systemd.unit=`。

`--dump-core`  
在崩溃时启用核心转储。以用户实例运行时此开关没有效果。同上文 `systemd.dump_core=`。

`--crash-vt=VT`  
崩溃时切换到特定虚拟控制台（VT）。以用户实例运行时此开关没有效果。同上文 `systemd.crash_chvt=`（但拼写不同！）。

在版本 227 中添加。

`--crash-shell`  
崩溃时运行 shell。以用户实例运行时此开关没有效果。参见上文 `systemd.crash_shell=`。

`--crash-action=`  
指定系统管理器（PID 1）崩溃时的操作。当 `systemd` 以用户实例运行时此开关没有效果。参见上文 `systemd.crash_action=`。

在版本 256 中添加。

`--confirm-spawn`  
生成进程时请求确认。以用户实例运行时此开关没有效果。参见上文 `systemd.confirm_spawn`。

`--show-status`  
在启动和关闭期间在控制台上显示简洁的单元状态信息。参见上文 `systemd.show_status`。

在版本 244 中添加。

`--log-color`  
高亮重要日志消息。参见上文 `systemd.log_color`。

在版本 244 中添加。

`--log-level=`  
设置日志级别。参见上文 `systemd.log_level`。

`--log-location`  
在日志消息中包含代码位置。参见上文 `systemd.log_location`。

在版本 244 中添加。

`--log-target=`  
设置日志目标。参见上文 `systemd.log_target`。

`--log-time=`  
为控制台消息添加时间戳前缀。参见上文 `systemd.log_time`。

在版本 246 中添加。

`--machine-id=`  
覆盖硬盘上设置的 machine-id。参见上文 `systemd.machine_id=`。

在版本 229 中添加。

`--service-watchdogs`  
全局启用/禁用所有服务看门狗超时和紧急动作。参见上文 `systemd.service_watchdogs`。

在版本 237 中添加。

`--default-standard-output=`、`--default-standard-error=`  
分别设置所有服务和套接字的默认输出或错误输出。参见上文 `systemd.default_standard_output=` 和 `systemd.default_standard_error=`。

## 系统时钟纪元

当 `systemd` 启动或重启时，它可能会将系统时钟设置为“纪元”。此机制用于确保在没有电池供电的本地 RTC 可用或其工作不正常的情况下，系统时钟在重启之间保持某种程度的合理初始化并大致单调。

纪元是假定系统时钟时间设置正确的最低日期。初始化时，如果本地时钟设置为较低值，则会将其*推进*到纪元。作为特殊情况，如果本地时钟足够远在未来（默认 15 年，但可在构建时配置），则假定硬件时钟已损坏，系统时钟被*回拨*到纪元。

纪元设置为以下最高者：systemd 的构建时间、`/usr/lib/clock-epoch` 的修改时间（“mtime”）以及 `/var/lib/systemd/timesync/clock` 的修改时间。

## 文件

`/run/systemd/notify`  
守护进程状态通知套接字。这是一个 `AF_UNIX` 数据报套接字，用于实现 [`sd_notify(3)`] 实现的守护进程通知逻辑。

`/run/systemd/private`  
内部用作 [`systemctl(1)`] 与 systemd 进程之间的通信通道。这是一个 `AF_UNIX` 流套接字。此接口是 systemd 私有的，不应在外部项目中使用。

`/usr/lib/clock-epoch`  
此文件的修改时间（“mtime”）用于时间纪元，参见上一节。

在版本 247 中添加。

`/var/lib/systemd/timesync/clock`  
此文件的修改时间（“mtime”）由 [`systemd-timesyncd.service(8)`] 更新。如果存在，文件的修改时间用于纪元，参见上一节。

在版本 257 中添加。

## 历史

systemd 252  
内核命令行参数 `systemd.unified_cgroup_hierarchy` 和 `systemd.legacy_systemd_cgroup_controller` 已弃用。请切换到统一 cgroup 层次结构。

## 另见

**systemd 主页**[9]、[`systemd-system.conf(5)`]、[`locale.conf(5)`]、[`systemctl(1)`]、[`journalctl(1)`]、[`systemd-notify(1)`]、[`daemon(7)`]、[`sd-daemon(3)`]、[`org.freedesktop.systemd1(5)`]、[`systemd.unit(5)`]、[`systemd.special(7)`]、`pkg-config(1)`、[`kernel-command-line(7)`]、[`bootup(7)`]、[`systemd.directives(7)`]、[`org.freedesktop.systemd1(5)`]

有关 systemd 背后概念和思想的更多信息，请参阅 **原始设计文档**[10]。

## 注释

1. 接口可移植性与稳定性承诺  
   <https://systemd.io/PORTABILITY_AND_STABILITY/>

2. 容器接口  
   <https://systemd.io/CONTAINER_INTERFACE>

3. initrd 接口  
   <https://systemd.io/INITRD_INTERFACE/>

4. Control Groups v2  
   <https://docs.kernel.org/admin-guide/cgroup-v2.html>

5. XDG Base Directory 规范  
   <https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html>

6. 建议其他工具酌情设置和检查 `$SUDO_UID`，将其视为常见接口。

7. 已知环境变量  
   <https://systemd.io/ENVIRONMENT>

8. 系统与服务凭据  
   <https://systemd.io/CREDENTIALS>

9. systemd 主页  
   <https://systemd.io/>

10. 原始设计文档  
    <https://0pointer.de/blog/projects/systemd.html>

## 版本信息

本页是 *systemd*（systemd 系统与服务管理器）项目的一部分。项目信息可在 ⟨<http://www.freedesktop.org/wiki/Software/systemd>⟩ 找到。如果你对本手册页有错误报告，请参见 ⟨<http://www.freedesktop.org/wiki/Software/systemd/#bugreports>⟩。本页于 2026-08-04 从项目的上游 Git 仓库 ⟨<https://github.com/systemd/systemd.git>⟩ 获取。（当时，仓库中找到的最新提交日期为 2026-08-03。）如果你发现此 HTML 版本页面中的渲染问题，或认为有更好或更新的页面来源，或对 COLOPHON 中的信息（其 *不是* 原始手册页的一部分）有更正或改进，请发送邮件至 man-pages@man7.org。

```text
systemd 262~devel                                              SYSTEMD(1)
```