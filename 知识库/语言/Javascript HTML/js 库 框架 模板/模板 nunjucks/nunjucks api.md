https://mozilla.github.io/nunjucks/cn/api.html

# API

Nunjucks 的 API 包括渲染模板，添加过滤器和扩展，自定义模板加载器等等。

**注意**：nunjucks 并不是在沙盒中运行的，所以使用用户定义的模板可能存在风险。这可能导致的风险有：在服务器上运行时敏感数据被窃取，或是在客户端运行时遭遇跨站脚本攻击（详情请查看 [这里](https://github.com/mozilla/nunjucks-docs/issues/17)）。

## Simple API

如果你不需要深度定制，可以直接使用高层级 API 来加载和渲染模板。

### `render`

```javascript
nunjucks.render(name, [context], [callback])
```

渲染模式时需要两个参数，模板名 **name** 和数据 **context**。如果 **callback** 存在，当渲染完成后会被调用，第一个参数是错误，第二个为返回的结果；如果不存在，`render` 方法会直接返回结果，错误时会抛错。更多查看 [异步的支持]。

```javascript
var res = nunjucks.render('foo.html');

var res = nunjucks.render('foo.html', { username: 'James' });

nunjucks.render('async.html', function(err, res) {
});
```

### `renderString`

```javascript
nunjucks.renderString(str, context, [callback])
```

与 [render] 类似，只是渲染一个字符串而不是渲染加载的模板。

```javascript
var res = nunjucks.renderString('Hello {{ username }}', { username: 'James' });
```