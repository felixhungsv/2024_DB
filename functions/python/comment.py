import utils

def comment_view(itemID):
    print("以下為最新的十則留言！")
    query = '''
    SELECT c.memberid, u.username, c.itemid, i.description, c.cmtime, c.cmcontent
    FROM COMMENTS AS c
    JOIN USERS AS u ON c.memberid = u.userid
    JOIN ITEM AS i ON c.itemid = i.itemid
    WHERE i.itemid = %s
    ORDER BY c.cmtime DESC
    LIMIT 10
    '''
    params = (itemID,)
    columns, data = utils.query(query, params)
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