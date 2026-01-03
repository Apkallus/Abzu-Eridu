---
id: 
title: Cross Site Scripting (mitigation)
---
<!-- muse start -->
Web Goat 使用 OWASP Java 库对 XSS 进行缓解的示例。
需查看对应项目的文档以了解如何使用，JSP 模板编码库以及 Java 的净化库。
<!-- muse end -->


## 2. XSS防御

### 原因

基于前述内容，核心原则是避免他人代码在用户登录会话上下文中执行。

### 编码对象

XSS防御的基本前提是对所有不可信输入进行输出编码后显示。尽管高级攻击手段可能使这一策略需调整，但目前仍是最有效的防御方式。需特别注意编码上下文差异。  

对于“不可信输入”的界定：如有疑虑，应将所有数据（包括数据库内自生成数据）视为不可信。跨系统数据流通过程中，非本团队创建的数据可能存在风险。

### 编码时机与位置

应在数据发送至浏览器时进行编码（而非在持久化数据阶段）。单页面应用（SPA）需在客户端完成编码，具体实现需参考所用框架/库的文档（后续页面将提供相关资源）。

### 编码方法

- **HTML正文内容**：采用HTML实体编码  
- **HTML属性值**：采用HTML属性编码  
- **JavaScript输出**：若需将用户输入嵌入页面JavaScript，需进行JavaScript编码（但需谨慎评估此种操作的风险性）  

**禁止**使用黑名单/负面过滤策略（如拦截`<script>`等字符串）。  

具体防御资源与扩展阅读详见后续页面。


## 3. 什么是编码？

不信任用户输入意味着当数据通过信任边界（例如从Web表单传递到应用程序脚本时），需验证其类型、长度、格式和范围，随后在动态页面中重新显示前进行编码处理。  

实践中，需审查站点中所有处理用户提供数据的位置，确保在将数据返回用户前，对客户端接收的值进行校验、过滤和编码。 

客户端验证不可依赖，但可通过服务器端处理将用户输入强制限制为最小字母数字字符集，再供Web应用程序使用。

### 转义

转义指转换（或标记）数据中的关键字符，防止其在危险上下文中被解释。对于HTML输出，需转换`<`和`>`等字符以避免恶意代码渲染。转义这些字符需将其转换为实体等价形式`&lt;`和`&gt;`，浏览器不会将其解释为HTML标签。

### 特殊字符

若从用户输入接收特殊字符（如`<`和`>`），需在重新显示前进行编码。例如，编码`<`和`>`可确保浏览器显示`<script>`但不会执行它。结合编码措施，网页必须始终明确定义字符集，防止浏览器解析其他字符集中的特殊字符编码。  

跨站脚本攻击通常发生在将脚本（通常为JavaScript）注入他人网站并恶意运行时。

### 相关XML/HTML特殊字符

| 字符 | 转义字符串 |
|------|------------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `'` | `&#x27;` |
| `&` | `&amp;` |
| `/` | `&#x2F;` |

## 4. XSS防御资源

### Java OWASP编码器

无需关注此项目的孵化状态。若进行Java Web应用程序开发并需防御XSS攻击，建议使用该项目。访问链接：https://www.owasp.org/index.php/OWASP_Java_Encoder_Project

### 通用XSS预防备忘单

链接：https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

### DOM型XSS预防备忘单

链接：https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html

### XSS过滤器绕过

知己知彼方能有效防御。链接：https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet

### JavaScript框架特定指南

客户端编码可能较为复杂。以下资源提供相关指导。若未涵盖您使用的框架（如Ember、React等）且希望贡献建议，请访问https://github.com/WebGoat/WebGoat提交问题（最好附建议/链接）或通过分支提交拉取请求。

#### jQuery

若使用类似
`$selector.html(userInputHere)`
方法需警惕风险。

如需使用此类方法，应确保采用
`$selector.html(someEncodeHtmlMethod(userInputHere))`
或
`$selector.text(someEncodeHtmlMethod(userInputHere))`
等安全形式。

若仅需输出用户输入的文本内容，可参考：http://stackoverflow.com/questions/9735045/is-jquery-text-method-xss-safe#9735118

#### Backbone.js

（细微差异可能导致重大安全影响）  
http://underscorejs.org/#template  
https://nvisium.com/blog/2015/05/21/dont-break-your-backbone-xss-mitigation.html

#### Angular

Angular默认采用转义机制，但其表达式语言存在"沙箱"逃逸漏洞。建议根据所用版本详情参考：https://docs.angularjs.org/guide/security


## 5. 反射型XSS

参考以下将数据传递给JSP文件的HTML文件：

```html
<html>
   <body>
      <form action = "main.jsp" method = "POST">
         First Name: <input type = "text" name = "first_name">
         <br />
         Last Name: <input type = "text" name = "last_name" />
         <input type = "submit" value = "Submit" />
      </form>
   </body>
</html>
```

对应的JSP文件内容：

```html
<html>

<head>
    <title>Using GET and POST Method to Read Form Data</title>
</head>

<body>
    <h1>Using POST Method to Read Form Data</h1>
    <table>
        <tbody>
            <tr>
                <td><b>First Name:</b></td>
                <td><%= request.getParameter("first_name")%></td>
            </tr>
            <tr>
                <td><b>Last Name:</b></td>
                <td>
                    <%= request.getParameter("last_name")%>
                </td>
            </tr>
        </tbody>
    </table>
</body>

</html>
```

如所见，该JSP文件直接输出未过滤的用户输入，这是极其危险的做法。正常访问应为：
`http://hostname.com/mywebapp/main.jsp?first_name=John&last_name=Smith`

但当攻击者使用此恶意链接时：
`http://hostname.com/mywebapp/main.jsp?first_name=<script>alert("XSS Test")</script>`

### 现在轮到你了！

请通过在JSP文件中转义URL参数来防御此类XSS攻击：

需查看[OWASP Java Encoder Project 的使用说明](https://owasp.org/www-project-java-encoder/)

项目示例：

基本 HTML 上下文
```jsp
<body>
    <b><%= Encode.forHtml(UNTRUSTED) %></b>
</body>
```

旧版 JSP（javax.servlet.jsp）的标签库：
```jsp
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@taglib prefix="e" uri="https://www.owasp.org/index.php/OWASP_Java_Encoder_Project" %>

<html>
    <head>
        <title>
            <b><e:forHtml value="${param.title}" /></b>
        </title>
    </head>
    <body>
        <h1>
            <b>${e:forHtml(param.data)}</b>
        </h1>
    </body>
</html>
```

修改挑战代码：添加旧版标签库，使用示例格式（新版标签库无法通过挑战）
```jsp
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@taglib prefix="e" uri="https://www.owasp.org/index.php/OWASP_Java_Encoder_Project" %>
<html>
<head>
    <title>Using GET and POST Method to Read Form Data</title>
</head>
<body>
    <h1>Using POST Method to Read Form Data</h1>
    <table>
        <tbody>
            <tr>
                <td><b>First Name:</b></td>
                <td>${e:forHtml(param.first_name)}</td>
            </tr>
            <tr>
                <td><b>Last Name:</b></td>
                <td>
                    ${e:forHtml(param.last_name)}
                </td>
            </tr>
        </tbody>
    </table>
</body>
</html>
```

## 6. 存储型XSS

防御存储型XSS的一种方法是使用OWASP AntiSamy。该工具可基于可配置的策略文件生成"净化后"的字符串。

参考以下将评论保存至数据库的Java类：

```java
public class MyCommentDAO {

    public static void addComment(int threadID, int userID, String newComment) {

                String sql = "INSERT INTO COMMENTS(THREADID, USERID, COMMENT) VALUES(?,?,?);";

                try {
                        PreparedStatement stmt = connection.prepareStatement(sql);

                        stmt.setInt(1, threadID);
                        stmt.setInt(2, userID);
                        stmt.setString(3, newComment);

                        stmt.executeUpdate();
                } catch (SQLException e) {
                        e.printStackTrace();
                }
        }
}
```

以及调用addComment函数的Java类：

```java
import org.owasp.validator.html.*;
import MyCommentDAO;

public class AntiSamyController {
    ...
    public void saveNewComment(int threadID, int userID, String newComment){
        MyCommentDAO.addComment(threadID, userID, newComment);
    }
    ...
}
```

该Java类将未过滤的用户输入存储至数据库，导致恶意代码完整留存于数据库中。

### 现在轮到你了！

请在saveNewComment()函数内部创建净化字符串来防御此类XSS攻击。使用"antisamy-slashdot.xml"作为策略文件：

此挑战需查看 [OWASP AntiSamy 项目的手册](https://github.com/nahsra/antisamy?tab=readme-ov-file#4-calling-the-antisamy-api)

AntiSamy 项目示例代码为：

```java
import org.owasp.validator.html.*;

Policy policy = Policy.getInstance(POLICY_FILE_LOCATION);

AntiSamy as = new AntiSamy();
CleanResults cr = as.scan(dirtyInput, policy);

MyUserDAO.storeUserProfile(cr.getCleanHTML()); // some custom function
```

对挑战代码进行修改
```java
import org.owasp.validator.html.*;
import MyCommentDAO;

public class AntiSamyController {
    public void saveNewComment(int threadID, int userID, String newComment){
        // 导入策略文件
        Policy policy = Policy.getInstance("antisamy-slashdot.xml");
        // 绑定输入与策略
        AntiSamy as = new AntiSamy();
        CleanResults newComment_cr = as.scan(newComment, policy);
        // 净化输入
        MyCommentDAO.addComment(threadID, userID, newComment_cr.getCleanHTML());
    }
}
```