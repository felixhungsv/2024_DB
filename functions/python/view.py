import utils
import comment

def view_posts_by_comments(page=1): # 檢視貼文排序依照貼文的留言數
    
    # 每頁顯示的貼文數量
    posts_per_page = 5
    offset = (page - 1) * posts_per_page

    query = '''
    WITH CommentCounts AS (
    SELECT 
        p.ItemID,
        COUNT(cm.CmContent) AS CommentCount
    FROM POSTS p
    LEFT JOIN COMMENTS cm ON p.ItemID = cm.ItemID
    GROUP BY p.ItemID
    ),
    UniqueClaims AS (
        SELECT 
            ItemID,
            MAX(Status) AS ClaimStatus -- 假設每個 ItemID 只有一個有效的 ClaimStatus
        FROM RETURNS_OR_CLAIMS
        GROUP BY ItemID
    )
    SELECT 
	    CASE 
            WHEN p.UserID LIKE 'US%' THEN '匿名'
            ELSE m.AccountName
        END AS AccountName,
        c.CategoryName, 
        i.Description, 
        lo.LocationDescription, 
        r.RewardName, 
        r.Amount,
        cc.CommentCount,
        uc.ClaimStatus
    FROM POSTS p
    LEFT JOIN MEMBERS m ON p.UserID = m.MemberID
    JOIN ITEM i ON p.ItemID = i.ItemID
    JOIN LOCATES l ON p.ItemID = l.ItemID
    JOIN LOCATIONS lo ON l.LocationID = lo.LocationID
    JOIN Belongs b ON p.ItemID = b.ItemID
    JOIN CATEGORY c ON b.CategoryID = c.CategoryID
    LEFT JOIN REWARD r ON p.ItemID = r.ItemID
    JOIN CommentCounts cc ON p.ItemID = cc.ItemID
    LEFT JOIN UniqueClaims uc ON p.ItemID = uc.ItemID -- 使用去重的結果
    ORDER BY cc.CommentCount DESC;
    '''
    
    columns, data = utils.query(query)
    df = utils.pd.DataFrame(data, columns=columns)

    # 過濾已認領的貼文
    df = df[df['ClaimStatus'] != 'S']

    # 計算總頁數
    total_posts = len(df)
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page

    # 獲取當前頁面的貼文
    page_data = df.iloc[offset:offset + posts_per_page]

    if page_data.empty:
        print("沒有更多貼文了！")
        return
   
    print(page_data.drop(columns=['ClaimStatus']))  # 顯示時隱藏過濾欄位
    return total_pages

def view_posts_by_posttime(page=1): # 檢視貼文排序依照貼文發布時間

     # 每頁顯示的貼文數量
    posts_per_page = 5
    offset = (page - 1) * posts_per_page
    
    query = '''
    WITH CommentCounts AS (
    SELECT 
        p.ItemID,
        COUNT(cm.CmContent) AS CommentCount
    FROM POSTS p
    LEFT JOIN COMMENTS cm ON p.ItemID = cm.ItemID
    GROUP BY p.ItemID
    ),
    UniqueClaims AS (
        SELECT 
            ItemID,
            MAX(Status) AS ClaimStatus -- 假設每個 ItemID 只有一個有效的 ClaimStatus
        FROM RETURNS_OR_CLAIMS
        GROUP BY ItemID
    )
    SELECT 
	    CASE 
            WHEN p.UserID LIKE 'US%' THEN '匿名'
            ELSE m.AccountName
        END AS AccountName,
        c.CategoryName, 
        i.Description, 
        lo.LocationDescription, 
        r.RewardName, 
        r.Amount,
	    p.PostTime,
        uc.ClaimStatus
    FROM POSTS p
    LEFT JOIN MEMBERS m ON p.UserID = m.MemberID
    JOIN ITEM i ON p.ItemID = i.ItemID
    JOIN LOCATES l ON p.ItemID = l.ItemID
    JOIN LOCATIONS lo ON l.LocationID = lo.LocationID
    JOIN Belongs b ON p.ItemID = b.ItemID
    JOIN CATEGORY c ON b.CategoryID = c.CategoryID
    LEFT JOIN REWARD r ON p.ItemID = r.ItemID
    JOIN CommentCounts cc ON p.ItemID = cc.ItemID
    LEFT JOIN UniqueClaims uc ON p.ItemID = uc.ItemID -- 使用去重的結果
    ORDER BY p.PostTime DESC;
    '''

    columns, data = utils.query(query)
    df = utils.pd.DataFrame(data, columns=columns)

    # 過濾已認領的貼文
    df = df[df['ClaimStatus'] != 'S']

    # 計算總頁數
    total_posts = len(df)
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page

    # 獲取當前頁面的貼文
    page_data = df.iloc[offset:offset + posts_per_page]

    if page_data.empty:
        print("沒有更多貼文了！")
        return
   
    print(page_data.drop(columns=['ClaimStatus']))  # 顯示時隱藏過濾欄位
    return total_pages

def type_of_posts():
    print("請問要以哪種排序檢視？")
    print("1: 依照時間序  2: 依照留言數")
    type = input("請輸入數字：")
    if type == "1":
        total_pages = view_posts_by_posttime(utils.page)
    elif type == "2":
        view_posts_by_comments(utils.page)
    else:
        print("輸入錯誤！請重新再試！")
        utils.delete_terminal_content(1.5,2)
    while True:
        print(f"\n頁數：{utils.page}/{total_pages}")
        print("請選擇：")
        print("1. 下一頁")
        print("2. 上一頁")
        print("3: 查看留言") 
        print("4: 發出留言")
        print("5: 返回")
        choice = input("請輸入選項（1/2）：")
        if choice == "1":
            # 查看下一頁
            if utils.page < total_pages:
                view_posts_by_comments(utils.page + 1)
            else:
                print("已經是最後一頁了！")
            break
        elif choice == "2":
            # 查看上一頁
            if utils.page > 1:
                view_posts_by_comments(utils.page - 1)
            else:
                print("已經是第一頁了！")
            break
        elif choice == "3":
            print("請輸入要查看的物品ID：")
            itemid = input("ItemID: ")
            print(comment.comment_view(itemid))
        elif choice == "4":
            comment.post_comment()
        elif choice == "5":
            break
        else:
            print("無效的選項，請重新輸入。")
		
    
 













    
