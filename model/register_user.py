import pymysql

class RegisterUser(object):
    def __init__(self,name,passwd,phone,email,db):
        self.name = name
        self.passwd = passwd
        self.phone = phone
        self.email =email
        self.db = db
    def register(self):
        #查询用户表
        cursor = self.db.cursor()
        try:
            cursor.execute("select * from user1 where username='%s'" % self.name)
            r = cursor.fetchone()
            print(r)
            if r == None:
                try:
                    cursor.execute("insert into user1(username,passwd,phone,email)values('%s','%s','%s','%s')"%(self.name,self.passwd,self.phone,self.email))
                    self.db.commit()
                    cursor.close()
                except:
                    self.db.rollback()
                    cursor.close()
                    return "None"
                else:
                    return "OK"
            else:
                cursor.close()
                return "EXIST"
        except TypeError:
            pass
        except Exception:
            pass

