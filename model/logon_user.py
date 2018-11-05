import pymysql
#创建数据库链接
db = pymysql.connect\
('localhost','root','root','user')
class LogonUser(object):
    def __init__(self, username, userpass, db):
        self.username = username
        self.userpass = userpass
        self.db = db
    def logon(self):
        #查询用户表
        cursor = self.db.cursor()
        try:
            cursor.execute("select * from user1 where username='%s'" % self.username)
            r = cursor.fetchone()
            print(r)
            if r != None:
                if r[1] == self.username and r[2] == self.userpass:
                    cursor.close()
                    return "OK"
                else:
                    cursor.close()
                    return "Error"
            else:
                cursor.close()
                return "None"       
        except TypeError:
            pass
        except Exception:
            pass
