https://twig.symfony.com/


- 全局变量
    https://twig.symfony.com/doc/2.x/templates.html#global-variables

    - `_self`: references the current template name;
    - `_context`: references the current context;
    - `_charset`: references the current charset.


查阅文档，寻找可对数组操作的方式
- 过滤器
    https://twig.symfony.com/doc/3.x/filters/index.html
    - 语法： `|` 传递过滤器
    - `keys` 返回序列映射
    - `join` 合并序列到字符串

- 查看可用对象的模板载荷
    `_context|keys|join('-')`

似乎除非显式设置，否则缺乏列举属性的方式。尝试爆破或触发可能的错误后揭示方法或泄露源码