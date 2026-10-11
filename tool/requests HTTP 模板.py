import requests
import re

"""
class requests.Request(
    method: str | None = None, 
    url: _t.UriType | None = None, 
    headers: _t.HeadersType = None, 
    files: _t.FilesType = None, 
    data: _t.DataType = None, 
    params: _t.ParamsType = None, 
    auth: _t.AuthType = None, 
    cookies: RequestsCookieJar | CookieJar | dict[str, str] | None = None, 
    hooks: _t.HooksInputType | None = None, 
    json: _t.JsonType = None
)
"""

def print_prepare_req(req: requests.PreparedRequest):
    """ 
    打印预备请求 
    """
    print("\n======= print prepare request =======")
    print("===== request headers =====")
    print(f"{req.method} {req.url}")
    headers = "\n".join([f"{name}: {value}" for name, value in req.headers.items()])
    print(headers)
    if req.body:
        print("===== request body =====")
        print("=== byte row body ===")
        print(req.body)
        print("=== pretty body ===")
        print(req.body.decode('latin-1'))
        print()


def print_res(res: requests.Response):
    """ 
    打印响应 
    """
    print("\n======= print response =======")
    print("===== response headers =====")
    print(f"{res.status_code} {res.reason}")
    headers = "\n".join([f"{name}: {value}" for name, value in res.headers.items()])
    print(headers)
    if res.content:
        print("===== response body =====")
        print("=== byte row body ===")
        print(res.content)
        print("=== pretty body ===")
        print(res.text)
        print()

def get_example():
    """ 
    GET 示例 
    """
    print(">>> get_example <<<")
    cookies = {"cookie_name": "cookie_value"}  
    req = requests.Request(
        method = "GET", 
        url = "https://httpbin.org/get",
        cookies = cookies
        )
    pre_req = req.prepare()
    print_prepare_req(pre_req)

    session = requests.Session()
    res = session.send(pre_req)
    print_res(res)
    return pre_req, session, res

def post_example():
    """ 
    POST 示例 
    """
    print(">>> post_example <<<")
    cookies = {"cookie_name": "cookie_value"}  
    body_json = {"body_json_name": "body_json_value"}

    req = requests.Request(
        method = 'POST', 
        url = "https://httpbin.org/post",
        cookies = cookies,
        json = body_json
        )
    pre_req = req.prepare()
    print_prepare_req(pre_req)

    session = requests.Session()
    res = session.send(pre_req)
    print_res(res)
    return pre_req, session, res

def regex_grep_data(res: requests.Response, re_pattern: re.Pattern):
    """
    正则表达式提取
    """
    print(">>> regex_grep_data example <<<")
    # 提取上下文 `"origin": "IP地址"`
    regex_list = re.findall(re_pattern, res.text)
    print(regex_list)
    grep_data = regex_list[-1]
    print(grep_data)
    return grep_data

# 传递编译的正则表达式字符串
re_pattern = re.compile(r'''"origin": "(.+?)"''')

pre_req, session, res = get_example()
regex_grep_data(res, re_pattern)
pre_req, session, res = post_example()
regex_grep_data(res, re_pattern)
