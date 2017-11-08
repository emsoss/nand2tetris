
output_file=open('/home/emmanuel/Desktop/from-nand2tetris/nand2tetris/projects/07/StackArithmetic/SimpleAdd/SimpleAdd.asm', 'w')

def rmv_comments(file):
    '''remove line starting by // and in code commenting'''
    fh=open(file,'r')
    txt=fh.read()
    new_list=[]
    p=txt.split('\n')
    for line in p:
        line=line.strip()
        if line.startswith('/')==False and line !='':
            candidate=line
            if '/' in candidate:
                idx=candidate.index('/')
                candidate=candidate[:idx]
                new_list.append(candidate.strip())
            else:
                new_list.append(candidate.strip())
    return new_list

test=rmv_comments('simpleadd.asm')
for i in test:
    print i

def StackArithmetic(vm_code):
    '''
    this function implement the arithmetic operation of a stack machine. it convert the VM Language to Jack assembly code
    '''
    asm=[]
    for line in vm_code:
        if 'push' in line and 'constant' in line:
            #store the value of a constant in the stack pointer and increment the stack pointer
            asm.append('@'+str(line[-1])+'\n')
            asm.append('D=A\n')
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            asm.append('@SP\n')
            asm.append('M=M+1\n')

        elif line== 'add':
            #decrement the stack pointer and store its value in the D register.
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            #decrement the stack pointer and complete the addition operation and store the value in the D register
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=D+M\n')

            #store the addition value in the stack pointer Memory
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')

            #increment the stack pointer
            asm.append('@SP\n')
            asm.append('M=M+1\n')

    for line in asm:
        output_file.write(line)
    output_file.close()
    return asm


test1=StackArithmetic(test)
print 'lenght', len(test1), test
for i in test1:
    print i
