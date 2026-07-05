#!/bin/python3

class mod:
    """设置模式字符串"""
    quick_str = "quick"
    full_str = "full"
    manual_str = "manual"

    # 设置模式列表
    mod_list = [
        quick_str, 
        full_str, 
        manual_str,
    ]

class task:
    """设置任务字符串"""
    host_find_str = "host_find"
    udp_fast_str = "udp_fast"
    tcp_default_str = "tcp_default"

    # 设置测试类型列表
    task_list = [
        host_find_str,
        udp_fast_str,
        tcp_default_str,
    ]


def select_mod_build_task():
    """
    打印输入模式列表，接收列表索引
    构建任务字典
    返回当前模式字符串与任务字典
    """

    # 设置自定义任务名称
    task_target_name = input("输入任务名称： ")

    # 显示并输入模式列表索引：
    mod_index = int(input(
        f"""
        模式设置：
        {mod.mod_list.index(mod.quick_str)}:  {mod.quick_str} 在主机发现后，使用发现的主机作为 iL 文件，进行 udp_fast + tcp_default
        {mod.mod_list.index(mod.full_str)}:   {mod.full_str} 在主机发现后，使用初始目标文件进行 udp_fast + tcp_default
        {mod.mod_list.index(mod.manual_str)}: {mod.manual_str} 手动设置端口扫描
        输入模式索引： 
        """
    ))

    cur_mod_str = mod.mod_list[mod_index]

    # 当前任务映射字典
    task_list_dict = {
        mod.quick_str : [task.host_find_str,task.udp_fast_str,task.tcp_default_str],
        mod.full_str : [task.host_find_str,task.udp_fast_str,task.tcp_default_str],
        mod.manual_str : None,
    }

    # 手动模式则选择任务
    if cur_mod_str == mod.manual_str:
        # 构造列表索引打印字符串
        all_task_list = ["任务设置，使用空格分隔多个任务索引"]
        for index, value in enumerate(task.task_list):
            all_task_list.append(f"{str(index)}: {value}")
        
        all_task_list.append("输入任务索引： ")
        all_task_list_str = "\n".join(all_task_list)
        # 得到索引并设置任务列表
        task_index = input(all_task_list_str)  
        # 使用空白符分割索引字符串，使用 int 索引映射任务列表字符串
        task_list_manual = [task.task_list[int(index)] for index in task_index.split()]
        # 设置手动模式任务列表
        task_list_dict[mod.manual_str] = task_list_manual

    # 设置文件名格式
    task_name = f"{task_target_name}_{cur_mod_str}" 
    # 得到当前任务列表
    cur_task_list = task_list_dict[cur_mod_str]
    
    return task_name, cur_mod_str, cur_task_list