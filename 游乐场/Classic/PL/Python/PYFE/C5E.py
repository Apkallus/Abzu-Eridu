# 练习 1： 编写一个程序，该程序反复读取 整数，直到用户输入“done”。
# 一旦输入了“done”，就打印出来。 总和、计数和这些整数的平均值。
# 如果用户输入 任何非整数的，使用 try 和 except 并打印错误消息，然后跳到下一个整数。

# Enter a number: 4
# Enter a number: 5
# Enter a number: bad data
# Invalid input
# Enter a number: 7
# Enter a number: done
# 16 3 5.333333333333333

# sum_n = 0
# count = 0
# while True:
#     usr_inpt = input("Enter a number: ")
#     if usr_inpt == 'done':
#         break
#     try:
#         sum_n += float(usr_inpt)
#     except:
#         print('Invalid input')
#         continue
#     count += 1
# print(sum_n, count, sum_n/count)


# 练习 2： 写另一个程序，提示输入一系列数字（如上所述），并在最后打印出这些数字的最大值和最小值，而不是平均值。

res_list = []
while True:
    usr_inpt = input("Enter a number: ")
    if usr_inpt == 'done':
        break
    try:
        res_list.append(int(usr_inpt))
    except:
        print('Invalid input')
        continue
print(f'Maximum is {max(res_list)}\nMinimum is {min(res_list)}')