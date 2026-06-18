## Nmap 脚本引擎（NSE）

Nmap 脚本引擎（NSE）是 Nmap 最强大、最灵活的功能之一。它允许用户编写（并分享）简单的脚本（使用 [Lua 编程语言](https://lua.org)），以自动化各种网络任务。这些脚本以 Nmap 所特有的速度和效率并行执行。用户可以依赖 Nmap 发行版中日益丰富和多样化的脚本集，也可以编写自己的脚本来满足定制需求。

我们设计该系统时设想的任务包括网络发现、更复杂的版本检测、漏洞检测。NSE 甚至可用于漏洞利用。

为了反映这些不同的用途并简化脚本选择，每个脚本都包含一个字段，将其与一个或多个类别关联。当前定义的类别有：`auth`、`broadcast`、`default`、`discovery`、`dos`、`exploit`、`external`、`fuzzer`、`intrusive`、`malware`、`safe`、`version` 和 `vuln`。所有这些都在 [脚本类别](nse-usage.html#nse-categories) 一节中进行了描述。

脚本不在沙盒中运行，因此可能意外或恶意地损坏您的系统或侵犯您的隐私。除非您信任作者或已仔细审核过脚本，否则切勿运行第三方脚本。

Nmap 脚本引擎在 [第 9 章《Nmap 脚本引擎》](nse.html) 中有详细描述，并通过以下选项进行控制：

- **`-sC`**  
  使用默认脚本集执行脚本扫描。等效于 `--script=default`。此类别中的某些脚本被认为是侵入性的，未经许可不应在目标网络上运行。  
  注意，只要还指定了至少一个 `--script` 选项，此简写选项就会被忽略。

- **`--script <filename>|<category>|<directory>/|<expression>[,...]`**  
  使用逗号分隔的文件名、脚本类别和目录列表运行脚本扫描。列表中的每个元素也可以是一个布尔表达式，描述更复杂的脚本集。每个元素首先被解释为表达式，然后是类别，最后是文件或目录名。

  有两个仅限高级用户的特殊功能。一是在脚本名称和表达式前加上 `+` 以强制它们运行（例如，即使相关服务未在目标端口上检测到也会运行）。另一个是参数 `all` 可用于指定 Nmap 数据库中的每个脚本。请谨慎使用，因为 NSE 包含危险的脚本，例如漏洞利用、暴力认证破解工具和拒绝服务攻击。

  文件名和目录名可以是相对路径或绝对路径。绝对名称直接使用。相对路径在以下每个位置的 `scripts` 目录中查找，直到找到为止：
  - `--datadir`
  - `$NMAPDIR`
  - `~/.nmap`（Windows 上不搜索）
  - `<APPDATA>\nmap`（仅在 Windows 上）
  - 包含 `nmap` 可执行文件的目录
  - 包含 `nmap` 可执行文件的目录，后跟 `../share/nmap`（Windows 上不搜索）
  - `NMAPDATADIR`（Windows 上不搜索）
  - 当前目录

  当给出以 `/` 结尾的目录名时，Nmap 会加载目录中所有以 `.nse` 结尾的文件。所有其他文件将被忽略，并且不会递归搜索子目录。当给出文件名时，它不必具有 `.nse` 扩展名；如有必要，会自动添加。

  Nmap 脚本默认存储在 Nmap 数据目录的 `scripts` 子目录中（参见 [第 14 章《理解和自定义 Nmap 数据文件》](data-files.html)）。为了提高效率，脚本被索引在 `scripts/script.db` 数据库中，该数据库列出了每个脚本所属的类别。

  通过名称引用 `script.db` 中的脚本时，可以使用 shell 风格的 `*` 通配符。
  - `nmap --script "http-*"`  
    加载所有名称以 `http-` 开头的脚本，例如 `http-auth` 和 `http-open-proxy`。`--script` 的参数必须用引号括起来，以保护通配符不被 shell 解析。

  可以使用 `and`、`or` 和 `not` 运算符构建布尔表达式来进行更复杂的脚本选择。这些运算符的优先级与 Lua 中相同：`not` 最高，其次是 `and`，然后是 `or`。可以使用括号改变优先级。由于表达式包含空格字符，因此需要将其引起来。
  - `nmap --script "not intrusive"`  
    加载除 `intrusive` 类别之外的所有脚本。
  - `nmap --script "default or safe"`  
    功能上等同于 `nmap --script "default,safe"`。加载属于 `default` 类别或 `safe` 类别（或两者兼有）的所有脚本。
  - `nmap --script "default and safe"`  
    加载同时属于 `default` 和 `safe` 类别的脚本。
  - `nmap --script "(default or safe or intrusive) and not http-*"`  
    加载属于 `default`、`safe` 或 `intrusive` 类别的脚本，但排除那些名称以 `http-` 开头的脚本。

- **`--script-args <n1>=<v1>,<n2>={<n3>=<v3>},<n4={<v4>,<v5>}`**  
  允许您向 NSE 脚本提供参数。参数是一个逗号分隔的 `name=value` 对列表。名称和值可以是字符串，不能包含空格或字符 `{`、`}`、`=` 或 `,`。要在字符串中包含这些字符之一，请将字符串用单引号或双引号括起来。在带引号的字符串中，`\` 用于转义引号。反斜杠仅在这种特殊情况下用于转义引号；在所有其他情况下，反斜杠按字面解释。值也可以是像 Lua 中一样用 `{}` 括起来的表。表可以包含简单的字符串值或更多的 name-value 对，包括嵌套表。一个复杂的脚本参数示例是：`--script-args 'user=foo,pass=",{}=bar",whois={whodb=nofollow+ripe},xmpp-info.server_name=localhost'`。许多脚本用脚本名称限定其参数，例如 `xmpp-info.server_name`。脚本会首先检查其完全限定的参数名称（在其文档中指定的名称），然后才会接受非限定的参数名称（本例中为 `server_name`）。某些参数不是特定于一个脚本的。它们通常影响库的行为，因此可能影响所有使用该库的脚本（例如 `http.useragent`，它为每个 Web 请求设置默认的 HTTP User-Agent 头，无论哪个脚本发送它）。不可能为不同的脚本对完全相同的参数赋予不同的值。在线 NSE 文档门户 [https://nmap.org/nsedoc/](https://nmap.org/nsedoc/) 列出了每个脚本接受的参数。

- **`--script-args-file <filename>`**  
  允许您从文件加载 NSE 脚本的参数。命令行上的任何参数会覆盖文件中的参数。文件可以是绝对路径，也可以是相对于 Nmap 常规搜索路径（NMAPDIR 等）的相对路径。参数可以是逗号分隔或换行分隔，但其他方面遵循与 `--script-args` 相同的规则，不需要特殊的引号和转义，因为它们不被 shell 解析。

- **`--script-help <filename>|<category>|<directory>|<expression>|all[, ...]`**  
  显示有关脚本的帮助。对于与给定规范匹配的每个脚本，Nmap 会打印脚本名称、其类别和描述。这些规范与 `--script` 接受的规范相同；例如，如果您想要获取 `ftp-anon` 脚本的帮助，可以运行 `nmap --script-help ftp-anon`。除了获取单个脚本的帮助外，您还可以使用此功能预览某个规范将运行哪些脚本，例如 `nmap --script-help default`。

- **`--script-trace`**  
  该选项所做的与 `--packet-trace` 类似，只是高了一个 ISO 层。如果指定此选项，则会打印脚本执行的所有传入和传出通信。显示的信息包括通信协议、源、目标和传输的数据。如果所有传输数据中超过 5% 不可打印，则跟踪输出将采用十六进制转储格式。指定 `--packet-trace` 也会启用脚本跟踪。

- **`--script-updatedb`**  
  此选项更新位于 `scripts/script.db` 中的脚本数据库，Nmap 使用该数据库来确定可用的默认脚本和类别。仅当您添加或删除了默认 `scripts` 目录中的 NSE 脚本，或更改了任何脚本的类别时，才需要更新数据库。此选项通常单独使用：`nmap --script-updatedb`。