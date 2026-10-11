[测试](https://play.vuejs.org/)
[v2](https://v2.vuejs.org/v2/guide/)
[v2 - v3 差异](https://v3-migration.vuejs.org/breaking-changes/)

[portswigger 研究文章](https://portswigger.net/research/evading-defences-using-vuejs-script-gadgets)

# API

## Global API

### Application
​
https://cn.vuejs.org/api/application

#### createApp() 

创建一个应用实例。
​
```js
function createApp(rootComponent: Component, rootProps?: object): App
```

- 第一个参数是根组件。
- 第二个参数可选，它是要传递给根组件的 props。

示例：
- 直接内联根组件：
    ```js
    import { createApp } from 'vue'

    const app = createApp({
    /* 根组件选项 */
    })
    ```

- 使用从别处导入的组件：
    ```js
    import { createApp } from 'vue'
    import App from './App.vue'

    const app = createApp(App)
    ```

---

v2

每个 Vue 应用都从使用 `Vue` 函数创建一个新的 **Vue 实例** 开始：

```js
var vm = new Vue({
  // options
})
```

尽管 Vue 的设计并非严格遵循 [MVVM 模式](https://en.wikipedia.org/wiki/Model_View_ViewModel)，但它部分受到该模式的启发。按照惯例，我们通常使用变量 `vm`（ViewModel 的缩写）来指代 Vue 实例。

创建 Vue 实例时，需要传入一个 **选项对象**。本指南的大部分内容描述如何使用这些选项来创建所需的行为。作为参考，你也可以在 [API 参考] 中浏览完整的选项列表。

一个 Vue 应用由使用 `new Vue` 创建的 **根 Vue 实例** 组成，并可选地组织为一棵嵌套、可复用组件的树。例如，一个待办事项应用的组件树可能如下所示：

```text
Root Instance
└─ TodoList
   ├─ TodoItem
   │  ├─ TodoButtonDelete
   │  └─ TodoButtonEdit
   └─ TodoListFooter
      ├─ TodosButtonClear
      └─ TodoListStatistics
```

我们稍后会详细讨论 [组件系统]。所有 Vue 组件也都是 Vue 实例，因此接受相同的选项对象（少数根实例特有的选项除外）。


## 选项式 API

https://cn.vuejs.org/api/component-instance.html

### 组件实例
​
本页文档描述了组件公共实例 (即 `this`) 上暴露的内置属性和方法。

本页罗列的所有属性，除了 `$data` 下的嵌套属性之外，都是只读的。

#### `$el`
​
该组件实例管理的 DOM 根节点。

```js
interface ComponentPublicInstance {
  $el: any
}
```

`$el` 直到组件 `挂载完成 (mounted)` 之前都会是 `undefined`。
- 对于单一根元素的组件，`$el` 将会指向该根元素。
- 对于以文本节点为根的组件，`$el` 将会指向该文本节点。
- 对于以多个元素为根的组件，`$el` 将是一个仅作占位符的 DOM 节点，Vue 使用它来跟踪组件在 DOM 中的位置 (文本节点或 SSR 激活模式下的注释节点)。

## Built-in 

https://vuejs.org/api/built-in-directives.html

### Directives 

#### 🎯 `v-html`

更新元素的 [innerHTML]。

- **期望类型：**
  `string`

- **详情**
  `v-html` 的内容会作为普通 HTML 插入——Vue 模板语法不会被处理。如果你发现自己试图使用 `v-html` 来组合模板，请尝试改用组件来重新思考解决方案。

  > **安全提示**
  > 在网站上动态渲染任意 HTML 可能非常危险，因为它很容易导致 [XSS 攻击]。只应在可信内容上使用 `v-html`，**绝不要**在用户提供的内容上使用。

  在 [Single-File Components] 中，`scoped` 样式不会应用到 `v-html` 内部的内容，因为该 HTML 不会被 Vue 的模板编译器处理。如果你希望用 scoped CSS 定位 `v-html` 内容，可以改用 [CSS modules]，或者添加一个额外的全局 `<style>` 元素并手动采用作用域策略，例如 BEM。

- **示例**
  ```html
  <div v-html="html"></div>
  ```
  - 此处设置变量值作为 HTML

- **另见**
  [Template Syntax - Raw HTML]