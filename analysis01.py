# --coding:utf-8--
from urllib2 import urlopen
import operateDB
import re
from bs4 import BeautifulSoup
pages = set()
out_text = []
linkList = [] #未使用的节点
linkedList=[] #已使用的节点
def init_list():
    html = urlopen("http://uyghur.news.cn/")
    bsObj = BeautifulSoup(html, "html.parser")
    bs = bsObj.findAll("div", {"class": "title"})
    for bst in bs:
        bst = bst.findAll("h2")
        for link in bst[0].findAll("a"):
            if 'href' in link.attrs:
                newPage = "http://uyghur.news.cn" + link.attrs['href']
                linkList.append(newPage)
    linkList.pop()
    linkList.pop()

def data_spider(my_url):
    try:
        html = urlopen(my_url)
        bsObj = BeautifulSoup(html, "html.parser")
        '''标题'''
        topic = ""
        topic_text = bsObj.find("div", {"class": "tit"})
        if topic_text is not None:
            topic_text = topic_text.findAll("h1")
            for text in topic_text:
                topic = text.get_text()
        #print topic
        time = ""
        time_text = bsObj.find("div", {"class": "gn"})
        if time_text is not None:
            time_text = time_text.findAll('div')
            time = time_text[3].get_text()
            time_str = time.split(" ")
            time_str=time_str[2]
            #print time_str
            '''文章内容'''
            content = ""
            textList = bsObj.findAll("div", {"class": "content1"})
            for text in textList:
                content += text.get_text()
        #print content
        if topic != "" and content != "":
            try:
                operateDB.insert_table("textlibrary", topic, time, content)
            except Exception as e:
                print e
        '''/news/rmt.htm自媒体不符合'''
        for url in linkList:
            if url not in linkedList:
                linkedList.append(url) #添加到已使用的节点
                html=urlopen(url)
                bsObj = BeautifulSoup(html, "html.parser")
                bs=bsObj.find("div",{"class":"body"})
                for link in bs.findAll("a",href=re.compile("^(http://uyghur.news.cn/20)")):
                    if 'href' in link.attrs:
                        if link.attrs['href'] not in pages:
                            newPage =link.attrs['href']
                            print newPage
                            out_text.append(newPage)
                            pages.add(link.attrs['href'])
                            data_spider(newPage)
    except Exception as e:
        return



def output():
    return out_text
if __name__ == '__main__':
    url = "http://uyghur.news.cn/2017-11/03/c_136723297.htm"
    init_list()
    data_spider(url)
    print linkList
        
        