对原 c 文件进行复制并修改 c 源代码后编译得到复刻程序，使用 gdb 进入复刻程序获得栈地址。虽然无法完全使用gdb对原程序进行调试，但可进入main开头获得rsp地址，以计算与本地复刻程序的差值，使用此差值即可实现地址覆盖 ———— 栈地址校准

`gcc -g -O0 -no-pie -fno-stack-protector  -z execstack -o integration-web-overflow integration-web-overflow.c`
- 使用与程序匹配的调试级编译，并匹配地址随机、栈保护、栈执行设置  

原可执行文件复刻后再进行库打桩，可能直接得到相同的栈地址。