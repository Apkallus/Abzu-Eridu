def count_sqrts(nums_list):
    """
    nums_list: a list
    Assumes that nums_list only contains positive numbers and that there are no duplicates.
    Returns how many elements in nums_list are exact squares of elements in the same list, including itself.
    nums_list: 一个列表
    假设 nums_list 仅包含正数且没有重复元素。
    返回 nums_list 中有多少元素是该列表中其他元素的完全平方数，包括其自身。
    """
    # Your code here
    count = 0
    for num in nums_list:
        if num**2 in nums_list:
            count += 1
    return count

# Examples:    
print(count_sqrts([3,4,2,1,9,25])) # prints 3