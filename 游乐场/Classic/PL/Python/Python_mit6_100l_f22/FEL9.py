def dot_product(tA, tB):
    """
    tA: a tuple of numbers
    tB: a tuple of numbers of the same length as tA
    Assumes tA and tB are the same length.
    Returns a tuple where the:
    * first element is the length of one of the tuples
    * second element is the sum of the pairwise products of tA and tB
    tA: 一个数字元组
    tB: 一个与 tA 长度相同的数字元组
    假设 tA 和 tB 的长度相同。
    返回一个元组，其中：
    * 第一个元素是其中一个元组的长度
    * 第二个元素是 tA 和 tB 的逐对乘积之和
    """
    # Your code here
    len_res = len(tA)
    mul_res = 0
    for i in range(len_res):
        mul_res += (tA[i] * tB[i])
    return len_res, mul_res
# Examples:
tA = (1, 2, 3)
tB = (4, 5, 6)   
print(dot_product(tA, tB)) # prints (3,32)