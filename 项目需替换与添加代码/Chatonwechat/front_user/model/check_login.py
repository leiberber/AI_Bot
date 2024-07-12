from templates.config import conn

cur = conn.cursor()


def is_null(username, password):
    if (username == '' or password == ''):
        return True
    else:
        return False


def is_existed(username, password):
    sql = "SELECT * FROM managers WHERE managername ='%s' and password ='%s'" % (username, password)
    cur.execute(sql)
    result = cur.fetchall()
    if (len(result) == 0):
        return False
    else:
        return True


def is_existed_user(username, password):
    sql = "SELECT * FROM users WHERE username ='%s' and password ='%s'" % (username, password)
    cur.execute(sql)
    result = cur.fetchall()
    if (len(result) == 0):
        return False
    else:
        return True


def exist_user(username):
    sql = "SELECT * FROM managers WHERE managername ='%s'" % (username)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    if (len(result) == 0):
        return False
    else:
        return True


def exist_user_user(username):
    sql = "SELECT * FROM users WHERE username ='%s'" % (username)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    if (len(result) == 0):
        return False
    else:
        return True


def get_permission(username):
    sql = "SELECT Permissions FROM users WHERE username ='%s'" % (username)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchone()
    return result[0]


# print(get_permission('喻瑞'))