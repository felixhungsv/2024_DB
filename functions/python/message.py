import utils

def message_view():
    """
    主功能：提供顯示聯絡人名單、查看聊天記錄或發送訊息的選項。
    """ 
    print("功能選項：")
    print("1. 查看與聯絡人的聊天記錄")
    print("2. 發送訊息給最近聯絡過的用戶")
    print("3. 發送訊息給新的用戶")

    choice = input("請選擇功能：")

    if choice == "1":
        while True:
            other_user = input("請輸入您想查看的聯絡人對話紀錄：")
            contacts_df = message_people_view()
            if other_user in contacts_df['the_username'].values:
                view_chat_history(other_user)
                break
            print("找不到該聯絡人，請重新輸入！")
    elif choice == "2":
        post_message_to_old_contact()
    elif choice == "3":
        post_message_to_new_contact()
    else:
        print("輸入錯誤，請重新嘗試。")
        
def message_people_view():
    """
    查看最近聯絡人名單。
    """
    utils.print_bold("以下為您的最近聯絡人的名單！")
    query = '''
    SELECT 
        CASE 
            WHEN m.senderid = %s THEN u_r.username
            ELSE u_s.username
        END AS the_username,
        MAX(m.mgtime) AS last_message_time
    FROM MESSAGE AS m
    JOIN USERS AS u_s ON m.senderid = u_s.userid
    JOIN USERS AS u_r ON m.receiverid = u_r.userid
    WHERE m.senderid = %s OR m.receiverid = %s
    GROUP BY the_username
    ORDER BY last_message_time DESC;
    '''
    params = (utils.username, utils.username, utils.username)
    columns, data = utils.query(query, params)
    return utils.pd.DataFrame(data, columns=columns)

def view_chat_history(other_user):
    """
    查看與指定聯絡人的聊天記錄。
    """
    utils.print_bold(f"以下為您與 {other_user} 的聊天記錄！")
    query = '''
    SELECT m.senderid, u_s.username AS senderName, m.receiverid, u_r.username AS receiverName, m.mgtime, m.mgcontent
    FROM MESSAGE AS m
    JOIN USERS AS u_s ON m.senderid = u_s.userid
    JOIN USERS AS u_r ON m.receiverid = u_r.userid
    WHERE 
        (u_s.username = %s AND u_r.username = %s) 
        OR (u_s.username = %s AND u_r.username = %s)
    ORDER BY m.mgtime DESC
    '''
    params = (utils.username, other_user, other_user, utils.username)
    columns, data = utils.query(query, params)
    chat_df = utils.pd.DataFrame(data, columns=columns)
    print(chat_df)

def post_message_to_old_contact():
    """
    發送訊息給最近聯絡過的聯絡人。
    """
    contacts_df = message_people_view()
    print(contacts_df)

    if contacts_df.empty:
        print("您目前沒有任何聯絡人記錄。")
        return

    while True:
        receivername = input("請輸入您想發送訊息的聯絡人名稱：")
        if receivername in contacts_df['the_username'].values:
            break
        print("找不到該聯絡人，請重新輸入！")

    message_content = input("請輸入訊息內容：")
    
    query = '''
    INSERT INTO MESSAGE (senderid, receiverid, mgtime, mgcontent)
    VALUES ((SELECT userid FROM USERS WHERE username = %s), (SELECT userid FROM USERS WHERE username = %s), CURRENT_TIMESTAMP, %s)
    '''
    params = (utils.username, receivername, message_content)

    try:
        utils.query(query, params)
        print("訊息已成功發送！")
    except Exception as e:
        print(f"訊息發送失敗，請重試！錯誤：{e}")
        utils.delete_terminal_content(1.5, 2)

def post_message_to_new_contact():
    """
    發送訊息給未聯絡過的用戶。
    """
    utils.print_bold("發送訊息給新聯絡人")

    query_users = '''
    SELECT MEMBERS.memberid, USERS.username AS membername
    FROM MEMBERS
    JOIN USERS ON MEMBERS.memberid = USERS.userid
    '''
    columns, data = utils.query(query_users)
    users_df = utils.pd.DataFrame(data, columns=columns)

    while True:
        receivername = input("請輸入對方的姓名：")
        if receivername in users_df['membername'].values:
            receiverID = users_df.loc[users_df['membername'] == receivername, 'memberid'].values[0]
            break
        print("找不到該用戶名稱，請重新輸入！")

    message_content = input("請輸入訊息內容：")

    query = '''
    INSERT INTO MESSAGE (senderid, receiverid, mgtime, mgcontent)
    VALUES (%s, %s, CURRENT_TIMESTAMP, %s)
    '''
    params = (utils.userid, receiverID, message_content)

    try:
        utils.query(query, params)
        print("訊息已成功發送！")
    except Exception as e:
        print(f"訊息發送失敗，請重試！錯誤：{e}")
        utils.delete_terminal_content(1.5, 2)


