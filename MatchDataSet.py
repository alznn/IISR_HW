import json

import yaml
from itertools import takewhile
import xlrd

stream = open("氣象詞彙與編碼表1.yaml", 'r',encoding='utf8')
data = yaml.load(stream)

wb = xlrd.open_workbook('已分類資料.xlsx')
sheet = wb.sheet_by_index(0)  #表示讀第幾張表，初始為0

clf = ""
main = ""
sub = ""
anly = ""
weather_text = []
weather_anly = []
def column_len(sheet, index):
    col_values = sheet.col_values(index)
    col_len = len(col_values)
    for _ in takewhile(lambda x: not x, reversed(col_values)):
        col_len -= 1
    return col_len

def MatchState(string):
    col_len = column_len(sheet, 8)
    anly = ""
    print("================================================================================================")
    print(string)
    for index in range (1,col_len):
        # print("22:::", sheet.cell(rowx=index, colx=2).value)
        if(string.strip() == str(sheet.cell(rowx = index, colx = 2).value)):
            #print("Get in if")
            if sheet.cell(rowx = index, colx = 8).value == '-9999' or sheet.cell(rowx = index, colx = 8).value == '-98':
                anly = data[sheet.cell(rowx = index, colx = 8).value]
                # print("Get in ifif")
            else:
                # print("Get in ifelse")
                clf = sheet.cell(rowx = index, colx = 8).value[0]+sheet.cell(rowx = index, colx = 8).value[1]
                #print(clf," , ",len(clf))
                main = sheet.cell(rowx = index, colx = 8).value[2]+sheet.cell(rowx = index, colx = 8).value[3]
                #print(main," , ",len(main))
                sub = sheet.cell(rowx=index, colx=8).value[4] + sheet.cell(rowx=index, colx=8).value[5]+sheet.cell(rowx = index, colx = 8).value[6]
                #print(sub," , ",len(sub))
                try:
                    #print("Get in try")
                    anly = data[clf][main][sub]['name']
                except KeyError:
                    anly = "none"
                    #print("1")
            print(anly)
            return anly

    anly = "none"
    print(anly)
    return anly
#===========================================================
import os
#path = "C:\\Users\\hp\\PycharmProjects\\weather\\"+k
#if not os.path.isdir(path):
#    os.mkdir(path)
print("Here is Matchdata")
with open('E.txt', 'r', encoding='utf8') as fp:
    for line in fp:
        weather_text.append(line)
#len(weather_text)
for i in range(0, len(weather_text)):
    weather_anly.append(MatchState(weather_text[i]))

W = open('對照資料.txt', 'w', encoding='utf8')
for line in range(0,len(weather_anly)):
    W.write(weather_anly[line])
    W.write("\n")
W.close()
#F = open("Ans.csv", "a", encoding='utf8')
#for i in range(0, len(weather_text)):
#    if(i % 1000 == 0):
#        print("classfy: ",i,"\n")
#        F.write(weather_text[i] + "," + weather_anly[i])
#F.close()