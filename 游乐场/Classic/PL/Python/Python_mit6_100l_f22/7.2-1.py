def findAnEven(L):
    for n in L:
        if n % 2 == 0:
            return n
    raise ValueError("not even number")

print(findAnEven([1,4,2]))
print(findAnEven([1,3]))