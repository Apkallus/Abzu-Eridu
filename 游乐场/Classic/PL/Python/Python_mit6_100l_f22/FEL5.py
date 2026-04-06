# Assume you are given a string variable named my_str. 
# Write a piece of Python code that prints out a new string containing the even indexed characters of my_str. 
# For example, if my_str = "abcdefg" then your code should print out aceg.
# 假设您有一个名为 my_str 的字符串变量。编写一段 Python 代码，
# 打印出一个包含 my_str 的偶数索引字符的新字符串。
# 例如，如果 my_str = “abcdefg”，则您的代码应打印出 aceg。
my_str = "abcdefg"
print(my_str[::2])