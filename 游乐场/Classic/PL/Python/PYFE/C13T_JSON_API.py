# 在这个作业中，你将编写一个与 http://www.py4e.com/code3/opengeo.py 有些相似的 Python 程序。 
# 该程序将提示输入一个位置，联系一个网络服务并获取该服务的 JSON 数据，解析这些数据，并获取第一个 plus_code 从 JSON 中。
# 一个 开放位置码 是一个基于地址位置的地址的另一种形式的文本标识符。

# API 端点

# 要完成这个作业，你应该使用这个 API 端点，它包含 Open Street Map 数据的静态子集。

# http://py4e-data.dr-chuck.net/opengeo?
# 这个 API 也没有速率限制，所以你可以随意测试。如果你访问没有参数的 URL，你会得到"No address..."的响应。
# 要调用 API，你需要将你请求的地址作为 q= 参数提供，并使用 urllib.parse.urlencode() 函数进行正确的 URL 编码，
# 如 http://www.py4e.com/code3/opengeo.py


# 测试数据 / 示例执行

# 你可以测试一下你的程序是否正常工作 "南联邦大学"的位置，它将会有 plus_code of "6FV8QPRJ+VQ".

# $ python solution.py
# Enter location: South Federal University
# Retrieving http://...
# Retrieved 1329 characters
# Plus code 6FV8QPRJ+VQ
# 提交

# 请运行您的程序以找到此位置的 plus_code：

# Sonoma State University
# 确保你输入的名称和大小写与上面完全一致 并在下方输入 plus_code 和你的 Python 代码。
# 提示：plus_code 的前五个字符是"84CV8 ..."
# 确保你从上面指定的 URL 获取数据，而不是不 标准 Google API。
# 你的程序应该能与 Google API 一起工作——但这个 plus_code 可能不适用于这个作业。

import urllib.request, urllib.parse
import json, ssl

# Heavily rate limited proxy of https://www.geoapify.com/ api
serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    ## 构建拥有参数的URL
    address = input('Enter location: ')
    if len(address) < 1: break

    address = address.strip()
    
    parms = {}
    parms['q'] = address
    # key为 q, value为地址。效果为 q=地址
    # 服务器url+参数
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    ## 使用URL
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'features' not in js:
        print('==== Download error ===')
        print(data)
        break

    if len(js['features']) == 0:
        print('==== Object not found ====')
        print(data)
        break

    # print(json.dumps(js, indent=4))

    lat = js['features'][0]['properties']['lat']
    lon = js['features'][0]['properties']['lon']
    print('lat', lat, 'lon', lon)
    location = js['features'][0]['properties']['formatted']
    print(location)
    plue_code = js['features'][0]['properties']['plus_code']
    print(plue_code)




