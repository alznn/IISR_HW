import csv
import re
from gensim.models import word2vec
from gensim import corpora, models, similarities
place = "<[^\>]+>[^<]+<\/L>"
name = "<[^\>]+>[^<]+<\/P>"
occupy = "<[^\>]+>[^<]+<\/O>"
army = "<[^\>]+>[^<]+<\/W>"
foreign = "<[^\>]+>[^<]+<\/B>"
unknow = u"[○|△|□]"
# 書名
book = u"《[\u4e00-\u9fff]+》"
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
# 標點符號
comma = u"[；|﹔|︰|﹕|：|，|﹐|、|．|﹒|˙|·|。|？|！|～|‥|‧|′|〃|〝|〞|‵|‘|’|『|』|「|」|“|”|…|❞|❝|﹁|﹂|﹃|﹄]"
# 標點符號
brackets = u"[（|）|〔|〕|【|】|﹝|﹞|〈|〉|﹙|﹚|《|》|（|（|）|｛|｝|﹛|﹜|︵|︶|︷|︸|︹|︺|︻|︼|︽|︾|︿|﹀|＜|＞|∩|∪]"


def regEXP(string):
    if re.findall(foreign, string):
        for reg in re.findall(foreign, string):
            tmp = str(reg)
            string = string.replace(tmp, "P")
    if re.findall(place, string):
        for reg in re.findall(place, string):
            tmp = str(reg)
            string = string.replace(tmp, "P")
    if re.findall(name, string):
        for reg in re.findall(name, string):
            tmp = str(reg)
            string = string.replace(tmp, "N")
    if re.findall(occupy, string):
        for reg in re.findall(occupy, string):
            tmp = str(reg)
            string = string.replace(tmp, "O")
    if re.findall(army, string):
        for reg in re.findall(army, string):
            tmp = str(reg)
            string = string.replace(tmp, "W")
    if re.findall(unknow, string):
        for reg in re.findall(unknow, string):
            string = string.replace(reg, "")
    if re.findall(book, string):
        for reg in re.findall(book, string):
            tmp = str(reg)
            string = string.replace(tmp, "B")
    if re.findall(comma, string) or re.findall(brackets, string):
        for reg in re.findall(comma, string):
            string = string.replace(reg, "")
        for reg in re.findall(brackets, string):
            string = string.replace(reg, "")
    # 處理 文言文時間
    if re.findall(stime + gtime, string):
        for reg in re.findall(stime + gtime, string):
            string = string.replace(reg, "T")
    # 處理 有 時 刻 的地支
    if re.findall(gtime + "刻", string) or re.findall(gtime + "時", string) or re.findall(stime + "時",
                                                                                        string) or re.findall(
            number + "時", string):
        for reg in re.findall(gtime + "刻", string):
            string = string.replace(reg, "T")
        for reg in re.findall(gtime + "時", string):
            string = string.replace(reg, "T")
        for reg in re.findall(stime + "時", string):
            string = string.replace(reg, "T")
        for reg in re.findall(number + "時", string):
            string = string.replace(reg, "T")
    # 東西南北
    if re.findall(direct, string):
        for reg in re.findall(direct, string):
            string = string.replace(reg, "D")
    # 量詞單位 錢 丈 兩 之類的
    if re.findall(number + unit, string):
        for reg in re.findall(number + unit, string):
            string = string.replace(reg, "L")
    # 處理年分
    if re.findall(stime + "年", string) or re.findall(number + "年", string):
        for reg in re.findall(stime + "年", string):
            string = string.replace(reg, "Y")
        for reg in re.findall(number + "年", string):
            string = string.replace(reg, "Y")
    # 處理日期
    if re.findall("[初]*" + number + "日", string) or re.findall("元旦", string):
        for reg in re.findall("[初]*" + number + "日", string):
            string = string.replace(reg, "D ")
        for reg in re.findall("元旦", string):
            string = string.replace(reg, "D")
    # 處理月
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


def traininw2v():
    print("trainingVec")
    sentences = word2vec.LineSentence("result.txt")
    model = word2vec.Word2Vec(sentences, size=200, window=5, min_count=10, min_alpha=0.0025, sg=1)
#   model = word2vec.Word2Vec(sentences,alpha=0.0025, window=5,size=250)
    # model = word2vec.Word2Vec(sentences,alpha=0.0025, window=5,size=250)

    # 保存模型，供日後使用
    model.save("w2vdata.model")
    model.wv.save_word2vec_format('w2vdata.txt', binary=False)
    model.wv.save_word2vec_format('w2vdata.w2v', binary=False)
    # 模型讀取方式
# model = word2vec.Word2Vec.load("data_2317.model")

def writeFile(data,filename):
    #寫檔
    pattern = re.compile('.{1,1}')
    F = open(filename, "w", encoding='utf8')
    print(len(data))
    for i in range(0, len(data)):
        string = ' '.join(pattern.findall(data[i]))
        F.write(str(string)+'\n')
        print(string+'\n')
    F.close()
    print("write file done")

def normalwriteFile(data,filename):
    #寫檔
    F = open(filename, "w", encoding='utf8')
    print(len(data))
    for i in range(0, len(data)):
        F.write(str(data[i])+'\n')
#        print((str(data[i])+'\n'))
    F.close()
    print("write file done")


def dataHandler():
    count = 0
    data = []

    #處理天資料
    with open('E.txt','r',encoding='utf8') as fp:
        for line in fp:
            line = regEXP(line)
            data.append(line)
    fp.close()
    writeFile(data, "test1.txt")
    #處理明實錄
    f = open('NewParagraph-data.csv', 'r', encoding='utf-8')
    for row in csv.reader(f):
        string = regEXP(row[4])
        data.append(string)
        count = count + 1
    f.close()
    writeFile(data, "test.txt")
    print(" data handler done")

def caculate():
    print("caculate")
    data = []
    result = []
    #處理天資料
    with open('test1.txt','r',encoding='utf8') as fp:
        for line in fp:
            data.append(line)
    fp.close()
    pattern = re.compile('.{1,1}')
    model = word2vec.Word2Vec.load("w2vdata.model")
    word_vectors = model.wv
    sum = [0 for x in range(200)]
    c = []
    print(len(data))
    for index in range(len(data)):
        print(index)
        sum = [0 for x in range(200)]
        for reg in pattern.findall(data[index]):
            print(index,"    ",len(data[index]))
            if reg == ' ':
                continue
            else:
                if reg in word_vectors.vocab:
                    for j in range(0, (len(model[reg]))):
                        sum[j] = sum[j] + model[reg][j]
                    for i in range(0, (len(sum))):
                        sum[i] = round(sum[i] / len(data[index]),6)
        result.append(sum)
    print(len(result))
    normalwriteFile(result, "result_w2v.txt")
    Kmenans(result)

def Kmenans():
    print("Kmenans")
    from sklearn import cluster, datasets,metrics
    X =[]
    with open('result_w2v_binary.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            tmp = []
            print(len(row))
            for i in range(0, len(row)-1):
                if (row[i] == ' '):
                    continue
                else:
#                    print(i)
#                    print(row[i])
                    f = float(row[i])
                    tmp.append(f)
            X.append(tmp)
            print(X)
    import matplotlib.pyplot as plt
    kmeans = cluster.KMeans(5)
    kmeans.fit(X)

    cluster_labels = kmeans.labels_
    print("分群結果：")
    with open('分群.txt', 'a') as the_file:
        the_file.write(str(cluster_labels))
    print(cluster_labels)
    print(len(cluster_labels))
    print("---")

    #最佳群
    # 迴圈
    silhouette_avgs = []
    ks = range(10, 30)
    for k in ks:
        kmeans_fit = cluster.KMeans(k).fit(X)
        cluster_labels = kmeans_fit.labels_
        silhouette_avg = metrics.silhouette_score(X, cluster_labels)
        silhouette_avgs.append(silhouette_avg)

    # 作圖並印出 k = 10 到 30 的績效
    plt.bar(ks, silhouette_avgs)
    plt.show()
    print(silhouette_avgs)
caculate()
