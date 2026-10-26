
# Spring Boot

https://docs.spring.io/spring-boot/index.html

## Rest APIs

### Actuator

#### 🎯 Heap Dump (heapdump)

https://docs.spring.io/spring-boot/api/rest/actuator/heapdump.html

##### 检索堆转储

`heapdump` 端点提供应用程序 JVM 的堆转储。

要检索堆转储，请向 `/actuator/heapdump` 发出 `GET` 请求。响应是二进制数据，可能很大。其格式取决于应用程序运行所在的 JVM。在 HotSpot JVM 上运行时，格式为 [HPROF](https://docs.oracle.com/javase/8/docs/technotes/samples/hprof.html)；在 OpenJ9 上，格式为 [PHD](https://www.eclipse.org/openj9/docs/dump_heapdump/#portable-heap-dump-phd-format)。通常，你应该将响应保存到磁盘以便后续分析。使用 curl 时，可以通过使用 `-O` 选项实现，如下例所示：

```bash
$ curl 'http://localhost:8080/actuator/heapdump' -O
```

前面的示例会生成一个名为 `heapdump` 的文件，写入当前工作目录。

