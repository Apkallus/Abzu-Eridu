s = '1.23, 2.4, 3.123'
# 使用split拆分字符串为列表
s = s.split(',')
sum = 0.0
print(s)
for i in s:
    print(f'float(i) = {float(i)}')
    sum = sum + float(i)
print(sum)