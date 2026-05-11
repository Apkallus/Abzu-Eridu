- Security Policy
    - 说明：在采取行动之前，要像任何“白帽”一样行为规范。
    - 提示：阅读安全政策 Security Policy
    - 示例解决方案：
        > 1. 访问 https://securitytxt.org/ 以了解一项提议的标准，该标准允许网站定义安全策略。 
        > 2. 从 http://localhost:3000/.well-known/security.txt 或 http://localhost:3000/security.txt 服务器请求安全策略文件以解决挑战。
    - security.txt 标准：
        > - 对于网站，security.txt 文件应放置在 /.well-known/ 路径下（ /.well-known/security.txt ）[RFC8615]。它也可以放置在网站的根目录（ /security.txt ）中，特别是当 /.well-known/ 目录因技术原因无法使用时，或者仅仅作为备用方案。该文件可以同时放置在网站的这两个位置。
    - 这正是查找计分板时发现的文件