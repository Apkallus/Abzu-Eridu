官网
- [标准库](https://pkg.go.dev/std)
- [规范](https://go.dev/ref/spec)
- [教程](https://go.dev/doc/tutorial/)

## Standard library
### os

https://pkg.go.dev/os

#### func Getenv

```go
func Getenv(key string) string
```

Getenv 检索由 key 命名的环境变量的值。它返回该值，如果变量不存在，则返回空字符串。要区分空值和未设置的值，请使用 [LookupEnv]。

