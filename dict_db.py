import pymysql
import hashlib

def encrypt(pwd):
    salt = "*1^2&a$z"
    hash = hashlib.md5(salt.encode())
    hash.update(pwd.encode())
    return hash.hexdigest()


class User:
    def __init__(self, database):
        self.db = pymysql.connect(user='root', passwd='123456', database=database, charset='utf8')
        self.create_cursor()

    def create_cursor(self):
        self.cur = self.db.cursor()

    def regist(self,name, pwd):
        passwd = encrypt(pwd)
        sql = "select name from users where name = %s"
        self.cur.execute(sql, [name])
        if self.cur.fetchone():
            print("用户名已存在")
            return False

        try:
            sql = "insert into users (name, pwd) values (%s, %s)"
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    def login(self, name, pwd):
        passwd = encrypt(pwd)
        sql = "select * from users where name = %s and pwd = %s;"
        self.cur.execute(sql, [name, passwd])
        if self.cur.fetchone():
            return True
        return False

    def query(self, word):
        sql = "select mean from words where word = %s"
        self.cur.execute(sql, [word])
        return self.cur.fetchone()

    def insert_history(self, name, word):
        sql = "insert into history (name, word) values (%s, %s)"
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def history(self, name):
        sql = "select name, word, time from history where name = %s order by time desc limit 10"
        self.cur.execute(sql, [name])
        return self.cur.fetchall()



if __name__ == '__main__':
    print("请注册")
    user1 = User('dict')
    user1.insert_history('aaaa', 'white')
    # while True:
    #     name = input("请输入姓名:")
    #     if not name:
    #         break
    #     pwd = input("请输入密码:")
    #
    #     if user1.regist(name, pwd):
    #         print("注册成功")
    #         break
    #
    # print("请登录")
    # while True:
    #     name = input("请输入用户名:")
    #     pwd = input("请输入密码:")
    #     if user1.login(name, pwd):
    #         print("登录成功")
    #         break
    #     else:
    #         print("用户名或密码错误")



