def part_c(initial_deposit):
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
	
	if initial_deposit * (1 + end / 12.0)**mouths + diff_range >= down_paymen:
	    # 只要端点在范围内
	    while start <= end and abs(down_paymen - amount_saved) > diff_range:
	        # 复利回报
	        amount_saved = initial_deposit * (1 + r / 12.0)**mouths
	        # if steps < 10:
	        #     print(f"amount_saved={amount_saved}, down_paymen={down_paymen}")
	        # 将储蓄的复利回报与首付款比较
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
	else:
	    r = None
	# if start > end:
	#     r = None
	print(f"r={r}, steps={steps}")
	        
	return r, steps