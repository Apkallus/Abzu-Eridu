https://jsdoc.app

## typedef - 设置自定义类型

```
@typedef [<type>] <namepath>
```

```js
/**
 * 自定义类型 NumberLike，值为数字或字符串
 * @typedef {(number|string)} NumberLike
 */

/**
 * 设置函数参数类型为自定义类型 NumberLike
 * @param {NumberLike} x
 */
function setMagicNumber(x) {
}
```

```js
/**  
 * 类属性注解的自定义类型
 * @typedef {Object} QueryArg
 * @property {string} element - 元素 css 选择器
 * @property {string} grep_mod - 提取类型
 * @property {string[] | undefined} [exclude_list] - 排除元素 css 选择器列表
 */    

class Query {
    /** 对类构造器应用自定义类型
     * @param {QueryArg} arg */  
    constructor({element, grep_mod="outerHTML", exclude_list=undefined}) {
        this.element = element;
        this.grep_mod = grep_mod;
        this.exclude_list = exclude_list;
    }
}
```

## param - 设置函数参数的名称、类型和描述

```js
/**
 * 设置函数参数 somebody，类型 string
 * @param {string} somebody - Somebody's name.
 */
function sayHello(somebody) {
    alert('Hello ' + somebody);
}
```

## property - 记录类、命名空间或其他对象的静态属性列表

```js
/**
* 设置自定义类，并设置其中的属性
* @typedef {Object} User
* @property {string} email
* @property {string} [nickName]
*/
```

## returns - 记录函数返回的值

```
@returns [{type}] [description]
```

```js
/**
 * Returns the sum of a and b
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
function sum(a, b) {
    return a + b;
}
```

## yields - 记录生成器函数返回的值

```
@yields [{type}] [description]
```

```js
/**
 * Generate the Fibonacci sequence of numbers.
 *
 * @yields {number} The next number in the Fibonacci sequence.
 */
function* fibonacci() {}
```