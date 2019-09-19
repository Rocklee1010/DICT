from socket import *
from multiprocessing import Process
import sys, signal
from time import sleep

from dict_db import User


HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)
db = User('dict')

signal.signal(signal.SIGCHLD, signal.SIG_IGN)


def do_regist(connfd, name, pwd):
    # print(name)
    # print(pwd)

    if db.regist(name, pwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'Fail')


def do_login(connfd, name, pwd):

    if db.login(name, pwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'Fail')


def do_query(connfd, name, word):
    mean = db.query(word)
    if mean:
        db.insert_history(name, word)
        msg = "%s : %s" % (word, mean[0])
        connfd.send(msg.encode())
    else:
        connfd.send("单词不存在".encode())


def do_history(connfd, name):
    result = db.history(name)
    for i in result:
        data = '%s  %-16s  %s' % i
        connfd.send(data.encode())
        sleep(0.1)
    connfd.send(b'##')

def request(connfd):
    db.create_cursor()
    while True:
        data = connfd.recv(1024).decode()
        # print(data)
        temp = data.split(' ')
        # print(temp)
        if not data or temp[0] == 'E':
            sys.exit(1)
        elif temp[0] == 'R':
            do_regist(connfd, temp[1], temp[2])
        elif temp[0] == 'L':
            do_login(connfd, temp[1], temp[2])
        elif temp[0] == 'Q':
            do_query(connfd, temp[1], temp[2])
        elif temp[0] == 'H':
            do_history(connfd, temp[1])

def main():

    s = socket()
    s.bind(ADDR)
    s.listen(5)

    print("Listen the port", PORT)
    while True:
        try:
            c, addr = s.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception:
            continue

        # 创建子进程
        p = Process(target=request, args=(c,))
        p.daemon=True
        p.start()




if __name__ == '__main__':
    main()

