## 示例

### 使用通配符与数量修饰，实现字符串分割

```js
// 分割字符串为每10个字符一组的数组
/.{1,10}/gs

>>> 'abcdefghi'.match(/.{1,3}/gs)
<<< Array(3) [ "abc", "def", "ghi" ]
```

### 字符集

```re
// `[]` 字符集
// `^` 在字符集中表示非
// 匹配所有非：大小写字符、数字、`.`
[^a-zA-Z0-9.]
```

#### 字符集与数量修饰，提取特定格式的字符串

```postgresql
// `$$ ... $$` 为 postgresql 中的字符字面量标记
// 匹配固定前缀 `_password = '`
// 使用捕获组提取之后的连续32个 hex 字符
$$_password = '([0-9a-f]{32})$$
```

### 捕获组

```py
# 提取字符串为捕获组
# 索引0为原始字符串，之后的索引为捕获的内容
r"前缀字符串(.+?)后缀字符串"

re.search(r"/\?data=(.+?)\">", req.response)[1]
```

### 匹配与移除，实现路径规范化

```php
// `#` php 中的正则表达式定界符
// `\p{C}` Unicode 控制字符
// `|` 或
// `#u` 末尾的 Unicode 修饰符

// 移除所有 Unicode 控制字符，或 `./` 本目录序列，使用 Unicode 解析
$normalized = preg_replace('#\p{C}+|^\./#u', '', $path);

// `(?=/)` 右方紧接1个字符 `/`，正向前瞻，不消耗字符 `/`
// `^` 开头
// `$` 结尾

// `.` 右侧紧接一个 `/`，或以 `./` 开头，或以 `./` 结尾
// 移除所有中间的右侧紧接 `/` 的 `.`，移除开头与末尾的 `./`
$normalized = preg_replace('#/\.(?=/)|^\./|\./$#', '', $normalized);


// 匹配0或多个 `/`，所有非 `/.` 字符，`/..` 序列。
// `#U` 末尾修饰符翻转量词贪婪属性，此处无实际效果
// 匹配路径遍历序列与上级目录。用来在规范化中移除
$regex = '#/*[^/\.]+/\.\.#Uu';
while (preg_match($regex, $normalized)) {
    $normalized = preg_replace($regex, '', $normalized);
}
```
- [文档](https://www.pcre.org/original/doc/html/pcrepattern.html)


### burp hackvertor 插件

替换多于2个的空白符到1个空白，确保移除换行

```log
# burp hackvertor 插件
<@regex_replace('[\s]{2,}|[\n]',' ')>

</@regex_replace>
```

### 负向前瞻

```re
(?:(?!>|(%25|%)3e).)*
```
- `(?!)` 负向前瞻，非则成功
- `>|(%25|%)3e` 字面量 `>` 及其双重/单重 URL 编码