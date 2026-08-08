# 第 16 章：客户端攻击

在应用安全的前现代时代（Web 1.0），人们认为 Web 应用的客户端（即浏览器）组件并不是黑客常见的攻击向量。因此，公司认为应用的大部分风险面在服务端，并在确保浏览器客户端安全方面投入甚少。

随着 Web 2.0 的到来，越来越多以前仅在服务端存在的功能被推向客户端。复杂的计算操作被从后端 Java 或 C 重写为客户端 JavaScript。后端数据存储被本地存储、会话存储或 IndexedDB 所取代。

异步 JavaScript 和 XML（AJAX）类型的网络查询使得开发能够维护、更新和存储状态的客户端应用成为可能。对 JavaScript 编程语言和浏览器 DOM 的客户端改进，使得复杂的组件生命周期（包括更新、渲染、重新渲染、删除等）得以实现——类似于桌面应用。

总而言之，Web 应用的总体架构从服务器负责所有计算操作、客户端仅为渲染（视图）层的模型，转变为服务器和客户端都负责各种复杂计算任务的模型。

现代 Web 反映了这种变化：世界上所有最大的网站都同时使用复杂的服务端和客户端功能。服务器不再是复杂计算操作的主要机制，因此安全专业人员需要快速更新技能，以能够帮助交付安全的服务端软件和安全的客户端软件。

本章涵盖了通过将客户端而非服务器作为目标来利用 Web 应用的常见方法。

## 攻击浏览器客户端的方法

首先，在考虑客户端攻击时，从排除服务器开始。客户端攻击是指任何不需要易受攻击的 Web 服务器或对客户端服务器进行网络调用的攻击形式（可利用的漏洞）。从分类上看，攻击浏览器客户端主要有两种方式：针对客户端的攻击和特定于客户端的攻击。

### 针对客户端的攻击

首先，存在一些可能影响客户端或服务器的通用漏洞形式。我们在前一章评估的正则表达式拒绝服务（ReDoS）漏洞就是一个例子。

正则表达式是一种常见的编程工具，几乎在所有主流服务端语言（如 Java、C#、Python）中都有实现，但也存在于浏览器（JavaScript）和其他较少见的客户端（如 Adobe Air）中。ReDoS 攻击并不总是客户端攻击，但当浏览器客户端上的 JavaScript 代码结构使得客户端无需任何网络调用或服务器交互即可受到攻击时，它偶尔也可能是一种客户端攻击。

### 特定于客户端的攻击

其次，有些客户端攻击仅存在于客户端，很可能永远不会出现在服务器上（除非服务器试图模拟 Web 浏览器）。我们在第 10 章中介绍了基于 DOM 的跨站脚本（DOM XSS）。这是仅针对浏览器客户端起作用的客户端攻击的典型例子。

在 DOM XSS 中，与存储型或反射型 XSS 不同，接收器和源都发生在浏览器中。例如，来自 `window.location.hash` 的字符串通过 `eval()` 被渲染为代码，从而导致客户端脚本执行。

因此，DOM XSS 是客户端攻击的典型代表。与 DOM XSS 和 ReDoS 类似，我们在本章中讨论的其他攻击也能够完全在浏览器客户端内发生。然而，在深入探讨特定攻击之前，让我们先看看为什么客户端攻击很重要。

### 客户端攻击的优势

在 DOM XSS 攻击的情况下，接收器和源都仅存在于浏览器 DOM 中。这意味着 DOM XSS（以及许多其他客户端攻击）可以在任何 Web 服务器都未察觉的情况下被利用。

载荷可以直接传递给浏览器客户端，从而避开那些可能记录网络流量并试图发现畸形请求的 Web 服务器。因此，客户端攻击往往是对成熟企业来说最难检测的攻击类型之一。

作为白帽黑客，这意味着可能可以在不被追踪或检测的情况下利用用户。作为漏洞赏金猎人，这意味着攻击者在客户端上可利用的攻击面不太可能已经被发现和修复，从而导致更高的发现概率。

除了无需服务器网络连接使客户端攻击能够悄无声息地溜走之外，客户端攻击对于恶意用户来说也可能更容易在未被识别的情况下开发。考虑黑客试图针对 Web 服务器开发利用的情况。在复杂 Web 应用的情况下，开发的第一个载荷成功渗透并绕过所有现有安全机制的可能性很小。因此，通常需要多次尝试传递载荷。

事实上，大多数成功的黑客会将这些尝试自动化以节省时间。他们通常每小时发送数十个载荷，直到有一个成功。所有这些网络请求都增加了被人工、防火墙或网络扫描工具检测到的概率。

对于客户端攻击，可以轻松地从企业下载整个 HTML/CSS/JS 客户端 Web 应用，然后关闭网络。从那时起，可以对本地客户端应用进行数百万次攻击尝试，而不会向生产 Web 服务器发送任何数据。

## 原型污染攻击

近年来，随着 npm 和其他 JavaScript 包管理器的兴起，原型污染攻击也在增加。原型污染是一种仅适用于使用原型继承系统（如 JavaScript）的语言的攻击形式，这种继承形式不同于 Java、C# 或其他流行语言中的传统 OOP 继承。原型污染攻击允许您通过破坏您有权访问的对象来破坏您无权访问的对象，该对象与您要攻击的对象存在原型继承关系。

### 理解原型污染

考虑以下用客户端 JavaScript 编写的代码片段：

```javascript
const Technician = function(name, birthdate, paymentId) {
  this.name = name;
  this.birthdate = birthdate;
  this.paymentId = paymentId; // 用于支付工作报酬
}
```

上述函数是在原型编程语言中实现的所谓伪类或类类结构。使用此伪类，您可以实例化一个从它派生的对象作为蓝图，该对象将继承父伪类的状态和函数。例如：

```javascript
const Bob = new Technician("Bob", "12/01/1970", 12345);
console.log(Bob.toString()); // [object Object]
```

JavaScript 和其他基于原型继承的语言存储这些数据的方式是在所谓的原型链中。每个对象在 JavaScript 中都有自己的原型，其中包含对其从中继承函数和数据的所有祖先对象的引用。

我们可以通过比较 Bob 的原型和 Technician 的原型来验证 Bob 确实是 Technician 的一个实例。注意，为了访问 Bob 的原型信息，我们将使用 `Bob.__proto__` 并将其与 `Technician.prototype` 进行比较。这是因为 `__proto__` 指向实际的 prototype 对象，而 `prototype` 指向用于构建更多原型的蓝图。由于 `Technician` 是构建实例 `Bob` 的构造函数，当两者使用相等运算符比较时，将返回 `true`：

```javascript
Bob.__proto__ == Technician.prototype; // true
```

除了验证 Bob 是 Technician 之外，我们还可以通过两种方式之一验证 Bob 是一个对象。首先，知道 Bob 继承自 Technician，我们可以手动沿着继承链向上走，因为 Technician 不继承自任何其他自定义对象：

```javascript
Bob.__proto__.__proto__ == Object.prototype; // true
```

接下来，我们可以使用 `instanceof` 运算符再次确认 Bob 确实是 Object 的实例，因为它是 Technician 的实例，而 Technician 像所有 JavaScript 函数一样继承自 Object：

```javascript
Bob instanceof Object; // true
```

我们也可以使用 `instanceof` 运算符来确认 Bob 是 Technician 的实例。可以将此运算符视为不必手动攀爬原型链的快捷方式：

```javascript
Bob instanceof Technician; // true
```

有了这些新知识，我们可以得出结论，此应用的继承层次结构如下：

`(Object) -> (Technician) -> (Bob)`

在能够部署原型污染攻击以入侵基于 JavaScript 原型的应用之前，最后要注意的一点是信息如何通过原型链传播。

之前我们调用了对象 Bob 的 `toString()` 函数。当我们这样做时，它返回了字符串 `[object Object]`，尽管 Bob 上没有定义返回此字符串的函数。这是因为 `Object` 包含一个 `toString()` 函数，当调用函数但在当前对象上未找到时，解释器会沿着原型链向上遍历每一层，直到找到同名函数。

如果在此原型遍历期间未找到函数，则会抛出错误。但是，如果父类包含一个适当命名的函数，则会调用该函数来代替当前类上的函数。

换句话说，`toString()` 函数不存在于 Bob 上。因为该函数在 Bob 上不存在，解释器会向上查找原型链，先停在 `Technician`，最后到达 `Object`，在那里它最终找到了适当命名的 `toString()` 函数。此过程如表 16-1 所示。

**表 16-1. 原型链**

| 步骤 | 调用的函数 | 评估的类 | 找到？ |
| :--- | :--- | :--- | :--- |
| 1 | `toString()` | Bob | False |
| 2 | `toString()` | Technician | False |
| 3 | `toString()` | Object | True |

在这种情况下，我们甚至可以在没有访问 Bob 的情况下对 Bob 类执行原型污染。如果我们能找到修改 `Technician` 或 `Object` 原型的函数，我们就可以改变 `toString()` 函数的功能，从而也影响 Bob。

考虑以下原型污染载荷，它作用于 Bob 类，尽管没有直接针对它：

```javascript
// 向 technician 类添加功能
const addTechnicianFunctionality = function(obj) {
  Technician.prototype[obj.name] = obj.data
}

// 用户输入载荷
{
  name: "toString",
  data: `function() { console.log("polluted!"); }`
}

Bob.toString(); // 打印 "polluted!"
```

在这种情况下，UI 预期 Technician 是一个可调整的类，用于客户端状态管理目的，但没有预期 Bob 也会被调整。通过更改 Technician 原型上的 `toString` 函数，Bob 的 `toString` 函数也被污染了。

原型污染攻击利用了原型继承系统如前所述在原型链上下遍历的特性。这允许攻击者污染单个对象，然后该对象将有效地“扩散”到附近可能无法直接攻击的相关对象。

### 利用原型污染进行攻击

之前，我们讨论了原型和原型链遍历的工作原理。现在我们知道，如果函数或属性在当前对象中不存在，它将沿着链向上查找，直到找到同名函数或属性。

当客户端无法进行完整脚本执行（XSS）时，很可能会有许多原型合并和更新的情况。这些是我们利用原型污染攻击的攻击面区域。

考虑 npm 开源 JavaScript 包 `merge` v2.0。尽管语法简单，但该包被广泛认为容易受到原型污染攻击。merge 库有一个 `merge()` 函数，可以简单地合并两个对象。它经常用于在 Node.js 服务器或基于 JavaScript 的客户端上建模状态。

让我们再次尝试污染 Bob 对象，以添加一个新属性 `isAdmin: true`。假设我们在 JavaScript 客户端代码中找到一个使用 `merge()` 函数合并 `Object` 和 `userData` 的代码片段。使用载荷 `{ isAdmin: true }` 作用于 `Object` 将导致 `Object` 获得 `{ isAdmin: true }` 属性，但由于 `Object` 原型尚未更新，因此不会反映在 Bob 上。

我们可以通过以下载荷看到这次攻击尝试的结果：

```javascript
merge(Object, { isAdmin: true });
console.log(Bob.isAdmin); // undefined
```

然而，当我们针对原型附加此载荷时，我们看到了不同的结果：

```javascript
merge(Object, { "__proto__.isAdmin": true });
console.log(Bob.isAdmin); // true
```

这里我们成功地污染了 `Object` 原型，使得 Bob 也变得易受攻击。

请注意，这个特定的库也容易受到构造函数污染。我们可以不直接污染 Object 原型，而是污染构造函数函数，它由 JavaScript 语言自动附加到 Object，并在每次创建 Object 实例时使用：

```javascript
merge(Object, { "constructor.prototype.isAdmin": true });
console.log(Bob.isAdmin); // true
```

在这种情况下，每个继承自 Object 的实例都会调用构造函数，导致污染与直接污染 Object 原型具有相同的最终结果。

### 原型污染原型

在获得对 Web 应用的原型污染后，您可以利用它做几件事来获取信息或干扰预期的客户端执行。

**拒绝服务**  
原型污染攻击可用于减慢或干扰正常的客户端脚本执行。例如，将值更改为浮点数而不是整数。这将在后续引起错误，并干扰客户端应用的预期用途。

**属性注入**  
如果脚本依赖于函数调用的特定值，则该值可以通过原型污染进行修改。这可能导致以最终用户未预期的方式对网络进行意外调用或在客户端上调用功能。

**远程代码执行**  
一般来说，这是原型污染最糟糕的情况。在客户端领域，原型污染将攻击升级为 XSS；在 Node.js（服务端）领域，攻击可以升级为真正的服务端代码执行。这两种结果都会导致应用状态、数据和功能受到破坏。通常，将原型污染升级为代码执行需要一个脚本执行接收器，如 `eval()`，或一个 DOM 节点生成函数，如 `DOMParser.parseFromString()`。

## 点击劫持攻击

点击劫持攻击是发生在浏览器内针对最终用户的微妙但影响重大的攻击。点击劫持攻击将恶意 UI 元素与良性 UI 元素合并，或透明地诱骗浏览器将输入发送到恶意服务器或函数调用，而非预期的函数调用。

有多种使用点击劫持攻击应用的方法，实现涉及 JavaScript、HTML 和 CSS，可以单独使用或与其他技术结合。可以将点击劫持攻击视为一种用户界面键盘记录器。当针对不知情的最终用户部署时，点击劫持攻击可以使攻击者窃取未预料会被第三方读取的有价值的用户输入。

### 摄像头和麦克风利用

点击劫持最著名的早期例子之一是 2008 年在安全研究人员 Robert Hansen 和 Jeremiah Grossman 发现后公开的 Adobe Flash 麦克风和摄像头劫持漏洞。这种点击劫持攻击以一组 Web 链接的形式出现，这些链接看起来像是一个完全与 Adobe Flash Player 无关的游戏或网页。

最终用户不知道的是，此游戏或网页中的每次点击都对应于其下方 iframe 中的 Adobe Flash 基于 Web 的设置页面上的点击。Adobe Flash 设置页面在 iframe 中加载，其不透明度设置为零，因此对最终用户不可见。

在与点击劫持网页交互时，最终用户被诱骗将点击传递到特权 Adobe Flash 隐私设置。结果是 Adobe Flash 浏览器插件将与黑客共享摄像头和麦克风控制。这成为信息安全领域中最著名的点击劫持事件之一，因为它能够利用插件升级到浏览器沙箱之外，并获得对计算机硬件的特权访问。

### 创建点击劫持利用

现代点击劫持可以通过多种方式完成。最常见的方法是生成一个看似合法的网站，其下方包含一个指向您要攻击的网站的不可见 iframe。

考虑以下示例网站：

```html
<html>
  <head>
    <title>Clickjacker</title>
  </head>
  <body>
    <div id="clickjacker">
      <span id="fake_button">click me</span>
    </div>
    <iframe id="target_website" src="target-website.com"></iframe>
  </body>
</html>
```

在此示例中，我们通过在 iframe 中实例化 target-website.com（该 iframe 出现在 `clickjacker` div 下方）来攻击它。我们可以使用以下 CSS 类使 target-website.com 对最终用户不可见：

```css
#target_website {
  opacity: 0;
}
```

`clickjacker` div 包含一个按钮，可以通过 CSS 定位将其直接放置在 iframe 中合法按钮的上方：

```css
#fake_button {
  position: relative;
  right: 25px;
  top: 25px;
  pointer-events: none;
  background-color: blue;
}
```

通过向 `#fake_button` 添加 `pointer-events: none` CSS 属性，对 `#fake_button` 的任何交互（点击）都将传递到其下方的元素。在本例中，其下方的元素存在于最终用户不打算点击的 iframe 中。当点击 `#fake_button` 时，点击事件将传递到 iframe 并触发另一个网站中的功能。

不幸的是，由于浏览器的安全模型，iframe 很可能可以访问被框架网站的会话 cookie。这意味着点击可能对 Web 服务器发起特权请求，例如调用 API 将配置文件公开或发起金融交易。

针对任何缺乏适当框架控制的 Web 应用的点击劫持攻击，是诱骗用户代表攻击者调用功能的最简单方法之一。

## 标签劫持与反向标签劫持

标签劫持及其姊妹攻击反向标签劫持是一种客户端攻击，它结合了网络钓鱼攻击（诱骗最终用户与恶意网页交互）和重定向攻击（将当前网页重定向到恶意网页）的元素。

在标签劫持攻击中，浏览器 DOM API 被滥用，以将当前页面重定向到新页面，或用黑客提供的 HTML/CSS 和 JS 覆盖当前页面的内容。

### 传统标签劫持

传统标签劫持的实现通过滥用所有主流浏览器都附带的 `window` 对象进行操作，该对象被定义为 WHATWG DOM 规范的一部分。当通过附加到 `window` 对象的 `window.open()` 函数打开新标签页时，函数调用会返回对新标签页的 `window` 对象的引用。

在传统标签劫持方法中，调用新标签页的网站是攻击者，如以下代码示例所示：

```html
<button onclick="goToLegitWebsite()">click to go to legit website</button>
```

```javascript
const goToLegitWebsite = function() {
  // 打开指向 legit-website.com 的新标签页
  const windowObj = window.open("https://website-b.com");
  // 5 分钟后，将另一个标签页更改为恶意网站
  setTimeout(() => {
    windowObj.location.replace("https://website-c.com");
  }, 1000 * 60 * 5);
};
```

在此传统标签劫持示例中，网站 A 向用户呈现一个链接，以在另一个标签页中打开网站 B。新标签页打开并加载了网站 B，但由于它是由 `open()` 函数调用打开的，因此对新标签页启动的 `window` 对象的引用存储在打开标签页（网站 A）中。

在稍后的时间点，在最终用户已验证新标签页为合法之后，打开标签页（网站 A）进入网站 B 的 DOM API 副本，并使用 `windowObj.location.replace()` 发起重定向。网站 B 现在被重定向到网站 C。网站 C 在外观上与网站 B（合法网站）完全相同，但当用户尝试重新登录时，它只是复制他们的凭据，将其发送到黑客的服务器，并重定向到网站 B 上的错误页面。

此攻击工作流程相当复杂，但最终结果是包含网站 B 的标签页被网站 C（黑客维护的恶意网站）暂时替换。由于用户最初验证了新标签页包含合法网站，他们不太可能注意到内容的快速变化，即使在他们浏览另一个标签页时也可能发生。因此，诱骗用户将凭据或其他敏感信息输入到被标签劫持的标签页中，比传统的网络钓鱼攻击要容易得多。

整个工作流程之所以成为可能，是因为浏览器 DOM 函数 `window.open` 返回对新标签页中 `window` 对象的引用，并允许打开标签页对新标签页进行函数调用。利用此漏洞只需开发一个包含标签劫持 JavaScript 代码的网站，开发一个匹配合法网站外观和用户体验的网络钓鱼网站，然后诱骗最终用户点击链接打开一个（被入侵的）新标签页。

### 反向标签劫持

反向标签劫持与传统标签劫持的方向相反。攻击者不是启动新标签页的网站，而是在新标签页中打开的网站，并针对初始标签页。通过反向标签劫持攻击最终用户有多种方法，每种方法都依赖于一个标签页对其打开它的标签页进行 DOM API 调用的机制。

**DOM API 攻击**  
通过反向标签劫持攻击的最简单方法同样是设置一个恶意网站。然后，您说服合法网站使用 `window.open()` 函数调用打开您的恶意网站。

当 `window.open()` 被调用以创建新标签页时，开启者默认会将其 `window` 对象的引用传递给新标签页。这与传统标签劫持攻击的工作方式类似。

考虑以下示例：

```html
<!-- 合法网站的 UI 元素 -->
<button onclick="openTab()">click me</button>
```

```javascript
// 合法网站的脚本
window.open("https://malicious-website.com");

// 恶意网站的脚本
window.opener.location.replace("https://get-hacked.com");
```

如您所见，通过引用新创建标签页的 `window` 对象上的 `opener` 属性，新标签页可以开始控制生成它的原始标签页。通过控制原始标签页，新标签页现在可以将原始标签页的位置从合法网站更改为非法网站，并使用该新网站窃取最终用户的凭据和其他信息。

与传统标签劫持非常相似，此攻击通过开发和托管一个对开启者的 `window.opener` 属性进行函数调用的恶意网站来轻松执行。主要缺点是，除了 `window.opener` 属性之外的其他形式的标签页生成和重定向并不都会生成带有 `window.opener` 引用的标签页，因此并非所有网站都会受到这种形式的攻击。

**HTML 链接攻击**  
如果您打算通过反向标签劫持攻击的网站中 `window.opener` 属性不可用，但您可以生成 HTML 链接或诱骗该网站代表您生成 HTML 链接，只要该链接使用 `target="_blank"` 属性，就可以执行攻击。

`target="_blank"` HTML 链接属性也会强制在包含 `opener` 引用的 `window` 对象中生成新标签页：

```html
<!-- 合法网站，在用户生成的链接中生成 -->
<a href="https://malicious-website.com" target="_blank">click me</a>
```

```javascript
// 恶意网站脚本
window.opener.location.replace("https://get-hacked.com");
```

**Iframe 攻击**  
最后，如果上述两种反向标签劫持攻击向量都不可能，您可以在 iframe 内执行反向标签劫持。如果调用的 iframe 链接到您的恶意网站，并且 iframe 没有实现针对反向标签劫持的缓解措施（例如 `sandbox` 属性或 CSP 策略），您将能够通过 DOM 属性 `window.parent` 访问父窗口对象：

```html
<!-- 合法网站 -->
<iframe src="https://malicious-website.com"></iframe>
```

```javascript
// 恶意网站 JavaScript
window.parent.location.replace("https://get-hacked.com");
```

总之，标签劫持攻击依赖于一个标签页通过不安全的浏览器 DOM API 函数调用获得对控制另一个标签页的 `window` 对象的访问。一旦恶意标签页通过直接 DOM 调用、不安全的 HTML 链接或不安全的 iframe 生成获得了对该 `window` 对象的访问，合法标签页现在就受到了入侵，因为浏览器 DOM 提供了可以从任何位置调用的控制 API。

## 小结

总而言之，客户端攻击要么仅针对浏览器客户端，要么能够在不向 Web 服务器发起请求的情况下部署到浏览器客户端。像标签劫持、点击劫持和原型污染这样的客户端攻击允许攻击者入侵用户的应用状态并拦截他们的击键——通常是在交付客户端应用代码的服务器不知情且无法检测的情况下。

对于任何类型的进攻性专家来说，理解客户端攻击是一个全面的现代工具包中必不可少的组成部分。
