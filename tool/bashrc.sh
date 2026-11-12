case $- in
    *i*) ;; # 交互式 shell，继续
    *) return ;; # 非交互式 shell，返回
esac

# 设置 set 命令的前缀
PS4='${BASH_SOURCE} >>> '

# 设置命令的颜色选项别名
alias ls='ls --color=auto'

# 设置挑战目录与复制目录，注意复制目录将被移除重建
CHALLENGE_DIR='/challenge'
MY_COPY_DIR=~/challenge-copy

# 使用 set 命令显示执行的命令
set -x
# 列出挑战目录
ls -al $CHALLENGE_DIR
set +x 

# 检查标记文件，tmp 每次清空，确保仅执行一次
BASHRC_FLAG_PATH="/tmp/bashrc_flag"
rm -f $BASHRC_FLAG_PATH # 调试
if [ -f $BASHRC_FLAG_PATH ]; then
    # 若存在标记文件，则返回
    echo $BASHRC_FLAG_PATH 'exist'
    return
else
    # 创建标记文件
    touch $BASHRC_FLAG_PATH

    rm --recursive --force "$MY_COPY_DIR"
    ln -sfn $CHALLENGE_DIR $MY_COPY_DIR
    # # 清空当前复制目录并新建
    
    # mkdir --parents "$MY_COPY_DIR"

    # # 在复制目录下，递归创建挑战目录的符号链接
    # # VSCode 中打开 home 即访问挑战目录文件
    # cp --recursive --symbolic-link $CHALLENGE_DIR ${MY_COPY_DIR}

    # # 查看挑战目录文件类型，复制 text 型文件
    # # find 得到按行分隔的路径，mapfile 去除换行符存入数组
    # mapfile -t file_list < <(find $CHALLENGE_DIR -ignore_readdir_race \
    # '!' -readable -prune \
    # -o \
    # -type f -exec file {} + | awk -F':' '$2 ~ /text/ {print $1}')
    
    # # 遍历文件路径数组
    # for file_path in "${file_list[@]}"; do

    #     # basename 提取文件名
    #     # file_name=$(basename $file_path)
    #     # dirname 提取前导目录
    #     dir_name=$(dirname $file_path)
    #     # 创造相同前导目录
    #     mkdir -p "${MY_COPY_DIR}${dir_name}"
        
    #     # 复制 text 文件到复制目录
    #     cp --symbolic-link $file_path "${MY_COPY_DIR}${file_path}"

    # done
fi

