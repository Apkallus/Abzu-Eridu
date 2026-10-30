
# 使用哨兵变量防止无限递归调用自身（.bashrc）
## 主进程尚不存在而进入分支，子进程存在而跳过分支
if [[ $first_flag != 1 ]]; then
    # 主进程导出哨兵变量
    export first_flag=1
    # script 创建子 shell 记录交互，子 shell 继承导出变量
    script -q --echo never --log-io /tmp/io --log-timing /tmp/time
fi
