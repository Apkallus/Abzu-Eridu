https://github.com/apache/apr/

https://apr.apache.org/docs/

## strings

### apr_strings.c

#### apr_pstrcat

```c
// include/apr_strings.h
/**
 * Concatenate multiple strings, allocating memory out a pool
 * @param p The pool to allocate out of
 * @param ... The strings to concatenate.  The final string must be NULL
 * @return The new string
 */
APR_DECLARE_NONSTD(char *) apr_pstrcat(apr_pool_t *p, ...)
#if defined(__GNUC__) && __GNUC__ >= 4
    __attribute__((sentinel))
#endif
    ;
```
```c
APR_DECLARE_NONSTD(char *) apr_pstrcat(apr_pool_t *a, ...)
{
    char *cp, *argp, *res;
    apr_size_t saved_lengths[MAX_SAVED_LENGTHS];
    int nargs = 0;

    /* Pass one --- find length of required string */

    apr_size_t len = 0;
    va_list adummy;

    va_start(adummy, a);

    while ((cp = va_arg(adummy, char *)) != NULL) {
        apr_size_t cplen = strlen(cp);
        if (nargs < MAX_SAVED_LENGTHS) {
            saved_lengths[nargs++] = cplen;
        }
        len += cplen;
    }

    va_end(adummy);

    /* Allocate the required string */

    res = (char *) apr_palloc(a, len + 1);
    cp = res;

    /* Pass two --- copy the argument strings into the result space */

    va_start(adummy, a);

    nargs = 0;
    while ((argp = va_arg(adummy, char *)) != NULL) {
        if (nargs < MAX_SAVED_LENGTHS) {
            len = saved_lengths[nargs++];
        }
        else {
            len = strlen(argp);
        }

        memcpy(cp, argp, len);
        cp += len;
    }

    va_end(adummy);

    /* Return the result string */

    *cp = '\0';

    return res;
}
```


## buckets

### apr_brigade.c

https://github.com/apache/apr/blob/c5db070f0800834ec9cbfef4a44862cdf87ccdf0/buckets/apr_brigade.c

#### apr_brigade_write

```c
// include/apr_buckets.h
/**
 * This function writes a string into a bucket brigade.
 *
 * The apr_brigade_write function attempts to be efficient with the
 * handling of heap buckets. Regardless of the amount of data stored
 * inside a heap bucket, heap buckets are a fixed size to promote their
 * reuse.
 *
 * If an attempt is made to write a string to a brigade that already
 * ends with a heap bucket, this function will attempt to pack the
 * string into the remaining space in the previous heap bucket, before
 * allocating a new heap bucket.
 *
 * This function always returns APR_SUCCESS, unless a flush function is
 * passed, in which case the return value of the flush function will be
 * returned if used.
 * @param b The bucket brigade to add to
 * @param flush The flush function to use if the brigade is full
 * @param ctx The structure to pass to the flush function
 * @param str The string to add
 * @param nbyte The number of bytes to write
 * @return APR_SUCCESS or error code
 */
APR_DECLARE(apr_status_t) apr_brigade_write(apr_bucket_brigade *b,
                                            apr_brigade_flush flush, void *ctx,
                                            const char *str, apr_size_t nbyte)
                          __attribute__((nonnull(1,4)));
```
```c
APR_DECLARE(apr_status_t) apr_brigade_write(apr_bucket_brigade *b,
                                            apr_brigade_flush flush,
                                            void *ctx,
                                            const char *str, apr_size_t nbyte)
{
    apr_bucket *e = APR_BRIGADE_LAST(b);
    apr_size_t remaining = APR_BUCKET_BUFF_SIZE;
    char *buf = NULL;

    /*
     * If the last bucket is a heap bucket and its buffer is not shared with
     * another bucket, we may write into that bucket.
     */
    if (!APR_BRIGADE_EMPTY(b) && APR_BUCKET_IS_HEAP(e)
        && ((apr_bucket_heap *)(e->data))->refcount.refcount == 1) {
        apr_bucket_heap *h = e->data;

        /* HEAP bucket start offsets are always in-memory, safe to cast */
        remaining = h->alloc_len - (e->length + (apr_size_t)e->start);
        buf = h->base + e->start + e->length;
    }

    if (nbyte > remaining) {
        /* either a buffer bucket exists but is full,
         * or no buffer bucket exists and the data is too big
         * to buffer.  In either case, we should flush.  */
        if (flush) {
            e = apr_bucket_transient_create(str, nbyte, b->bucket_alloc);
            APR_BRIGADE_INSERT_TAIL(b, e);
            return flush(b, ctx);
        }
        else {
            e = apr_bucket_heap_create(str, nbyte, NULL, b->bucket_alloc);
            APR_BRIGADE_INSERT_TAIL(b, e);
            return APR_SUCCESS;
        }
    }
    else if (!buf) {
        /* we don't have a buffer, but the data is small enough
         * that we don't mind making a new buffer */
        buf = apr_bucket_alloc(APR_BUCKET_BUFF_SIZE, b->bucket_alloc);
        e = apr_bucket_heap_create(buf, APR_BUCKET_BUFF_SIZE,
                                   apr_bucket_free, b->bucket_alloc);
        APR_BRIGADE_INSERT_TAIL(b, e);
        e->length = 0;   /* We are writing into the brigade, and
                          * allocating more memory than we need.  This
                          * ensures that the bucket thinks it is empty just
                          * after we create it.  We'll fix the length
                          * once we put data in it below.
                          */
    }

    /* there is a sufficiently big buffer bucket available now */
    memcpy(buf, str, nbyte);
    e->length += nbyte;

    return APR_SUCCESS;
}
```