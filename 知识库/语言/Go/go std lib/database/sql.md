https://pkg.go.dev/database/sql

## type DB

```go
type DB struct {
    // 包含已过滤或未导出的字段
}
```

`DB` 是数据库句柄，表示零个或多个底层连接的池。它可由多个 goroutine 安全地并发使用。

`sql` 包会自动创建和释放连接；它还维护一个空闲连接池。如果数据库有每连接状态的概念，这种状态可以在事务（`Tx`）或连接（`Conn`）中可靠地观察到。一旦调用 `DB.Begin`，返回的 `Tx` 就绑定到单个连接。一旦在事务上调用 `Tx.Commit` 或 `Tx.Rollback`，该事务的连接就会被返回到 `DB` 的空闲连接池。池的大小可以通过 `DB.SetMaxIdleConns` 控制。

### func Open

```go
func Open(driverName, dataSourceName string) (*DB, error)
```

`Open` 打开一个由其数据库驱动名称和特定于驱动的数据源名称指定的数据库，数据源名称通常至少包含数据库名称和连接信息。

大多数用户会通过返回 `*DB` 的驱动特定连接辅助函数来打开数据库。Go 标准库中不包含任何数据库驱动。有关第三方驱动的列表，请参见 https://golang.org/s/sqldrivers。

`Open` 可能只是验证其参数而不创建到数据库的连接。要验证数据源名称是否有效，请调用 `DB.Ping`。

返回的 `DB` 可由多个 goroutine 安全地并发使用，并维护自己的空闲连接池。因此，`Open` 函数应该只调用一次。很少需要关闭 `DB`。

### func OpenDB

自 Go 1.10 起可用。

```go
func OpenDB(c driver.Connector) *DB
```

`OpenDB` 使用 `driver.Connector` 打开数据库，允许驱动绕过基于字符串的数据源名称。

大多数用户会通过返回 `*DB` 的驱动特定连接辅助函数来打开数据库。Go 标准库中不包含任何数据库驱动。有关第三方驱动的列表，请参见 https://golang.org/s/sqldrivers。

`OpenDB` 可能只是验证其参数而不创建到数据库的连接。要验证数据源名称是否有效，请调用 `DB.Ping`。

返回的 `DB` 可由多个 goroutine 安全地并发使用，并维护自己的空闲连接池。因此，`OpenDB` 函数应该只调用一次。很少需要关闭 `DB`。

### func (*DB) Begin

```go
func (db *DB) Begin() (*Tx, error)
```

`Begin` 启动一个事务。默认隔离级别取决于驱动。

`Begin` 内部使用 `context.Background`；要指定上下文，请使用 `DB.BeginTx`。

### func (*DB) BeginTx

自 Go 1.8 起可用。

```go
func (db *DB) BeginTx(ctx context.Context, opts *TxOptions) (*Tx, error)
```

`BeginTx` 启动一个事务。

提供的上下文会一直使用到事务提交或回滚。如果上下文被取消，`sql` 包将回滚事务。如果提供给 `BeginTx` 的上下文被取消，`Tx.Commit` 将返回错误。

提供的 `TxOptions` 是可选的，如果应使用默认值，则可以为 `nil`。如果使用了驱动不支持的非默认隔离级别，将返回错误。

### func (*DB) Close

```go
func (db *DB) Close() error
```

`Close` 关闭数据库并阻止新查询启动。然后 `Close` 等待所有已在服务器上开始处理的查询完成。

很少需要关闭 `DB`，因为 `DB` 句柄旨在长期存在并在多个 goroutine 之间共享。

### func (*DB) Conn

自 Go 1.9 起可用。

```go
func (db *DB) Conn(ctx context.Context) (*Conn, error)
```

`Conn` 返回单个连接，要么打开一个新连接，要么从连接池中返回一个现有连接。`Conn` 将阻塞，直到返回一个连接或 `ctx` 被取消。在同一个 `Conn` 上运行的查询将在同一个数据库会话中运行。

每个 `Conn` 在使用后都必须通过调用 `Conn.Close` 返回到数据库池。

### func (*DB) Driver

```go
func (db *DB) Driver() driver.Driver
```

`Driver` 返回数据库的底层驱动。

### func (*DB) Exec

```go
func (db *DB) Exec(query string, args ...any) (Result, error)
```

`Exec` 执行查询而不返回任何行。`args` 用于查询中的任何占位符参数。

`Exec` 内部使用 `context.Background`；要指定上下文，请使用 `DB.ExecContext`。

### func (*DB) ExecContext

自 Go 1.8 起可用。

```go
func (db *DB) ExecContext(ctx context.Context, query string, args ...any) (Result, error)
```

`ExecContext` 执行查询而不返回任何行。`args` 用于查询中的任何占位符参数。

### func (*DB) Ping

自 Go 1.1 起可用。

```go
func (db *DB) Ping() error
```

`Ping` 验证与数据库的连接是否仍然有效，必要时建立连接。

`Ping` 内部使用 `context.Background`；要指定上下文，请使用 `DB.PingContext`。

### func (*DB) PingContext

自 Go 1.8 起可用。

```go
func (db *DB) PingContext(ctx context.Context) error
```

`PingContext` 验证与数据库的连接是否仍然有效，必要时建立连接。

### func (*DB) Prepare

```go
func (db *DB) Prepare(query string) (*Stmt, error)
```

`Prepare` 为后续查询或执行创建预处理语句。可以从返回的语句并发运行多个查询或执行。调用方必须在不再需要该语句时调用该语句的 `*Stmt.Close` 方法。

`Prepare` 内部使用 `context.Background`；要指定上下文，请使用 `DB.PrepareContext`。

### func (*DB) PrepareContext

自 Go 1.8 起可用。

```go
func (db *DB) PrepareContext(ctx context.Context, query string) (*Stmt, error)
```

`PrepareContext` 为后续查询或执行创建预处理语句。可以从返回的语句并发运行多个查询或执行。调用方必须在不再需要该语句时调用该语句的 `*Stmt.Close` 方法。

提供的上下文用于语句的准备，而不是语句的执行。

### func (*DB) Query

```go
func (db *DB) Query(query string, args ...any) (*Rows, error)
```

`Query` 执行返回行的查询，通常是 `SELECT`。`args` 用于查询中的任何占位符参数。

`Query` 内部使用 `context.Background`；要指定上下文，请使用 `DB.QueryContext`。

### func (*DB) QueryContext

自 Go 1.8 起可用。

```go
func (db *DB) QueryContext(ctx context.Context, query string, args ...any) (*Rows, error)
```

`QueryContext` 执行返回行的查询，通常是 `SELECT`。`args` 用于查询中的任何占位符参数。

### func (*DB) QueryRow

```go
func (db *DB) QueryRow(query string, args ...any) *Row
```

`QueryRow` 执行预期最多返回一行的查询。`QueryRow` 总是返回非 `nil` 值。错误会延迟到调用 `Row` 的 `Scan` 方法时。如果查询未选择任何行，`*Row.Scan` 将返回 `ErrNoRows`。否则，`*Row.Scan` 扫描第一行并丢弃其余行。

`QueryRow` 内部使用 `context.Background`；要指定上下文，请使用 `DB.QueryRowContext`。

### func (*DB) QueryRowContext

自 Go 1.8 起可用。

```go
func (db *DB) QueryRowContext(ctx context.Context, query string, args ...any) *Row
```

`QueryRowContext` 执行预期最多返回一行的查询。`QueryRowContext` 总是返回非 `nil` 值。错误会延迟到调用 `Row` 的 `Scan` 方法时。如果查询未选择任何行，`*Row.Scan` 将返回 `ErrNoRows`。否则，`*Row.Scan` 扫描第一行并丢弃其余行。

### func (*DB) SetConnMaxIdleTime

自 Go 1.15 起可用。

```go
func (db *DB) SetConnMaxIdleTime(d time.Duration)
```

`SetConnMaxIdleTime` 设置连接可以空闲的最长时间。

过期连接可能会在重用之前被惰性关闭。

如果 `d <= 0`，则连接不会因空闲时间而被关闭。

### func (*DB) SetConnMaxLifetime

自 Go 1.6 起可用。

```go
func (db *DB) SetConnMaxLifetime(d time.Duration)
```

`SetConnMaxLifetime` 设置连接可以重用的最长时间。

过期连接可能会在重用之前被惰性关闭。

如果 `d <= 0`，则连接不会因存在时间而被关闭。

### func (*DB) SetMaxIdleConns

自 Go 1.1 起可用。

```go
func (db *DB) SetMaxIdleConns(n int)
```

`SetMaxIdleConns` 设置空闲连接池中的最大连接数。

如果 `MaxOpenConns` 大于 0 但小于新的 `MaxIdleConns`，则新的 `MaxIdleConns` 将减少以匹配 `MaxOpenConns` 限制。

如果 `n <= 0`，则不保留空闲连接。

默认最大空闲连接数当前为 2。这可能会在将来的版本中更改。

### func (*DB) SetMaxOpenConns

自 Go 1.2 起可用。

```go
func (db *DB) SetMaxOpenConns(n int)
```

`SetMaxOpenConns` 设置与数据库的最大打开连接数。

如果 `MaxIdleConns` 大于 0 且新的 `MaxOpenConns` 小于 `MaxIdleConns`，则 `MaxIdleConns` 将减少以匹配新的 `MaxOpenConns` 限制。

如果 `n <= 0`，则打开连接数没有限制。默认值为 0（无限制）。

### func (*DB) Stats

自 Go 1.5 起可用。

```go
func (db *DB) Stats() DBStats
```

`Stats` 返回数据库统计信息。