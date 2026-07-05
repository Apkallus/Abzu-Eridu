#!/bin/python3

min_hostgroup = 512
# 设置通用项，之后扩展合并到其他字典
basic_dict = {
    # 时序模板与速率控制
    "time_set": ["-T4",
                # RTT 往返时间尝试根据当前状态减少
                "--max-rtt-timeout", "600ms", # T4 1250ms
                "--initial-rtt-timeout", "400ms", # T4 500ms

                # 自动调整的并行主机扫描速率 5~1000
                # 根据主机数量将 ip 池分块，初始的扫描将设置之后的状态，后续将提高速度。
                # 对于大范围 IP 设置较高的组主机数量，提高了并行等待超时的主机数量，以提高 UDP 扫描速度
                # 对于少量主机，设置较低主机数以迅速更新状态，以缩短之后的扫描时间
                "--min-hostgroup", f"{min_hostgroup}",

                # 单个端口最大重试次数，T4 6次
                "--max-retries", "3", 
                ],
    "log_set": [
                "-v", # 详细输出
                # "-d", # 调试输出
                # "--reason", # 端口状态原因
                # "--packet-trace", # 包追踪
                ],
    # 规避
    "avoid_set": ["--randomize-hosts", # 随机主机扫描       
                  ],
    # 排除端口
    "exclude_ports": [
        # TCP 端口扫描中 "32769/tcp closed filenet-rpc" 几乎总是出现
        # hping3 显示为 ISP 网关伪造响应
        "--exclude-ports", "32769", 
    ]
}

# 设置主机发现参数
host_find_dict = {
    **basic_dict,
    # TCP SYN 标志空包探测
    "tcp_syn_ping": ["-PS21,22,23,25,53,80,111,113,137,139,443,3389,5900,8080,8443,31339"],
    # TCP ACK 标志探测
    "tcp_ack_ping": ["-PA21,80,113,443,10042"],
    # UDP 标志探测
    "udp_ping": ["-PU40125,161"],
    # ICMP 探测
    "icmp_ping": ["-PE", "-PP"],
    # IP 探测
    "ip_ping": [],
    # 文件名由 core 程序设置
    # 其他选项，详细级别，DNS 解析
    "other": [
            "-sn", # 禁用端口扫描而仅进行主机发现
            "-R", # 开启 DNS 解析
            ],
    # 设置反向 DNS 服务器，增加服务器数量以提高速度，至少2个
    "dns-servers": ["--dns-servers", 
                    "9.9.9.9,149.112.112.112"  # quad9
                    ",8.8.8.8,8.8.4.4" # google
                    ",1.1.1.1,1.0.0.1" # Cloudflare
                    ",84.200.69.80,84.200.70.40" # dns.watch
                    ",209.244.0.3,209.244.0.4" # Level3
                    ",95.85.95.85,2.56.220.2" # gcore
                    ",223.5.5.5,223.6.6.6" # alidns
                    ",210.94.0.73,221.139.13.130" # hananet.net
                    ",159.69.114.157,80.241.218.68" # dismail.de
                    ",208.67.222.222,208.67.220.220" # Cisco Umbrella
                    ],

    ## 设置主机发现规避参数
    # 发包源端口
    "source_port": ["--source-port", "53"],
    # 数据包随机字节数据，实测添加长度后导致探测失败
    # "data_length": ["--data-length", "0"],
}

# 设置 UDP 快速端口扫描参数
udp_fast_scan_dict = {
    **basic_dict,
    # 文件名由 core 程序设置
    # 其他选项，详细级别，DNS 解析
    "other": [
            "-Pn", # 禁用主机发现
            "-n", # 禁用反向 DNS 查询
            ],
    # 扫描范围: 常用的精简端口 -F 有100个，或使用 --top-ports 100 设置最常见的100个端口
    "target_range" : ["--top-ports", "200"], 
    # UDP 扫描组合: 仅对最可能的端口进行版本检测以确认开放状态
    "udp_scan" : ["-sU", "-sV", "--version-intensity", "0",
                  # 广度优先策略
                  # 单个主机扫描延迟最大递增到1s，默认或设置以不至于淹没单个主机
                  "--max-scan-delay", "1075ms", 
                  # 单个主机扫描延迟与主机组并行任务数同时使用，以控制单主机发包速率
                  "--scan-delay","300ms",
                  # 提高主机组中的并行任务数量，同时等待多任务超时。
                  # 避免拥塞回退时，大主机组中并行少量任务
                  # 四分之一轮换执行，二分之一拥有性能损失
                  "--min-parallelism", f"{max(min(min_hostgroup//4, 128), 1)}", 
                  ],
}

# 设置 TCP 默认端口扫描参数
tcp_default_scan_dict = {
    **basic_dict,
    # 文件名由 core 程序设置
    # 其他选项，详细级别，DNS 解析
    "other": [
            "-Pn", # 禁用主机发现
            "-n", # 禁用反向 DNS 查询
            ],
    # 扫描方式: 使用默认的 TCP SYN 扫描默认的1000个常用端口
    "tcp_scan" : ["-sS"],
}

# 设置 TCP 全端口扫描参数
tcp_full_scan_dict = {
    **basic_dict,
    # 文件名由 core 程序设置
    # 其他选项，详细级别，DNS 解析
    "other": [
            "-Pn", # 禁用主机发现
            "-n", # 禁用反向 DNS 查询
            ],
    # 扫描范围: 所有端口
    "tcp_scan" : ["-sS", "-p0-"],
}

"""
-O --osscan-limit --max-os-tries 1

若进行操作系统识别(-O 或 -A): 
    --osscan-limit 参数仅对拥有打开和关闭的TCP端口的主机进行 OS 检测
    --max-os-tries 1 仅尝试匹配1次 OS 检测
"""

"""
-sC 脚本扫描？
"""

"""
对少量端口进行各种数据包类型的防火墙探测
调整源端口号测试 --source-port 似乎稍微减慢速度
"-f", # 分片，似乎可稍微加快速度
源路由 --ip-options "L 192.168.0.7 192.168.30.9"
"""