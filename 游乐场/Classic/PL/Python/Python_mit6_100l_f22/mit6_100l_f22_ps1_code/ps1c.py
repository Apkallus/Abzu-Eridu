## 6.100A PSet 1: Part C
## Name:
## Time Spent:
## Collaborators:

##############################################
## Get user input for initial_deposit below ##
##############################################
# initial_deposit = float(input())
initial_deposit = 65000
#########################################################################
## Initialize other variables you need (if any) for your program below ##
#########################################################################
cost_of_dream_home = 800000
portion_down_payment = 0.25
# 首付款 = 花费 * 首付款比例
down_paymen = cost_of_dream_home * portion_down_payment

amount_saved = initial_deposit
diff_range = 100
# 初始r为50% 设置端点
r = 0.5
start = 0.0
end = 1.0

mouths = 36
import sys
# min_float = 0.00001
steps = 0
##################################################################################################
## Determine the lowest rate of return needed to get the down payment for your dream home below ##
##################################################################################################

# 如果按照在在最大利率在36个月内能够达到首府款则查找最低利率
# 精度即为diff_range的100差值，否则得手动设置利率的精度
if initial_deposit * (1 + end / 12.0)**mouths + diff_range >= down_paymen:
    # 只要端点在范围内 且未达到精度
    while start <= end and abs(down_paymen - amount_saved) > diff_range:
        # 计算复利回报
        amount_saved = initial_deposit * (1 + r / 12.0)**mouths
        # if steps < 10:
        #     print(f"amount_saved={amount_saved}, down_paymen={down_paymen}")
        # 将储蓄的复利回报与首付款比较，来移动端点
        # 如果储蓄少于则增加利率
        if down_paymen > amount_saved:
            # start = r + min_float
            start = r
            r = (start + end) / 2
        # 如果储蓄超过则减少利率
        else:
            # end = r - min_float
            end = r
            r = (start + end) / 2
        
        steps = steps + 1

    # if steps < 10:
    #     print(f"steps={steps}, start={start}, end={end}")
# 如果达不到则返回None
else:
    r = None
# if start > end:
#     r = None
print(f"r={r}, steps={steps}")
        