def flatten(L):
    """ 
    L: a list 
    Returns a copy of L, which is a flattened version of L 
    L: 一个列表  
    返回 L 的一个副本，该副本是 L 的扁平化版本
    """
    # Your code here  
    if L == []:
        return []
    elif type(L[0]) == list:
        # 若此处flatten(L[0])外加[]则为深层复制，结构不变
        # 否则将只有else的最外层[]
        return flatten(L[0]) + flatten(L[1:])
    else:
        return [L[0]] + flatten(L[1:])

# Examples:
L = [[1,4,[6],2],[[[3]],2],4,5]
print(flatten(L)) # prints the list [1,4,6,2,3,2,4,5]