from socket import *
import sys

ADDR = ('127.0.0.1', 8888)


def do_query(s, name):
    while True:
        word = input("单词:")
        if word == '##':
            return
        else:
            msg = 'Q '+name+' '+word
            s.send(msg.encode())
            data = s.recv(1024).decode()
            print(data)


def do_history(s, name):
    msg = 'H '+name
    s.send(msg.encode())
    while True:
        data = s.recv(1024).decode()
        if data == '##':
            break
        print(data)


def skip(s, name):
    while True:
        print("+------------------+")
        print("|      1.查单词     |")
        print("|      2.查历史     |")
        print("|      3.注销       |")
        print("+------------------+")
        choice = input("请选择:")
        if choice == '1':
            do_query(s, name)
        elif choice == '2':
            do_history(s, name)
        elif choice == '3':
            return
        else:
            print("请输入正确的命令")


def regist(s):
    while True:
        name = input("请输入用户名:")
        pwd = input("请输入密码:")
        confirm_pwd = input("请再次输入密码:")
        if ' ' in name or ' ' in pwd:
            print("用户名和密码不能有空格")
            continue
        if pwd != confirm_pwd:
            print("两次密码不一致")
            continue
        data = 'R '+name+' '+pwd
        s.send(data.encode())
        msg = s.recv(1024).decode()
        print(msg)
        if msg == 'OK':
            print("恭喜,注册成功")
            return
        else:
            print("用户名已存在")

def login(s):
    while True:
        name = input("请输入用户名:")
        pwd = input("请输入密码:")
        data = 'L '+name+' '+pwd
        s.send(data.encode())
        msg = s.recv(1024).decode()
        if msg == 'OK':
            print("登录成功")
            skip(s, name)
            return
        else:
            print("用户名或密码错误")


def do_quit(s):
    s.send(b'E')
    sys.exit(2)


def main():
    s = socket()
    s.connect(ADDR)

    while True:
        print("+----------------+")
        print("|     1.注册      |")
        print("|     2.登录      |")
        print("|     3.退出      |")
        print("+----------------+")
        choice = input("请选择:")
        if choice == '1':
            regist(s)
        elif choice == '2':
            login(s)
        elif choice == '3':
            do_quit(s)

if __name__ == '__main__':
    main()








