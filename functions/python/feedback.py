import utils

def feedback_view():
    print("以下為最新的十則回饋！")
    query = '''
    SELECT f.userid, u.username, f.fbtime, f.fbcontent
    FROM feedback AS f
    JOIN USERS AS u ON f.userid = u.userid
    ORDER BY fbtime DESC
    LIMIT 10
    '''
    columns, data = utils.query(query)
    return utils.pd.DataFrame(data, columns=columns).sort_values("fbtime")

    
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
        utils.delete_terminal_content(1.5, 2)