The noise-fix.patch is the patch applied to Noise challenge source code.

```yaml
services:
  noise-harder:
    image: anssi/fcsc2024-web-noise-harder:latest
    ports:
      - "8000:3000"

```



## 探测与代码审计


测试
- 全局对象
    ```js
    {{ range }}
    ```
    
    ```js
    function range(start, stop, step) {
            if (typeof stop === "undefined") {
            stop = start;
    ...
    ```

- `__proto__` 原型链
    ```js
    {{ range.__proto__ }}
    ```
    
    ```js
    function() {
        for (var _len2 = arguments.length, args = new Array(_len2), _key2 = 0; _key2 < _len2; _key2)
            args[_key2] = arguments[_key2];
        return obj[val].apply(obj, args);
    }
    ```

- `constructor` 原型链
    ```js
    {{ range.constructor }}
    ```
    - 空

- 组合原型链
    ```js
    {{ range.__proto__.constructor }}
    ```
    - 空

- 原型链后 `__proto__`
    ```js
    {{ range.__lookupGetter__("__proto__") }}
    ```
    ```js
    function get __proto__() {
        [native code]
    }
    ```

- 原型链后 `constructor`
    ```js
    {{ range.__lookupGetter__("constructor") }}
    ```
    - 空，`constructor` 或被完全拦截

- 原型链后调用
    ```js
    {{ range.__lookupGetter__("__proto__").call(range, "constructor") }}
    ```
    ```js
    function () {
        [native code]
    }
    ```

- 使用函数原型
    ```js
    {{ range.__lookupGetter__("__proto__").call(range, "constructor")("return 1")() }}
    ```
    - 500 异常

- 其他构造函数
    ```js
    {{ AsyncFunction("return 1")() }}
    {{ GeneratorFunction("return 1")() }}
    ```
    - 500 异常

查看代码，寻找对原型链遍历的防御
- `src\app\server\worker.ts`
    ```ts
    // I've heard that nunjucks is vulnerable to SSTI
    // But I think this is enough to prevent it
    const removeConstructor = (obj: any) =>
    Object.defineProperty(obj.__proto__, "constructor", { value: null });

    removeConstructor(async function* () {});
    removeConstructor(async function () {});
    removeConstructor(function* () {});
    removeConstructor(function () {});
    // ----------------------------
    ```

⚠️ 终止挑战 ⚠️