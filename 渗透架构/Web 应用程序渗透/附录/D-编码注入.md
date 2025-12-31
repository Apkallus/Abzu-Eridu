# 编码注入

## 背景

字符编码是将字符、数字和其他符号映射为标准格式的过程。通常，这样做是为了创建准备在发送方和接收方之间传输的消息。简而言之，它是将字符（属于不同语言，如英语、中文、希腊语或任何其他已知语言）转换为字节的过程。一个广泛使用的字符编码方案示例是初始使用7位代码的美国信息交换标准代码（ASCII）。更新近的编码方案示例是Unicode `UTF-8`和`UTF-16`计算行业标准。

在应用安全领域，由于存在大量可用的编码方案，字符编码有一种常见的滥用行为。它被用来以混淆恶意注入字符串的方式进行编码。这可能导致绕过输入验证过滤器，或者利用浏览器渲染编码文本的特定方式。

## 输入编码 – 过滤绕过

Web应用通常采用不同类型的输入过滤机制来限制用户可提交的输入。如果这些输入过滤器的实现不够充分，就有可能使一两个字符绕过这些过滤器。例如，`/` 在ASCII中可表示为 `2F`（十六进制），而同一字符（`/`）在Unicode中编码为 `C0` `AF`（双字节序列）。因此，输入过滤控件必须能够识别所使用的编码方案。如果发现过滤器仅检测 `UTF-8` 编码的注入，则可采用不同的编码方案来绕过此过滤器。

## 输出编码 – 服务器与浏览器共识

Web浏览器需要识别所使用的编码方案以正确显示网页内容。理想情况下，此信息应通过HTTP头部（`Content-Type`）字段提供给浏览器，如下所示：

```http
Content-Type: text/html; charset=UTF-8
```

或通过HTML META标签（`META HTTP-EQUIV`）声明，如下所示：

``` html
<META http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
```

浏览器正是通过这些字符编码声明来理解在将字节转换为字符时应使用哪组字符。需要注意的是，HTTP头部中声明的字符编码优先级高于META标签声明。

CERT对此描述如下：

许多网页未定义字符编码（HTTP中的`charset`参数）。在早期版本的HTML和HTTP中，如果未定义字符编码，默认应使用`ISO-8859-1`。但实际上，许多浏览器采用不同的默认编码，因此无法依赖默认值为`ISO-8859-1`。HTML 4版本对此进行了规范——如果未指定字符编码，可以使用任何字符编码。

如果Web服务器未指定正在使用的字符编码，则无法识别哪些字符是特殊字符。未指定字符编码的网页在大多数情况下可以正常工作，因为大多数字符集将为128以下的字节值分配相同的字符。但128以上的哪些值具有特殊性？某些16位`character-encoding`方案为特殊字符（如`<`）提供了额外的多字节表示法。部分浏览器能识别这种替代编码并据此执行操作。这虽然是"正确"的行为，但使得利用恶意脚本的攻击更难以防范。服务器根本无法知道哪些字节序列代表特殊字符。

因此，当未从服务器接收到字符编码信息时，浏览器会尝试猜测编码方案或回退到默认方案。某些情况下，用户会在浏览器中显式将默认编码设置为不同的方案。网页（服务器）和浏览器使用的编码方案之间的任何不匹配，都可能导致浏览器以非预期或意外的方式解析页面。

### 编码注入

以下所列的所有场景仅构成通过混淆手段绕过输入过滤器的多种方式中的一个子集。此外，编码注入的成功与否取决于所使用的浏览器。例如，`US-ASCII`编码的注入过去仅在IE浏览器中能够成功，而在Firefox中则无效。因此需要注意，编码注入在很大程度上取决于浏览器特性。

### 基础编码

假设存在一个基础输入验证过滤器，用于防护单引号字符的注入。在这种情况下，以下注入可轻松绕过该过滤器：

``` html
<script>alert(String.fromCharCode(88,83,83))</script>
```

`String.fromCharCode` JavaScript 函数接收给定的 Unicode 值并返回对应的字符串。这是最基础的编码注入形式之一。可用于绕过此过滤器的另一种向量为（HTML属性值将被浏览器进行HTML解码）：

``` html
<IMG src="" onerror=javascript:alert(&quot;XSS&quot;)>
```

或通过使用相应的 [HTML 字符编码](https://www.rapidtables.com/code/text/unicode-characters.html)：

``` html
<IMG src="" onerror="javascript:alert(&#34;XSS&#34;)">
```

上述方法使用 HTML 实体构建注入字符串。HTML 实体编码用于显示在 HTML 中具有特殊含义的字符。例如，`>` 作为 HTML 标签的闭合括号使用。若要在网页上实际显示该字符，则需在页面源码中插入 HTML 字符实体。上述注入仅是编码方式的一种，还存在大量其他字符串编码（混淆）方法可用于绕过前述过滤器。

### 十六进制编码

十六进制（Hex，Hexadecimal）是一种基数为16的计数系统，即使用16个不同的值（从`0`到`9`和`A`到`F`）来表示各种字符。十六进制编码是另一种混淆形式，有时用于绕过输入验证过滤器。例如，字符串`<IMG SRC=javascript:alert('XSS')>`的十六进制编码版本为：

``` html
<IMG SRC=%6A%61%76%61%73%63%72%69%70%74%3A%61%6C%65%72%74%28%27%58%53%53%27%29>
```

以下是上述字符串的变体。在"%"字符被过滤时可使用：

``` html
<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>
```

还存在其他可用于混淆的编码方案，例如Base64和八进制编码。尽管每种编码方案未必每次都能生效，但通过少量试验并结合智能操作，必定能揭示薄弱输入验证过滤器中的漏洞。

### UTF-7 编码

字符串

``` html
<SCRIPT>
    alert(‘XSS’);
</SCRIPT>
```

的 UTF-7 编码如下：

`+ADw-SCRIPT+AD4-alert('XSS');+ADw-/SCRIPT+AD4-`

要使上述脚本生效，浏览器必须将网页解析为 `UTF-7` 编码。

### 多字节编码

可变宽度编码是另一种字符编码方案，它使用不同长度的代码来编码字符。多字节编码是一种可变宽度编码，使用可变数量的字节来表示一个字符。多字节编码主要用于编码属于大型字符集的字符，例如中文、日文和韩文。
多字节编码在过去曾被用于绕过标准输入验证函数，并实施跨站脚本和 SQL 注入攻击。

## References

- [WSTG 6-Appendix D-Encoded_Injection](https://github.com/OWASP/wstg/blob/master/document/6-Appendix/D-Encoded_Injection.md#encoded-injections)
- [Encoding (Semiotics)](https://en.wikipedia.org/wiki/Encoding_(semiotics))
- [HTML Entities](https://www.w3schools.com/HTML/html_entities.asp)
- [How to prevent input validation attacks](https://searchsecurity.techtarget.com/answer/How-to-prevent-input-validation-attacks)
- [Unicode and Character Sets](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)