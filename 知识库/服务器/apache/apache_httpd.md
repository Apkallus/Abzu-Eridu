https://github.com/apache/httpd

## modules

### http

#### http_protocol.c

https://github.com/apache/httpd/blob/4a521896a65ffcce6648ff379d0a81265ace04eb/modules/http/http_protocol.c

##### methods_registry / ap_method_registry_init —— 方法注册表及相关函数

```c
/**
 * 附加方法的单例注册表。它将新方法名（例如 "MYGET"）映射到方法编号，
 * 这些编号是位掩码中的整数偏移量。
 *
 * 这沿用了标准 M_GET、M_POST 等所采用的技术。这些编号会在模块加载
 * 以及处理 <Limit GET MYGET> 指令时动态分配。
 */
static apr_hash_t *methods_registry = NULL;
static int cur_method_number = METHOD_NUMBER_FIRST;
```

```c
AP_DECLARE(void) ap_method_registry_init(apr_pool_t *p)
{
    methods_registry = apr_hash_make(p);
    apr_pool_cleanup_register(p, NULL,
                              ap_method_registry_destroy,
                              apr_pool_cleanup_null);

    /*§ 注意 GET 与 HEAD 使用相同编号 `M_GET` §*/
    /* put all the standard methods into the registry hash to ease the
     * mapping operations between name and number
     * HEAD is a special-instance of the GET method and shares the same ID
     */
    register_one_method(p, "GET", M_GET);
    register_one_method(p, "HEAD", M_GET);
    register_one_method(p, "PUT", M_PUT);
    ...
}
```

##### ap_method_number_of —— 返回 HTTP 动词对应的编号

> 似乎对应旧版的 `lookup_builtin_method()` 与 `UNKNOWN_METHOD`

```c
// include/http_protocol.h
/**
 * 获取与给定字符串关联的方法编号，假定该字符串包含一个 HTTP 方法。
 * 若无法识别，则返回 M_INVALID。
 * @param method 包含有效 HTTP 方法的字符串
 * @return 方法编号
 */
AP_DECLARE(int) ap_method_number_of(const char *method);
```

```c
/* 获取与给定字符串关联的方法编号，假定该字符串包含一个 HTTP 方法。
 * 若无法识别，则返回 M_INVALID。
 *
 * 这是将方法名称纳入可配置列表的第一步。
 * 希望它（以及其他例程）最终能迁移到类似 mod_http_methods.c 的模块中，
 * 并带有完整的配置功能。
 */
AP_DECLARE(int) ap_method_number_of(const char *method)
{
    int len = strlen(method);

   /* 检查该方法是否已动态注册 */
    int *methnum = apr_hash_get(methods_registry, method, len);

    if (methnum != NULL) {
        return *methnum;
    }

    return M_INVALID;
}
```

##### ap_h1_append_header

```c
// include/http_protocol.h
/**
 * Append a header in HTTP/1.1 format to the brigade.
 * @param b the brigade to append to
 * @param p the pool to use
 * @param name the name of the header field
 * @param value the value of the header field
 */
AP_DECLARE(apr_status_t) ap_h1_append_header(apr_bucket_brigade *b,
                                             apr_pool_t *pool,
                                             const char *name, const char *value);
```
```c
P_DECLARE(apr_status_t) ap_h1_append_header(apr_bucket_brigade *bb,
                                             apr_pool_t *pool,
                                             const char *name, const char *value)
{
#if APR_CHARSET_EBCDIC
    char *headfield;
    apr_size_t len;

    headfield = apr_pstrcat(pool, name, ": ", value, CRLF, NULL);
    len = strlen(headfield);

    ap_xlate_proto_to_ascii(headfield, len);
    return apr_brigade_write(bb, NULL, NULL, headfield, len);
#else
    struct iovec vec[4];
    struct iovec *v = vec;
    v->iov_base = (void *)name;
    v->iov_len = strlen(name);
    v++;
    v->iov_base = ": ";
    v->iov_len = sizeof(": ") - 1;
    v++;
    v->iov_base = (void *)value;
    v->iov_len = strlen(value);
    v++;
    v->iov_base = CRLF;
    v->iov_len = sizeof(CRLF) - 1;
    return apr_brigade_writev(bb, NULL, NULL, vec, 4);
#endif /* !APR_CHARSET_EBCDIC */
}
```

##### ap_h1_append_headers

```c
/**
 * Append the headers in HTTP/1.1 format to the brigade.
 * @param b the brigade to append to
 * @param r the request this is done for (pool and logging)
 * @param headers the headers to append
 */
AP_DECLARE(apr_status_t) ap_h1_append_headers(apr_bucket_brigade *b,
                                              request_rec *r,
                                              apr_table_t *headers);
```
```c
AP_DECLARE(apr_status_t) ap_h1_append_headers(apr_bucket_brigade *bb,
                                              request_rec *r,
                                              apr_table_t *headers)
{
    const apr_array_header_t *elts;
    const apr_table_entry_t *t_elt;
    const apr_table_entry_t *t_end;
    struct iovec *vec;
    struct iovec *vec_next;

    elts = apr_table_elts(headers);
    if (elts->nelts == 0) {
        return APR_SUCCESS;
    }
    t_elt = (const apr_table_entry_t *)(elts->elts);
    t_end = t_elt + elts->nelts;
    vec = (struct iovec *)apr_palloc(r->pool, 4 * elts->nelts *
                                     sizeof(struct iovec));
    vec_next = vec;

    /* For each field, generate
     *    name ": " value CRLF
     */
    do {
        if (t_elt->key && t_elt->val) {
            vec_next->iov_base = (void*)(t_elt->key);
            vec_next->iov_len = strlen(t_elt->key);
            vec_next++;
            vec_next->iov_base = ": ";
            vec_next->iov_len = sizeof(": ") - 1;
            vec_next++;
            vec_next->iov_base = (void*)(t_elt->val);
            vec_next->iov_len = strlen(t_elt->val);
            vec_next++;
            vec_next->iov_base = CRLF;
            vec_next->iov_len = sizeof(CRLF) - 1;
            vec_next++;
        }
        t_elt++;
    } while (t_elt < t_end);

    if (APLOGrtrace4(r)) {
        t_elt = (const apr_table_entry_t *)(elts->elts);
        do {
            ap_log_rerror(APLOG_MARK, APLOG_TRACE4, 0, r, "  %s: %s",
                          t_elt->key, t_elt->val);
            t_elt++;
        } while (t_elt < t_end);
    }

#if APR_CHARSET_EBCDIC
    {
        apr_size_t len;
        char *tmp = apr_pstrcatv(r->pool, vec, vec_next - vec, &len);
        ap_xlate_proto_to_ascii(tmp, len);
        return apr_brigade_write(bb, NULL, NULL, tmp, len);
    }
#else
    return apr_brigade_writev(bb, NULL, NULL, vec, vec_next - vec);
#endif
}
```

### proxy

#### proxy_util.c

https://github.com/apache/httpd/blob/0f8f5f3f0d87a7a90d3f00c34634397defe0aa5b/modules/proxy/proxy_util.c

##### ap_proxy_create_hdrbrgd

```c
// modules/proxy/mod_proxy.h
/**
 * Create a HTTP request header brigade,  old_cl_val and old_te_val as required.
 * @param p               pool
 * @param header_brigade  header brigade to use/fill
 * @param r               request
 * @param p_conn          proxy connection rec
 * @param worker          selected worker
 * @param conf            per-server proxy config
 * @param uri             uri
 * @param url             url
 * @param server_portstr  port as string
 * @param old_cl_val      stored old content-len val
 * @param old_te_val      stored old TE val
 * @return                OK or HTTP_EXPECTATION_FAILED
 */
PROXY_DECLARE(int) ap_proxy_create_hdrbrgd(apr_pool_t *p,
                                           apr_bucket_brigade *header_brigade,
                                           request_rec *r,
                                           proxy_conn_rec *p_conn,
                                           proxy_worker *worker,
                                           proxy_server_conf *conf,
                                           apr_uri_t *uri,
                                           char *url, char *server_portstr,
                                           char **old_cl_val,
                                           char **old_te_val);
```

```c
PROXY_DECLARE(int) ap_proxy_create_hdrbrgd(apr_pool_t *p,
                                            apr_bucket_brigade *header_brigade,
                                            request_rec *r,
                                            proxy_conn_rec *p_conn,
                                            proxy_worker *worker,
                                            proxy_server_conf *conf,
                                            apr_uri_t *uri,
                                            char *url, char *server_portstr,
                                            char **old_cl_val,
                                            char **old_te_val)
{
    int rc = OK;
    conn_rec *c = r->connection;
    char *buf;
    apr_table_t *saved_headers_in = r->headers_in;
    const char *saved_host = apr_table_get(saved_headers_in, "Host");
    apr_bucket *e;
    int force10 = 0, do_100_continue = 0;
    conn_rec *origin = p_conn->connection;
    const char *host, *creds, *val;
    proxy_dir_conf *dconf = ap_get_module_config(r->per_dir_config, &proxy_module);

    /*
    * HTTP “Ping” 测试？最简单的方式是 100-Continue。不过：
    * 为符合规范，我们只对带有请求体的请求使用 100-Continue。
    * 同时还要确保不会以 HTTP/1.0 进行通信。
    */
    if (apr_table_get(r->subprocess_env, "force-proxy-request-1.0")) {
        force10 = 1;
    }
    else if (apr_table_get(r->notes, "proxy-100-continue")
             || PROXY_SHOULD_PING_100_CONTINUE(worker, r)) {
        do_100_continue = 1;
    }
    if (force10 || apr_table_get(r->subprocess_env, "proxy-nokeepalive")) {
        if (origin) {
            origin->keepalive = AP_CONN_CLOSE;
        }
        p_conn->close = 1;
    }

    /*§
        拼接 HTTP 动词。pr_pstrcat 函数仅拼接字符串
    §*/
    if (force10) {
        buf = apr_pstrcat(p, r->method, " ", url, " HTTP/1.0" CRLF, NULL);
    }
    else {
        buf = apr_pstrcat(p, r->method, " ", url, " HTTP/1.1" CRLF, NULL);
    }
    ap_xlate_proto_to_ascii(buf, strlen(buf));
    e = apr_bucket_pool_create(buf, strlen(buf), p, c->bucket_alloc);
    APR_BRIGADE_INSERT_TAIL(header_brigade, e);

    /*
    * 针对我们发往后端的请求，在 r->headers_in 上创建一份副本，
    * 根据我们的配置和连接处理就地修改该副本，
    * 用其填充转发的头部 brigade，最后在 r->headers_in 中恢复
    * 已保存的/原始的头部。
    *
    * 注意：为 apr_table_copy 传入 r->pool，因为 r->headers_in 中的
    * 键/值对是由 r->pool 创建的，而 p 可能（实际上也确实）是
    * 生命周期更长的内存池。
    * 如果 apr 编译时启用了 APR_POOL_DEBUG，这会触发 apr_table_copy
    * 中的 bad pool ancestry 中止。
    *
    * icing：如果 p 的生命周期确实长于 r->pool，那么我们也应从
    * r->pool 分配所有新的头部值，以避免泄漏。
    */
    r->headers_in = apr_table_copy(r->pool, saved_headers_in);

    /* 返回原始的 Transfer-Encoding 和/或 Content-Length 值，
    * 然后删除这些头部；代理处理器必须根据实际转发的请求体
    * 来设置它们。
    */
    if ((*old_te_val = (char *)apr_table_get(r->headers_in,
                                             "Transfer-Encoding"))) {
        apr_table_unset(r->headers_in, "Transfer-Encoding");
    }
    if ((*old_cl_val = (char *)apr_table_get(r->headers_in,
                                             "Content-Length"))) {
        apr_table_unset(r->headers_in, "Content-Length");
    }

    /* 清除不转发的逐跳请求头部 */
    if (ap_proxy_clear_connection(r, r->headers_in) < 0) {
        rc = HTTP_BAD_REQUEST;
        goto cleanup;
    }

    /* RFC2616 13.5.1 规定我们应该剥离这些头部 */
    apr_table_unset(r->headers_in, "Keep-Alive");
    apr_table_unset(r->headers_in, "Upgrade");
    apr_table_unset(r->headers_in, "TE");

    /* FIXME：既然我们现在会在转发请求体时处理 r->trailers_in，
    * 那么清除任何现有的 Trailer 头部似乎并不明智。
    * 现在这样做是否正确？
    */
    if (force10)
        apr_table_unset(r->headers_in, "Trailer");

    /* 计算 Host 头部 */
    if (dconf->preserve_host == 0) {
        if (!uri->hostname) {
            rc = HTTP_BAD_REQUEST;
            goto cleanup;
        }
        /* 如果是字面量 IPv6 地址 */
        if (ap_strchr_c(uri->hostname, ':')) { 
            if (uri->port_str && uri->port != DEFAULT_HTTP_PORT) {
                host = apr_pstrcat(r->pool, "[", uri->hostname, "]:",
                                   uri->port_str, NULL);
            } else {
                host = apr_pstrcat(r->pool, "[", uri->hostname, "]", NULL);
            }
        } else {
            if (uri->port_str && uri->port != DEFAULT_HTTP_PORT) {
                host = apr_pstrcat(r->pool, uri->hostname, ":",
                                   uri->port_str, NULL);
            } else {
                host = uri->hostname;
            }
        }
        apr_table_setn(r->headers_in, "Host", host);
    }
    else {
        /* 不想使用 r->hostname，因为传入的头部可能带有端口；
        * 我们改用原始头部。
        */
        host = saved_host;
        if (!host) {
            host =  r->server->server_hostname;
            ap_log_rerror(APLOG_MARK, APLOG_WARNING, 0, r, APLOGNO(01092)
                          "incoming HTTP/0.9 request (with no Host header) "
                          "and preserve host set, "
                          "forcing hostname to be %s for uri %s",
                          host, r->uri);
            apr_table_setn(r->headers_in, "Host", host);
        }
    }

    /* 处理 Via */
    if (conf->viaopt == via_block) {
        /* 阻止所有出站 Via: 头部 */
        apr_table_unset(r->headers_in, "Via");
    } else if (conf->viaopt != via_off) {
        const char *server_name = ap_get_server_name(r);
        /* 如果为代理虚拟主机配置了 USE_CANONICAL_NAME_OFF，
        * 那么 ap_get_server_name() 返回的服务器名就是源服务器名
        * （用于 Via: 头部时意义不大），因此我们改用代理虚拟主机的名称。
        */
        if (server_name == r->hostname)
            server_name = r->server->server_hostname;
        /* 创建 "Via:" 请求头部条目并合并它 */
        /* 生成带/不带服务器注释的出站 Via: 头部： */
        apr_table_mergen(r->headers_in, "Via",
                         (conf->viaopt == via_full)
                         ? apr_psprintf(r->pool, "%d.%d %s%s (%s)",
                                        HTTP_VERSION_MAJOR(r->proto_num),
                                        HTTP_VERSION_MINOR(r->proto_num),
                                        server_name, server_portstr,
                                        AP_SERVER_BASEVERSION)
                         : apr_psprintf(r->pool, "%d.%d %s%s",
                                        HTTP_VERSION_MAJOR(r->proto_num),
                                        HTTP_VERSION_MINOR(r->proto_num),
                                        server_name, server_portstr)
                         );
    }

    /* 使用 HTTP/1.1 100-Continue 作为对后端的快速 “HTTP ping” 测试 */
    if (do_100_continue) {
        /* 如果尚不存在 Expect 头部，则添加它。 */
        if (!(val = apr_table_get(r->headers_in, "Expect"))
            || (ap_cstr_casecmp(val, "100-Continue") != 0 /* fast path */
                && !ap_find_token(r->pool, val, "100-Continue"))) {
            apr_table_mergen(r->headers_in, "Expect", "100-Continue");
        }
    }
    else {
        /* XXX：我们应该只从 Expect 头部中剥离 100-continue 标记，
        * 但实际中还有别的标记在用吗？
        */
        apr_table_unset(r->headers_in, "Expect");
    }

    /* X-Forwarded-*：处理
    *
    * XXX 隐私说明：
    * -----------------
    *
    * 这些请求头部只有在 mod_proxy 用于反向代理配置时才真正有用，
    * 这样关于客户端的有用信息就可以通过反向代理传递到后端服务器，
    * 而后端服务器可能需要这些信息才能正常工作。
    *
    * 在前向代理场景中，这些选项可能构成隐私侵犯，
    * 因为代理后方客户端的信息会被泄露给互联网上的任意服务器。
    *
    * HTTP/1.1 Via: 头部就是为通过代理向服务器传递客户端信息而设计的，
    * 在前向代理配置中应使用它，而不是 X-Forwarded-*。
    * 有关详细信息，请参阅 ProxyVia 选项。
    */
    if (dconf->add_forwarded_headers) {
        if (PROXYREQ_REVERSE == r->proxyreq) {
            /* 添加 X-Forwarded-For：以便上游有机会确定原始请求来自哪里。 */
            apr_table_mergen(r->headers_in, "X-Forwarded-For",
                             r->useragent_ip);

            /* 添加 X-Forwarded-Host：以便上游知道原始请求的主机名是什么。 */
            if (saved_host) {
                apr_table_mergen(r->headers_in, "X-Forwarded-Host",
                                 saved_host);
            }

            /* 添加 X-Forwarded-Server：以便上游知道此代理服务器的名称是什么
            * （如果有多个代理服务器）
            * XXX：这与 Via: 重复——我们严格需要它吗？
            */
            apr_table_mergen(r->headers_in, "X-Forwarded-Server",
                             r->server->server_hostname);
        }
    }

    /* 我们要剥离 Proxy-Authorization 吗？
    * 如果尚未使用它，则不要剥离。
    * 如果已经使用过它，则也许要剥离：RFC2616 表示我们可以传播它。
    * 因此，我们让它可以通过环境变量配置。
    */
    if (r->user != NULL /* we've authenticated */
        && !apr_table_get(r->subprocess_env, "Proxy-Chain-Auth")) {
        apr_table_unset(r->headers_in, "Proxy-Authorization");
    }

    /* 对于子请求，忽略新鲜度/过期头部 */
    if (r->main) {
        apr_table_unset(r->headers_in, "If-Match");
        apr_table_unset(r->headers_in, "If-Modified-Since");
        apr_table_unset(r->headers_in, "If-Range");
        apr_table_unset(r->headers_in, "If-Unmodified-Since");
        apr_table_unset(r->headers_in, "If-None-Match");
    }

    /* 如果有凭据（按 worker），则添加 */
    creds = apr_table_get(r->notes, "proxy-basic-creds");
    if (creds) {
        apr_table_mergen(r->headers_in, "Proxy-Authorization", creds);
    }

    /* 运行钩子，以修正我们即将发送的请求 */
    proxy_run_fixups(r);

    /*§ Host 头部被追加而不是维持原顺序的就地替换 §*/
    /* 我们过去总是先发送 `Host: `，所以保持这种方式。
    * 说不准哪个遗留后端依赖这一点。
    * 如果 proxy_run_fixups() 修改了该值，则使用它（不过删除操作会被忽略）。
    */
    val = apr_table_get(r->headers_in, "Host");
    if (val) {
        apr_table_unset(r->headers_in, "Host");
        host = val;
    }
    ap_h1_append_header(header_brigade, r->pool, "Host", host);

    /* 将（剩余的）头部追加到 brigade */
    ap_h1_append_headers(header_brigade, r, r->headers_in);

cleanup:
    r->headers_in = saved_headers_in;
    return rc;
}
```

步骤
1. 拼接 HTTP 动词并设置 header_brigade，此处无任何检查（第一行）
2. 在副本中清理头部
3. 在副本中原地修改头部
4. 在 header_brigade 追加 Host 头部（第二行）
5. 在 header_brigade 追加剩余头部
6. 返回主调函数 `ap_proxy_http_prefetch`，最终执行 `terminate_headers`
7. 若配置为不持续连接，则在 header_brigade 追加连接关闭头部

#### mod_proxy_http.c

https://github.com/apache/httpd/blob/0f8f5f3f0d87a7a90d3f00c34634397defe0aa5b/modules/proxy/mod_proxy_http.c

##### terminate_headers —— Connection 头部设置函数


```c
static void terminate_headers(proxy_http_req_t *req)
{
    /*
     * Handle Connection: header if we do HTTP/1.1 request:
     * If we plan to close the backend connection sent Connection: close
     * otherwise sent Connection: Keep-Alive.
     */
    if (!req->force10) {
        if (req->upgrade) {
            /* Tell the backend that it can upgrade the connection. */
            ap_h1_append_header(req->header_brigade, req->p, "Connection", "Upgrade");
            ap_h1_append_header(req->header_brigade, req->p, "Upgrade", req->upgrade);
        }
        else if (ap_proxy_connection_reusable(req->backend)) {
            ap_h1_append_header(req->header_brigade, req->p, "Connection", "Keep-Alive");
        }
        else {
            ap_h1_append_header(req->header_brigade, req->p, "Connection", "close");
        }
    }

    /* add empty line at the end of the headers */
    ap_h1_terminate_header(req->header_brigade);
}
```

##### ap_proxy_http_prefetch

```c
static int ap_proxy_http_prefetch(proxy_http_req_t *req,
                                  apr_uri_t *uri, char *url)
{
    ...

    rv = ap_proxy_create_hdrbrgd(p, header_brigade, r, p_conn,
                                 req->worker, req->sconf,
                                 uri, url, req->server_portstr,
                                 &req->old_cl_val, &req->old_te_val);
    if (rv != OK) {
        return rv;
    }

    ...
/* Yes I hate gotos.  This is the subrequest shortcut */
skip_body:
    terminate_headers(req);

    return OK;
}
```

## server

### protocol.c

#### ap_get_mime_headers_core —— Unsafe 模式所在函数

```c
//include/http_protocol.h
/**
 * Optimized version of ap_get_mime_headers() that requires a
 * temporary brigade to work with
 * @param r The current request
 * @param bb temp brigade
 */
AP_DECLARE(void) ap_get_mime_headers_core(request_rec *r,
                                          apr_bucket_brigade *bb);
```
```c
AP_DECLARE(void) ap_get_mime_headers_core(request_rec *r, apr_bucket_brigade *bb)
{
    ...

    core_server_config *conf = ap_get_core_module_config(r->server->module_config);
    int strict = (conf->http_conformance != AP_HTTP_CONFORMANCE_UNSAFE);

    /*
     * Read header lines until we get the empty separator line, a read error,
     * the connection closes (EOF), reach the server limit, or we timeout.
     */
    while(1) {
        /*§ Unsafe 模式下接受 `\r\n` 或 `\n` 作为行尾结束序列 §*/
        apr_status_t rv;

        field = NULL;
        rv = ap_rgetline(&field, r->server->limit_req_fieldsize + 2,
                         &len, r, strict ? AP_GETLINE_CRLF : 0, bb);
        ...
    }
    ...

            /*§ 宽松模式下的头部解析 §*/
            if (!strict)
            {
                /*§ 
                    仅需存在 `:` 作为分隔符
                    last_field 为当前头部字符串指针
                    value 为 `:` 分隔符指针
                §*/
                /* Not Strict ('Unsafe' mode), using the legacy parser */

                if (!(value = strchr(last_field, ':'))) { /* Find ':' or */
                    r->status = HTTP_BAD_REQUEST;   /* abort bad request */
                    ap_log_rerror(APLOG_MARK, APLOG_DEBUG, 0, r, APLOGNO(00564)
                                  "Request header field is missing ':' "
                                  "separator: %.*s", (int)LOG_NAME_MAX_LEN,
                                  last_field);
                    return;
                }

                /*§ 分隔符 `:` 不应位于开头 §*/
                if (value == last_field) {
                    r->status = HTTP_BAD_REQUEST;
                    ap_log_rerror(APLOG_MARK, APLOG_DEBUG, 0, r, APLOGNO(03453)
                                  "Request header field name was empty");
                    return;
                }

                /*§ 替换分隔符 `:` 为 `\0` 终止字符串 §*/
                *value++ = '\0'; /* NUL-terminate at colon */

                /*§ 仅确保6个空白符不出现在头部名 §*/
                if (strpbrk(last_field, "\t\n\v\f\r ")) {
                    r->status = HTTP_BAD_REQUEST;
                    ap_log_rerror(APLOG_MARK, APLOG_DEBUG, 0, r, APLOGNO(03452)
                                  "Request header field name presented"
                                  " invalid whitespace");
                    return;
                }

                /*§ 忽略前缀中出现的两个空白符 §*/
                while (*value == ' ' || *value == '\t') {
                     ++value;            /* Skip to start of value   */
                }

                /*§ 仅确保4个空白符不出现在头部值 §*/
                if (strpbrk(value, "\n\v\f\r")) {
                    r->status = HTTP_BAD_REQUEST;
                    ap_log_rerror(APLOG_MARK, APLOG_DEBUG, 0, r, APLOGNO(03451)
                                  "Request header field value presented"
                                  " bad whitespace");
                    return;
                }
            }
            else /* Using strict RFC7230 parsing */
            {
                ...
            }
    ...
}
```

#### ap_fgetline_core

```c
/* 从输入过滤器中读取一行；如果 fold != 0，则还包括由 MIME 折行
 * （或异常客户端）导致的任何续行，并将其放入大小为 n 字节的
 * 缓冲区 s 中，且不包含末尾换行符。
 *
 * 如果 s 为 NULL，ap_fgetline_core 会从 p 中分配所需内存。
 *
 * 如果一切正常，返回 APR_SUCCESS，并将 *read 设为 s 的完整长度。
 *
 * 如果缓冲区空间不足，则返回 APR_ENOSPC。
 * 其他错误情形下可能返回其他错误。
 *
 * 缓冲区中 *不会* 返回 [CR]LF。因此，*read 为 0 表示读取到空行。
 *
 * 注意：由于缓冲区需要用 1 个字符存放 NUL，因此最多只能返回
 *        (n - 1) 个实际字符。
 *
 *        如果由于连接中断或缓冲区已满，在最后一行未检测到 LF，
 *        则视为错误。
 */
static apr_status_t ap_fgetline_core(char **s, apr_size_t n,
                                     apr_size_t *read, ap_filter_t *f,
                                     int flags, apr_bucket_brigade *bb,
                                     apr_pool_t *p)
{
    ...
    int crlf = flags & AP_GETLINE_CRLF;
    ...

    /*§ 似乎此时对应末尾包含 \n 的判断分支，APR_EINVAL 或为异常 flag： 
        \r\n，完整回车换行继续
        X\n，仅换行而缺乏回车，在严格模式异常，宽松模式继续
        其余状态，如仅换行 `X\r` 或 `\rX` 或在之前被清理
    §*/
    /* 现在在行尾终止字符串；
     * 如果倒数第二个字符是 CR，则在那里终止。
     * 当 saw_eol == 2 时，LF 已在上方处理（未计入），
     * 若最后一个字符是 CR，则仍要在此处终止。
     */
    if (saw_eol < 2) {
        if (last_char > *s && last_char[-1] == APR_ASCII_CR) {
            last_char--;
        }
        else if (crlf) {
            rv = APR_EINVAL;
            goto cleanup;
        }
    }
    bytes_handled = last_char - *s;
    ...
}
```


#### r_assign_protocol —— HTTP 协议字段

```c
static http_error r_assign_protocol(request_rec *r,
                                    const char *protocol,
                                    int strict)
{
    int proto_num;
    http_error error = http_error_none;

    /*§ 严格模式： 
        `HTTP` 全部大写 
        主版本号不为 0
    §*/
    if (protocol[0] == 'H' && protocol[1] == 'T'
            && protocol[2] == 'T' && protocol[3] == 'P'
            && protocol[4] == '/' && apr_isdigit(protocol[5])
            && protocol[6] == '.' && apr_isdigit(protocol[7])
            && !protocol[8] && protocol[5] != '0') {
        r->assbackwards = 0;
        proto_num = HTTP_VERSION(protocol[5] - '0', protocol[7] - '0');
    }
    /*§ 宽松模式： 
        `hTtP` 大小写不限 
        主版本号不为 0
    §*/
    else if ((protocol[0] == 'H' || protocol[0] == 'h')
                 && (protocol[1] == 'T' || protocol[1] == 't')
                 && (protocol[2] == 'T' || protocol[2] == 't')
                 && (protocol[3] == 'P' || protocol[3] == 'p')
                 && protocol[4] == '/' && apr_isdigit(protocol[5])
                 && protocol[6] == '.' && apr_isdigit(protocol[7])
                 && !protocol[8] && protocol[5] != '0') {
        r->assbackwards = 0;
        proto_num = HTTP_VERSION(protocol[5] - '0', protocol[7] - '0');
        if (strict && error == http_error_none)
            error = http_error_badprotocol;
        else
            protocol = apr_psprintf(r->pool, "HTTP/%d.%d", HTTP_VERSION_MAJOR(proto_num),
                                    HTTP_VERSION_MINOR(proto_num));
    }
    ...
}
```

#### ap_assign_request_line —— URI 字段

```c
// include/http_protocol.h
/**
 * Assign the method, uri and protocol (in HTTP/1.x the
 * items from the first line) to the request.
 * @param r The current request
 * @param method the HTTP method
 * @param uri the request uri
 * @param protocol the request protocol
 * @return 1 on success, 0 on failure
 */
AP_DECLARE(int) ap_assign_request_line(request_rec *r,
                                       const char *method, const char *uri,
                                       const char *protocol);
```
```c
AP_DECLARE(int) ap_assign_request_line(request_rec *r,
                                       const char *method, const char *uri,
                                       const char *protocol)
{
    ...

    /*§ 当请求方法为 HEAD 时，设置 head flag `r->header_only` §*/
    /* Determine the method_number and parse the uri prior to invoking error
     * handling, such that these fields are available for substitution
     */
    r->method = method;
    r->method_number = ap_method_number_of(r->method);
    if (r->method_number == M_GET && r->method[0] == 'H')
        r->header_only = 1;

    ...
    /*§ 严格模式： 
        不应包含 `#` 片段
        不应包含 `用户名:密码@` 

        而宽松模式无限制
    §*/
    if (strict) {
        if (r->parsed_uri.fragment) {
            /* RFC3986 3.5: no fragment */
            ap_log_rerror(APLOG_MARK, APLOG_DEBUG, 0, r, APLOGNO(02421)
                          "HTTP Request Line; URI must not contain a fragment");
            r->status = HTTP_BAD_REQUEST;
            goto failed;
        }
        if (r->parsed_uri.user || r->parsed_uri.password) {
            ap_log_rerror(APLOG_MARK, APLOG_DEBUG, 0, r, APLOGNO(02422)
                          "HTTP Request Line; URI must not contain a "
                          "username/password");
            r->status = HTTP_BAD_REQUEST;
            goto failed;
        }
    }
    ...

    /*§ 
        当 HTTP 协议版本号为 HTTP/0.9 时，error 仅置位 HTTP 主版本号为0时设置的 flag http_error_none
    §*/
    /* With the request understood, we can consider HTTP/0.9 specific errors */
    if (r->proto_num == HTTP_VERSION(0, 9) && error == http_error_none) {
        /*§ 若服务器未启用 0.9 版本，则设置对应拒绝 flag §*/
        if (conf->http09_enable == AP_HTTP09_DISABLE)
            error = http_error_reject09;
        /*§ 
            若服务器启用 0.9 版本
            严格模式：仅限 GET（由于 HEAD 与 GET 共享编号，使用 `r->header_only` 排除 HEAD 方法）
            宽松模式：对 HTTP 方法无任何限制
        §*/
        else if (strict && (r->method_number != M_GET || r->header_only))
            error = http_error_badmethod09;
    }
}
```