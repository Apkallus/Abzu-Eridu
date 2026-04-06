def part_a(yearly_salary, portion_saved, cost_of_dream_home):
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
	
	months = 0
	###############################################################################################
	## Determine how many months it would take to get the down payment for your dream home below ## 
	###############################################################################################
	# 只要收入与储蓄少于首付款就继续
	while down_paymen > amount_saved:
	    # 计算当前储蓄月回报
	    amount_saved = amount_saved * r_month_plus1
	    # 然后将月收入存入
	    amount_saved = amount_saved + month_portion_saved
	    # 月份数增加
	    months = months + 1
	
	print(months)
	return months