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
    for line vm_code lst:
        if push in vm_code and constant in vm_code:
            #store the value of a constant in the stack pointer and increment the stack pointer
            asm.append('@SP')
            asm.append('A=M')
            asm.append('M='+str(line[-1]))
            asm.append('@SP')
            asm.append('M=M+1')

        elif line== add:
            #decrement the stack pointer and store its value in the D register.
            asm.append('@SP')
            asm.append('M=M-1')
            asm.append('A=M')
            asm.append('D=M')
            #decrement the stack pointer and complete the addition operation and store the value in the D register
            asm.append('@SP')
            asm.append('M=M-1')
            asm.append('A=M')
            asm.append('D=D+M')

            #store the addition value in the stack pointer Memory
            asm.append('@SP')
            asm.append('A=M')
            asm.append('M=D')
    return asm

print test1=StackArithmetic(test)
