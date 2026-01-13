### HTTP (JavaScript)  
现在，困难的部分开始了……通常你需要渗出的是 JavaScript 在网站上可访问的其他数据，但往往需要通过 HTTP 请求来获取这些数据。在现代 JavaScript 中，HTTP 请求使用 `fetch()` 函数实现。其基本用法如下：

```javascript
fetch("http://google.com").then(response => response.text()).then(website_content => ???);
```

当然，`???` 部分是你想在网站内容上执行的代码。这个 API 看起来非常复杂，一方面是因为 JavaScript 本身的设计特点，另一方面是因为它需要解决一个难题：它必须在网络错误、CPU 负载、笔记本电脑休眠与唤醒、防火墙等可能干扰资源加载和运行的复杂环境中执行逻辑。

上述代码使用了 JavaScript 的 "Promise"，这是一种复杂的编程模式，允许你为*尚未*可用的数据编写*将要*执行的逻辑。`.then()` 是 Promise 的一部分，用于指定最终要执行的代码。流程大致如下：

1. `fetch()` 返回一个 Promise 并开始获取 `http://google.com`。这可能需要一段时间，可能永远不会成功，也可能立即成功。无论如何，它最初返回一个 `promise` 对象，该对象具有一个 `then()` 成员函数，会在响应可用时运行。
2. 响应可用后，Promise 中的代码执行。这段代码获取 Promise 返回的响应并调用 `response.text()`，从而获取 `http://google.com` 返回的*完整*文本内容。由于完全加载可能需要时间，这*同样*返回一个 Promise，而*该* Promise 也有一个我们可以指定代码的 `.then()` 方法。
3. 最后，所有内容都可用时，我们最终的 Promise 代码运行。这可以是任何操作，但在我们的大部分应用场景中，这里就是像之前挑战中那样渗出数据的地方。

这可能非常难以理解和调试。请准备好在实际模式下的 Firefox 中进行调试。  
在本关卡中，Flag 不再整齐地包裹在 JavaScript 中，它只是普通的旧文本。你需要获取并渗出它以得分。祝你好运！
