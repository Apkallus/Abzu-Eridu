def eval_quadratic(a, b, c, x):
    """
    a, b, c: numerical values for the coefficients of a quadratic equation
    x: numerical value at which to evaluate the quadratic.
    Returns the value of the quadratic a×x² + b×x + c.
    a, b, c: 二次方程系数的数值  
    x: 用于计算二次方程的数值点  
    返回二次方程 a×x² + b×x + c 的值。
    """
    # Your code here
    return a*x**2 + b*x + c
# Examples:    
print(eval_quadratic(1, 1, 1, 1)) # prints 3

def two_quadratics(a1, b1, c1, x1, a2, b2, c2, x2):
    """
    a1, b1, c1: one set of coefficients of a quadratic equation
    a2, b2, c2: another set of coefficients of a quadratic equation
    x1, x2: values at which to evaluate the quadratics
    Evaluates one quadratic with coefficients a1, b1, c1, at x1.
    Evaluates another quadratic with coefficients a2, b2, c2, at x2.
    Prints the sum of the two evaluations. Does not return anything.
    a1, b1, c1: 一组二次方程的系数
    a2, b2, c2: 另一组二次方程的系数
    x1, x2: 用于计算二次方程的值
    使用系数 a1, b1, c1 计算在 x1 处的二次方程值。
    使用系数 a2, b2, c2 计算在 x2 处的二次方程值。
    输出两次计算结果的之和。不返回任何值。
    """
    # Your code here
    res1 = eval_quadratic(a1, b1, c1, x1)
    res2 = eval_quadratic(a2, b2, c2, x2)
    print(res1 + res2)

# Examples:    
two_quadratics(1, 1, 1, 1, 1, 1, 1, 1) # prints 6
print(two_quadratics(1, 1, 1, 1, 1, 1, 1, 1)) # prints 6 then None