https://www.w3.org/TR/xml/

# Extensible Markup Language (XML) 1.0 (Fifth Edition)

## 2 Documents

### 2.11 行尾处理

XML [解析实体](#dt-parsedent)通常存储在计算机文件中，为了编辑方便，这些文件被组织成行。这些行通常由回车符（#xD）和换行符（#xA）的某种组合分隔。

为了简化[应用程序](#dt-app)的任务，[XML 处理器](#dt-xml-proc) **必须** 表现得像在解析之前对输入的外部解析实体（包括文档实体）中的所有换行进行了规范化，即将双字符序列 #xD #xA（回车 换行） 以及任何后面不跟 #xA 的 #xD 都转换为单个 #xA 字符。

> 即，XML 处理器将所有 URL 编码的回车换行组合转为单个换行。但不作用到 HTML 编码的字符引用