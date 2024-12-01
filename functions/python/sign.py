def is_valid_code(input_str):
    pattern = r"^[A-Za-z]\d{8}$"
    return bool(re.match(pattern, input_str))

def is_valid_password(password):
    pattern = r"^[A-Za-z0-9]{8,20}$"
    return bool(re.match(pattern, password))

def is_valid_phonenumber(phonenumber):
    pattern = r"^[0-9]{10}$"
    return bool(re.match(pattern, phonenumber))

def delete_terminal_content(lines):
    time.sleep(2)
    sys.stdout.write(Cursor.UP(lines)) 
    sys.stdout.write("\033[J")   
    sys.stdout.flush()

def handle_user_id_input():
    while True:
        user_id = input("請輸入台大證件號碼：")
        if is_valid_code(user_id):
            return user_id
        else:
            print("格式錯誤！\n")
            delete_terminal_content(2)

def prompt_password_confirmation():
    while True:
        password = input("請設定密碼（8-20碼，僅由英文字母與數字組成）：")
        while is_valid_password(password) == 0:
            print("格式錯誤！\n")
            delete_terminal_content(2)
            password = input("請設定密碼（8-20碼，僅由英文字母與數字組成）：")
        password2 = input("請再次輸入密碼：")
        while password != password2:
            print("前後密碼不一致！\n")
            delete_terminal_content(2)
            password2 = input("請重新輸入：")
        return password

def check_user_existence(UserID):
    query_str = '''
    SELECT UserID
    FROM USER
    WHERE UserID=%s
    '''
    columns, data = query(query_str, (UserID,))
    return bool(data)

def check_phonenumber_existence(phonenumber):
    query_str = '''
    SELECT UserID
    FROM USER
    WHERE PhoneNumber=%s
    '''
    columns, data = query(query_str, (phonenumber,))
    return bool(data)

def prompt_phonenumber():
    while True:
        PhoneNumber = input("請輸入電話號碼：")
        if is_valid_phonenumber(PhoneNumber) == 0:
            print("格式錯誤！\n")
            delete_terminal_content(2)
        elif check_phonenumber_existence(PhoneNumber) == 0:
            print("此電話號碼已註冊！\n")
            delete_terminal_content(2)
        else:
            return PhoneNumber

def sign_up():
    UserID = handle_user_id_input()
    if is_valid_code(UserID):
        check = check_user_existence(UserID)
        if check:
            print("此帳號已註冊！\n")
            print("前往登入頁面？\n")
        else:
            UserName = input("請輸入姓名：")
            Email = input("請輸入電子郵件：")
            PhoneNumber = prompt_phonenumber()
            Password = prompt_password_confirmation()
            # 需確認能不能一次兩個query
            query_str = '''
            INSERT INTO USER (UserID, UserName, Email, PhoneNumber) 
            VALUES (%s, %s, %s, %s)
            INSERT INTO MEMBER (MemberID, AccountName, Password) 
            VALUES (%s, %s, %s)
            '''
            query(query_str, (UserID, UserName, Email, PhoneNumber, UserID, UserName, Password))
            print("註冊成功！\n")

def sign_in():
    UserID = handle_user_id_input()
    if is_valid_code(UserID):
        check = check_user_existence(UserID)
        if check:
            while True:
                Password = input("請輸入密碼：")
                if is_valid_password(Password) == 0:
                    print("格式錯誤！\n")
                    delete_terminal_content(2)
                    continue
                query_str = '''
                SELECT MemberID AccountName
                FROM MEMBER
                WHERE MemberID=%s and Password=%s
                '''
                columns, data = query(query_str, (UserID, Password))
                if not data:
                    print("密碼錯誤！\n")
                    delete_terminal_content(2)
                    continue
                break
            account_name_index = columns.index('AccountName')
            account_name = data[0][account_name_index]
            print(f"歡迎！{account_name}！\n")
        else:
            print("查無此帳號！\n")
            delete_terminal_content(2)

def change_password():
    UserID = handle_user_id_input()
    if is_valid_code(UserID):
        check = check_user_existence(UserID)
        if check:
            while True:
                Password = input("請輸入原密碼：")
                if is_valid_password(Password) == 0:
                    print("格式錯誤！\n")
                    delete_terminal_content(2)
                    continue
                query_str = '''
                SELECT MemberID AccountName
                FROM MEMBER
                WHERE MemberID=%s and Password=%s
                '''
                columns, data = query(query_str, (UserID, Password))
                if not data:
                    print("密碼錯誤！\n")
                    delete_terminal_content(2)
                    continue
                break
            Password = prompt_password_confirmation()
            query_str = '''
            UPDATE MEMBER
            SET Password=%s
            WHERE MemberID=%s;
            '''
            query(query_str, (Password, UserID))
            print("更改密碼成功！\n")
        else:
            print("查無此帳號！\n")
            delete_terminal_content(2)

def anonymous_sign_in():
    PhoneNumber = prompt_phonenumber()