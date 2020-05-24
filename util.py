import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()
try:
    c.execute("DROP TABLE user")
except:
    pass
try:
    c.execute("DROP TABLE session")
except:
    pass
c.execute('''CREATE TABLE user (id integer primary key, username text, password text)''')
c.execute('''CREATE TABLE session (id integer primary key, sid text)''')
c.execute("INSERT INTO user(username, password) VALUES ('admin','57yczPEJH)~!')")
c.execute("INSERT INTO user(username, password) VALUES ('Alice','Pcsv5JE-McNb')")
c.execute("INSERT INTO user(username, password) VALUES ('Bob','123456')")
c.execute("INSERT INTO user(username, password) VALUES ('Charlie','password')")
conn.commit()
conn.close()

def valid_login(username, password):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    sql = "SELECT id FROM user WHERE username='" + username + "' AND password='" + password + "'"
    print(sql)
    c.execute(sql)
    result = c.fetchone()
    conn.close()

    if result is None:
        return None
    
    return result[0]

def contain_user(username):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    t = (username,)
    sql = "SELECT id FROM user WHERE username=?"
    c.execute(sql, t)
    result = c.fetchone()
    conn.close()

    return result is not None

def regist_user(username, password):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    t = (username, password)
    c.execute("INSERT INTO user(username, password) VALUES (?,?)", t)
    conn.commit()
    conn.close

def get_username(id):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    t = (id,)
    c.execute("SELECT username FROM user WHERE id = ?", t)
    result = c.fetchone()
    conn.close

    return result[0]

def get_users():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    rows = c.execute("SELECT username FROM user WHERE id > 1")
    conn.close

    users = []
    for row in rows:
        users.append(row[0])

    return users

def save_sid(id, sid):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    t = (id, sid)
    sql = "INSERT OR REPLACE INTO session (id, sid) VALUES (?, ?)"
    c.execute(sql, t)
    conn.commit()
    conn.close

def get_sid(id):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    t = (id,)
    c.execute("SELECT sid FROM session WHERE id = ?", t)
    result = c.fetchone()
    conn.close
    if result is None:
        return None

    return result[0]
