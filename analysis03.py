# --coding:utf-8--
from urllib2 import urlopen
import operateDB
import re
from bs4 import BeautifulSoup
pages = set()
out_text = []
linkList = []

def data_spider(my_url):
    html = urlopen(my_url)
    bsObj = BeautifulSoup(html, "html.parser")
    '''标题'''
    topic = ""
    topic_text = bsObj.find("div", {"class": "article m-l mobile-m0"})
    if topic_text is not None:
        topic_text = topic_text.findAll("h1")
        for text in topic_text:
            topic = text.get_text()
    #print topic
    '''发送时间,发送人'''
    time = ""
    time_text = bsObj.find("div", {"class": "article-info"})
    if time_text is not None:
        time = time_text.find("span", {"class":"left time en"})
        time = time.get_text()
    content = ""
    textList = bsObj.find("div", {"class": "article-content"})
    if textList is not None:
        textList = textList.findAll("p")
        for text in textList:
            content += text.get_text()
    if topic != "" and content != "":
        try:
            operateDB.insert_table("textlibrary", topic, time, content)
        except Exception as e:
            print e
    coo = bsObj.findAll("div",{"class":"column"})
    coo = coo[1].find("div",{"class":"column-body"})
    coo = coo.find("div",{"class":"column-img-news"})
    for link in coo.findAll("a"):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage =link.attrs['href']
                print newPage
                out_text.append(newPage)
                pages.add(newPage)
                data_spider(newPage)



def output():
    return out_text
if __name__ == '__main__':
    url = "http://uy.ts.cn/system/2017/11/01/035027655.shtml"
    data_spider(url)




