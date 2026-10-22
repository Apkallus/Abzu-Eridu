https://pkg.go.dev/github.com/gorilla/sessions

## type CookieStore

```go
type CookieStore struct {
    Codecs  []securecookie.Codec
    Options *Options // 默认配置
}
```

CookieStore 使用安全 cookie 存储会话。

### func NewCookieStore

```go
func NewCookieStore(keyPairs ...[]byte) *CookieStore
```

`NewCookieStore` 返回一个新的 `CookieStore`。

键以成对方式定义，以支持密钥轮换；但常见情况是设置单个认证密钥以及可选的加密密钥。

每对中的第一个密钥用于认证，第二个用于加密。最后一对中的加密密钥可以设置为 `nil` 或省略，但所有对中都需要认证密钥。

建议使用 32 或 64 字节的认证密钥。如果设置了加密密钥，则其长度必须是 16、24 或 32 字节，以分别选择 AES-128、AES-192 或 AES-256 模式。

### func (*CookieStore) Get

```go
func (s *CookieStore) Get(r *http.Request, name string) (*Session, error)
```

`Get` 返回指定名称的会话，并将其添加到注册表中。

如果会话不存在，它会返回一个新会话。访问会话的 `IsNew` 方法以检查它是现有会话还是新会话。

如果会话存在但无法解码，它会返回一个新会话和一个错误。

### func (*CookieStore) MaxAge

```go
func (s *CookieStore) MaxAge(age int)
```

`MaxAge` 设置存储和底层 cookie 实现的最大年龄。可以通过为该会话设置 `Options.MaxAge = -1` 来删除单个会话。

### func (*CookieStore) New

```go
func (s *CookieStore) New(r *http.Request, name string) (*Session, error)
```

`New` 返回指定名称的会话，但不将其添加到注册表中。

`New()` 与 `Get()` 的区别在于：调用 `New()` 两次会解码会话数据两次，而 `Get()` 在第一次调用后注册并重用同一个已解码的会话。

### func (*CookieStore) Save

```go
func (s *CookieStore) Save(r *http.Request, w http.ResponseWriter,
    session *Session) error
```

`Save` 将单个会话添加到响应中。