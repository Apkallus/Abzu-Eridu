def sum_str_lengths(L):
    """
    L is a non-empty list containing either: 
    * string elements or 
    * a non-empty sublist of string elements
    Returns the sum of the length of all strings in L and 
    lengths of strings in the sublists of L. If L contains an 
    element that is not a string or a list, or L's sublists 
    contain an element that is not a string, raise a ValueError.
    L 是一个非空列表，其中包含以下元素之一：
    * 字符串元素，或
    * 由字符串元素组成的非空子列表
    返回 L 中所有字符串的长度之和，以及 L 的子列表中字符串的长度之和。
    如果 L 包含非字符串或非列表的元素，或者 L 的子列表包含非字符串的元素，则抛出 ValueError 异常。
    """
    # Your code here  
    # 只使用一组异常处理将漏掉一个异常, 但增加组数后仍然漏掉
    # @ 不使用try except，而只raise
    res_sum = 0

    if type(L) != list:
        raise ValueError('L error')
    for e in L:
        if type(e) == list:
            for le in e:
                if type(le) != str:
                    raise ValueError('sub list error')
                res_sum += len(le)
        else:
            if type(e) != str:
                raise ValueError('e error')
            a = len(e)
            res_sum += a

    return res_sum


# Examples:
print(sum_str_lengths(["abcd", ["e", "fg"]]))  # prints 7
print(sum_str_lengths([12, ["e", "fg"]]))      # raises ValueError
print(sum_str_lengths(["abcd", [3, "fg"]]))    # raises ValueError