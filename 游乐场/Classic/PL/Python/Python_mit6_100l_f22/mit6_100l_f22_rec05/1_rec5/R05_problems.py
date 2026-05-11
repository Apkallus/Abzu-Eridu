# Problem 1: Given a list of numbers. Write a function to turn every item of 
# a list into its square.
# 问题1：给定一个数字列表。编写一个函数，将列表中的每个元素转换为其平方。
def square_list(my_list):
    return [x**2 for x in my_list]

# test
# print(square_list([1, 2, 3, 4]))
# print(square_list([10, 12, 13]))



# Problem 2: Write a Python program to concatenate element-wise 
# three given lists of same length
# 问题2：编写一个Python程序，将三个长度相同的给定列表按元素逐个连接
# Original lists:
list1 = ['0', '1', '2', '3', '4']
list2 = ['red', 'green', 'black', 'blue', 'white']
list3 = ['100', '200', '300', '400', '500']
# Expected output : ['0red100', '1green200', '2black300', '3blue400', '4white500']

def concatenate_lists(list_a, list_b, list_c):
    list_res = []
    for i in map(lambda a,b,c: a+b+c, list_a, list_b, list_c):
        list_res.append(i)
    return list_res

# test
# print(concatenate_lists(list1, list2, list3))




# Problem 3: Write a function to shift a given list to the right or left 
# direction by a specified amount. Direction, rotation amount, and a 
# list of integers should be inputs to the function.
# 问题3：编写一个函数，将给定列表向右或向左移动指定数量。方向、旋转量和整数列表应作为函数的输入。
# e.g. 
# Input list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Rotate the input list in left direction by 2:
# [3, 4, 5, 6, 7, 8, 9, 10, 1, 2]
# Rotate the input list in Right direction by 4:
# [7, 8, 9, 10, 1, 2, 3, 4, 5, 6]

# edit this to be "right" or "left"
direction = "right" 

def rotate_list(input_list, direction, shift):
    shift = shift % len(input_list)
    head = input_list[-shift:] if direction == 'right' else input_list[shift:]
    tail = input_list[:-shift] if direction == 'right' else input_list[:shift]
    return head+tail

# test 
input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(rotate_list(input_list, "left", 2))
print(rotate_list(input_list, "right", 4))
print(rotate_list(input_list, "right", 14))
print(rotate_list(input_list, "left", 4))


