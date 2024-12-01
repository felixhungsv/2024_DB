def is_valid_code(input_str):
    pattern = r"^[A-Za-z]\d{8}$"
    return bool(re.match(pattern, input_str))

def is_valid_password(password):
    pattern = r"^[A-Za-z0-9]{8,20}$"
    return bool(re.match(pattern, password))

def delete_terminal_content(lines):
    sys.stdout.write(Cursor.UP(lines)) 
    sys.stdout.write("\033[J")   
    sys.stdout.flush()

def sign_up():
    while True:
        UserID = input("請輸入台大證件號碼：")

        if is_valid_code(UserID):
            query_str = '''
            SELECT UserID
            FROM USER
            WHERE UserID=%s
            '''
            columns, data = query(query_str, (UserID,))
            if data:
                print("此帳號已註冊！\n")
                print("前往登入頁面？\n")
            else:
                UserName = input("請輸入姓名：")
                Email = input("請輸入電子郵件：")
                PhoneNumber = input("請輸入電話號碼：")
                Password1 = input("請設定密碼（8-20碼，僅由英文字母與數字組成）：")
                while is_valid_password(Password1) == 0:
                    print("格式錯誤！\n")
                    time.sleep(2)
                    delete_terminal_content(2)
                    Password1 = input("請設定密碼（8-20碼，僅由英文字母與數字組成）：")
                Password2 = input("請再次輸入密碼：")
                while Password1 != Password2:
                    print("前後密碼不一致！\n")
                    time.sleep(2)
                    delete_terminal_content(2)
                    Password2 = input("請重新輸入：")
                query_str = '''
                INSERT INTO USER (UserID, UserName, Email, PhoneNumber) 
                VALUES (%s, %s, %s, %s)
                INSERT INTO MEMBER (MemberID, AccountName, Password) 
                VALUES (%s, %s, %s)
                '''
                columns, data = query(query_str, (UserID, UserName, Email, PhoneNumber, UserID, UserName, Password1))
                print("註冊成功！\n")
                break
        else:
            print("格式錯誤！\n")
        time.sleep(2)
        delete_terminal_content(2)