########################################################################
# Problem 1: List concatenation
original_list = [1,2,35,10,5,8,9,23]

# a) Using List concatenation create a new list from the orignal list, 
# removing all multiples of 5 from a list of numbers.
# expected output: [1, 2, 8, 9, 23]
# a) 使用列表拼接从原始列表中创建一个新列表，
# 移除列表中所有5的倍数。
# 预期输出: [1, 2, 8, 9, 23]
# INSERT CODE HERE
# 列表推导
# p1_alist = [e for e in original_list if e%5!=0 ] 
# 列表拼接
p1_alist = []
for e in original_list:
    if e%5!=0:
        p1_alist += [e]
# print(p1_alist)

# b) Using list concatenation create a new list from the original list, 
# where each element is half the original element
# b) 使用列表拼接从原列表创建一个新列表，
# 其中每个元素是原元素的一半
# Expected output: [0.5, 1.0, 17.5, 5.0, 2.5, 4.0, 4.5, 11.5]
# INSERT CODE HERE
# 列表推导
p1_blist = [e/2 for e in original_list]
# 列表拼接
p1_blist = []
for e in original_list:
    p1_blist += [e/2]
# print(p1_blist)
########################################################################
# Problem 2: Write a Function to insert a specified element x in a given list 
# after every nth element.
# Return the new list. 
# 问题2：编写一个函数，在给定列表中每隔第n个元素后插入指定元素x。
# 返回新列表。
# Example
# Original list:
# [1, 3, 5, 7, 9, 11, 0, 2, 4, 6, 8, 10, 8, 9, 0, 4, 3, 0]
# Insert 20 in list after every 4th element:
# [1, 3, 5, 7, 20, 9, 11, 0, 2, 20, 4, 6, 8, 10, 20, 8, 9, 0, 4, 20, 3, 0]

def insert_element_list1(lst, x, n):
    """
    Parameters:
    lst: input list
    x: element to insert
    n: x will be inserted after every nth element
    Returns: new modified list 
    参数：
    lst: 输入列表
    x: 要插入的元素
    n: 每第n个元素后插入x
    返回：修改后的新列表
    """
    # INSERT CODE HERE
    # 还可将循环序列设置为列表长度，直接使用下标
    count = 0
    new_l = []
    for e in lst:
        count +=1
        new_l.append(e)
        # 每n个新增x
        if count%n == 0:
            new_l.append(x)
    return new_l

    #@ 关联答案 ##
    #@ 使用while循环控制下标，每次循环变量到对应位置 
    #@ 第一次在n，后续在n+1
# testing
nums = [1, 3, 5, 7, 9, 11,0, 2, 4, 6, 8, 10, 8, 9, 0, 4, 3, 0]
x = 20
n = 4
# print(insert_element_list1(nums, x, n))


########################################################################
# Problem 3: Write a Function to sort list of lists containing integers such that the 
# sub-lists are sorted in increasing order. How would you sort in decreasing order?
# 问题3：编写一个函数，对包含整数的列表进行排序，使得子列表按递增顺序排列。如何按递减顺序排序？

# Example:
# Original list of tuples:
# [[10, 10.12, 10.11], [5, 5.3, 4.9], [2.4, 2.6, 2.2]]
# Expected output:
# [[10, 10.11, 10.12], [4.9, 5, 5.3], [2.2, 2.4, 2.6]]

def sort_list_of_lists(lst):
    """
    Parameters:
    lst: input list
    n: index to sort by
    Returns: the sorted list 
    参数：
    lst: 输入列表
    n: 排序依据的索引
    返回：排序后的列表
    """
    # INSERT CODE HERE
    new_l = []
    for el in lst:
        # 使用sorted创建排序后的子列表，再添加到返回列表中
        new_l.append(sorted(el))
    return new_l

# testing
items = [[10, 10.12, 10.11], [5, 5.3, 4.9], [2.4, 2.6, 2.2]]
# print(sort_list_of_lists(items))


########################################################################
# Problem 4: Write a Function to split a given list into size n chunks 
# using list comprehension. If the list does not divide equally, the last 
# chunk should be short. Return the new list. 
# 问题4：编写一个函数，使用列表推导将给定列表分割为大小为n的块。
# 如果列表不能均分，最后一个块可以较短。返回新列表。

# Example:
# Original list:
# [12, 45, 23, 67, 78, 90, 45, 32, 100, 76, 38, 62, 73, 29, 83]
# Split the list into equal size 4
# [[12, 45, 23, 67], [78, 90, 45, 32], [100, 76, 38, 62], [73, 29, 83]]
# Split the list into equal size 5
# [[12, 45, 23, 67, 78], [90, 45, 32, 100, 76], [38, 62, 73, 29, 83]]
def split_list(lst, n):
    """
    Parameters:
    lst: input list
    n: size of chunks
    Returns: new split list 
    参数：
    lst: 输入列表
    n: 分块大小
    返回：新的分割列表
    """
    # INSERT CODE HERE
    # 子列表数量
    num_sublist = len(lst)//n + (1 if len(lst) % n else 0)
    print(num_sublist)
    # 外循环为子列表数量，创建子列表。
    # 内循环在子列表中添加对应的元素，如果不超过范围
    # return [[lst[oute*n + ine] for ine in range(n) if oute*n + ine < len(lst)] 
    #         for oute in range(num_sublist)]

    #@ 关联答案 ## 序列的步进与切片
    #@ 使用切片的版本，切片的终点在超出时自动到最后一个元素而不会报错
    #@ 使用步进为n的循环序列，即可实现range(num_sublist)的列表长度/n再向上舍入的效果
    return [lst[oute*n:oute*n + n]
            for oute in range(num_sublist)]

# testing
nums = [12,45,23,67,78,90,45,32,100,76,38,62,73,29,83]
n = 4
print(split_list(nums,n))
n = 5
print(split_list(nums,n))








