#!/bin/python3

import logging
import ipaddress
import os
import itertools




# 初始化日志
logging.basicConfig(
    # level=logging.DEBUG, # 日志级别
    level=logging.INFO, # 日志级别
    format='%(levelname)s   %(message)s', # 日志格式
)

# 输出 ip 文件参数
class out_file_config:
    # 初始版本的类仅保存数据，修改为初始化类，按照预设数量写入文件的行为类似 buffer
    def __init__(self, out_dir_str: str, fragment_num: int):
        self.out_dir_str = out_dir_str
        self.fragment_num = fragment_num
        self.ip_buf_list = []
        self.file_num = 0

    # 并且，由于全局函数使用数据类控制文件写入状态，将方法归入类中
    def add_ip(self, ip):
        self.ip_buf_list.append(ip)
        # 达到预设分段数量时一次性写入文件
        if len(self.ip_buf_list) >= self.fragment_num:
            self._flush()

    # 达到上限后写入，或写入结尾残留
    def _flush(self):
        with open(f"{self.out_dir_str}/{self.file_num}.txt", "w") as f:
            f.writelines(self.ip_buf_list)
        self.file_num += 1  
        self.ip_buf_list = []   

    # 末尾写入列表残留
    def end_push_list(self):
        self._flush()

    

def split_netmask(ip: str):
    """
    分离网络掩码为两部分：基本IP与掩码
    若掩码为空则设置为 32
    """

    base_mask = ip.split("/")
    base_mask_len = len(base_mask)

    ip_base = base_mask[0]
    ip_mask = "32"

    if base_mask_len == 2:
        ip_mask = base_mask[1]
    elif base_mask_len > 2:
        raise ValueError(f"掩码格式异常: {base_mask}")
    
    return ip_base, ip_mask

def parse_ip_base(ip_base: str):
    """
    解析基本IP范围
    """
    # 解析为4段
    netblock_list = ip_base.split(".")
    logging.debug(f"netblock_list: {netblock_list}")

    # 替换通配符为对应范围 0-255
    netblock_list = ["0-255" if e == "*" else e for e in netblock_list]
    
    # 之后设置4个范围对象到列表
    netblock_ip_buf_list = []
    for netblock in netblock_list:

        # 解析范围符号
        netblock_parts = netblock.split("-")
        netblock_parts_len = len(netblock_parts)

        netblock_start = netblock_end = int(netblock_parts[0])
        # 若存在范围符号则设置 end
        if netblock_parts_len == 2:
            netblock_end = int(netblock_parts[1])
        elif netblock_parts_len > 2:
            raise ValueError(f"范围格式异常: {netblock}")
        
        # 若超出范围，或 start > end
        if not (0 <= netblock_start <= 255 and 0 <= netblock_end <= 255):
            raise ValueError(f"超出范围: {netblock}")
        if netblock_start > netblock_end:
            raise ValueError(f"start > end: {netblock}")
            
        # 设置范围对象到列表
        netblock_ip_buf_list.append(range(netblock_start, netblock_end+1))

    logging.debug(f"netblock_ip_buf_list: {netblock_ip_buf_list}")
    return netblock_ip_buf_list

def count_ip(netblock_ip_buf_list, ip_mask):
    """
    快速 ip 数量计算
    """
    def count_ip_base(netblock_ip_buf_list):
        """
        仅计算 ip base 数量
        """
        ip_base_count = 1
        for netblock_ip in netblock_ip_buf_list:
            ip_base_count *= len(netblock_ip)
        logging.debug(f"ip_base_count: {ip_base_count}")

        return ip_base_count

    def parse_ip_mask(ip_mask: str):
        """
        掩码对应2的幂
        """
        ip_exp = 0
        if ip_mask != None:
            ip_exp = 32 - int(ip_mask)
        return ip_exp

    def count_apply_netmask(ip_base_count, ip_exp):
        """
        应用掩码到基本IP
        """
        ip_mask_count = pow(2, ip_exp)
        
        total = ip_base_count * ip_mask_count
        return total
    
    # 仅计算 ip base 数量
    ip_base_count = count_ip_base(netblock_ip_buf_list)
    # 掩码对应指数
    ip_exp = parse_ip_mask(ip_mask)
    # 仅计算应用网络掩码后的 ip 数量
    total = count_apply_netmask(ip_base_count, ip_exp)

    return total

def print_apply_netmask(netblock_ip_buf_list, ip_mask, out_file_obj):
    """
    传入 ip 范围列表，打印 IP 到文件
    mask 为空时，传入 32
    netblock_ip_buf_list: [range(),range(),range(),range()]
    """
    logging.debug(f"netblock_ip_buf_list: {netblock_ip_buf_list}")

    # 移除 mask 判断，归一处理
    # 使用 product 笛卡尔积惰性迭代器替代多重嵌套循环
    for b1, b2, b3, b4 in itertools.product(*netblock_ip_buf_list):
        # 设置 ip 掩码字符串
        ip_dot = f"{b1}.{b2}.{b3}.{b4}/{ip_mask}"
        logging.debug(f"ip_dot {ip_dot}")

        # 设置库对象
        ip_obj = ipaddress.ip_network(ip_dot, strict=False)

        # 遍历库对象写入所有 ip 
        for ip in ip_obj:
            ip_str = f"{str(ip)}\n"
            logging.debug(f"ip {ip_str}")   

            out_file_obj.add_ip(ip_str)

def main():

    #################

    out_dir_str = "IP_split"
    fragment_num = 4096    

    out_file_obj = out_file_config(out_dir_str=out_dir_str,
                                fragment_num=fragment_num)

    input_file_str = "nmap_target_list.txt"

    mod = "write"

    #################

    with open(input_file_str, "r") as f:
        data_list = f.readlines()

    logging.info(f"lines: {len(data_list)}")



    # 写入模式设置目录
    if mod == "write":
        os.makedirs(out_file_obj.out_dir_str, exist_ok=True)

    total_ip_count = 0

    for ip in data_list:
        ip = ip.strip()
        logging.debug(f"ip: {ip}")
        if ip == '':
            continue

        # 分离基础IP与网络掩码
        ip_base, ip_mask = split_netmask(ip)
        logging.debug(f"ip_base, ip_mask {ip_base, ip_mask}")

        # 解析无掩码部分为4个 range 对象组成的列表
        netblock_ip_buf_list = parse_ip_base(ip_base)

        # ip 计数
        total = count_ip(netblock_ip_buf_list, ip_mask)
        logging.debug(f"total: {total}")
        total_ip_count += total # IP 数量

        if mod == "write":
            # 根据设置的分段，打印所有 ip 到文件
            print_apply_netmask(netblock_ip_buf_list, ip_mask, out_file_obj)

    if mod == "write":
        # 输出剩余 ip 到文件
        out_file_obj.end_push_list()

    logging.info(f"total_ip_count: {total_ip_count}")

# 区分直接执行与作为模块导入
if __name__ == '__main__':
   main()
else:
   print(f'{__name__} 作为模块导入')