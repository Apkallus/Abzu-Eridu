# python的多重赋值
x, y, z = 11, 7, 9
flag = False
# 逻辑判断 python使用and    C使用&&
# 条件/循环语句后表示代码块的开始与范围 python使用:与缩进 C使用{}     
# 语句末 python无 C使用;
if x % 2 == 1:
    if flag == False:
        max = x
        flag = True
if y % 2 == 1:
    if flag == False:
        max = y
        flag = True
    elif y > max:
        max = y
if z % 2 == 1:
    if flag == False:
        max = z
        flag = True
    elif z > max:
        max = z
# python2中print是一个命令，于是可写为 print "not exist"
# python3中print是一个函数，于是应当为 print ("not exist")
if flag == False:
    print ("not exist")
else:
    print("is", max)