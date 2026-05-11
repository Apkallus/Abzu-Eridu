def all_true(n, Lf):
    """ n is an int
        Lf is a list of functions that take in an int and return a Boolean
    Returns True if each and every function in Lf returns True when called 
    with n as a parameter. Otherwise returns False. 
    n 是一个整数
        Lf 是一个函数列表，这些函数接受一个整数并返回一个布尔值
    如果 Lf 中的每一个函数在以 n 作为参数调用时都返回 True，则返回 True。否则返回 False。
    """
    # Your code here
    for ef in Lf:
        if not ef(n):
            return False
    return True

# Examples:    
all_true() # prints 6