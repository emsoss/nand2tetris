import os

path='/home/emmanuel/Desktop/programming_project/from-nand2tetris/git-nand2tetris/output_file'
path1='/home/emmanuel/Desktop/programming_project/from-nand2tetris/git-nand2tetris/input_file'

output_file=open(path, 'w')
os.remove('input_file') # removes input_file if it exist and recreate it. in the next line.
input_file=open(path1, 'w')

def combine_vmfile(directory):
    files=os.listdir(directory)

    print 'files', files
    for file in files:
        if file.startswith('Sys'):
            fh=open(file,'r')
            txt=fh.read()
            input_file.write(txt)

    for file in files:
        if file.endswith('.vm') and file!='Sys.vm':
            fh=open(file,'r')
            txt=fh.read()
            input_file.write(txt)


def rmv_comments(file):
    '''remove line starting by // and in code commenting and removes spaces'''
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


def StackArithmetic(vm_code):
    '''
     function implement the arithmetic operation of a stack machine. it convert the VM Language to Jack assembly code
    arithmetic operation= add, sub,eq, lt, gt, not, or, and, neg
    '''
    asm=[]
    count=0
    #the True and False label are placed at the top in assembly code. initial point where the
    #execution should start is line 22 so we save 22 in RAM 13 which is a general purpose memory aand
    #we jump to it. that is what the below code is doing.
    if 'True' not in asm:
        asm.append('@22\n')
        asm.append('D=A\n')
        asm.append('@13\n')  #13 is save the next instruction to run
        asm.append('M=D\n')
        asm.append('A=M\n')
        asm.append('0;JMP\n')

    #the below code initializes the True segment of the assembly code for ex
    #if we push 3 and push 4 and want to run the code gt. if the result is true the the execution jumps to this segment
    #which starts on line 6 in assembly code. from here -1 which means True is written to memory of the current Stack
    #and we jump to the address saved in RAM 13 which was saved before jumping here.


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

    #the below if statement initializes the False segment of the assembly code for ex
    #if we push 3 and push 4 and want to run the code gt. the code will jump to this segment
    #which starts at on line 15 in assembly code

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
        #push constant value implementation
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
            count+=skip  #this is the address that should be jump to from True/False label segment
            asm.append('@'+str(count)+'\n')
            asm.append('D=A\n')
            asm.append('@13\n')
            asm.append('M=D\n')
            asm.append('@14\n')
            asm.append('D=M\n')

            #checking if result=0?
            asm.append('@True\n')

            #from here we go to the False label or True label. depending on the value of D. from the label
            #we jump to the address saved in RAM 14.
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



            ''' this function takes a list of VM command and convert it to assembly code by sending virtual addresses to their physical
            location '''

        elif 'pop' in line.split() and 'local' in line.split():
            #implementation for ex pop local 5. removes the last value pushed on the stack to the memory located at local 5.
            #LCL is a pointer for the base of the local segment. so local 5 is LCL+5. so to effect a pop local value operation
            #we select the LCL point and add the value of the pop command to the content of LCL. next save the resultant value
            #to RAM 14 which is a general purpose memory. next we remove the value from stack(sp) to the addr that RAM 14
            #points to.
            asm.append('@LCL\n')
            asm.append('D=M\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('@14\n')  #save the addr of local 5 in the general purpose RAM 14
            #this the local address ready to be used
            asm.append('M=D\n')
            #now we can pop the value in the  right local address
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            asm.append('@14\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            count+=13

        elif 'pop' in line.split() and 'argument' in line.split():
            asm.append('@ARG\n')
            asm.append('D=M\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('@14\n')
            #this the argument address ready to be used
            asm.append('M=D\n')
            #now we can pop the value in the  right argument address
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            asm.append('@14\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            count+=13

        elif 'pop' in line.split() and 'this' in line.split():
            asm.append('@THIS\n')
            asm.append('D=M\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('@14\n')
            #this the 'this' address ready to be used
            asm.append('M=D\n')
            #now we can pop the value in the  right 'this' address
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            asm.append('@14\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            count+=13


        elif 'pop' in line.split() and 'that' in line.split():
            asm.append('@THAT\n')
            asm.append('D=M\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('@14\n')
            #this the that address ready to be used
            asm.append('M=D\n')
            #now we can pop the value in the  right 'that' address
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            asm.append('@14\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            count+=13

        elif 'pop' in line.split() and 'temp' in line.split():
            asm.append('@5\n') #temp= register 5, temp i= register (5+i)
            asm.append('D=A\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('@14\n')
            #this the temp address ready to be used
            asm.append('M=D\n')
            #now we can pop the value in the  right temp address
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            asm.append('@14\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            count+=13

        #the below condition implement for ex: pop pointer 1. pointer 0 refers to THIS
        #and point That refers to That
        elif 'pop' in line.split() and 'pointer' in line.split():
            asm.append('@3\n') #pointer= register 3, pointer i= register (3+i)
            asm.append('D=A\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('@14\n')
            #this the temp address ready to be used
            asm.append('M=D\n')
            #now we can pop the value in the  right pointer address
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            asm.append('@14\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            count+=13

        elif 'pop' in line.split() and 'static' in line.split():
            asm.append('@16\n') #pointer= register 3, pointer i= register (3+i)
            asm.append('D=A\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('@14\n')
            #this the temp address ready to be used
            asm.append('M=D\n')
            #now we can pop the value in the  right pointer address
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            asm.append('@14\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            count+=13

        elif 'push' in line and 'argument' in line:
            #store the value of a constant in the stack pointer and increment the stack pointer
            asm.append('@ARG\n')
            asm.append('D=M\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('A=D\n')
            asm.append('D=M\n')      #this the value contained in argument addr
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=11

        elif 'push' in line and 'argument' in line:
            #store the value of a constant in the stack pointer and increment the stack pointer
            asm.append('@ARG\n')
            asm.append('D=M\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('A=D\n')
            asm.append('D=M\n')      #this the value contained in argument addr
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=11

        elif 'push' in line and 'local' in line:
            #store the value of a constant in the stack pointer and increment the stack pointer
            asm.append('@LCL\n')
            asm.append('D=M\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('A=D\n')
            asm.append('D=M\n')      #this the value contained in argument addr
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=11

        elif 'push' in line and 'that' in line:
            #store the value of a constant in the stack pointer and increment the stack pointer
            asm.append('@THAT\n')
            asm.append('D=M\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('A=D\n')
            asm.append('D=M\n')      #this the value contained in argument addr
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=11

        elif 'push' in line and 'this' in line:
            #store the value of a constant in the stack pointer and increment the stack pointer
            asm.append('@THIS\n')
            asm.append('D=M\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('A=D\n')
            asm.append('D=M\n')      #this the value contained in argument addr
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=11

        elif 'push' in line and 'temp' in line:
            #store the value of a constant in the stack pointer and increment the stack pointer
            asm.append('@5\n')
            asm.append('D=A\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('A=D\n')
            asm.append('D=M\n')      #this the value contained in argument addr
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=11

        elif 'push' in line and 'pointer' in line:
            #store the value of a constant in the stack pointer and increment the stack pointer
            asm.append('@3\n')
            asm.append('D=A\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('A=D\n')
            asm.append('D=M\n')      #this the value contained in argument addr
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=11

        elif 'push' in line and 'static' in line:
            #store the value of a constant in the stack pointer and increment the stack pointer
            asm.append('@16\n')
            asm.append('D=A\n')
            asm.append('@'+line.split()[-1]+'\n')
            asm.append('D=D+A\n')
            asm.append('A=D\n')
            asm.append('D=M\n')      #this the value contained in argument addr
            asm.append('@SP\n')
            asm.append('A=M\n')
            asm.append('M=D\n')
            asm.append('@SP\n')
            asm.append('M=M+1\n')
            count+=11

        #the next elif implement label insertion and if-go command.
        elif 'label' in line :
            label_name= line.split(' ')[1:][0]
            asm.append('('+label_name+')\n')

        elif 'if-goto' in line:
            label_name= line.split(' ')[1:][0]

            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n')
            asm.append('@'+label_name+'\n')
            asm.append('D;JGT\n')

        #unconditional jump implementation. ex: goto End_program
        elif line.startswith('goto'):
            label_name=line[5:]
            asm.append('@'+label_name+'\n')
            asm.append('0;JMP\n')

        elif line=='return':
            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')
            asm.append('D=M\n') # stores value to be returned in D register
            asm.append('@ARG\n')
            asm.append('A=M\n')
            asm.append('M=D\n') #stores the returned value in addr pointed by arg

            asm.append('@ARG\n')
            asm.append('D=M\n')
            asm.append('@13\n')
            asm.append('M=D+1\n') #store arg0 pointer +1 in register 13 which is a general purpose register

            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')  #selects the saved That
            asm.append('D=M\n')
            asm.append('@THAT\n') #THAT=register 4
            asm.append('M=D\n')

            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')  #selects the saved This
            asm.append('D=M\n')
            asm.append('@THIS\n')  #THIS =register 3
            asm.append('M=D\n')

            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')  #selects the saved ARG
            asm.append('D=M\n')
            asm.append('@ARG\n')
            asm.append('M=D\n')


            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')  #selects the saved LCL
            asm.append('D=M\n')
            asm.append('@LCL\n')
            asm.append('M=D\n')

            asm.append('@SP\n')
            asm.append('M=M-1\n')
            asm.append('A=M\n')  #selects the saved address
            asm.append('D=M\n')
            asm.append('@14\n') # store the return address in register 14
            asm.append('M=D\n')

            asm.append('@13\n')
            asm.append('D=M\n') #this is where the stack point should be after the func returns
            asm.append('@SP\n')
            asm.append('M=D\n') #

            asm.append('@14\n')
            asm.append('A=M\n')  #select the return address and jump to it
            asm.append('0;JMP\n')



    for line in asm:
        output_file.write(line)
    output_file.close()
    return asm

#combine all .vm file in a given directory.
combine_vmfile('/home/emmanuel/Desktop/programming_project/from-nand2tetris/git-nand2tetris')
#def memory_acc(lst):
test=rmv_comments('simpleadd.asm')
for i in test:
    print i

file_check=open('file2','w')
test1=StackArithmetic(test)
ex_lst=[]
for i in test1:
    #if '(' not in i:
    ex_lst.append(i)
count=0
for e in ex_lst:
    count+=1
    file_check.write(str(count-1)+'   '+e)
