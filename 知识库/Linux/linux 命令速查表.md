# 命令速查表



## 系统信息

```sh
# 架构信息
uname -a

# 操作系统版本信息
cat /etc/os-release

# 内核编译信息
cat /proc/version                 
```

## 用户权限

```sh
# 当前用户
whoami 

# 用户组
id

# sudo 权限
sudo -ll
# 输出：`!authenticate` 无密码验证
# Sudoers entry:
#     RunAsUsers: ALL
#     Options: !authenticate
#     Commands:
#     ALL

# 用户表
cat /etc/passwd

# 用户组
cat /etc/group

# 当前登录用户及其操作 
w

# 登录历史记录
last
```

## 文件环境

```sh
# 查看工作目录
pwd

# 查看环境变量
env
cat /proc/self/environ

# 文件挂载
cat /etc/fstab
```

## 网络

```sh
# 主机
cat /etc/hosts
```

## 进程

```sh
# 进程信息
ps aux

# 服务状态
service --status-all 
```

## 计划任务

```sh
# 所有计划任务
ls -al /etc/cron*
```

## 命令位置

```sh
# 内置命令 command
command -v id

which id
```