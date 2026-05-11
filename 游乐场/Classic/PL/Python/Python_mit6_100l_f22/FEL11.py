def remove_and_sort(Lin, k):
    """ Lin is a list of ints
        k is an int >= 0
    Mutates Lin to remove the first k elements in Lin and 
    then sorts the remaining elements in ascending order.
    If you run out of items to remove, Lin is mutated to an empty list.
    Does not return anything.
        Lin 是一个整数列表
        k 是一个大于等于 0 的整数
    修改 Lin，移除 Lin 中的前 k 个元素，
    然后将剩余元素按升序排序。
    如果移除的元素数量超过列表长度，Lin 将被修改为空列表。
    不返回任何值。
    """
    # Your code here  
    if k < len(Lin):
        for i in range(k):
            del(Lin[0])
        Lin.sort()
    else:
        Lin.clear()
    

# Examples:
L = [1,6,3]
k = 1
remove_and_sort(L, k)
print(L)   # prints the list [3, 6]