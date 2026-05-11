# Question 1: Choose the worst case asymptotic order of growth (upper and lower bound) for the following function. Assume n = a.
# 问题1：请为以下函数选择最坏情况下的渐近增长阶数（上界和下界）。假设n = a。
# n
def running_product(a):
    """ a is an int """
    product = 1
    for i in range(5,a+5):
        product *= i
        if product == a:
            return True
    return False
# Question 2: Choose the worst case asymptotic order of growth (upper and lower bound) for the following function. Assume n = len(L).
# 问题2：请为以下函数选择最坏情况下的渐进增长阶数（上界和下界）。假设 n = len(L)。
# 2* n**2
def tricky_f(L, L2):
    """ L and L2 are lists of equal length """
    inL = False
    for e1 in L:
        if e1 in L2:
            inL = True
    inL2 = False
    for e2 in L2:
        if e2 in L:
            inL2 = True
    return inL and inL2
# Question 3: Choose the worst-case asymptotic order of growth (upper and lower bound) for the following function.
# 问题3：请选择以下函数的最坏情况渐进增长阶数（上界和下界）。
# log(n)
def sum_f(n):
    """ n > 0 """
    answer = 0
    while n > 0:
        answer += n%10
        n = int(n/10)
    return answer