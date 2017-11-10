
output_file=open('/home/emmanuel/Desktop/from-nand2tetris/nand2tetris/projects/07/StackArithmetic/StackTest/StackTest.asm', 'w')

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
    arithmetic operation= add, sub,eq, lt, gt, not, or, and, neg
    '''
    asm=[]
    count=0
    if 'True' not in asm:
        asm.append('@22\n')
        asm.append('D=A\n')
        asm.append('@13\n')  #13 is save the next instruction to run
        asm.append('M=D\n')
        asm.append('A=M\n')
        asm.append('0;JMP\n')

        asm.append('(True)\n')
        asm.append('@SP\n')
        asm.append('A=M\n')
        asm.append('M=-1\n')
        #point sp to next available space and jump to the next instruction
        asm.append('@SP\n')
        asm.append('M=M+1\n')
        asm.append('@13\n')
        asm.append('A=M\n')
        asm.append('0;JMP\n')
        count+=14

    if 'False' not in asm:
        asm.append('(False)\n')
        asm.append('@SP\n')
        asm.append('A=M\n')
        asm.append('M=0\n')
        #point sp to next available space and jump to the next instruction
        asm.append('@SP\n')
        asm.append('M=M+1\n')
        asm.append('@13\n')
        asm.append('A=M\n')
        asm.append('0;JMP\n')
        count+=8

    for line in vm_code:
        if 'push' in line and 'constant' in line:
            #store the value of a constant in the stack pointer and increment the stack pointer
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=A\n')
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=7

        elif line=='eq':

            #checking if the result=0 ?
            #decrement the stack pointer and store its value in the D register.
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            #decrement the stack pointer and complete the addition operation and store the value in the D register
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=D-M\n')
            asm.append('@14\n')   # saves the value of push substraction
            asm.append('M=D\n')
            count+=10
            skip=10
            count+=skip
            asm.append('@'+str(count)+'\n')
            asm.append('D=A\n')
            asm.append('@13\n')
            asm.append('M=D\n')
            asm.append('@14\n')
            asm.append('D=M\n')

            #checking if result=0?
            asm.append('@True\n')
            #count+=12
            asm.append('D;JEQ\n')
            asm.append('@False\n')
            asm.append('D;JNE\n')



        elif line=='lt':

            #checking if the result=0 ?
            #decrement the stack pointer and store its value in the D register.
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            #decrement the stack pointer and complete the addition operation and store the value in the D register
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=D-M\n')
            asm.append('@14\n')
            asm.append('M=D\n')
            count+=10
            skip=10
            count+=skip
            asm.append('@'+str(count)+'\n')
            asm.append('D=A\n')
            asm.append('@13\n')
            asm.append('M=D\n')
            asm.append('@14\n')
            asm.append('D=M\n')
            #checking if result=0?
            asm.append('@True\n')
            #count+=12
            asm.append('D;JGT\n')
            asm.append('@False\n')
            asm.append('D,JLE\n')

        elif line=='gt':

            #checking if the result=0 ?
            #decrement the stack pointer and store its value in the D register.
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            #decrement the stack pointer and complete the addition operation and store the value in the D register
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=D-M\n')
            asm.append('@14\n')
            asm.append('M=D\n')
            count+=10
            skip=10
            count+=skip
            asm.append('@'+str(count)+'\n')
            asm.append('D=A\n')
            asm.append('@13\n')
            asm.append('M=D\n')
            asm.append('@14\n')
            asm.append('D=M\n')
            #checking if result=0?
            asm.append('@True\n')
            #count+=12
            asm.append('D;JLT\n')
            asm.append('@False\n')
            asm.append('D,JGE\n')


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
            count+=13

        elif line== 'sub':
            #decrement the stack pointer and store its value in the D register.
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            #decrement the stack pointer and complete the addition operation and store the value in the D register
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M-D\n')

            #store the addition value in the stack pointer Memory
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')

            #increment the stack pointer
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=13

        elif line== 'neg':
            #decrement the stack pointer and store its value in the D register.
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('M=-M\n')
            #increment the stack pointer
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=6

        elif line== 'and':
            #decrement the stack pointer and store its value in the D register.
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            #decrement the stack pointer and complete the addition operation and store the value in the D register
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=D&M\n')

            #store the  value in the stack pointer Memory
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')

            #increment the stack pointer
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=13

        elif line== 'or':
            #decrement the stack pointer and store its value in the D register.
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            #decrement the stack pointer and complete the addition operation and store the value in the D register
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=D|M\n')

            #store the  value in the stack pointer Memory
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')

            #increment the stack pointer
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=13

        elif line== 'not':
            #decrement the stack pointer and store its value in the D register.
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=!M\n')
            #decrement the stack pointer and complete the addition operation and store the value in the D register
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')

            #increment the stack pointer
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=9



    for line in asm:
        output_file.write(line)
    output_file.close()
    return asm

def memory_acc(lst):
    ''' this function takes a list of VM command and convert it to assembly code by sending virtual addresses to their physical
    location '''
    asm=[]
    for line in lst:
        if 'pop' in line.split() and 'local' in line.split():
            asm.append('@LCL')
            asm.append('D=M')
            asm.append('@'+line.split()[-1])
            asm.append('D=D+A')
            asm.append('@14')
            #this the local address ready to be used
            asm.append('M=D')
            #now we can pop the value in the  right local address
            asm.append('@SP')
            asm.append('M=M-1')
            asm.append('A=M')
            asm.append('D=M')
            asm.append('@14')
            asm.append('A=M')
            asm.append('M=D')

        if 'pop' in line.split() and 'argument' in line.split():
            asm.append('@ARG')
            asm.append('D=M')
            asm.append('@'+line.split()[-1])
            asm.append('D=D+A')
            asm.append('@14')
            #this the argument address ready to be used
            asm.append('M=D')
            #now we can pop the value in the  right argument address
            asm.append('@SP')
            asm.append('M=M-1')
            asm.append('A=M')
            asm.append('D=M')
            asm.append('@14')
            asm.append('A=M')
            asm.append('M=D')

        if 'pop' in line.split() and 'this' in line.split():
            asm.append('@THIS')
            asm.append('D=M')
            asm.append('@'+line.split()[-1])
            asm.append('D=D+A')
            asm.append('@14')
            #this the 'this' address ready to be used
            asm.append('M=D')
            #now we can pop the value in the  right 'this' address
            asm.append('@SP')
            asm.append('M=M-1')
            asm.append('A=M')
            asm.append('D=M')
            asm.append('@14')
            asm.append('A=M')
            asm.append('M=D')


        if 'pop' in line.split() and 'that' in line.split():
            asm.append('@THAT')
            asm.append('D=M')
            asm.append('@'+line.split()[-1])
            asm.append('D=D+A')
            asm.append('@14')
            #this the that address ready to be used
            asm.append('M=D')
            #now we can pop the value in the  right 'that' address
            asm.append('@SP')
            asm.append('M=M-1')
            asm.append('A=M')
            asm.append('D=M')
            asm.append('@14')
            asm.append('A=M')
            asm.append('M=D')

        if 'pop' in line.split() and 'temp' in line.split():
            asm.append('@5') #temp= register 5, temp i= register (5+i)
            asm.append('D=A')
            asm.append('@'+line.split()[-1])
            asm.append('D=D+A')
            asm.append('@14')
            #this the temp address ready to be used
            asm.append('M=D')
            #now we can pop the value in the  right temp address
            asm.append('@SP')
            asm.append('M=M-1')
            asm.append('A=M')
            asm.append('D=M')
            asm.append('@14')
            asm.append('A=M')
            asm.append('M=D')

            asm.append('')
            asm.append('')
            asm.append('')
            asm.append('')
            asm.append('')
            asm.append('')



file_check=open('file2','w')
test1=StackArithmetic(test)
ex_lst=[]
for i in test1:
    if '(' not in i:
        ex_lst.append(i)
count=0
for e in ex_lst:
    count+=1
    file_check.write(str(count-1)+'   '+e)
