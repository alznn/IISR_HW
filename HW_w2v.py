import logging

import jieba
jieba.load_userdict("userdict.txt")
import jieba.posseg as pseg
import jieba.analyse  

from gensim.models import word2vec
import numpy 
import csv

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB

#先將新聞資料進行斷詞
def main():
    print("main : 斷詞")
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # jieba custom setting.
    jieba.set_dictionary('jieba_dict/dict.txt.big')

    # load stopwords set
    stopword_set = set()
    with open('jieba_dict/stopwords.txt','r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))

    output = open('data_2317_train_token.txt', 'w', encoding='utf-8')
    with open('data_2317_train.csv', 'r', encoding='utf-8') as content :
        for texts_num, line in enumerate(content):
            line = line.strip('\n')
            words = jieba.cut(line, cut_all=False)
            #關鍵詞擷取 > 不是很關鍵
            #tags = jieba.analyse.extract_tags(line)
            #print ("关键词抽取:","/".join(tags))
            
            for word in words:
                if word not in stopword_set:
                    output.write(word + ' ')
            output.write('\n')
            
            #詞性標註
            seg = pseg.cut(line)
            for word, flag in seg:
                print(' 詞性標註 %s %s' % (word, flag))

            if (texts_num + 1) % 10000 == 0:
                logging.info("已完成前 %d 行的斷詞" % (texts_num + 1))
    output.close()
    
def outputFile(line):
    print(line)
    with open('關鍵字抽取.txt', 'a',encoding='utf8') as the_file:
        the_file.write(line)
        the_file.write('\n')

#執行word2vec訓練出一個model
def trainingVec():
    print("trainingVec")
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.LineSentence("data_2317_train_token.txt")
    model = word2vec.Word2Vec(sentences,size=100, window=5, min_count=3, min_alpha=0.0025)
    #model = word2vec.Word2Vec(sentences,alpha=0.0025, window=5,size=250)

    #保存模型，供日後使用
    model.save("data_2317.model")
    model.wv.save_word2vec_format('data_txt.txt', binary=False)
    model.wv.save_word2vec_format('data_w2v.w2v', binary=False)
    #模型讀取方式
    # model = word2vec.Word2Vec.load("your_model_name")



    #加入其它feature(Ex: bag of words)
def demo():
    print("demo")
    model = word2vec.Word2Vec.load("data_2317.model")

    y2 =model.most_similar(u"台股",topn = 10)
    print("台股")
    for item in y2:
        print(item[0],item[1])
    y3 =model.most_similar(u"台積電",topn = 10)
    print("台積電")
    for item in y2:
        print(item[0],item[1])
    y4 =model.doesnt_match(u"漲 跌".split())
    print("doesnt_match")
    for item in y2:
        print(item[0],item[1])
    print(model[u"台積電"])
    
#進行Classification評估分數(accuracy)
    #Classifier
#    X = train_vec
#    Y = train_and
#    A = test_vec
#    B = test_ans
#    clf = LogisticRegression()
#    clf.fit(X,Y)
#    clf.score(A,B)
if __name__ == "__main__":
    print("Hi")
    main()
  #  trainingVec()
    print("done")
  #  demo()
