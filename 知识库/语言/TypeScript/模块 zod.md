# 模块 - zod

https://zod.dev/

- 搜索功能
- 文档 LLM
- github 链接

## Defining schemas —— 定义模式

为了验证数据，你必须首先定义一个*模式*。模式表示*类型*，从简单的原始值到复杂的嵌套对象和数组。

### 原始类型

```ts
import * as z from "zod";

// 原始类型
z.string();
z.number();
z.bigint();
z.boolean();
z.symbol();
z.undefined();
z.null();
```

#### Coercion —— 强制转换

要将输入数据强制转换为适当的类型，请改用 `z.coerce`：

```ts
z.coerce.string();    // String(input)
z.coerce.number();    // Number(input)
z.coerce.boolean();   // Boolean(input)
z.coerce.bigint();    // BigInt(input)
```

这些模式的强制转换变体会尝试将输入值转换为适当的类型。

```ts
const schema = z.coerce.string();

schema.parse("tuna");    // => "tuna"
schema.parse(42);        // => "42"
schema.parse(true);      // => "true"
schema.parse(null);      // => "null"
```

这些强制转换模式的输入类型默认为 `unknown`。要指定更具体的输入类型，请传入一个泛型参数：

```ts
const A = z.coerce.number();
type AInput = z.input<typeof A>; // => unknown

const B = z.coerce.number<number>();
type BInput = z.input<typeof B>; // => number
```

##### Zod 中的强制转换如何工作

Zod 使用内置构造函数强制转换所有输入。

| Zod API              | 强制转换          |
| -------------------- | ----------------- |
| `z.coerce.string()`  | `String(value)`   |
| `z.coerce.number()`  | `Number(value)`   |
| `z.coerce.boolean()` | `Boolean(value)`  |
| `z.coerce.bigint()`  | `BigInt(value)`   |
| `z.coerce.date()`    | `new Date(value)` |

使用 `z.coerce.boolean()` 进行布尔强制转换可能不会像你预期的那样工作。任何 [truthy](https://developer.mozilla.org/en-US/docs/Glossary/Truthy) 值都会被强制转换为 `true`，任何 [falsy](https://developer.mozilla.org/en-US/docs/Glossary/Falsy) 值都会被强制转换为 `false`。

```ts
const schema = z.coerce.boolean(); // Boolean(input)

schema.parse("tuna"); // => true
schema.parse("true"); // => true
schema.parse("false"); // => true
schema.parse(1); // => true
schema.parse([]); // => true

schema.parse(0); // => false
schema.parse(""); // => false
schema.parse(undefined); // => false
schema.parse(null); // => false
```

要完全控制强制转换逻辑，请考虑使用 [`z.transform()`](#transforms) 或 [`z.pipe()`](#pipes)。

##### 自定义输入类型

默认情况下，任何 `z.coerce` 模式的*输入*类型都是 `unknown`。在某些情况下，输入类型更具体可能更好。你可以使用泛型参数指定输入类型。

```ts
const regularCoerce = z.coerce.string();
type RegularInput = z.input<typeof regularCoerce>; // => unknown
type RegularOutput = z.output<typeof regularCoerce>; // => string

const customInput = z.coerce.string<string>();
type CustomInput = z.input<typeof customInput>; // => string
type CustomOutput = z.output<typeof customInput>; // => string
```

#### transform —— 转换

> **注意** — 对于双向转换，请使用 [编解码器](/codecs)。

转换是一种特殊类型的模式，执行单向转换。它们不验证输入，而是接受任何内容并对数据执行某种转换。要定义转换：

**Zod**
```ts
const castToString = z.transform((val) => String(val));

castToString.parse("asdf"); // => "asdf"
castToString.parse(123); // => "123"
castToString.parse(true); // => "true"
```

**Zod Mini**
```ts
const castToString = z.transform((val) => String(val));

z.parse(castToString, "asdf"); // => "asdf"
z.parse(castToString, 123); // => "123"
z.parse(castToString, true); // => "true"
```

> **警告**
>
> 转换函数不应抛出错误。抛出的错误不会被 Zod 捕获。

要在转换中执行验证逻辑，请使用 `ctx`。要报告验证问题，请将新问题推送到 `ctx.issues`（类似于 [`.check()`](#check) API）。

```ts
const coercedInt = z.transform((val, ctx) => {
  try {
    const parsed = Number.parseInt(String(val));
    return parsed;
  } catch (e) {
    ctx.issues.push({
      code: "custom",
      message: "Not a number",
      input: val,
    });

    // 这是一个类型为 `never` 的特殊常量
    // 返回它可以让你退出转换，而不影响推断出的返回类型
    return z.NEVER;
  }
});
```

最常见的是，转换与[管道](#pipes)结合使用。这种组合对于执行一些初始验证，然后将解析后的数据转换为另一种形式很有用。

**Zod**
```ts
const stringToLength = z.string().pipe(z.transform(val => val.length));

stringToLength.parse("hello"); // => 5
```

**Zod Mini**
```ts
const stringToLength = z.pipe(z.string(), z.transform(val => val.length));

z.parse(stringToLength, "hello"); // => 5
```

##### `.transform()`

将某个模式管道传入转换是一种常见模式，因此 Zod 提供了便捷的 `.transform()` 方法。

**Zod**
```ts
const stringToLength = z.string().transform(val => val.length); 
```

**Zod Mini**
```ts
// 无等效实现
```

转换也可以是异步的：

**Zod**
```ts
const idToUser = z
  .string()
  .transform(async (id) => {
    // 从数据库获取用户
    return db.getUserById(id); 
  });

const user = await idToUser.parseAsync("abc123");
```

**Zod Mini**
```ts
const idToUser = z.pipe(
  z.string(),
  z.transform(async (id) => {
    // 从数据库获取用户
    return db.getUserById(id); 
  }));

const user = await idToUser.parse("abc123");
```

> **注意**
>
> 如果使用异步转换，解析数据时必须使用 `.parseAsync` 或 `.safeParseAsync`！否则 Zod 会抛出错误。

##### `.preprocess()`

将转换管道传入另一个模式是另一种常见模式，因此 Zod 提供了便捷的 `z.preprocess()` 函数。

```ts
const coercedInt = z.preprocess((val) => {
  if (typeof val === "string") {
    return Number.parseInt(val);
  }
  return val;
}, z.int());
```

默认情况下，`z.preprocess()` 模式的输入类型是 `unknown`，因为预处理器需要处理任意输入。要缩小输入类型，直接标注预处理器的参数：

```ts
const trimmed = z.preprocess(
  (val: string | null | undefined) => val?.trim() ?? "",
  z.string()
);

type Input = z.input<typeof trimmed>;  // string | null | undefined
type Output = z.output<typeof trimmed>; // string
```

当与 `react-hook-form` 等从 `z.input<>` 派生表单值类型的库集成时，这很有用。

### Numbers

```ts
const schema = z.number();
 
schema.parse(3.14);      // ✅
schema.parse(NaN);       // ❌
schema.parse(Infinity);  // ❌
``` 
- 新版的无穷不无法被解析为 number，而旧版存在

## Migration guide —— 迁移指南，新旧版差异

### z.number()

no infinite values

`POSITIVE_INFINITY` and `NEGATIVE_INFINITY` are no longer considered valid values for `z.number()`.