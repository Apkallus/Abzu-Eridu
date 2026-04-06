####################################################################################
# Practice Problem 1
# Write a program that takes your name as an Input and Outputs the length of your name minus 5.
# 编写一个程序，将你的名字作为输入，并输出名字长度减去5的结果。

# Insert code below
name = input("input name: ")
# print(name[:len(name)-5])
# 名字的长度的数字-5 而不是整个名字-5后的字符
print(len(name)-5)

####################################################################################
# Practice Problem 2
# Write a program to remove the nth character from a non empty string.
# Print the old string and the new string.

test_string = "We want to remove the nth character from this string"
n = 8

# Insert code below
# res_str = test_string[:n-1] + test_string[n-1:]
# 后半字符串应从n开始，n为数字，n-1为下标，那么从n-1+1开始即为后半开始
res_str = test_string[:n-1] + test_string[n:]
print(test_string)
print(res_str)

####################################################################################
# Practice Problem 3
# Write a program which answers the following:
# Does a given string have length greater than 10 or less than 5? If True, output True. If False, output False.
# 给定字符串的长度是否大于10或小于5？如果为真，则输出True。如果为假，则输出False。

my_string = "This is my string"  # example string - modify to test

# Insert code below
len_str = len(my_string)
print(len_str > 10 or len_str < 5)

####################################################################################
# Practice Problem 4
# Write a program which answers the following using a for loop:
# Count the number of e's in the following string

my_string = "How many times is the letter e in this string?"

# Insert code below
count = 0
for ch in my_string:
    if ch == 'e':
        count += 1
print(count)




