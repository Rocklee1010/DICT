def login():
    while True:
        print("+----------------+")
        print("|      查单词     |")
        print("|      查历史     |")
        print("|      注销       |")
        print("+----------------+")
        choice = input("请选择:")
        if choice == '查单词':
            pass
        elif choice == '查历史':
            pass
        elif choice == '注销':
            break


while True:
    print("+----------------+")
    print("|      注册      |")
    print("|      登录      |")
    print("|      退出      |")
    print("+----------------+")
    choice = input("请选择:")
    if choice == '注册':
        pass
    elif choice == '登录':
        login()
    elif choice == '退出':
        break
    
    
    
    