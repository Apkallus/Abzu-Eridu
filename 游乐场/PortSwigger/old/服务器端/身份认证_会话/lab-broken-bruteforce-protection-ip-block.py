with open('pwd_list.txt', 'r', encoding='utf-8') as readfile:
    with open('test_pwd.txt', 'w', encoding='utf-8') as writefile:
        for i in range(1, 101):
            line = readfile.readline()
            if(i<100):
                writefile.writelines(line+'peter\n')
            else:
                writefile.writelines(line+'\npeter\n')

with open('test_name.txt', 'w', encoding='utf-8') as writefile:
    for i in range(1, 101):
        writefile.writelines('carlos\n'+'wiener\n')