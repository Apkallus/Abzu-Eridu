	.file	"3-61@.c"
	.text
	.globl	cread_alt
	.type	cread_alt, @function
cread_alt:
.LFB0:
	.cfi_startproc
	endbr64
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movq	%fs:40, %rax
	movq	%rax, 8(%rsp)
	xorl	%eax, %eax
	movq	$0, (%rsp)
	movq	%rsp, %rax
	testq	%rdi, %rdi
	cmove	%rax, %rdi
	movq	(%rdi), %rax
	movq	8(%rsp), %rdx
	subq	%fs:40, %rdx
	jne	.L5
	addq	$24, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 8
	ret
.L5:
	.cfi_restore_state
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE0:
	.size	cread_alt, .-cread_alt
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
