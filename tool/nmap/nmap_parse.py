#!/bin/python3

import os
import xml.etree.ElementTree as ET
import csv

# 预期 Nmap XML 格式
"""
<nmaprun scanner="nmap"
    <host>
        <status state="up" reason="echo-reply" reason_ttl="240" />
        <address addr="192.168.1.1" addrtype="ipv4" />
        <hostnames>
            <hostname name="localhost.net" type="PTR" />
        </hostnames>
        <times srtt="212734" rttvar="30266" to="333798" />
    </host>
</nmaprun>
"""


def parse_data(file_str):
    # 使用 XML 库解析数据到对象
    tree = ET.parse(file_str)
    root = tree.getroot()


    data_list = [] # 设置 cve 字段数据
    for host in root.findall('host'): # 遍历所有 host 节点
        state = host.find("status").get("state") # 得到探测状态
        addr = host.find("address").get("addr") # 得到 IP 地址

        # 若有则得到主机名
        name = ''
        if (hostname := host.find("hostnames/hostname")) != None:
            name = hostname.get("name")
        print(state, addr, name)

        # 若存在反向记录或探测为up则记录到csv数据中
        if name != "" or state == "up":
            data_list.append({
                "state":state,
                "addr":addr,
                "name":name
            })

    with open(f'{file_str}.csv', 'w', encoding='utf-8') as f:
        # 使用文件句柄与 csv 头部设置字典写入对象
        writer = csv.DictWriter(f, fieldnames=['addr', 'state', 'name'])
        # 写入头部与数据
        writer.writeheader()
        writer.writerows(data_list)

    il_file_name = f'{file_str}.txt'
    with open(il_file_name, 'w', encoding='utf-8') as f:
        # 遍历地址写入到文件，作为之后的 -iL 列表文件
        addr_str = "\n".join([dict_e["addr"] for dict_e in data_list])
        f.write(addr_str)

    # 返回列表文件名
    return il_file_name

