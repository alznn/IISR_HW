import re


def regreplace(line):
#1 First and last Name
    FLName = '(([A-Z]{1}[a-z]+) ([A-Z]{1}[a-z]+))$'
#2 Gental
    Gental = '((Miss|Mrs|Mr)\s([A-Z][a-z]+))'
#3 introduce
    Name = '((name)\s(is)\s([A-Z][a-z]*(\s[A-Z][a-z]*)*))'
    print("----------------------------------------------------------------------------------------------")
    
    if re.search(Gental,line):
        reg = re.search(Gental,line)
        print(reg.group())
        print('1\n')
        reg = re.findall(Gental,line)
        for i in range(0,len(re.findall(Gental,line))):
            print(line)
            print(reg[i][2])
            tmp = "<t>"+str(reg[i][2])+"<\\t>"
            line = line.replace(reg[i][2],tmp)
            print(line)
    elif re.search(Name,line):
        reg = re.search(Name,line)
        print(reg.group())
        print('2\n')
        reg = re.findall(Name,line)
        for i in range(0,len(re.findall(Name,line))):
            print(line)
            print(reg[i][3])
            tmp = "<t>"+str(reg[i][3])+"<\\t>"
            line = line.replace(reg[i][3],tmp)
            print(line)
    if re.search(FLName,line):
        print('3\n')
        reg = re.findall(FLName,line)
        for i in range(0,len(re.findall(FLName,line))):
            print(line)
            print(reg)
            print(reg[i][0])
            tmp = "<t>"+str(reg[i][0])+"<\\t>"
            line = line.replace(reg[i][0],tmp)
            print(line)
    outputFile(line)

def outputFile(line):
    print(line)
    with open('outout2.txt', 'a',encoding='utf8') as the_file:
        the_file.write(line)
        the_file.write('\n')

with open('novel.txt',encoding='utf8') as fp:
    for line in fp:
        regreplace(line)
