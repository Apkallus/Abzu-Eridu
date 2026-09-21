#!/bin/python3

cur_list = [
    60941863,
    58797407,
    49420184,
    25382329,
    41971243
    ]
print(f"cur_list {cur_list}")

# 每个位初始仅与自身关联，状态标记仅设置自身
mask = [1 << i for i in range(64)]
# 每个位初始无翻转
const = [0]*64

def bit_tracker(mask, const):
    # 仅追踪位关联记录
    ## 即，正向演化位，而非对实际数据进行操作
    
    """
    state = (state << 1) ^ (state >> 61)
    """
    def step_one(old_list, i):
        # (state << 1)
        p1 = old_list[i-1] if i>=1 else 0
        # (state >> 61)
        p2 = old_list[i+61] if i<=2 else 0
        # (state << 1) ^ (state >> 61)
        res = p1 ^ p2
        return res

    new_mask = [0]*64
    new_const = [0]*64
    for i in range(64):
        new_mask[i] = step_one(mask, i)
        new_const[i] = step_one(const, i)
    
    mask = new_mask
    const = new_const


    """
    state ^= 0xFFFFFFFFFFFFFFFF
    """
    for i in range(64):
        const[i] ^= 1


    """
    for j in xrange(0, 64, 4):
        cur = (state >> j) & 0xF
        cur = (cur >> 3) | ((cur >> 2) & 2) | ((cur << 3) & 8) | ((cur << 2) & 4)
        state ^= cur << j
    """

    def step_three(the_list, i):
        old_list = the_list[:]
        the_list[i+3] = old_list[i+3] ^ old_list[i]
        the_list[i+2] = old_list[i+2] ^ old_list[i]
        the_list[i+1] = old_list[i+1] ^ old_list[i+3]
        the_list[i] = old_list[i] ^ old_list[i+3]

    for i in range(0, 64, 4):
        step_three(mask, i)
        step_three(const, i)

    return mask, const

# 构建 origin_state 方程初始状态，使用步骤3的异或转换
## 顺序：origin_state -> cur_1 -> cur_2 -> cur_3
## 仅顺序执行之前解析的步骤
equa = []

# ## row64 方法1，设置16组半字节首尾相同方程
# for i in range(0, 64, 4):
#     equa.append(((1 << i) | (1 << (i+3)), 0))

# ## row64 方法2，设置16组半字节首尾相同方程
# for i in range(0, 64, 4):
#     equa.append((mask[i] ^ mask[i+3], const[i] ^ const[i+3]))

for cur in cur_list:
    for cur_index in range(25,-1,-1):
        cur_bit = (cur >> cur_index) & 1
        # 对应之前的异或转换方程
        equa.append((mask[0], cur_bit ^ const[0]))
        # 对应两轮异或转换方程之间的所有步骤
        ## 更新二维数组 mask 与一维数组 const
        mask, const = bit_tracker(mask, const)

"""
int.bit_count(origin_state & mask[0])%2 = cur_bit ^ const[0]
"""

def gauss(equa, n):

    # 将1位的右端 `cur_bit ^ const[0]` 与64位的 mask 扩展为1个增广矩阵
    ## 64：`cur_bit ^ const[0]`
    ## 63~0：mask
    matrix = [mask | (right<<64) for mask, right in equa]
    total_row = len(matrix)
    ## 此时矩阵为：行 26*3，列65（索引0~64）


    def get_index_bit(num, index):
        return (num >> index) & 1
    # 逐列消元
    ## 当前主元行 row
    row = 0
    ## 遍历列
    for col in range(n):
        # 1. 在每列中找主元 pivot，即遍历二维数组中所有行的对应列
        pivot = -1
        for r in range(row, total_row):
            # 从行提取当前列（对应的位）
            cur_bit = get_index_bit(matrix[r], col)
            # 若在当前列找到1作为主元，保存并退出循环
            if cur_bit:
                pivot = r
                break

        ## 若在当前列未找到任何1作为主元，所有位均为0，则继续寻找下一列
        if pivot == -1:
            continue

        # 2. 交换主元所在行 pivot 与当前行 row
        ## *尝试*放置主元到对角线（找不到则错位），后续用来消元
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
            

        # 3. 消元，使用主元所在行（2.交互到对角线）消去所有其他行的1（简化行阶梯形）
        for r in range(total_row):
            # 非主元所在行，且其他行的对应列存在1
            if r != row and get_index_bit(matrix[r], col):
                # ** 计算操作 **
                # 行级异或，其他行被主元所在行异或消元
                ## 当前列被消元到0，其他列互相异或
                ## 最终导致：在当前列中仅主元行存在1
                ### 且由于修改当前列的其他行为0，之后的操作将使得主元行的当前列维持1，而不会再有其他变化
                matrix[r] ^= matrix[row]

        # 4. 寻找下一个主元，+1 到下一行，*尝试*延续对角线放置（若找不到则错位）
        row += 1

    print(f"row: {row}")

    # 此时，矩阵中的行索引 [0, row) 均为主元行
    ## 读出解（每行均有唯一的1）
    solve = [0]*n
    ## 对于主元行，遍历所有列
    for r in range(row):
        for col in range(n):
            cur_col_bit = get_index_bit(matrix[r], col)
            if cur_col_bit:
                # ** 取值操作 **
                # 读出当前行的第64位常数到结果
                cur_row_right = get_index_bit(matrix[r], n)
                solve[col] = cur_row_right
                break
    
    return solve

solve = gauss(equa, 64)
    


# 解的64位恢复到数字
origin_state = sum(solve[i] << i for i in range(64))
print(f"origin_state: {origin_state}")
state = origin_state

# next(26) 揭示魔数为 bits
def next(bits):
    global state

    ret = 0
    for i in range(bits):
        ret <<= 1
        ret |= state & 1
        state = (state << 1) ^ (state >> 61)
        state &= 0xFFFFFFFFFFFFFFFF
        state ^= 0xFFFFFFFFFFFFFFFF

        for j in range(0, 64, 4):
            cur = (state >> j) & 0xF
            cur = (cur >> 3) | ((cur >> 2) & 2) | ((cur << 3) & 8) | ((cur << 2) & 4)
            state ^= cur << j

    return ret

test_cur_list = [next(26) for i in range(len(cur_list)+1)]
print(f"test_cur_list: {test_cur_list}")