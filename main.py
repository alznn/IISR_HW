import re
import pandas as pd

name = "<[^\>]+>[^<]+<\/P>"
data = pd.read_csv("DataSet.csv")
data = data.drop(["paraId","fileId","year","title","date"], axis=1)
contexs = data["text"].as_matrix()
names = []

for contex in contexs:
    if re.findall(name, contex):
        for reg in re.findall(name, contex):
            tmp = str(reg)
            tmp = re.sub('^<P>', '', tmp)
            tmp = re.sub('</P>$', '', tmp)
            names.append(tmp)
#            if(isNotExit(tmp)):
#                names.append(tmp)

names = list(set(names))
print(data.shape)
names = sorted(names)
data1 = pd.Series(names)
data1.to_csv("Names.csv",encoding='utf-8', index = False)

data2 = pd.read_csv("21214.txt", sep="	", header=None)
data2.columns = ["IsCorrect", "Name", "ID", "TitleAndYear","Text","Links"]

CheckName = data2["Name"].as_matrix()
ContentText = data2["Text"].as_matrix()

print(CheckName)
dicTest2 = {}
dicTest3 = {}
dicTestS = {}
li = []
tmp=""
for count in range(len(CheckName)-1):
    if len(CheckName[count]) == 2:
        if CheckName[count] == CheckName[count+1]:
            li.append(count)
        else:
            lii=[]
            li.append(count)
            lii.clear()
            for it in li:
                lii.append(it)
            tmp = CheckName[count]
            dicTest2[tmp]=lii
            li.clear()
    elif len(CheckName[count]) == 3:
        if CheckName[count] == CheckName[count+1]:
            li.append(count)
        else:
            ii=[]
            li.append(count)
            for it in li:
                ii.append(it)
            tmp = CheckName[count]
            dicTest3[tmp]=ii
            li.clear()
    else:
        if CheckName[count] == CheckName[count+1]:
            li.append(count)
        else:
            ii=[]
            li.append(count)
            for it in li:
                ii.append(it)
            tmp = CheckName[count]
            dicTestS[tmp]=ii
            li.clear()

print("name2 : \n",dicTest2)
# print("\n\n\nname3 : \n",dicTest3)
buf = []
errCollect = []
for n in dicTest2:
    print("############################")
    reg = n
    print("tmp  ",tmp)
#    reg = "吳良."
    print("---------------處理文本相似名字------------------")
    for name in names:
        if re.match(reg, name):
            buf.append(name)
    print(buf)
    count = 0
    print("---------------處理內文重複名字------------------")
    for index in range(len(dicTest2[n])):
        for i in buf:
            if(i == reg):
                continue
            # print(i,"\n")
            #print(ContentText[dicTest2[n][index]])
            if re.findall(i,ContentText[dicTest2[n][index]]):
#                print(ContentText[dicTest2[n][index]])
                print(i,"有錯誤重複了!!!")
#                errCollect.append(data2[1:dicTest2[n][index]])
                errCollect.append(dicTest2[n][index])
                count+=1
                continue
    buf.clear()
    print(errCollect)

data2.take(errCollect).to_csv("err.csv", header=False)
data3 = data2.drop(errCollect)
data3.to_csv("post_process.csv", header=False)