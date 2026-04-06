- 更新
    ```typescript
    db.collection.update(
        { query }, // 查询条件
        { update }, // 更新操作（如 $set）
        { multi: true } // 是否更新多条（默认 false）
    )
    ```
