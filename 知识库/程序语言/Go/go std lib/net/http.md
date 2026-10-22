https://pkg.go.dev/net/http

## type ServeMux —— HTTP 请求多路复用器

```go
type ServeMux struct {
    // 包含已过滤或未导出的字段
}
```

`ServeMux` 是 HTTP 请求多路复用器。它将每个传入请求的 URL 与已注册的模式列表进行匹配，并调用与 URL 最匹配的模式对应的处理程序。

### 模式

模式可以匹配请求的方法、主机和路径。示例如下：

- `"/index.html"` 匹配任意主机、任意方法下路径为 `"/index.html"` 的请求。
- `"GET /static/"` 匹配路径以 `"/static/"` 开头的 GET 请求。
- `"example.com/"` 匹配发送到主机 `"example.com"` 的任意请求。
- `"example.com/{$}"` 匹配主机为 `"example.com"` 且路径为 `"/"` 的请求。
- `"/b/{bucket}/o/{objectname...}"` 匹配第一段为 `"b"`、第三段为 `"o"` 的路径。名称 `"bucket"` 表示第二段，`"objectname"` 表示路径的剩余部分。

通常，模式形式如下：

```text
[METHOD ][HOST]/[PATH]
```

所有三个部分都是可选的；`"/"` 是有效模式。如果存在 `METHOD`，其后必须至少有一个空格或制表符。

模式中的字面量（即非通配符）部分以区分大小写的方式匹配请求的对应部分。

没有方法的模式匹配所有方法。方法为 `GET` 的模式同时匹配 `GET` 和 `HEAD` 请求。除此之外，方法必须精确匹配。

没有主机的模式匹配所有主机。带主机的模式仅匹配该主机上的 URL。

路径可以包含 `{NAME}` 或 `{NAME...}` 形式的通配符段。例如 `"/b/{bucket}/o/{objectname...}"`。通配符名称必须是有效的 Go 标识符。通配符必须占据完整的路径段：前面必须有斜杠，后面必须是斜杠或字符串结尾。例如 `"/b_{bucket}"` 不是有效模式。

通常，通配符只匹配单个路径段，并在请求 URL 中的下一个字面量斜杠（不是 `%2F`）处结束。但如果存在 `...`，则通配符匹配 URL 路径的剩余部分，包括斜杠。（因此，`...` 通配符出现在模式末尾以外的任何位置都是无效的。）通配符的匹配值可以通过使用通配符名称调用 `Request.PathValue` 获得。路径末尾的斜杠充当匿名的 `...` 通配符。

特殊通配符 `{$}` 仅匹配 URL 的结尾。例如，模式 `"/{$}"` 仅匹配路径 `"/"`，而模式 `"/"` 匹配所有路径。

匹配时，模式路径和传入请求路径都会逐段反转义。因此，例如路径 `"/a%2Fb/100%25"` 被视为包含 `"a/b"` 和 `"100%"` 两段。模式 `"/a%2fb/"` 可以匹配它，但模式 `"/a/b/"` 不能。

### 优先级

如果两个或多个模式匹配同一请求，则最具体的模式优先。如果 P1 匹配的是 P2 所匹配请求的严格子集，即 P2 匹配 P1 的所有请求并且还匹配更多请求，则模式 P1 比 P2 更具体。如果两者都不更具体，则这些模式冲突。此规则有一个为了向后兼容而设的例外：如果两个模式原本会冲突，且一个有主机而另一个没有，则有主机的模式优先。如果传递给 `ServeMux.Handle` 或 `ServeMux.HandleFunc` 的模式与已注册的另一个模式冲突，这些函数会触发 `panic`。

作为一般规则的示例，`"/images/thumbnails/"` 比 `"/images/"` 更具体，因此两者都可以注册。前者匹配以 `"/images/thumbnails/"` 开头的路径，后者将匹配 `"/images/"` 子树中的任何其他路径。

再举一个例子，考虑模式 `"GET /"` 和 `"/index.html"`：两者都匹配对 `"/index.html"` 的 GET 请求，但前者模式匹配所有其他 GET 和 HEAD 请求，而后者匹配使用不同方法对 `"/index.html"` 的任意请求。这些模式冲突。

### 尾部斜杠重定向

考虑一个 `ServeMux`，其中使用尾部斜杠或 `...` 通配符为某个子树注册了处理程序。如果 `ServeMux` 收到对子树根路径且不带尾部斜杠的请求，它会通过添加尾部斜杠来重定向该请求。可以通过为不带尾部斜杠或 `...` 通配符的路径单独注册来覆盖此行为。例如，注册 `"/images/"` 会导致 `ServeMux` 将对 `"/images"` 的请求重定向到 `"/images/"`，除非 `"/images"` 已被单独注册。

### 请求清理

`ServeMux` 还负责清理 URL 请求路径和 `Host` 头，去除端口号，并将任何包含 `.` 或 `..` 段或重复斜杠的请求重定向到等价的更干净 URL。诸如 `"%2e"`（表示 `.`）和 `"%2f"`（表示 `/`）这样的转义路径元素会被保留，并且不会被视为请求路由的分隔符。

### 兼容性

`ServeMux` 的模式语法和匹配行为在 Go 1.22 中发生了显著变化。要恢复旧行为，请将 `GODEBUG` 环境变量设置为 `"httpmuxgo121=1"` 这个值。此设置只在程序启动时读取一次；执行期间的更改将被忽略。

向后不兼容的变更包括：

- 在 Go 1.21 中，通配符只是普通的字面量路径段。例如，模式 `"/{x}"` 在 Go 1.21 中只匹配该路径，但在 Go 1.22 中将匹配任意单段路径。
- 在 Go 1.21 中，除非模式为空或与现有模式冲突，否则不会拒绝任何模式。在 Go 1.22 中，语法无效的模式会导致 `ServeMux.Handle` 和 `ServeMux.HandleFunc` 触发 `panic`。例如，在 Go 1.21 中，模式 `"/{"` 和 `"/a{x}"` 匹配它们自身，但在 Go 1.22 中它们无效，注册时会触发 `panic`。
- 在 Go 1.22 中，模式的每个段都会被反转义；这在 Go 1.21 中并未进行。例如，在 Go 1.22 中，模式 `"/%61"` 匹配路径 `"/a"`（`"%61"` 是 `"a"` 的 URL 转义序列），但在 Go 1.21 中它只匹配路径 `"/%2561"`（其中 `"%25"` 是百分号的转义）。
- 将模式与路径匹配时，在 Go 1.22 中路径的每个段都会被反转义；在 Go 1.21 中，整个路径会被反转义。此变更主要影响带有紧邻斜杠的 `%2F` 转义的路径处理方式。详情参见 https://go.dev/issue/21955。

### func NewServeMux

```go
func NewServeMux() *ServeMux
```

`NewServeMux` 分配并返回一个新的 `ServeMux` 实例。

### func (*ServeMux) Handle

```go
func (mux *ServeMux) Handle(pattern string, handler Handler)
```

`Handle` 为给定模式注册处理程序。如果给定模式与已注册的模式冲突，或者模式无效，`Handle` 会触发 `panic`。

有关有效模式和冲突规则的详细信息，请参见 `ServeMux` 的说明。

### func (*ServeMux) HandleFunc

```go
func (mux *ServeMux) HandleFunc(pattern string, handler func(ResponseWriter, *Request))
```

`HandleFunc` 为给定模式注册处理函数。如果给定模式与已注册的模式冲突，或者模式无效，`HandleFunc` 会触发 `panic`。

有关有效模式和冲突规则的详细信息，请参见 `ServeMux` 的说明。

### func (*ServeMux) Handler

自 Go 1.1 起可用。

```go
func (mux *ServeMux) Handler(r *Request) (h Handler, pattern string)
```

`Handler` 返回用于给定请求的处理程序，并参考 `r.Method`、`r.Host` 和 `r.URL.Path` 等字段。它总是返回非 nil 处理程序。如果路径不是规范形式，处理程序将是一个内部生成的、重定向到规范路径的处理程序。如果主机包含端口，匹配处理程序时会忽略该端口。

对于 CONNECT 请求，路径和主机会原样使用。

`Handler` 还会返回与请求匹配的已注册模式；对于内部生成的重定向，则返回跟随重定向后将匹配的路径。

如果没有适用于该请求的已注册处理程序，`Handler` 返回一个“页面未找到”或“方法不支持”的处理程序，以及空模式。

`Handler` 不会修改其参数。特别地，它不会填充命名路径通配符，因此 `r.PathValue` 将始终返回空字符串。

### func (*ServeMux) ServeHTTP

```go
func (mux *ServeMux) ServeHTTP(w ResponseWriter, r *Request)
```

`ServeHTTP` 将请求分派给其模式与请求 URL 最匹配的处理程序。


## type Dir

```go
type Dir string
```

Dir 使用原生文件系统实现 [`FileSystem`]，并限制在特定的目录树中。

虽然 [`FileSystem.Open`] 方法接受以 `'/'` 分隔的路径，但 Dir 的字符串值是原生文件系统上的目录路径，而不是 URL，因此它由 [`filepath.Separator`] 分隔，而该分隔符不一定是 `'/'`。

请注意，Dir 可能会暴露敏感文件和目录。Dir 会跟随指向目录树外部的符号链接，如果从用户能够创建任意符号链接的目录中提供服务，这尤其危险。Dir 还允许访问以句点开头的文件和目录，这可能会暴露诸如 `.git` 之类的敏感目录或诸如 `.htpasswd` 之类的敏感文件。要排除以句点开头的文件，请从服务器中移除这些文件/目录，或创建自定义的 FileSystem 实现。

空的 Dir 被视为 `"."`。

### func (Dir) Open

```go
func (d Dir) Open(name string) (File, error)
```

Open 使用 [`os.Open`] 实现 [`FileSystem`]，打开以目录 d 为根并相对于 d 的文件以供读取。

## func FileServer

```go
func FileServer(root FileSystem) Handler
```

`FileServer` 返回一个处理程序，用于以 `root` 为根的文件系统的内容提供 HTTP 请求。

作为特殊情况，返回的文件服务器会将任何以 `"/index.html"` 结尾的请求重定向到相同路径，但不包含末尾的 `"index.html"`。

要使用操作系统的文件系统实现，请使用 `http.Dir`：

```go
http.Handle("/", http.FileServer(http.Dir("/tmp")))
```

要使用 `fs.FS` 实现，请改用 `http.FileServerFS`。