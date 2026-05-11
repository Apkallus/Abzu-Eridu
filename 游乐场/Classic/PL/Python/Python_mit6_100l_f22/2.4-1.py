numXs = int(input("n tims of X: "))
toPrint = ''
if numXs > 0:
    count = numXs
    while count:
        toPrint = toPrint + 'X'
        count = count -1
print(toPrint)