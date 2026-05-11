	.file	"3-73@.c"
	.text
	.globl	find_range
	.type	find_range, @function
find_range:
.LFB23:
	.cfi_startproc
	endbr64
#APP
# 19 "3-73@.c" 1
	vxorps %xmm1, %xmm1, %xmm1     # 之前在第二与第三操作数间少了一个','
	vucomiss %xmm1, %xmm0
	ja .above
	jb .below
	je .equal
	movl $3, %eax
	jmp .Done                      # 之前使用ret报错 
	.above: 
	movl $2, %eax
	jmp .Done
	.below: 
	movl $0, %eax
	jmp .Done
	.equal: 
	movl $1, %eax
	.Done:
	                     # 使用内联汇编时编译器自动在结尾加入ret
# 0 "" 2
#NO_APP
	ret
	.cfi_endproc
.LFE23:
	.size	find_range, .-find_range
	.globl	main
	.type	main, @function
main:
.LFB24:
	.cfi_startproc
	endbr64
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	subq	$32, %rsp
	.cfi_def_cfa_offset 64
	movq	%fs:40, %rax
	movq	%rax, 24(%rsp)
	xorl	%eax, %eax
	movl	$0xbf800000, 12(%rsp)
	movl	$0x00000000, 16(%rsp)
	movl	$0x3f800000, 20(%rsp)
	leaq	12(%rsp), %rbx
	leaq	24(%rsp), %r12
	leaq	a(%rip), %rbp
.L3:
	movss	(%rbx), %xmm0
	call	find_range
	cltq
	movq	0(%rbp,%rax,8), %rdi
	call	puts@PLT
	addq	$4, %rbx
	cmpq	%r12, %rbx
	jne	.L3
	movq	24(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L7
	movl	$0, %eax
	addq	$32, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 32
	popq	%rbx
	.cfi_def_cfa_offset 24
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	ret
.L7:
	.cfi_restore_state
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE24:
	.size	main, .-main
	.globl	a
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC3:
	.string	"NEG"
.LC4:
	.string	"ZERO"
.LC5:
	.string	"POS"
.LC6:
	.string	"OTHER"
	.section	.data.rel.local,"aw"
	.align 32
	.type	a, @object
	.size	a, 32
a:
	.quad	.LC3
	.quad	.LC4
	.quad	.LC5
	.quad	.LC6
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
