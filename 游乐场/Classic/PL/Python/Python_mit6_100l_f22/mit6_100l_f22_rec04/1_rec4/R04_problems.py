# Problem 1: Lamba Functions Practice
# a) Write a lambda function that calculates the cube root of a given number 
# passed in as an argument
# 问题1：Lambda函数练习
# a) 编写一个lambda函数，计算作为参数传入的给定数字的立方根
# INSERT CODE BELOW HERE
f1 = lambda x: x**(1/3)

# b) Write a lambda function that takes in two arguments and outputs the product
# of those two numbers. 
# b) 编写一个接受两个参数并输出这两个数字乘积的 lambda 函数。
# INSERT CODE BELOW HERE
f2 = lambda x, y: x*y

# uncomment to test function
# print(f1(8))
# print(f1(4))
# print(f2(1,2))
# print(f2(4,5))



#############################################################################
# Problem 2: Practice working with Tuples:
# Write a function that counts the number of times the number 1 appears 
# in an inputted tuple.
# 问题2：练习使用元组：
# 编写一个函数，用于统计输入元组中数字1出现的次数。
# INSERT CODE BELOW HERE
def count_number_one(tuples):
    return tuples.count(1)



# uncomment to test function
# print(count_number_one((1,2,3,4,5,1,1)))  


#############################################################################
# Problem 3: Practice working with Python Tuples
# Write a Function that takes in two tuples and outputs a single tuple containing 
# only common elements of both tuples. 
# 问题3：练习使用Python元组
# 编写一个函数，该函数接收两个元组作为输入，并输出一个仅包含两个元组中共同元素的单一元组。
# INSERT CODE BELOW HERE
def common_elements(a,b):
    res = ()
    for e in a:
        if e in b and e not in res:
            res += (e,)
    return res


# uncomment to test function
# print(common_elements((2,3,4), (3,4,5,6)))


#############################################################################
# Problem 4: Practice working with Python Lists
# Write a Python program to remove sublists from a given list of lists, which 
# contain an element outside a given range.
# 问题4：练习使用Python列表
# 编写一个Python程序，从给定的列表的列表中移除包含超出指定范围元素的子列表。
# e.g 
# Original list:
# [[2], [0], [1, 2, 3], [0, 1, 2, 3, 6, 7], [9, 11], [13, 14, 15, 17]]
# After removing sublists from a given list of lists, which contain an 
# element outside the given range of 12 - 20 (inclusive):
# 从给定的列表列表中移除包含超出指定范围（12至20，含边界）元素的子列表后：
# [[13, 14, 15, 17]]
# INSERT CODE BELOW HERE
def remove_list_range(list_t, low, high):
    for e1 in list_t[:]:
        if min(e1) < low or max(e1) > high:
            list_t.remove(e1)
    return list_t




# uncomment to test function
print(remove_list_range([[2], [0], [1, 2, 3], [0, 1, 2, 3, 6, 7], [9, 11], [13, 14, 15, 17]], 13, 17))

