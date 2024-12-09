import utils

def is_valid_code(input_str):
    pattern = r"^[A-Za-z]\d{8}$"
    return bool(utils.re.match(pattern, input_str))

def is_valid_password(password):
    pattern = r"^[A-Za-z0-9]{8,20}$"
    return bool(utils.re.match(pattern, password))

def is_valid_phonenumber(phonenumber):
    pattern = r"^[0-9]{10}$"
    return bool(utils.re.match(pattern, phonenumber))

def handle_user_id_input():
    while True:
        user_id = input("請輸入台大證件號碼：")
        if is_valid_code(user_id):
            return 'U' + user_id.upper()
        elif user_id[:2].upper() == 'MG':
            return user_id.upper()
        else:
            print("格式錯誤！")
            utils.delete_terminal_content(1.5, 2)

def prompt_password_confirmation():
    while True:
        password = input("請設定密碼（8-20碼，僅由英文字母與數字組成）：")
        while is_valid_password(password) == 0:
            print("格式錯誤！")
            utils.delete_terminal_content(1.5, 2)
            password = input("請設定密碼（8-20碼，僅由英文字母與數字組成）：")
        password2 = input("請再次輸入密碼：")
        while password != password2:
            print("前後密碼不一致！")
            utils.delete_terminal_content(1.5, 2)
            password2 = input("請重新輸入：")
        return password

def check_user_existence(UserID):
    query_str = '''
    SELECT UserID
    FROM users
    WHERE UserID=%s
    '''
    columns, data = utils.query(query_str, (UserID,))
    return bool(data)

def check_phonenumber_existence(phonenumber):
    query_str = '''
    SELECT UserID
    FROM users
    WHERE PhoneNumber=%s
    '''
    columns, data = utils.query(query_str, (phonenumber,))
    return data

def prompt_phonenumber():
    while True:
        PhoneNumber = input("請輸入電話號碼：")
        if is_valid_phonenumber(PhoneNumber) == 0:
            print("格式錯誤！")
            utils.delete_terminal_content(1.5, 2)
        elif bool(check_phonenumber_existence(PhoneNumber)):
            print("此電話號碼已註冊！")
            utils.delete_terminal_content(1.5, 2)
        else:
            return PhoneNumber

def sign_up():
    utils.print_bold("註冊")
    UserID = "U" + handle_user_id_input()
    check = check_user_existence(UserID)
    if check:
        print("此帳號已註冊！")
        print("前往登入頁面？")
    else:
        UserName = input("請輸入姓名：")
        Email = input("請輸入電子郵件：")
        PhoneNumber = prompt_phonenumber()
        Password = prompt_password_confirmation()
        query_str = '''
        BEGIN;
        INSERT INTO users (UserID, UserName, Email, PhoneNumber) 
        VALUES (%s, %s, %s, %s);
        '''
        utils.query(query_str, (UserID, UserName, Email, PhoneNumber))
        query_str = '''
        INSERT INTO members (MemberID, AccountName, Password) 
        VALUES (%s, %s, %s);
        COMMIT;
        '''
        utils.query(query_str, (UserID, UserName, Password))
        print("註冊成功！")

def sign_in():
    while True:
        utils.print_bold("登入")
        UserID = handle_user_id_input()
        check = check_user_existence(UserID)
        if check:
            while True:
                Password = input("請輸入密碼：")
                if is_valid_password(Password) == 0:
                    print("格式錯誤！")
                    utils.delete_terminal_content(1.5, 2)
                    continue
                query_str = '''
                SELECT MemberID, AccountName
                FROM members
                WHERE MemberID=%s and Password=%s
                '''
                columns, data = utils.query(query_str, (UserID, Password))
                if not data:
                    print("密碼錯誤！")
                    utils.delete_terminal_content(1.5, 2)
                    continue
                break
            print(columns,data)
            account_name_index = columns.index('accountname')
            account_name = data[0][account_name_index]
            print(f"歡迎！{account_name}！")
            return UserID, account_name
        else:
            print("查無此帳號！")
            utils.delete_terminal_content(1.5, 3)

def change_password():
    utils.print_bold("更改密碼")
    UserID = "U" + handle_user_id_input()
    check = check_user_existence(UserID)
    if check:
        while True:
            Password = input("請輸入原密碼：")
            if is_valid_password(Password) == 0:
                print("格式錯誤！")
                utils.delete_terminal_content(1.5, 2)
                continue
            query_str = '''
            SELECT MemberID, AccountName
            FROM members
            WHERE MemberID=%s and Password=%s
            '''
            columns, data = utils.query(query_str, (UserID, Password))
            if not data:
                print("密碼錯誤！")
                utils.delete_terminal_content(1.5, 2)
                continue
            break
        Password = prompt_password_confirmation()
        query_str = '''
        UPDATE members
        SET Password=%s
        WHERE MemberID=%s;
        '''
        utils.query(query_str, (Password, UserID))
        print("更改密碼成功！")
    else:
        print("查無此帳號！")
        utils.delete_terminal_content(1.5, 2)

def anonymous_sign_up():
    utils.print_bold("訪客註冊")
    PhoneNumber = prompt_phonenumber()
    query_str = '''
    WITH users_with_numbers AS (
        SELECT UserID,
            CAST(SUBSTRING(UserID FROM 3) AS INTEGER) AS number_part
        FROM users
        WHERE UserID LIKE 'US%'
    )
    SELECT 'US' || LPAD((MAX(number_part) + 1)::TEXT, 8, '0') AS next_UserID
    FROM users_with_numbers
    '''
    columns, data = utils.query(query_str)
    UserID = data[0]
    query_str = '''
    INSERT INTO users (UserID, PhoneNumber) 
    VALUES (%s, %s)
    '''
    utils.query(query_str, (UserID, PhoneNumber))
    print("匿名註冊成功！")

def anonymous_sign_in():
    utils.print_bold("訪客登入")
    while True:
        PhoneNumber = input("請輸入電話號碼：")
        if is_valid_phonenumber(PhoneNumber) == 0:
            print("格式錯誤！")
            utils.delete_terminal_content(1.5, 2)
        elif bool(check_phonenumber_existence(PhoneNumber)) == 0:
            print("查無此電話號碼！")
            utils.delete_terminal_content(1.5, 2)
        else:
            UserID = check_phonenumber_existence(PhoneNumber)[0][0]
            if UserID[:2] == "US":
                print("提醒您，現在是以匿名登入！")
                return UserID, "匿名使用者"
            else:
                # 此處需連接登入頁面func
                print("此電話號碼不適用匿名登入，請前往會員登入頁面！")
                utils.delete_terminal_content(1.5, 2)

def log_out():
    utils.userid = ""
    utils.username = ""
    utils.role = ""
    utils.print_bold("Bye!")

