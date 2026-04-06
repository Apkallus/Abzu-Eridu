#############################################################################
# Problem 1:
# For each of the following expressions, what is the order of growth class 
# that best describes it?
# a) 8n   #n
# b) 3n**2 + 7n**3 + 4   #@n**3
# c) 5log(n) + 5n #n
# d) 3**n + n**2 #@3**n
# e) 20n + nlog(n) #@nlog(n) n相同：20为常数，log(n)为变量
# f) 5 + 60 #1
# g) log(n) + 4n #n




#############################################################################
# Problem 2:
# Rank the following functions by runtime complexity. Note some may have 
# the same runtime complexity.

# f(n) = n**2 + 4n + 2 #n**2
# g(n) = log(n**2) #@#log2(n) #@# 具体转换见当前目录图片
# h(n) = log2(n)  (i.e. read as log base 2 n) #log2(n)
# j(n) = 3n**3 + 2 #n**3
# l(n) = n! #@# 这里的n！不是计算n的阶乘，而是时间复杂度为n!，于是为最慢

# k(n) = 2**n #2**n

#  l#n! > k#2**n > j#n**3 > f#n**2 > g = h#log2(n)


#############################################################################
# Problem 3:
# What is the time complexity for the following programs? 

def program1():
    my_list = [1,2,3,4,5,6,7,8]
    my_list_even= []
    for i in range(len(my_list)):
        if i % 2 == 0:
            my_list_even.append(i)
    return my_list
# len(my_list)
# n

def program2():
    my_list = [1,2,3,4,5,7]
    my_second_list = [1,2,3,4,5,7]
    
    output_list1 = [i for i in my_list]

    output_list2 = []
    for i in my_list:
        for j in my_second_list:
            output_list2 += [i,j]
    
    return (output_list1, output_list2)
# len(my_list) + len(my_list)*len(my_second_list)
# n + n**2
# n**2

def program3(n):
    epsilon = 0.01
    low = 0
    high = n
    ans = (high + low) / 2 
    
    while abs(ans**4 - n) >= epsilon:
        if ans**4 > n:
            high = ans 
        else: 
            low = ans
        ans = (high + low) / 2
    return ans
# log2(n)



#############################################################################
# Problem 4:
# Describe two ways to construct an algorithm to find the maximum number is a list. 
# One algorithm should have time complexity O(n), the other O(n**2). (Note the 
# O(n**2) algorithm is highly inefficient and we'd never actually use it 
# in practice).
# 描述两种构建算法以查找列表中最大数的方法。
# 一种算法的时间复杂度应为O(n)，另一种为O(n**2)。（注意，
# O(n**2)的算法效率极低，我们在实际中永远不会使用它）。

# 普通的遍历列表即为O(n) -> 比较后，保存最大数的数值或i索引
# 使用循环嵌套能够达到n**2 @-> 外循环遍历，查看当前数是否在列表中为最大，内循环与其他数进行比较
#       只在外循环元素为最大时保存


#@# 答案
# 答案：
# 第一个函数应遍历列表，
# 将每个元素与当前所见的最大元素进行比较。我们仅需遍历列表一次，因此时间复杂度为O(n)。

# 第二个函数会将每个数字与列表中的其他所有数字进行比较。
# 这可以通过使用嵌套的for循环实现，即我们遍历列表两次，时间复杂度为O(n**2)。