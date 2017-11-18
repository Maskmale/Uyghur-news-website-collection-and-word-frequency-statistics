# --coding:utf-8--
from Tkinter import *
import analysis00
import countWords


def gui():
    win = Tk()
    # 添加标题
    win.title("维吾尔语网站采集与分析系统")
    # 窗口大小
    win.geometry("800x600")
    # 长宽不可变
    win.resizable(width=False, height=False)
    title = Label(win, text="维吾尔语网站采集与分析系统", font=("Arial", 12), width=50, height=2).pack()
    # 创建布局
    frm = Frame(win)
    # Left布局
    frm_L = Frame(frm)
    # frm_L1
    frm_L1 = Frame(frm_L)
    Label(frm_L1, text='URL:', font=('Arial', 10)).pack(side=LEFT)
    url_text = StringVar()
    url_entry = Entry(frm_L1, textvariable=url_text, width=40)
    url_text.set("http://www.hawar.cn/news/2017/10/24/71269.shtml")
    url_entry.pack(side=RIGHT)
    frm_L1.pack(side=LEFT)
    frm_L2 = Frame(frm_L)
    data_view = Text(win, width=100, height=20)

    def url_listener():
        url = url_text.get()
        analysis00.data_spider(url)
        out = analysis00.output()
        for o in out:
            data_view.insert('1.0', o+"\n")
    Button(frm_L2, text="网址采集", command=url_listener).pack(side=RIGHT)
    frm_L2.pack(side=LEFT)
    frm_L.pack()
    #
    frm_R = Frame(frm_L)
    ana_view = Text(win, width=100, height=20)
    ana_view.pack(side=BOTTOM)

    def ana_listener():
        countWords.select_data()
        list = countWords.get_dict()
        for i in list:
            print i
            ana_view.insert('1.0', i)
            ana_view.insert('1.0', '\n')
        '''
        for key, value in my_dict.items():
            temp = key+':'+bytes(value)+'\n'
            ana_view.insert('1.0', temp)
        '''

    Button(win, text="数据分析", command=ana_listener).pack(side=BOTTOM)
    frm.pack()
    data_view.pack()
    frm_R.pack()
    win.mainloop()
if __name__ == '__main__':
    gui()