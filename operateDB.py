# --coding:utf-8--
import MySQLdb


def connect():
    conn = MySQLdb.connect(host='192.168.1.113', port=3306, user='root', passwd='root', db='antext', charset="utf8")
    return conn


def insert_table(table_name, value_title, value_time, value_text):
    conn = connect()
    cur = conn.cursor()
    cur.execute("insert into "+table_name+" values('"+value_title+"','"+value_time+"','"+value_text+"')")
    conn.commit()
    conn.close()