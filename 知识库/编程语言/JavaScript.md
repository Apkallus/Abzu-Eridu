### ```atob()```与```btoa()``` 
[mdn文档](https://mdn.org.cn/en-US/docs/Web/API/Window/atob)：

```typescript
const routes: Routes = [
{
path: atob('c2NvcmUtYm9hcmQ='),
component: ScoreBoardComponent
}
]
```
    
> Window 接口的 atob() 方法解码使用 Base64 编码的数据字符串。使用 Window.btoa() 方法编码和传输可能导致通信问题的数据，然后传输它并使用 atob() 方法再次解码数据。

### 阻止当前页面及同源的其他页面修改本地 localStorage 的特定字段

如果仅在单个页面设置，需监测其他页面。
若对所有页面生效则只需第一段阻止本页面存储。

```javascript
const block_key = 'target_key';
window.localStorage.getItem(block_key)

const originalSetItem = localStorage.setItem;
localStorage.setItem = function(key, value) {
    if (key != block_key){
        originalSetItem.call(this, key, value);
    }
};

window.addEventListener('storage', (event) => {
    if (event.key == block_key && event.newValue != null){
        localStorage.removeItem(block_key);
    }
});
```
在当前页面，创建一个`localStorage.setItem`的包装函数，添加储存条件为储存字段非拦截字段。
`storage` 事件，在同源的其他页面存储操作完成时触发。
在当前页面添加存储事件监听器，当其他页面的存储事件触时清空拦截字段的值（清空后值为 `null`，添加条件判断避免死循环）。


### 选择所有编辑链接，将跳转替换为复制链接地址到粘贴板，并阻止跳转

```js
const edit_links = document.querySelectorAll("a.github-edit-link");

edit_links.forEach(link => {
    link.addEventListener('click', (event) => {
        console.log(event.currentTarget.href);
        navigator.clipboard.writeText(event.currentTarget.href);
        event.preventDefault();
    });
});
```

### fetch

<https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API/Using_Fetch>