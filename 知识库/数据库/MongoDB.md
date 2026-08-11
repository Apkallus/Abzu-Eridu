
见 “Web - NoSQL” 主题，其中的示例基于 MongoDB 

- 更新
    ```typescript
    db.collection.update(
        { query }, // 查询条件
        { update }, // 更新操作（如 $set）
        { multi: true } // 是否更新多条（默认 false）
    )
    ```

### $regex

www.mongodb.com/zh-cn/docs/manual/reference/operator/query/regex/

```mongodb
{ <field>: { $regex: /.*admin.*/, $options: '<options>' } }
{ "<field>": { "$regex": ".*admin.*", "$options": "<options>" } }
{ <field>: { $regex: /.*admin.*/<options> } }
```
- json 字符串中无需外层斜杠 `/`