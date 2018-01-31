import logging
import jieba
import jieba.posseg as pseg
import jieba.analyse
import re
from operator import itemgetter
#model.save("data_2317.model")
#model.wv.save_word2vec_format('data_txt.txt', binary=False)
#model.wv.save_word2vec_format('data_w2v.w2v', binary=False)

from gensim.models import word2vec
from gensim import corpora, models, similarities

import numpy
import csv

from sklearn.linear_model import LogisticRegression

sum = [0 for x in range(100)]
train_vec = []
train_and = []
test_vec = [0 for x in range(100)]
test_ans = []
data = []
text = []
date = '2015/0[1-9]/[0-9][1-9]'
num = '[0-9]{3,}'
id = '[A-Z][0-9]+'
regup = "[*][漲|升]"
positive = ["上升", "上漲", "高達", "氣勢如虹", "優異", "看好", "穩定", "信心"]


##################################################################資料排序#################################################################
def main():
    output = open('data_2317_train_sorting.txt', 'w', encoding='utf-8')
    with open('data_2317_train.csv', 'r', encoding='utf-8') as content:
        for texts_num, line in enumerate(content):
            if re.findall(date, line):
                tmp=[]
                reg = re.findall(date, line)
                tmp.append(reg)
                tmp.append(line)
                data.append(tmp)

        data.sort(key=itemgetter(0, 1))
        for i in range(0,len(data)):
            outputfile("data_2317_train_sorting.csv", data[i][1])

##################################################################  斷詞  #######################################################
def getToken():
    print("main : 斷詞")
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # jieba custom setting.
    jieba.set_dictionary('jieba_dict/dict.txt.big')

    # load stopwords set
    stopword_set = set()
    with open('jieba_dict/stopwords.txt', 'r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))

    output = open('data_2317_train_sorting_token.csv', 'w', encoding='utf-8')
    with open('data_2317_train_sorting.csv', 'r', encoding='utf-8') as content:
        for texts_num, line in enumerate(content):
            line = line.strip('\n')
            words = jieba.cut(line, cut_all=False)
            # 關鍵詞擷取 > 不是很關鍵
#            tags = jieba.analyse.extract_tags(line)
#            print ("关键词抽取:","/".join(tags))
            tmp = []
            for word in words:
                if word not in stopword_set:
                    if(word == " " or word == "  " or re.findall(date, word)):
                        continue
#                    tmp.append(word)
                    output.write(word+",")
#            text.append(tmp)
            output.write('\n')
            if (texts_num + 1) % 10000 == 0:
                logging.info("已完成前 %d 行的斷詞" % (texts_num + 1))
    output.close()

##################################################################  word2vec model  #################################################################
def trainingvec():
    print("trainingVec")
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.LineSentence("data_2317_train_sorting_token.txt")
    model = word2vec.Word2Vec(sentences, size=100, window=5, min_count=3, min_alpha=0.0025)
#    model = word2vec.Word2Vec(sentences,alpha=0.0025, window=5,size=250)
    # model = word2vec.Word2Vec(sentences,alpha=0.0025, window=5,size=250)

    # 保存模型，供日後使用
    model.save("data_2317.model")
    model.wv.save_word2vec_format('data_txt.txt', binary=False)
    model.wv.save_word2vec_format('data_w2v.w2v', binary=False)
    # 模型讀取方式
    # model = word2vec.Word2Vec.load("data_2317.model")


##################################################################  詞性標註  #################################################################
def tagging():
    jieba.load_userdict("userdict.txt")
    with open('data_2317_train_token.txt', 'r', encoding='utf-8') as content:
        for texts_num, line in enumerate(content):
            #            s=SnowNLP(line)
            #            tags = [x for x in s.tags]
            #            print("詞性標註 ",tags)
            line = line.strip('\n')
            print(line)
            # jieba詞性標註
            seg = pseg.cut(line)
            for word, flag in seg:
                print(' 詞性標註 %s %s' % (word, flag))
                outputfile("tagging.txt", (word, flag))


def dataHandler():
    f = open('data_2317_train.csv', 'r', encoding='utf-8')
    for row in csv.reader(f):
        data.append(row[3])
        train_and.append(row[7])
    f.close()

    f = open('data_2317_train_sorting_token.csv', 'r', encoding='utf-8')
    for row in csv.reader(f):
#        print(len(row))
        tmp = []
        for i in range(2, len(row)):
            tmp.append(row[i])
#            print(row[i])
        text.append(tmp)
    print(data[0])
    f.close()

##################################################################word2vec model#################################################################
def compare():

    counter = 0
    vec = []

    #text = [["曾芝", "華碩", "權證"], ["郁文", "鴻海", "日", "月光"], ["股票", "台股", "漲"], ["跌", "郭台銘", "文創", "產業","開發"]]
    model = word2vec.Word2Vec.load("data_2317.model")
    word_vectors = model.wv
#    print(model['華碩'])
#    print(model['華碩'][0])
    for index in range(0,len(text)-1):
        print(index)
        sum = [0 for x in range(100)]
        for i in range(0, len(text[index])):
            word = text[index][i]
            print(word)
            if word in word_vectors.vocab:
                print(word)
                counter+=1
                #train_vec.append(model[word])
                for j in range(0, (len(model[word])-1)):
                    sum[j] = sum[j]+model[word][j]
#                    print(sum)
                total = 0
        for j in range(0, (len(sum))-1):
            sum[j] = sum[j] / counter
            total += sum[j]
        vex = []
        vex.append(total)
        train_vec.append(vex)
##    print(model[u"權證"])
##    print(model[u"權證"][0])
#    y2 = model.most_similar(u"台股", topn=10)
#    print("台股")
#    for item in y2:
#        print(item[0], item[1])
#    y3 = model.most_similar(u"台積電", topn=10)
#    print("台積電")
#    for item in y3:
#        print(item[0], item[1])
#    y4 = model.most_similar(u"下跌".split())
#    print("漲")
#    for item in y4:
#        print(item[0], item[1])


################################################################## output #################################################################
def outputfile(name, line):
    print(line)
    with open(name, 'a', encoding='utf8') as the_file:
        the_file.write(str(line))


##################################################################  詞袋模型test  #################################################################
def bow():
#        print("row", row[i])
    texts = [[word for word in jieba.cut(document, cut_all=True)] for document in data]

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(t) for t in texts]
    print(corpus)
    # TF-IDF特徵值
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    #在TFIDF的基础上，进行相似性检索, 然后进行similarity检索。
    similarity = similarities.Similarity('Similarity-tfidf-index', corpus_tfidf, num_features=10000)

#    new_sensence = "昨日金融期則是下跌17.4點，指數為1,051點，跌幅1.63％。股價皆重挫3～4％，回到年線的位置。工商,2015/01/07 00:00:00,外資變臉 電子期重摔 昨日下跌8.7點，跌幅達2.35％，為各期指中最弱,1"
#   test_corpus_1 = dictionary.doc2bow(jieba.cut(new_sensence, cut_all=True))
#    vec_tfidf = tfidf[test_corpus_1]
#    print(vec_tfidf)
#    print(similarity[test_corpus_1])  # 返回最相似的样本材料,(index_of_document, similarity) tuples
    for item in corpus_tfidf:
        print(item)
    tfidf.save("data.tfidf")
    tfidf.save("data_tfidf.txt")
    tfidf.save("data_tfidf.csv")
    tfidf = models.TfidfModel.load("data.tfidf")
    print(tfidf)


# 進行Classification評估分數(accuracy)
# Classifier
def classfy():
    X = train_vec
#    X = train_vec
    Y = train_and
    A = train_vec
    B = train_and
#    A = test_vec
#    B = test_ans
    print(X)
    print(Y)
#    X = X.reshape(-1, 1)
    clf = LogisticRegression()
    clf.fit(X, Y)
    print(clf.score(A, B))


print("Hi")
#main()
#getToken()
#trainingvec()
dataHandler()
#compare()
bow()
#classfy()
print("done")
