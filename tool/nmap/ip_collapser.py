#!/bin/python3

import ipaddress
from ip_count_print import split_netmask, parse_ip_base
import itertools

class collapse_config():

    def __init__(self, flush_num = 1000):
        self.flush_num = flush_num
        self.add_count = 0
        self.ip_obj_list = []

    # 添加 ip 对象
    def add_ipobj(self, ipobj):
        self.ip_obj_list.append(ipobj)
        self.add_count += 1
        # 达到预设分段数量时一次性写入文件
        if self.add_count >= self.flush_num:
            self._flush()

    # 达到上限后更新列表，或结尾整合
    def _flush(self):
        self.ip_obj_list = [ipaddr for ipaddr in 
                            ipaddress.collapse_addresses(self.ip_obj_list)]
        self.add_count = 0

    # 结尾整合
    def end_push_list(self):
        self._flush()  

def list_apply_netmask(netblock_ip_buf_list, ip_mask, collapse_buf):
    """
    传入 ip 范围列表，设置 ip 到列表
    netblock_ip_buf_list: [range(),range(),range(),range()]
    """

    # 使用 product 笛卡尔积惰性迭代器替代多重嵌套循环
    for b1, b2, b3, b4 in itertools.product(*netblock_ip_buf_list):
        # 设置 ip 掩码字符串
        ip_dot = f"{b1}.{b2}.{b3}.{b4}/{ip_mask}"

        # 设置库对象
        ip_obj = ipaddress.ip_network(ip_dot, strict=False)

        collapse_buf.add_ipobj(ip_obj)
            

def main():

    #################

    input_file_str = "ip_dirty.txt"
    out_file_str = "ip_collapsed.txt"

    collapse_buf = collapse_config()

    #################

    with open(input_file_str, "r") as f:
        data_list = f.readlines()


    for ip_item in data_list:
        ip_str = ip_item.strip()
        if ip_str == '':
            continue

        # 移除判断，归一处理
        # 分离基础IP与网络掩码
        ip_base, ip_mask = split_netmask(ip_str)

        # 解析无掩码部分为4个 range 对象组成的列表
        netblock_ip_buf_list = parse_ip_base(ip_base)

        list_apply_netmask(netblock_ip_buf_list, ip_mask, collapse_buf)


    collapse_buf.end_push_list()

    clean_ip_list = []
    for clean_ip_item in collapse_buf.ip_obj_list:
        clean_ip_list.append(f"{str(clean_ip_item)}\n")

    with open(out_file_str, "w") as f:
        f.writelines(clean_ip_list)


# 区分直接执行与作为模块导入
if __name__ == '__main__':
   main()
else:
   print(f'{__name__} 作为模块导入')