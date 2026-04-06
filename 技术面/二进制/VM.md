VM 逆向：
- 数据结构：
    - 指令 buf
    - 内存 buf
    - 寄存器
- 指令包字段顺序
- 寄存器功能
    - 控制流/栈/条件寄存器 rip rsp flag 
    - 参数/额外寄存器 rdi rsi rdx
- 打印内容  
    类型：
    - 静态全局总览，无运行时值/栈/内存
    - 动态运行解析，仅运行范围指令的值/栈/内存

    内容：
    - rip 行号
    - 功能与参数
    - 控制流变化标注
        - 设置 rip  
            - 立即数到 rip
            - 栈弹出到 rip
        - 条件跳转
    - 动态的栈状态 
        - push/pop
            - 栈层数、入栈出栈值

- 分析重复代码段提取模式
- 设置配置表后，编写解释器将文本解析为指令字节
    - 字典/类

- 探测配置映射，结合静态代码分析与运行状态分析
    信号：
    - 退出码值
    - 阻塞延迟（也可转为退出码值）
    - 输出

    观测特性(排除)与共性(集合)：
    - 指令功能的参数
    - 寄存器语义
    - 条件结构
        - 位模式的顺序执行
        - 条件的特定块执行

    值（短路）：
    - 不匹配任何
    - 匹配所有
    - 匹配特定

- 探测到的配置使用解释器进行解析而无需手动设置字节序列
    - 解释器将字符串转为编码
        - 即，字符串格式与编码值的映射
    - 使用对应的字符串格式编写指令
        - 即，基本指令、函数调用（设置寄存器/参数）

- 劫持
    - 查看内存操作的边界检查，确定是否存在 buf 溢出或指针任意地址读写
    - 查看程序计数器控制方式，确定是否存在可控位置，以设置偏移或跳转到代码中段以执行非预期指令


各种 VM：
- chroot 设置绝对路径解析的根目录
    - 若之后未使用 chdir 切换到对应目录
        - 当前工作目录在设置目录外，使用当前工作目录的相对路径遍历
    - 若在 chroot 前拥有打开的外部目录fd
        - 使用 openat 打开目录下的文件
            - 若为使用绝对路径的软链接，则解析时使用 chroot 设置的绝对路径根目录而无法逃逸
        - 调用 fchdir 使用外部目录fd，切换工作目录到外部目录

- seccomp
    - 宽松的策略
        - 大量 syscall
        - 沙箱进程使用 `ptrace()` 控制外部进程
        - `sendmsg()` 传递 fd对象，而不只是 fd数字
        - `prctl()` 
        - `process_vm_writev()` 访问其他进程的内存
    - 系统调用混淆
        - 拥有多个架构接口
            - exit() syscall 60 (mov rax, 60; syscall) on amd64
            - exit() syscall 1 (mov eax, 1; int 0x80) on x86
    - 内核漏洞
    - 数据泄露/带外，逐比特提取信息
        - 运行时间（sleep/无限循环）
        - 正常退出或崩溃
        - 返回值/退出码（exit）

    - 语法功能
        ```c
        // 设置过滤器变量
        scmp_filter_ctx ctx;
        // 设置初始化状态，此处默认为 kill 终止
        ctx = seccomp_init(SCMP_ACT_KILL);
        // 添加过滤规则，此处添加 open 系统调用到 SCMP_ACT_ALLOW 白名单
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0)
        // 应用过滤器
        seccomp_load(ctx)
        // 添加额外的 32位架构
        seccomp_arch_add(ctx, SCMP_ARCH_X86);
        ```
        - 若添加额外架构 `seccomp_arch_add`，位于设置规则之后，那么此额外架构仅使用初始化的规则
            - 若初始化为允许，主架构设置禁止条目，之后添加额外架构。那么额外架构不应用主架构的禁止条目，而是全部允许。
        
        常量：
        - `SCMP_ACT_KILL` 0x0
        - `SCMP_ACT_ALLOW` 0x7fff0000

- namespace
    - 语法功能
    ```c
    // 调用 unshare 分离共享命名空间
    unshare(CLONE_NEWNS)

    // 创建之后用作新根目录的临时目录 /tmp/jail-XXXXXX
    mkdtemp(new_root)

    // 将根目录 "/" 改为递归私有挂载，修改仅限当前命名空间，不会传播到外面
    mount(NULL, "/", NULL, MS_REC | MS_PRIVATE, NULL) 

    // 将新根目录绑定挂载到自身，将目录创建为挂载点
    mount(new_root, new_root, NULL, MS_BIND, NULL) 

    // 在新目录下设置 /old 目录 /tmp/jail-XXXXXX/old
    mkdir(old_root, 0777)

    // pivot_root 移动进程的根文件系统
    // 新根文件目录 /tmp/jail-XXXXXX
    // 旧根文件目录 /tmp/jail-XXXXXX/old
    syscall(SYS_pivot_root, new_root, old_root)

    // 在新根目录下创建 /tmp/jail-XXXXXX/bin
    mkdir("/bin", 0755)
    // 将旧根文件目录的 /bin 挂在到新根文件目录 /tmp/jail-XXXXXX/bin
    mount("/old/bin", "/bin", NULL, MS_BIND, NULL)

    // 卸载并移除旧根目录
    umount2("/old", MNT_DETACH)
    rmdir("/old") 
    ```

- tips：
    - 执行挑战程序前在 shell 或 pwntool 打开 fd，则可从父进程继承或重定向 fd 到作为子进程的挑战程序中
        - shell 重定向 fd 并打印 `exec {d}</; echo $d`
        - pwntool 设置参数为 `close_fds=False`，调用 `os.open('/', 0)`，似乎默认不继承 fd
    - ns 中使用外部挂载点。若无法直接使用，但拥有 root 权限时：
        - 任意挂载点均可设置目录/文件权限
        - /proc 挂载点可访问其他进程的 fd
        - 若挂载点设置为只读，重新挂载以解除只读限制


- yan 解释器

    ```py
    import re
    from pwn import *

    context.arch = "amd64"

    // 设置全局数组对象保存映射
    REG = {
        "REG_I": 0x1, 
        "REG_D": 0x2, 
        "REG_S": 0x4, 
        "REG_C": 0x8, 
        "REG_F": 0x10, 
        "REG_A": 0x20, 
        "REG_B": 0x40, 
        "REG_DS": 0x80, 
        "REG_CS": 0xff
        }

    INS = {
        "ins_imm": 0x20, 
        "ins_add": 0x1, 
        "ins_stk": 0x40, 
        "ins_rtm": 0x8, 
        "ins_mtr": 0x80, 
        "ins_cmp": 0x2, 
        "ins_jmp": 0x10, 
        "ins_sys": 0x4
        }

    SYS = {
        "sys_open": 0x8, 
        "sys_read": 0x20, 
        "sys_exec": 0x40, 
        "sys_sleep": 0x2, 
        "sys_exit": 0x10
        }
        
    COND = {
        "cmp_less": 0x4, 
        "cmp_great": 0x8, 
        "cmp_eq": 0x10, 
        "cmp_noteq": 0x2, 
        "cmp_both0": 0x1 
        }

    // 其他函数使用固定 ins/op1/op2 接口，构建调整字节排布的函数
    def pk_seq_rev(pk, is_x86=False):
        # 传入顺序固定
        ins, op1, op2 = pk
        # !! 查看并调整顺序 !!
        if is_x86 == True:
            seq_rev_pk = op2 + ins + op1
        else:
            seq_rev_pk = bytes([ins, op1 ,op2])
        return seq_rev_pk

    // 字符串按照固定结构解析为字节编码，最后调用 pk_seq_rev 构建实际结构顺序
    def parse_str(yan_str, is_x86=False):
        // re 解析为字符串包的数组
        r = re.compile(r'(ins.*?) \((.*?), (.*?)\)')
        ins_op1_op2_list = r.findall(yan_str)
        for i, pk in enumerate(ins_op1_op2_list):
            print(f'parse_str {i} ', pk)

        // 遍历包数组解析操作符与操作数，格式固定为 ins/op1/op2
        payload_bytes = bytearray()
        for ins, op1, op2 in ins_op1_op2_list:
            match ins:
                case "ins_sys":
                    # sys(系统调用值，调用结果寄存器) 
                    sys_value = SYS[op1]
                    result_reg = REG[op2]

                    payload_ins = INS[ins]
                    payload_op1 = sys_value
                    payload_op2 = result_reg   
                    
                case "ins_imm":
                    # imm(目标寄存器，源值)
                    reg = REG[op1]
                    value = int(op2, 16)

                    payload_ins = INS[ins]
                    payload_op1 = reg
                    payload_op2 = value     
                case "ins_rtm":
                    # rtm(内存偏移寄存器，源寄存器)  
                    mem_offset = REG[op1]
                    value = REG[op2]

                    payload_ins = INS[ins]
                    payload_op1 = mem_offset
                    payload_op2 = value     
                case "ins_stk":
                    # stk(pop寄存器, push寄存器)
                    pop_reg = REG[op1]
                    push_reg = REG[op2]

                    payload_ins = INS[ins]
                    payload_op1 = pop_reg
                    payload_op2 = push_reg    
                case "ins_add":
                    # add(op1&结果寄存器, op2寄存器)
                    add_op1 = REG[op1]
                    add_op2 = REG[op2]

                    payload_ins = INS[ins]
                    payload_op1 = add_op1
                    payload_op2 = add_op2   
                case "ins_cmp":
                    # cmp(op1寄存器, op2寄存器)
                    cmp_op1 =REG[op1]
                    cmp_op2 = REG[op2]

                    payload_ins = INS[ins]
                    payload_op1 = cmp_op1
                    payload_op2 = cmp_op2   
                case "ins_jmp":
                    # jmp(跳转条件值，指令地址寄存器)
                    jmp_cond = COND[op1]
                    jmp_targ = REG[op2]

                    payload_ins = INS[ins]
                    payload_op1 = jmp_cond
                    payload_op2 = jmp_targ   

                    # mtr(目标寄存器，内存偏移寄存器) 
                case _:
                    raise ValueError("not match ins: ", ins)
                
            // 若为 64 位版本则使用 8 字节编码
            if is_x86 == True:
                payload_byte = [p64(payload_ins), p64(payload_op1), p64(payload_op2)]
            // 否则使用 1 字节编码
            else:
                payload_byte = bytes([payload_ins, payload_op1, payload_op2])

            // 调用 pk_seq_rev 将固定结构顺序修改为实际顺序
            payload_byte_rev = pk_seq_rev(payload_byte, is_x86)
            # print(f"payload_byte_rev ", payload_byte_rev.hex())
            payload_bytes += payload_byte_rev

        # print(f"payload_bytes ", payload_bytes.hex())
        return payload_bytes

    def build_shellcode_payload(yan_str=None, is_x86=False):
        # 设置文件名 a 到内存
        # 调用 open 得到文件 a 的 fd
        if yan_str == None:
            yan_str = """
                ins_imm (REG_A, 0x61)
                ins_imm (REG_B, 0x1)
                ins_rtm (REG_B, REG_A)

                ins_imm (REG_A, 0x0)
                ins_imm (REG_B, 0x2)
                ins_rtm (REG_B, REG_A)

                ins_imm (REG_A, 0x1)
                ins_imm (REG_B, 0x0)
                ins_sys (sys_open, REG_D)

                ins_imm (REG_A, 0x0)
                ins_imm (REG_B, 0x3)
                ins_imm (REG_C, 0x40)
                ins_sys (sys_read, REG_D)
            """

        yan_str = yan_str.strip()
        # print(f">{yan_str}<")
        
        payload_bytes = parse_str(yan_str, is_x86)

        return payload_bytes
        
    // 保存到文件或在 pwntool 中使用
    payload = build_shellcode_payload(yan_str)
    print(payload.hex())
    print(len(payload))

    with open('payload.bin', 'wb') as f:
        f.write(payload)

    ```