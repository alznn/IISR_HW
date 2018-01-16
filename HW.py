import requests
import re
import lxml
from bs4 import BeautifulSoup

goodart = []
badart = []
urlList = []

def getGoodContent(tittle,link):
    i=0
    user = []
    context = []
    news_url = "https://www.ptt.cc/"+link
    res = requests.get(news_url)
    soup = BeautifulSoup(res.text.encode('utf-8'),'lxml')
    for userID in soup.findAll("span",{'class':'push-userid'}):
        user.append(userID.contents[0])
    for Content in soup.findAll("span",{'class':'push-content'}):
        context.append(Content.contents[0])
        
    print("length are ")
    print(len(context))
    print(len(user))
    for i in range(1,len(context)):
        if user[i-1] == user[i]:
            context[i] = context[i-1]+ context[i]
        else :
            goodart.append(context[i-1])
    if(len(context) > 1):
        goodart.append(context[len(context)-1])

def getBadContent(tittle,link):
    i=0
    user = []
    context = []
    news_url = "https://www.ptt.cc/"+link
    res = requests.get(news_url)
    soup = BeautifulSoup(res.text.encode('utf-8'),'lxml')
    for userID in soup.findAll("span",{'class':'push-userid'}):
        user.append(userID.contents[0])
    for Content in soup.findAll("span",{'class':'push-content'}):
        context.append(Content.contents[0])
        
    print("length are ")
    print(len(context))
    print(len(user))
    for i in range(1,len(context)):
        if user[i-1] == user[i]:
            context[i] = context[i-1]+ context[i]
        else :
            badart.append(context[i-1])
    if(len(context) > 1):
        badart.append(context[len(context)-1])
# main 
for i in range(6000, 6201):
    print (i)
    news_url = "https://www.ptt.cc/bbs/movie/index"+str(i)+".html"
    urlList.append(news_url)
    res = requests.get(news_url)
    soup = BeautifulSoup(res.text.encode('utf-8'),'lxml')
    #print (soup)

    articles = soup.find_all('div', 'r-ent')
    for article in articles:
        meta = article.find('div', 'title').find('a')
        title = meta.getText().strip()
        link = meta.get('href')
        #print(title,link)
        gname = re.search("好雷",title,re.M|re.I)
        bname = re.search("負雷",title,re.M|re.I)
        if gname:
            print(title)
            getGoodContent(title,link)
        elif bname:
            print(title)
            getBadContent(title,link)
f = open(r'C:\Users\hp\Desktop\HW.txt', 'w', encoding = 'UTF-8')    # 也可使用指定路徑等方式，如： C:\A.txt
f.write('好雷\n')
for ip in goodart:  
    f.write(ip)  
    f.write('  1  \n') 
f.write('負雷\n')
for ip in badart:  
    f.write(ip)  
    f.write('  0  \n') 
f.close()
