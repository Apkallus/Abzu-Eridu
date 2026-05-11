def keys_with_value(aDict, target):
    """
    aDict: a dictionary
    target: an integer or string
    Assume that keys and values in aDict are integers or strings.
    Returns a sorted list of the keys in aDict with the value target.
    If aDict does not contain the value target, returns an empty list.
    aDict: 一个字典
    target: 一个整数或字符串
    假设aDict中的键和值都是整数或字符串。
    返回aDict中值为target的键的排序列表。
    如果aDict中不包含值target，则返回一个空列表。
    """
    # Your code here  
    res_list = []
    for k,v in aDict.items():
        if v == target:
            res_list.append(k)
    res_list.sort()
    return res_list

# Examples:
aDict = {1:2, 2:4, 5:2}
target = 2   
# print(keys_with_value(aDict, target)) # prints the list [1,5]


def all_positive(d):
    """
    d is a dictionary that maps int:list
    Suppose an element in d is a key k mapping to value v (a non-empty list).
    Returns the sorted list of all k whose v elements sums up to a 
    positive value.
    d 是一个将整数映射到列表的字典。  
    假设字典 d 中的一个元素是键 k，其对应的值为 v（一个非空列表）。  
    返回所有满足 v 中元素之和为正数的 k 的排序列表。
    """
    # Your code here  
    res_list = []
    for k,v in d.items():
        if sum(v) > 0:
            res_list.append(k)
    res_list.sort()
    return res_list


# Examples:
d = {5:[2,-4], 2:[1,2,3], 1:[2]}
print(all_positive(d))   # prints the list [1, 2]