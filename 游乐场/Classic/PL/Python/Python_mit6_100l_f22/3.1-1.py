num = int(input())

pwr = 1
root = 0
flag = False
# pwr范围从1到5
while pwr < 6:
    root = 0
    # 每次进入内循环前初始化root
    # 根据num的正负进入对应循环
    if num > 0:
        # 如num为正数，root只需+1
        while root**pwr < num:
            root = root + 1
    else:
        # 如果num为负数，root除了-1外，还要确保作为幂次的pwr不为偶数
        # 否则偶数幂次将为正数，无限循环
        while root**pwr > num and pwr % 2 != 0:
            root = root - 1        
    if root**pwr == num:
        flag = True
        print(f"root={root}, pwr={pwr}")
    pwr = pwr + 1

if flag == False:
    print("not exist")