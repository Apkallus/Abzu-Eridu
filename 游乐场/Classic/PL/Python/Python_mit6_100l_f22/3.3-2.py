num = int(input())

epsilon = 0.01
pwr = 3


# 包含负数
low = min(-1, num)
# 确保区间包含num为小于1的分数
high = max(1, num)
# 若调整负数high到0,正数low到0,可稍微减少查找次数
mid = (low + high) / 2
while abs(mid**pwr - num) >= epsilon:
    print(f"low={low},high={high},mid={mid},mid**pwr={mid**pwr}")
    if mid**pwr > num:
        high = mid
    else:
        low = mid
    mid = (low + high) / 2

print(mid)