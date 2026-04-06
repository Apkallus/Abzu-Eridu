long cread_alt(long *xp){
    long z=0;
    long *res=&z;
    if(xp){
        res=xp;
    }
    return *res;
}
/* o1优化下使用条件传送
    既然直接获取值将跳转
    那么间接获得地址后再引用
	movq	$0, (%rsp)
	movq	%rsp, %rax
	testq	%rdi, %rdi
	cmove	%rax, %rdi
	movq	(%rdi), %rax
*/