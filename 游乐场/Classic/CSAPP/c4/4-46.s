movq (%rsp), REG
addq $8, %rsp
# 如果REG为寄存器rsp，将得到栈中保存的值+8
# 将栈中保存的值移动到另一个寄存器，在rsp+8后再从那个寄存器到REG