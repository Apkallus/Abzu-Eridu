/*
int x,y,z
double dx=(double)x
double dy=(double)y
double dz=(double)z

A
(float)x==(float)dx
false int转float损失精度
#错误 虽然int转float损失精度，int转double后再转float同样损失精度

B
dx-dy==(double)(x-y)
false double范围大于int (x-y)作为int运算后转为double已经损失精度

C
(dx+dy)+dz==dx+(dy+dz)
true 浮点数无结合性 也无正负溢出
但由于int转double后精度增加，应该在表示范围内

D
(dx*dy)*dz==dx*(dx*dz)
false 
应该超过范围而损失精度

E
dx/dx==dz/dz
true
#错误 考虑0的情况

*/