import utils

def message_people_view():
    utils.print_bold("以下為您的最近聯絡人的名單！")
    query = '''
    SELECT 
        CASE 
            WHEN u_s.username = %s THEN u_r.username
            ELSE u_s.username
        END AS the_username,
        MAX(m.mgtime) AS last_message_time
    FROM MESSAGE AS m
    JOIN USERS AS u_s ON m.senderid = u_s.userid
    JOIN USERS AS u_r ON m.receiverid = u_r.userid
    WHERE u_s.username = %s OR u_r.username = %s
    GROUP BY the_username
    ORDER BY last_message_time DESC
    '''
    params = (utils.username, utils.username, utils.username)
    columns, data = utils.query(query, params)
    return utils.pd.DataFrame(data, columns=columns)


def message_content_view():
    # 顯示最近聯絡人
    contacts_df = message_people_view()
    print(contacts_df)
    
    # 如果沒有聯絡人，直接結束
    if contacts_df.empty:
        print("您目前沒有任何聯絡人記錄。")
        return
    
    # 輸入並檢查聯絡人
    while True:
        other_user = input("請輸入您想查看的聯絡人對話紀錄：")
        if other_user in contacts_df['the_username'].values:
            break
        print("找不到該聯絡人，請重新輸入！")
    
    utils.print_bold(f"以下為您與 {other_user} 的聊天記錄！")
    
    # 查詢與指定聯絡人的聊天記錄
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
    
    # 顯示聊天記錄
    chat_df = utils.pd.DataFrame(data, columns=columns)
    print(chat_df)


def feedback_view():
    print("以下為最新的十則回饋！")
    columns, data = utils.query('''
    SELECT f.userid, u.username, f.fbtime, f.fbcontent
    from feedback as f
    join USERS as u on f.userid = u.userid
    order by fbtime desc
    limit 10
    ''')
    return utils.pd.DataFrame(data, columns=columns).sort_values("fbtime")

def comment_view(itemID):
    print("以下為最新的十則留言！")
    columns, data = utils.query(f'''
    SELECT c.memberid, u.username, c.itemid, i.description, c.cmtime, c.cmcontent
    from COMMENTS as c
    join USERS as u on c.memberid = u.userid
    join ITEM as i on c.itemid = i.itemid
    WHERE i.itemid = '{itemID}'
    order bt cmtime desc
    limit 10
    ''')
    # 將結果轉換為 DataFrame
    return utils.pd.DataFrame(data, columns=columns).sort_values("cmtime")

def post_comment():
    utils.print_bold("發表留言")
    itemID = input("請輸入您要留言的物品ID：")
    comment_content = input("請輸入留言內容：")
    
    query = '''
    INSERT INTO COMMENTS (itemid, memberid, cmtime, cmcontent)
    VALUES (%s, %s, CURRENT_TIMESTAMP, %s)
    '''
    params = (itemID, utils.userid, comment_content)
    
    try:
        utils.query(query, params)
        print("留言已成功送出！")
    except Exception as e:
        print(f"留言送出失敗，請重試！錯誤：{e}")


    
def post_feedback():
    utils.print_bold("提供回饋")
    feedback_content = input("請輸入您的回饋內容：")
    
    query = '''
    INSERT INTO FEEDBACK (userid, fbtime, fbcontent)
    VALUES (%s, CURRENT_TIMESTAMP, %s)
    '''
    params = (utils.userid, feedback_content)
    
    try:
        utils.query(query, params)
        print("感謝您的回饋！已成功提交。")
    except Exception as e:
        print(f"回饋提交失敗，請重試！錯誤：{e}")


    
def post_message():
    utils.print_bold("發送訊息")
    
    # 查詢所有用戶 ID 和用戶名
    query_users = '''
    SELECT MEMBERS.memberid, USERS.username AS membername
    FROM MEMBERS
    JOIN USERS ON MEMBERS.memberid = USERS.userid
    '''
    columns, data = utils.query(query_users)
    users_df = utils.pd.DataFrame(data, columns=columns)
    
    print("以下為可用的用戶：")
    print(users_df)

    # 確認收件人是否存在
    while True:
        receivername = input("請輸入收件人的用戶名稱：")
        if receivername in users_df['membername'].values:
            # 獲取收件人的 memberid
            receiverID = users_df.loc[users_df['membername'] == receivername, 'memberid'].values[0]
            break
        print("找不到該用戶名稱，請重新輸入！")
    
    message_content = input("請輸入訊息內容：")
    
    # 插入訊息
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



