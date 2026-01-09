edit_url = """https://github.com/pwncollege/linux-luminarium/edit/master/processes/kill/DESCRIPTION.md#L1"""
tree_url = edit_url.replace("/edit/", "/refs/heads/")
tree_url = tree_url.replace("//github.com/", "//raw.githubusercontent.com/")

print(tree_url)

import sys
print("参数个数为:", len(sys.argv))
print("参数列表:", sys.argv)

import urllib.request

url = tree_url
response = urllib.request.urlopen(url)
content = response.read()

print(content)
