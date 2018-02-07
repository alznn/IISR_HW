import re
from gensim.models import word2vec
from gensim import corpora, models, similarities
import json
from pprint import pprint
def regexpRule(line):
    # 書名
    book = u"《[\u4e00-\u9fff]+》"
    # 無法辨識
    unknow = u"[○|△|□]"
    # 程度副詞
    adv = u"[大|更]"
    # 天干
    stime = u"[甲|乙|丙|丁|戊|己|庚|辛|壬|癸]+"
    # 地支
    gtime = u"[子|丑|寅|卯|辰|巳|午|未|申|酉|戌|亥]+"
    # 日期
    number = u"[一|二|三|四|五|六|日|七|八|九|十|千|百|萬]+"
    # 單位
    unit = u"[餘]*[石|丈|兩|錢|斗|里|分|頃|畝|文]"
    # 方位
    direct = u"[東|西|南|北]{1,2}"
    # 地區
    province = u"[北京|天津|上海|重慶|安徽|福建]" #省分
    #city = u"[廈門|合肥|宿州|淮北|阜陽|蚌埠|淮南|滁州|馬鞍山|蕪湖|銅陵|安慶|黃山|六安|巢湖|池州|宣城|亳州]"#城市
    county = u"[界首|明光|天長|桐城|寧國]"
    # 標點符號
    comma = u"[；|﹔|︰|﹕|：|，|﹐|、|．|﹒|˙|·|。|？|！|～|‥|‧|′|〃|〝|〞|‵|‘|’|『|』|「|」|“|”|…|❞|❝|﹁|﹂|﹃|﹄]"
    # 標點符號
    brackets = u"[（|）|〔|〕|【|】|﹝|﹞|〈|〉|﹙|﹚|《|》|（|（|）|｛|｝|﹛|﹜|︵|︶|︷|︸|︹|︺|︻|︼|︽|︾|︿|﹀|＜|＞|∩|∪]"
    string = line

    data = json.load(open('city.json',encoding='utf8'))
    # 處理 無法辨識符號
    if re.findall(unknow, string):
        for reg in re.findall(unknow, string):
            string = string.replace(reg, "")
    #處理 地名
    for i in range(0,len(data)):
        city = data[i]["name"]
        if re.findall(city, string):
            for reg in re.findall(city, string):
                string = string.replace(reg, "C")
    # 處理 書名
    if re.findall(book, string):
        for reg in re.findall(book, string):
            tmp = str(reg)
            string = string.replace(tmp, "B")
    # 處理 標點符號
    if re.findall(comma, string) or re.findall(brackets, string):
        for reg in re.findall(comma, string):
            string = string.replace(reg, "")
        for reg in re.findall(brackets, string):
            string = string.replace(reg, "")
    # 處理 文言文時間
    if re.findall(stime+gtime, string):
        for reg in re.findall(stime+gtime, string):
            string = string.replace(reg, "T")
    #處理 有 時 刻 的地支
    if re.findall(gtime+"刻", string) or re.findall(gtime+"時", string) or re.findall(stime+"時", string) or re.findall(number+"時", string):
        for reg in re.findall(gtime+"刻", string):
            string = string.replace(reg, "T")
        for reg in re.findall(gtime+"時", string):
            string = string.replace(reg, "T")
        for reg in re.findall(stime+"時", string):
            string = string.replace(reg, "T")
        for reg in re.findall(number+"時", string):
            string = string.replace(reg, "T")
    #東西南北
    if re.findall(direct, string):
        for reg in re.findall(direct, string):
            string = string.replace(reg, "P")
    #量詞單位 錢 丈 兩 之類的
    if re.findall(number+unit, string):
#        print('7\n')
        #print(re.findall(number+unit, string))
        for reg in re.findall(number+unit, string):
            string = string.replace(reg, "L")
    #處理年分
    if re.findall(stime+"年", string) or re.findall(number+"年", string):
        for reg in re.findall(stime+"年", string):
            string = string.replace(reg, "Y")
        for reg in re.findall(number+"年", string):
            string = string.replace(reg, "Y")
    #處理日期
    if re.findall("[初]*"+number+"日", string) or re.findall("元旦", string):
        for reg in re.findall("[初]*"+number+"日", string):
            string = string.replace(reg, "D ")
        for reg in re.findall("元旦", string):
            string = string.replace(reg, "D")
    #處理月
    if re.findall(number + "月", string) or re.findall("正月", string):
        for reg in re.findall(number + "月", string):
            string = string.replace(reg, "M")
        for reg in re.findall("正月", string):
            string = string.replace(reg, "M")
    # 無意義副詞 形容詞
    if re.findall(adv, string):
        for reg in re.findall(adv, string):
            string = string.replace(reg, "a")
    return string


def cutWord(line):
    pattern = re.compile('.{1,1}')
    string = ' '.join(pattern.findall(line))
#    English = "[A-Za-z]{1}"
#    book = u"[\u4e00-\u9fff]{1}"
#    if re.findall(English, line) or re.findall(book, line):
#        for reg in re.findall(English, line):
#            line = line.replace(reg, reg+" ")
#        for reg in re.findall(book, line):
#            line = line.replace(reg, reg+" ")
    return string

def traininw2v():
    print("trainingVec")
    sentences = word2vec.LineSentence("data.txt")
    model = word2vec.Word2Vec(sentences, size=200, window=5, min_count=3, min_alpha=0.0025)
#   model = word2vec.Word2Vec(sentences,alpha=0.0025, window=5,size=250)
    # model = word2vec.Word2Vec(sentences,alpha=0.0025, window=5,size=250)

    # 保存模型，供日後使用
    model.save("data_2317.model")
    model.wv.save_word2vec_format('data_txt.txt', binary=False)
    model.wv.save_word2vec_format('data_w2v.w2v', binary=False)
    # 模型讀取方式
    # model = word2vec.Word2Vec.load("data_2317.model")

def dataHandler():
    output = open("origin.txt","w",encoding='utf8')
    import os
    path = "C:/Users/hp/Desktop/clean-4626"  # 文件夹目录
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            f = open(path + "/" + file,'r',encoding='utf8', errors='ignore');  # 打开文件
            iter_f = iter(f);  # 创建迭代器
            str = ""
            for line in iter_f:  # 遍历文件，一行行遍历，读取文本
                str = str + line
            s.append(str)  # 每个文件的文本存到list中
    print(len(s))
    for i in range(0,len(s)):
        output.write(s[i]+'\n')  # 打印结果
    with open('E.txt', 'r', encoding='utf8') as fp:
        for line in fp:
            output.write(line)

#dataHandler()
#string = "夜有流星大如杯色赤光燭地起天棓東北行至天津"
#print(regexpRule(string))
F = open("result1.txt","w",encoding='utf8')
#output = open("all.txt","w",encoding='utf8')
with open('origin.txt','r',encoding='utf8') as fp:
    for line in fp:
        line = regexpRule(line)
        line = cutWord(line)
        F.write(str(line)+'\n')

#traininw2v()
F.close()
fp.close()
