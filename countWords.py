# --coding:utf-8--
import MySQLdb
import operateDB
data_dict = {}


def select_data():
    conn = operateDB.connect()
    cursor = conn.cursor()
    sql = "select * from textlibrary"
    text_str = ""
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for text in results:
            text_str = text[0]+" "+text[2]
            text_str = text_str.split(" ")
            for str1 in text_str:
                if str1 not in data_dict:
                    data_dict[str1] = 1
                else:
                    data_dict[str1] += 1
    except Exception as e:
        print e


def get_dict():
    list = sorted(data_dict.items(), key=lambda d: d[1])
    return list

'''
for key, value in data_dict.items():
    print value, ":", key
'''
if __name__ == '__main__':
    select_data()
    get_dict()