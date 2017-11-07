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
