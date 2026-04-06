def sumDigits(s):
    res_sum = 0
    
    for ch in s:
        try:
            res_sum += int(ch)
        except:
            print(f"{ch} non")
    return res_sum

print(sumDigits('a1b2c3'))