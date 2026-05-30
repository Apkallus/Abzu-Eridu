### scapy

<https://scapy.readthedocs.io/en/latest/usage.html>

基础使用：

- 堆叠层:
    `/` 运算符已被用作两层之间的组合运算符。这样做时，较低层的一个或多个默认字段可以根据较高层进行重载。一个字符串可以用作原始层。例：
    ```py
    Ether()/IP()/TCP()

    IP()/TCP()/"GET / HTTP/1.0\r\n\r\n"

    Ether()/IP()/IP()/UDP()
    ```

    堆叠对象使用 `.show2()` 方法展示字段

    当 Scapy 解析到某一层之后，剩下的字节它不知道该按什么协议解释时，就会把它放进一个通用层: `Raw`。
    - 对 TCP 来说，`Raw` 往往就是“应用层数据”。
        - 判断是否有应用层数据：`pkt.haslayer(scapy.Raw)`
        - 取出这段原始数据：`pkt[scapy.Raw].load`（类型是 `bytes`）

- 发送数据包:
    `send()`函数会在第 3 层发送数据包。也就是说，它会为你处理路由和第 2 层。
    `sendp()`函数会在第 2 层工作。你需要自己选择正确的接口和正确的链路层协议。
    如果将 return_packets=True 作为参数传递，send()和 sendp()也会返回发送的数据包列表。
    即，使用`send()`同时堆叠`Ether()`将报错

- 接收数据包：
    `sr1()` 函数发送并等待响应，返回响应内容

网络栈：

- 获取接口的 IP 地址
    ```py
    get_if_addr(conf.iface)  # default interface
    get_if_addr("eth0")
    ```

- 获取接口的 MAC 地址 
    ```py
    get_if_hwaddr(conf.iface)  # default interface
    get_if_hwaddr("eth0")
    ```

- 获取到达 IP 的下一跳的 MAC 地址
    ```py
    getmacbyip("10.0.0.1")
    ```

嗅探：
我们可以轻松捕获一些数据包，甚至可以克隆 tcpdump 或 tshark。可以提供一个接口或接口列表来进行嗅探。如果没有给出接口，嗅探将在 conf.iface 上进行。

```py
sniff(
    iface="eth0",                         # scapy.conf.iface 接口
    filter="tcp port 31337 or arp",       # BPF 过滤
    prn=handle,                           # 抓包的处理函数
    store=False,                          # 不存内存
)
```

其他：
- `包.haslayer(scapy.Ether)` 判断是否存在对应网络层
- 删除  
    在修改各字段后删除校验和，scapy 将自动重新计算
    ```py
    del pkt[scapy.IP].len
    del pkt[scapy.IP].chksum
    del pkt[scapy.TCP].chksum
    ```
