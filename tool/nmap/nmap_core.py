#!/bin/python3

import subprocess
import itertools
import nmap_scan_opt 
import nmap_init
import nmap_parse
import nmap_mod_and_task
import logging 

# 初始化日志
logging.basicConfig(
    level=logging.DEBUG, # 日志级别
    format='%(asctime)s - %(levelname)s\n%(message)s', # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S' # 时间格式
)

# 任务类型与参数映射
task_type_dict = {
    nmap_mod_and_task.task.host_find_str : nmap_scan_opt.host_find_dict,
    nmap_mod_and_task.task.udp_fast_str : nmap_scan_opt.udp_fast_scan_dict,
    nmap_mod_and_task.task.tcp_default_str : nmap_scan_opt.tcp_default_scan_dict
}

# 单次任务执行
def do_task(target_file_str: str, cur_type: str, task_name: str, exclude_file_str: str):
    # 初始化目录，得到格式化文件名
    out_file_str = nmap_init.nmap_init(target_file_str, cur_type, task_name)

    cur_task_dict = task_type_dict.get(cur_type)
    if cur_task_dict is None:
        raise ValueError(f"task type not found: {cur_type}")

    # 设置命令列表，目标文件、输出文件、排除文件
    cmd_list = ["nmap", 
                "-iL", target_file_str, 
                "-oA", out_file_str,
                "--excludefile", exclude_file_str,
                ]
    # sum() 进行列表加法，得到浅层列表扩展效果 [] + [a, b] + [c, d] = [a,b,c,d]
    cmd_list.extend(sum(cur_task_dict.values(), []))
    logging.debug(f"task cmd_list: {cmd_list}") # 打印测试
    logging.info("task cmd: " + " ".join(cmd_list))

    subprocess.run(cmd_list) # 执行探测

    return out_file_str


logging.info('all task start')

#########

# 设置目标文件
target_file_str = "./nmap_target_list.txt"
# 设置排除文件
exclude_file_str = "./nmap_exclude_file.txt"

#########

# 打印输入模式列表，构建任务字典，返回当前模式字符串与任务字典
task_name, cur_mod_str, cur_task_list = nmap_mod_and_task.select_mod_build_task()

# 遍历任务列表执行
for cur_type in cur_task_list:
    logging.info('cur task start')
    out_file_str = do_task(target_file_str, cur_type, task_name, exclude_file_str)
    logging.info('cur task end')

    # 主机发现任务结束后执行数据解析
    if cur_type == nmap_mod_and_task.task.host_find_str:
        logging.info('host_find parse data start')
        host_find_il_file_name = nmap_parse.parse_data(f"{out_file_str}.xml")
        logging.info('host_find parse data end')
        # 设置 iL 文件，仅对主机发现探测到的主机进行后续端口扫描
        if cur_mod_str == nmap_mod_and_task.mod.quick_str:
            target_file_str = host_find_il_file_name

logging.info('all task end')

