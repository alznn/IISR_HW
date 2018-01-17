import re

def regreplace(line):
#1 月日年
    Format1 = '(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:st)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:vember)?|Dec(?:ember)?)\.?\s[0-3][0-9][,][\s]?[1-9]{3,4}'
#2 月日
    Format2 = '(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:st)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:vember)?|Dec(?:ember)?)\.?\s[0-3]?[0-9]'
#3 月日-日 年
    Format3 = '(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:st)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:vember)?|Dec(?:ember)?)\.?\s[0-3][0-9]-[0-3][0-9][,]\s?[1-9]{3,4}'
#4 月日in年
    Format4 = '(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:st)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:vember)?|Dec(?:ember)?)\.?\s[0-9]{,2}\s?in?\s[1-9]{3,4}'
# 日/日-日/日
    Date1 = '([1-9]/[0-3]?[0-9]|[1][0-2]/[0-3][0-9]-[1-9]/[0-3]?[0-9]|[1][0-2]/[0-3][0-9])'
# 日-日
    Date2 = '([0-9]{1,4}[\-][0-9]{1,4})'
#月
    Month = '(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:st)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:vember)?|Dec(?:ember)?)\.?'
#年
    year = '[i|I]n\s[1-9]{4}|[i|I]n\sthe\s[1-9]{4}|from\s[1-9]{4}|[1-9][0-9]{3}'
    print("--------------------------------------------------------------------------")
    print(line)
    reg = [Format1,Format2,Format3,Date1,Date2,Month,year]
#    line = 'in the 1991 The Chinese Lunar New Y 1/3-1/4 ear fell on Jan. 22-18, 1873 18-22' 
    if re.findall(Format1,line):
        print('1\n')
        print(re.findall(Format1,line))
        for reg in re.findall(Format1,line):
            line = line.replace(reg,"<t>"+reg+"<\\t>")
            print(line)
    elif re.findall(Format3,line):
        print('3\n')
        print(re.findall(Format3,line))
        for reg in re.findall(Format3,line):
            line = line.replace(reg,"<t>"+reg+"<\\t>")
            print(line)
    elif re.findall(Format4,line):
        print('6\n')
        print(re.findall(Format4,line))
        for reg in re.findall(Format4,line):
            line = line.replace(reg,"<t>"+reg+"<\\t>")
            print(line)
    elif re.findall(Format2,line):
        print('2\n')
        print(re.findall(Format2,line))
        for reg in re.findall(Format2,line):
            line = line.replace(reg,"<t>"+reg+"<\\t>")
            print(line)
    elif re.findall(Date1,line):
        print('4\n')
        print(re.findall(Date1,line))
        for reg in re.findall(Date1,line):
            line = line.replace(reg,"<t>"+reg+"<\\t>")
            print(line)
    elif re.findall(Date2,line):
        print('5\n')
        print(re.findall(Date2,line))
        for reg in re.findall(Date2,line):
            line = line.replace(reg,"<t>"+reg+"<\\t>")
            print(line)
    elif re.findall(Month,line):
        print('7\n')
        print(re.findall(Month,line))
        for reg in re.findall(Month,line):
            line = line.replace(reg,"<t>"+reg+"<\\t>")
            print(line)
    elif re.findall(year,line):
        print('8\n')
        print(re.findall(year,line))
        for reg in re.findall(year,line):
            line = line.replace(reg,"<t>"+reg+"<\\t>")
            print(line)
    else: 
        print("non match!\n")
    outputFile(line)

def outputFile(line):
    print(line)
    with open('outout1.txt', 'a') as the_file:
        the_file.write(line)
        the_file.write('\n')
    
text = 'in 1991 The Chinese Lunar New Y 1/3-1/4 ear fell on Jan. 22-18, 1873 18-22' 
#regreplace(text)
with open('Taiwan.txt') as fp:
    for line in fp:
        regreplace(line)
