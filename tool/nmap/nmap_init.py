#!/bin/python3

import subprocess
import time
import os
import logging


def nmap_init(target_file_str: str, cur_type: str, target_str: str):
    """
    传入目标文件名、当前测试类型，
    使用当前日期与类型创建目录，
    使用时间与目标设置文件名，
    返回文件名
    """
    
    with open(target_file_str, 'r', encoding='utf-8') as f:
        target = f.read()

    # 按照日期设置目录
    # 日期目录内设置类型目录
    # 类型目录内的文件名设置为 `小时-分钟__自定义名称`
    dir_time_str = time.strftime("%Y-%m-%d", time.localtime())
    file_time_str = time.strftime("%H-%M", time.localtime())

    dir_type_str = f"{dir_time_str}/{cur_type}"
    out_file_str = f"{dir_type_str}/{file_time_str}__{target_str}"
    logging.info(out_file_str) # 打印测试
    # os._exit(0)

    def subprocess_mkdir_with_realuser(dir_name: str):
        """传入目录名称，子进程以实际用户身份创建目录"""

        # 从环境变量得到用户名
        subprocess.run(["sudo", "-u", os.environ['SUDO_USER'], 
                    "mkdir", dir_name]) 


    # 创建“日期”目录
    subprocess_mkdir_with_realuser(dir_time_str) 

    # 在日期目录下，创建“类型”子目录
    subprocess_mkdir_with_realuser(dir_type_str) 

    # 返回文件名
    return out_file_str
