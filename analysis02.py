# --coding:utf-8--
from urllib2 import urlopen
import operateDB
import re
from bs4 import BeautifulSoup
pages = set()
out_text = []
linkList = []
linkedList=[]


def init_list():
    html = urlopen("http://uyghur.people.com.cn")
    bsObj = BeautifulSoup(html, "html.parser")
    my_uls = bsObj.findAll("li")
    for my_ul in my_uls:
        my_ul_list= my_ul.findAll("a", href=re.compile("^(/1([0-9]+)/index)"))
        for ul in my_ul_list:
            if 'href' in ul.attrs:
                newPage = "http://uyghur.people.com.cn" + ul.attrs['href']
                linkList.append(newPage)


def data_spider(my_url):
    html = urlopen(my_url)
    bsObj = BeautifulSoup(html, "html.parser")
    '''标题'''
    topic = ""
    topic_text = bsObj.find("div", {"class": "text text_new width978 clearfix"})
    if topic_text is not None:
        topic_text = topic_text.findAll("h1")
        for text in topic_text:
            topic = text.get_text()
    elif bsObj.find("div",{"class":"ej_right"}) is not None:
        topic_text=bsObj.find("div",{"class":"ej_right"})
        topic_text=topic_text.findAll("h1")
        for text in topic_text:
            topic=text.get_text()
            topic=topic.encode('utf-8')
            #print ""
            #print topic
    '''时间'''
    time = ""
    time_text = bsObj.find("div", {"class": "text text_new width978 clearfix"})
    if time_text is not None:
        time_text = time_text.findAll("h2")
        for text in time_text:
            time=text.get_text()
    elif bsObj.find("div",{"class":"ej_right"}) is not None:
        time_text = bsObj.find("div",{"class":"ej_right"})
        time_text=time_text.find("p").findAll("strong")
        time=time_text[0].get_text()
    time_text = time.split(" ")
    time=time_text[0]
    #print time
    content = ""
    textList = bsObj.find("div", {"class": "text text_new width978 clearfix"})
    if textList is not None:
        textList=textList.findAll("p")
        for text in textList:
            content += text.get_text()
    elif bsObj.find("div",{"class":"ej_right"}):
        textList = bsObj.find("div",{"class":"ej_right"})
        textList = textList.find("span")
        reg=re.compile("<[^>]*>")
        textList=reg.sub('',textList.prettify())
        textList=textList.split("\n")
        for text in textList:
            content+=text
    if topic != "" and content != "":
        try:
            operateDB.insert_table("textlibrary", topic, time, content)
        except Exception as e:
            print e
    #print content
    for url in linkList:
        if url not in linkedList:
            linkedList.append(url)  # 添加到已使用的节点
            html = urlopen(url)
            bsObj = BeautifulSoup(html, "html.parser")
            myLink_list = bsObj.findAll("div", {"class":"ztone_6"})
            for myLi in myLink_list:
                for link in myLi.findAll("a", href=re.compile("^(/1)")):
                    if 'href' in link.attrs:
                        if link.attrs['href'] not in pages:
                            newPage = "http://uyghur.people.com.cn" + link.attrs['href']
                            out_text.append(newPage)
                            print newPage
                            pages.add(link.attrs['href'])
                            data_spider(newPage)

def output():
    return out_text
if __name__ == '__main__':
    init_list()
    data_spider("http://uyghur.people.com.cn/155988/15688304.html")
    print linkList
