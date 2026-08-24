## 

- `puts File.read('/flag')`


- 执行系统命令

    ```ruby
    system("id")

    `id`

    %x{id} 
    %x[id]
    %x|id|
    %x(id)
    %x<id>
    ```

## rubyonrails

### 路由

https://guides.rubyonrails.org/routing.html

#### format

通过请求 `'/foo/bar.json'`，你的 `params[:pages]` 将等于 `'foo/bar'`，并且请求格式（JSON）会包含在 `params[:format]` 中。

关于 `format` 的默认行为是：如果它被包含在 URL 中，Rails 会自动从 URL 中捕获它并将其放入 `params[:format]`，但 `format` 并不是 URL 中必需的部分。
