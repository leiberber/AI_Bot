import pymysql

conn = pymysql.connect(
    user="root",
    password="123456",
    host="127.0.0.1",
    port=3306,
    db="smartqa",
    charset="utf8"
)


