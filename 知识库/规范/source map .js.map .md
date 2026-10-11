[规范文档](https://tc39.es/ecma426/)

https://tc39.es/ecma426/#sec-source-map-format

## 9 Source map 格式

Source map 是一个 JSON 文档，包含一个具有以下结构的顶层 [JSON 对象](#type-json-object)：

```json
{
  "version": 3,
  "file": "out.js",
  "sourceRoot": "",
  "sources": ["foo.js", "bar.js"],
  "sourcesContent": [null, null],
  "names": ["src", "maps", "are", "fun"],
  "mappings": "A,AAAB;;ABCDE",
  "ignoreList": [0]
}
```

- **`version` 字段** 应始终为数字 3，作为一个[整数](https://tc39.es/ecma262/#integer)。如果该字段具有任何其他值，source map 可能会被拒绝。
- **`file` 字段** 是与此 source map 关联的[生成代码](#sec-terms-and-definitions-generated-code)的可选名称。未规定它可以是 [URL](#external-whatwg-url)、相对路径名还是仅为基础名。Source map 生成器可以根据其使用上下文选择适当的解释。
- **`sourceRoot` 字段** 是可选的源根字符串，用于在服务器上重新定位源文件或移除 sources 条目中的重复值。此值会前置到 [sources 字段](#json-sources)中的各个条目。
- **`sources` 字段** 是 [mappings 字段](#json-mappings)所使用的原始源列表。每个条目要么是一个（可能是相对的）[URL](#external-whatwg-url) 字符串，要么在源名称未知时为 `null`。
- **`sourcesContent` 字段** 是可选的源内容（即[原始源](#sec-terms-and-definitions-original-source)）字符串列表，在源无法托管时使用。内容按与 [sources 字段](#json-sources)相同的顺序列出。如果某些[原始源](#sec-terms-and-definitions-original-source)应按名称检索，则条目可以为 `null`。
- **`names` 字段** 是可选的符号名称列表，可供 [mappings 字段](#json-mappings)使用。
- **`mappings` 字段** 是包含编码映射数据的字符串（参见 [9.2](#sec-mappings) 节）。
- **`ignoreList` 字段** 是可选的、应被视为第三方代码（如框架代码或打包器生成的代码）的文件索引列表。这允许开发者工具避免显示或单步执行开发者可能不想看到或逐步调试的代码，而无需开发者事先配置。它引用 [sources 字段](#json-sources)，并列出 source map 中所有已知第三方源的索引。如果 `ignoreList` 不存在，某些浏览器还可能使用已弃用的 `x_google_ignoreList` 字段。

### 9.2 Mappings 结构

[mappings 字段](#json-mappings)数据按如下方式拆分：

- 每个组表示生成文件中的一行，由分号（`;`）分隔
- 每个段由逗号（`,`）分隔
- 每个段由 1、4 或 5 个可变长度字段组成。

每个段中的字段为：

1. 该段所表示的[生成代码](#sec-terms-and-definitions-generated-code)中行的从零开始的起始[列](#sec-terms-and-definitions-colun)。如果这是第一个段的第一个字段，或者是新生成行（`;`）之后的第一个段，则该字段保存完整的 [base64 VLQ](#sec-base64-vlq)。否则，该字段包含相对于该字段上一次出现的 [base64 VLQ](#sec-base64-vlq)。*注意，这与下面的后续字段不同，因为上一个值在每一生成行之后都会重置。*
2. 如果存在，则为 sources 列表中的从零开始的索引。该字段包含相对于该字段上一次出现的 [base64 VLQ](#sec-base64-vlq)，除非这是该字段的第一次出现，此时表示完整值。
3. 如果存在，则为[原始源](#sec-terms-and-definitions-original-source)中从零开始的起始行。该字段包含相对于该字段上一次出现的 [base64 VLQ](#sec-base64-vlq)，除非这是该字段的第一次出现，此时表示完整值。如果存在 source 字段，则应存在。
4. 如果存在，则为[原始源](#sec-terms-and-definitions-original-source)中行的从零开始的起始[列](#sec-terms-and-definitions-colun)。该字段包含相对于该字段上一次出现的 [base64 VLQ](#sec-base64-vlq)，除非这是该字段的第一次出现，此时表示完整值。如果存在 source 字段，则应存在。
5. 如果存在，则为与此段关联的 names 列表中的从零开始的索引。该字段包含相对于该字段上一次出现的 [base64 VLQ](#sec-base64-vlq)，除非这是该字段的第一次出现，此时表示完整值。

> **注意 1**
>
> 此编码的目的是减小 source map 的大小。在使用 Google Calendar 进行的测试中，相对于 [Source Map Revision 2 Proposal](#biblio-source-map-v2)，VLQ 编码将 source map 大小减少了 50%。

> **注意 2**
>
> 具有一个字段的段用于表示未映射的[生成代码](#sec-terms-and-definitions-generated-code)，因为没有对应的[原始源](#sec-terms-and-definitions-original-source)代码，例如编译器生成的代码。具有四个字段的段表示已映射代码，但不存在对应名称。具有五个字段的段表示已映射代码，并且还具有映射的名称。

> **注意 3**
>
> 曾考虑使用文件偏移量，但最终被拒绝，转而使用行/列数据，以避免因平台特定的行尾符而与原始内容发生错位。

#### 9.2.1 Mappings 语法

mappings String 必须遵循以下语法：

```grammar
MappingsField :
    LineList

LineList :
    Line
    Line ; LineList

Line :
    MappingListopt

MappingList :
    Mapping
    Mapping , MappingList

Mapping :
    GeneratedColumn
    GeneratedColumn OriginalSource OriginalLine OriginalColumn Nameopt

GeneratedColumn :
    Vlq

OriginalSource :
    Vlq

OriginalLine :
    Vlq

OriginalColumn :
    Vlq

Name :
    Vlq
```
