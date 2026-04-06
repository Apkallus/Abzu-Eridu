# Assume you are given an integer 0 \<= N \\<= 1000. 
# Write a piece of Python code that uses bisection search to guess N. 
# The code prints two lines: count: with how many guesses it took to find N, 
# and answer: with the value of N. 
# Hints: If the halfway value is exactly in between two integers, choose the smaller one.
# 假设你得到一个整数 0 <= N \<= 1000。
# 编写一段使用二分搜索来猜测 N 的 Python 代码。
# 该代码打印两行： count： with how many guesses did to find N， and answer： with the value of N. 
# 提示：如果中间值正好在两个整数之间，请选择较小的一个。

N = 500
start = 0
end = 1000
mid = (start + end)//2
count = 0

while start <= end:
    count +=1
    if mid > N:
        end = mid - 1
    elif mid < N:
        start = mid + 1
    else:
        break
    mid = (start + end)//2
    

print(f"mid={mid},count={count}")
    