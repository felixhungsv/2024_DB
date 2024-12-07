import utils
import comment

def view_posts_by_comments(page=1): # 檢視貼文排序依照貼文的留言數
    if page < 1:
        raise ValueError("頁碼必須為 1 或更大.")
    
    offset = (page - 1) * 10 # 每一頁有10個貼文

    columns, data = utils.query(f'''
    SELECT 
        p.memberid, 
        u.username,
        p.itemid, 
        i.itemdescription, 
        p.posttime, 
        rc.status,
        COUNT(c.comment_id) AS comment_count
    FROM POSTS AS p
    JOIN USERS AS u ON p.memberid = u.userid
    JOIN ITEMS AS i ON p.itemid = i.itemid
    LEFT JOIN COMMENTS AS c ON p.itemid = c.itemid
    LEFT JOIN RETURNS_OR_CLAIMS AS rc ON p.itemid = rc.itemid
    GROUP BY p.itemid
    ORDER BY c.count(*) DESC
    LIMIT 10 OFFSET {offset}
    ''')

    return utils.pd.DataFrame(data, columns=columns)

def view_posts_by_posttime(page=1): # 檢視貼文排序依照貼文發布時間
    if page < 1:
        raise ValueError("頁碼必須為 1 或更大")
    
    offset = (page - 1) * 10

    columns, data = utils.query(f'''
    SELECT 
        p.memberid, 
        u.username,
        p.itemid, 
        i.itemdescription, 
        p.posttime, 
        rc.status,
        COUNT(c.comment_id) AS comment_count
    FROM POSTS AS p
    JOIN USERS AS u ON p.memberid = u.userid
    JOIN ITEMS AS i ON p.itemid = i.itemid
    LEFT JOIN COMMENTS AS c ON p.itemid = c.itemid
    LEFT JOIN RETURNS_OR_CLAIMS AS rc ON p.itemid = rc.itemid
    GROUP BY p.itemid
    ORDER BY p.posttime DESC
    LIMIT 10 OFFSET {offset}
    ''')

    return utils.pd.DataFrame(data, columns=columns)

#def view_user_profile(user_id): # 檢視個人主頁

    #columns, data = utils.query(f'''
    #SELECT 
        #u.userid,
        #u.username,
        #u.email,
        #u.phonenumber,
    #FROM USERS AS u
    #WHERE u.userid = '{user_id}'
    #''')
    #return utils.pd.DataFrame(data, columns=columns)

# user_id = 'UB07050678'  # 假設用戶的 ID 是 UB07050678
# profile_data = view_user_profile(user_id)
# print(profile_data)

def type_of_posts():
    print("請問要以哪種排序檢視？")
    print("1: 依照時間序  2: 依照留言數")
    type = input("請輸入數字：")
    if type == "1":
        view_posts_by_posttime(utils.page)
    elif type == "2":
        view_posts_by_comments(utils.page)
    else:
        print("輸入錯誤！請重新再試！")
        utils.delete_terminal_content(1.5,2)
    while True:
        print("請問是否要查看留言或發出留言？")
        print("1: 查看留言  2: 發出留言 3: 返回")   
        type = input("請輸入數字：")
        if type == "1":
            print("請輸入要查看的物品ID：")
            itemid = input("ItemID: ")
            print(comment.comment_view(itemid))
        elif type == "2":
            comment.post_comment()
        elif type == "3":
            break
    

def delete_post(role, member_id=None, item_id=None): # 刪除貼文
    
    if role == 'Member':
        # 會員：刪除自己的貼文
        utils.query(f'''
        DELETE FROM POSTS
        WHERE UserID = '{member_id}' AND ItemID = '{item_id}'
        ''')
        return f"temID {item_id} 的貼文已被成功刪除。"
    
    elif role == 'User':
        # 匿名用戶：只能刪除自己的貼文
        utils.query(f'''
        DELETE FROM POSTS
        WHERE UserID = '{user_id}' AND ItemID = '{item_id}'
        ''')
        return f"ItemID {item_id} 的貼文已被成功刪除。"
    
    elif role == 'Manager':
        # 業務經理者：可以刪除所有人的貼文
        utils.query(f'''
        DELETE FROM POSTS
        WHERE ItemID = '{item_id}'
        ''')
        return f"ItemID {item_id} 的貼文已被成功刪除。"
    
    else:
        raise ValueError("刪除貼文無效.")
    
# role = 'Manager'
# item_id = 'IT00000001'

# result = delete_post(role, item_id=item_id)
# print(result)

def delete_comment(role, member_id=None, item_id=None, commenter_id=None, comment_time=None): # 刪除留言
    
    if role == 'Member':
        # 會員：只能刪除自己的留言
        utils.query(f'''
        DELETE FROM COMMENTS
        WHERE MemberID = '{member_id}' AND ItemID = '{item_id}' AND CmContent = '{comment_content}'
        ''')
        return f"已成功刪除對 ItemID {item_id} 的評論。"
    
    elif role == 'Manager':
        # 業務經理者：可以刪除所有人的留言
        utils.query(f'''
        DELETE FROM COMMENTS
        WHERE ItemID = '{item_id}' AND CmContent = '{comment_content}'
        ''')
        return f"已成功刪除對 ItemID {item_id} 的評論。"
    
    else:
        raise PermissionError("您沒有刪除評論的權限。")

# role = 'Member'
# member_id = 'UB09340643'
# item_id = 'IT00000823'
# comment_content = '我弄丟了它，請問可以提供更詳細的描述嗎？0'

# result = delete_comment(role, member_id=member_id, item_id=item_id, comment_content=comment_content)
# print(result)

def delete_message(role, sender_id=None, receiver_id=None, message_content=None): # 刪除私訊
    
    if role == 'Member':
        # 會員：只能刪除自己發送或接收的私訊
        utils.query(f'''
        DELETE FROM MESSAGES
        WHERE (SenderID = '{sender_id}' OR ReceiverID = '{receiver_id}')
          AND MgContent = '{message_content}'
        ''')
        return f"已成功刪除 {message_content}。"
    
    elif role == 'Manager':
        # 業務經理者：可以刪除所有私訊
        utils.query(f'''
        DELETE FROM MESSAGES
        WHERE MgContent = '{message_content}'
        ''')
        return f"已成功刪除 {message_content}。"
    
    else:
        raise PermissionError("Role does not have permission to delete messages.")
    
# role = 'Member'
# sender_id = 'UD01195700'
# message_content = '我記得放在椅子上，請問可以再提供一些細節嗎？'

# result = delete_message(role, sender_id=sender_id, message_content=message_content)
# print(result)
# 輸出：Message at 我記得放在椅子上，請問可以再提供一些細節嗎？ deleted successfully by Member.
 













    
