import pandas as pd
import numpy
import re


data = pd.read_csv("post_process.csv", sep=",", header=None)
data.columns = ["ID","IsCorrect", "Name", "ID", "TitleAndYear","Text","Links"]
CheckName = data["Name"].as_matrix()
ContentText = data["Text"].as_matrix()
Number2 = []
errCollect = []

CheckData2 =[]
CheckData3 =[]
CheckData4 =[]
print("################ 第二階段後處理 ######################")

for i in range(len(data['Name'])):
    if data.index[len(data['Name'][i]) ==2]:
        Number2.append(i)
    else:continue

print("################ 名字錄長度分類 ######################")
Names = pd.read_csv("Names.csv", sep="	", header=None)
Names.columns = ["Name"]
names = Names["Name"].as_matrix()

for name in names:
    if len(name) == 3:
        CheckData3.append(name)
    elif len(name)>3:
        CheckData4.append(name)
    elif len(name)==2:
        CheckData2.append(name)

print(Number2)
count = 0
for index in Number2:
    count+=1
#    nameList = []
    if count % 1000 == 0:
        print("############# ", index, " ##############")
    for name3 in CheckData3:
        reg = name3+CheckName[index][1]
        if re.search(reg,ContentText[index]):
            if(name3[2] == CheckName[index][0]):
                errCollect.append(index)
#                nameList.append(name3)

data.take(errCollect).to_csv("err.csv",mode="a", header=False)
data3 = data.drop(errCollect)
data3.to_csv("Post_post_process.csv", header=False)

