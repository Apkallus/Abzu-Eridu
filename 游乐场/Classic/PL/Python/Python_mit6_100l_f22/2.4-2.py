count = 10
find = False

while count:
    num = int(input(str(count) + " number left: "))
    # 如果当前数字为奇数
    if num % 2 == 1:
        # 如果还未找到任何奇数，最大奇数即为当前数字
        if find == False:
            maxn = num
            find = True
        # 否则与最大奇数比较
        elif find == True and num > maxn:
            maxn = num

    count = count - 1

if(find == True):
    print("max num is",maxn)
else:
    print("not exist")