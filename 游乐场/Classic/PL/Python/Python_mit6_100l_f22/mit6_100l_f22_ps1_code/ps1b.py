## 6.100A PSet 1: Part B
## Name:
## Time Spent:
## Collaborators:

##########################################################################################
## Get user input for yearly_salary, portion_saved, cost_of_dream_home, semi_annual_raise below ##
##########################################################################################
yearly_salary = float(input())
portion_saved = float(input())
cost_of_dream_home = float(input())
semi_annual_raise = float(input())

# yearly_salary = 110000.0
# portion_saved = 0.15
# cost_of_dream_home = 750000
# semi_annual_raise = 0.03
#########################################################################
## Initialize other variables you need (if any) for your program below ##
#########################################################################
portion_down_payment = 0.25

# 首付款 = 花费 * 首付款比例
down_paymen = cost_of_dream_home * portion_down_payment

# 月收入 = 年收入 / 12
month_salary = yearly_salary / 12
# 月储蓄 = 月收入 * 储蓄率
month_portion_saved = month_salary * portion_saved

amount_saved = 0.0

r = 0.05
# 月回报率 = 年回报率 / 12
r_month = r / 12.0
r_month_plus1 = r_month + 1

semi_annual_raise_plus1 = semi_annual_raise + 1

months = 0

###############################################################################################
## Determine how many months it would take to get the down payment for your dream home below ## 
###############################################################################################

while down_paymen > amount_saved:
    # 计算当前储蓄月回报
    amount_saved = amount_saved * r_month_plus1
    # 然后将月收入存入
    amount_saved = amount_saved + month_portion_saved
    # 月份数增加
    months = months + 1
    # 如果到了半年加薪，则增加月储蓄
    if months % 6 == 0:
        month_portion_saved = month_portion_saved * semi_annual_raise_plus1


print(months)