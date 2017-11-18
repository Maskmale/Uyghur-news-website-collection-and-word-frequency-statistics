# --coding:utf-8--
from urllib2 import urlopen
import operateDB
import re
from bs4 import BeautifulSoup
pages = set()
out_text = []


def data_spider(my_url):
    if len(pages) >= 200:
        return
    html = urlopen(my_url)
    bsObj = BeautifulSoup(html, "html.parser")
    '''标题'''
    topic = ""
    topic_text = bsObj.find("div", {"class": "show_tima"})
    if topic_text is not None:
        topic_text = topic_text.findAll("h2")
        for text in topic_text:
            topic = text.get_text()
    '''发送时间,发送人'''
    time = ""
    time_text = bsObj.find("div", {"class": "show_info"})
    if time_text is not None:
        time_text = time_text.findAll('div')
        time = time_text[1].get_text()
        time_str = time.split(":")
        str1=time_str[2].split(" ")
        clock=str1[0] + time_str[1]
        time_str =str1[1]
        clock=clock.split(" ")
        clock.reverse()
        clock = ":".join(clock)

        time = []
        for text in time_str.split("-"):
            time.append(text)
        time.reverse()
        time = "-".join(time)
        time = time+" "+clock
    '''文章内容'''
    content = ""
    textList = bsObj.findAll("div", {"class": "show_gpic_text"})
    for text in textList:
        content += text.get_text()
    if topic != "" and content != "":
        try:
            operateDB.insert_table("textlibrary", topic, time, content)
        except Exception as e:
            print e
    pages.add("/news/2017/01/03/59691.shtml")
    pages.add("/news/2017/01/11/60370.shtml")
    pages.add("/news/2017/01/18/60844.shtml")
    pages.add("/news/2017/02/07/61835.shtml")
    for link in bsObj.findAll("a", href=re.compile("^(/news/2017)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = "http://www.hawar.cn"+link.attrs['href']
                out_text.append(newPage)
                pages.add(link.attrs['href'])
                data_spider(newPage)


def output():
        return out_text
if __name__ == '__main__':
    url = "http://www.hawar.cn/news/2017/10/24/71269.shtml"
    data_spider(url)
