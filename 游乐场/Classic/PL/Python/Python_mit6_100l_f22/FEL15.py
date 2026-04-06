def recur_power(base, exp):
    """
    base: int or float.
    exp: int >= 0

    Returns base to the power of exp using recursion.
    Hint: Base case is when exp = 0. Otherwise, in the recursive
    case you return base * base^(exp-1).
    base: 整数或浮点数。
    exp: 整数 >= 0

    使用递归返回 base 的 exp 次幂。
    提示：基准情况是当 exp = 0 时。否则，在递归情况下，返回 base * base^(exp-1)。
    """
    # Your code here  
    if exp == 0:
        return 1
    else:
        return base * recur_power(base, exp - 1)


# Examples:
print(recur_power(2,5))  # prints 32