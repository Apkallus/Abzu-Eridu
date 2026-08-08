# 测试服务器端模板注入

|ID          |
|------------|
|WSTG-INPV-18|

## 概述

Web 应用程序通常使用服务器端模板技术（Jinja2、Twig、FreeMaker 等）来生成动态 HTML 响应。当用户输入以不安全的方式嵌入模板时，就会出现服务器端模板注入漏洞（SSTI），并可能导致服务器上的远程代码执行。任何支持高级用户提供标记的功能都可能容易受到 SSTI 攻击，包括 Wiki 页面、评论、营销应用程序、CMS 系统等。某些模板引擎采用各种机制（例如沙盒、白名单等）来防范 SSTI。

### 示例 - Twig

以下示例摘自 [Extreme Vulnerable Web Application](https://github.com/s4n7h0/xvwa) 项目。

```php
public function getFilter($name)
{
        [snip]
        foreach ($this->filterCallbacks as $callback) {
        if (false !== $filter = call_user_func($callback, $name)) {
            return $filter;
        }
    }
    return false;
}
```

在 getFilter 函数中，`call_user_func($callback, $name)` 存在 SSTI 漏洞：`name` 参数从 HTTP GET 请求中获取并由服务器执行：

![SSTI XVWA 示例](images/SSTI_XVWA.jpeg)\
*图 4.7.18-1：SSTI XVWA 示例*

### 示例 - Flask/Jinja2

以下示例使用 Flask 和 Jinja2 模板引擎。`page` 函数从 HTTP GET 请求中接受一个 'name' 参数，并使用 `name` 变量内容渲染 HTML 响应：

```python
@app.route("/page")
def page():
    name = request.values.get('name')
    output = Jinja2.from_string('Hello ' + name + '!').render()
    return output
```

此代码片段容易受到 XSS 攻击，同时也容易受到 SSTI 攻击。在 `name` 参数中使用以下负载：

```bash
$ curl -g 'https://www.target.com/page?name={{7*7}}'
Hello 49!
```

## 测试目标

- 检测模板注入漏洞点。
- 识别模板引擎。
- 构建漏洞利用。

## 如何测试

SSTI 漏洞存在于文本上下文或代码上下文中。在纯文本上下文中，允许用户使用带有直接 HTML 代码的自由格式“文本”。在代码上下文中，用户输入也可能被放置在模板语句中（例如在变量名中）。

### 识别模板注入漏洞

在纯文本上下文中测试 SSTI 的第一步是构造各种模板引擎常用的模板表达式作为负载，并监视服务器响应，以识别服务器执行了哪个模板表达式。

常见的模板表达式示例：

```text
a{{bar}}b
a{{7*7}}
{var} ${var} {{var}} <%var%> [% var %]
```

在此步骤中，建议使用广泛的[模板表达式测试字符串/负载列表](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)。

在代码上下文中测试 SSTI 略有不同。首先，测试人员构造导致空白或错误服务器响应的请求。在下面的示例中，HTTP GET 参数被插入到模板语句中的变量 `personal_greeting` 中：

```text
personal_greeting=username
Hello user01
```

使用以下负载时，服务器响应为空白 "Hello"：

```text
personal_greeting=username<tag>
Hello
```

下一步是跳出模板语句，并在其后注入 HTML 标签，使用以下负载：

```text
personal_greeting=username}}<tag>
Hello user01 <tag>
```

### 识别模板引擎

基于上一步的信息，测试人员现在必须通过提供各种模板表达式来识别使用了哪个模板引擎。根据服务器响应，测试人员推断所使用的模板引擎。这种手动方法在 [此](https://portswigger.net/blog/server-side-template-injection?#Identify) PortSwigger 文章中有更详细的讨论。为了自动识别 SSTI 漏洞和模板引擎，可以使用各种工具，包括 [Tplmap](https://github.com/epinna/tplmap) 或 [Backslash Powered Scanner Burp Suite 扩展](https://github.com/PortSwigger/backslash-powered-scanner)。

### 构建 RCE 利用

此步骤的主要目标是通过研究模板文档和研究来获得对服务器的进一步控制，实现 RCE 利用。关键的兴趣领域是：

- **面向模板作者** 涵盖基本语法的部分。
- **安全注意事项** 部分。
- 内置方法、函数、过滤器和变量的列表。
- 扩展/插件列表。

测试人员还可以通过关注 `self` 对象来识别哪些其他对象、方法和属性可以被暴露。如果 `self` 对象不可用，且文档未揭示技术细节，则建议对变量名进行暴力破解。一旦识别出对象，下一步是遍历该对象，以识别可通过模板引擎访问的所有方法、属性和属性。这可能导致其他类型的安全发现，包括权限提升、应用程序密码、API 密钥、配置和环境变量等信息泄露。

## 工具

- [Tplmap](https://github.com/epinna/tplmap)
- [Backslash Powered Scanner Burp Suite 扩展](https://github.com/PortSwigger/backslash-powered-scanner)
- [模板表达式测试字符串/负载列表](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)

## 参考资料

- [James Kettle：服务器端模板注入：现代 Web 应用的 RCE（白皮书）](https://portswigger.net/kb/papers/serversidetemplateinjection.pdf)
- [服务器端模板注入](https://portswigger.net/blog/server-side-template-injection)
- [探索 Flask/Jinja2 中的 SSTI](https://www.lanmaster53.com/2016/03/exploring-ssti-flask-jinja2/)
- [服务器端模板注入：从检测到远程 Shell](https://www.okiok.com/server-side-template-injection-from-detection-to-remote-shell/)
- [Extreme Vulnerable Web Application](https://github.com/s4n7h0/xvwa)
- [在 Thymeleaf 中利用 SSTI](https://www.acunetix.com/blog/web-security-zone/exploiting-ssti-in-thymeleaf/)
