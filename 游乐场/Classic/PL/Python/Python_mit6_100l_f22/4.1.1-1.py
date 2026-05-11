def isIn(str1, str2):
    if str1 in str2 or str2 in str1:
        res = True
    else:
        res = False
    return res

str2 = 'abcde'
str1 = 'fe'
print(isIn(str1, str2))