from templates.config import conn

cur = conn.cursor()


def add_user(username, password):
    # sql commands
    sql = "INSERT INTO managers(managername, password) VALUES ('%s','%s')" %(username, password)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()


def add_user_user(username, password):
    # sql commands
    sql = "INSERT INTO users(username, password) VALUES ('%s','%s')" %(username, password)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()


