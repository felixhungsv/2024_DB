import utils

def run_analysis():
    print("請選擇要執行的分析：")
    print("1: 最常見的地點")
    print("2: 用戶參與度")
    print("3: 物品類別趨勢")
    print("4: 失物歸還時間趨勢")
    print("5: 失物尋回成功率")
    selected_option = int(input("請輸入數字："))
    # 根據用戶選擇執行對應的分析
    if selected_option == 1:
        return top_locations_analysis()
    elif selected_option == 2:
        return user_engagement_analysis()
    elif selected_option == 3:
        return item_category_trends_analysis()
    elif selected_option == 4:
        return item_return_time_trends_analysis()  
    elif selected_option == 5:
        return item_recovery_success_rate_analysis()
    else:
        return "Invalid selection. Please choose a number between 1 and 5."

# 定義每個分析的函數
def top_locations_analysis():
    query = '''
    SELECT 
        L.locationdescription,
        COUNT(DISTINCT F.itemid) AS found_count,
        COUNT(DISTINCT LST.itemid) AS lost_count
    FROM 
        locations L
    LEFT JOIN locates LO ON L.locationid = LO.locationid
    LEFT JOIN found_item F ON LO.itemid = F.itemid
    LEFT JOIN lost_item LST ON LO.itemid = LST.itemid
    GROUP BY L.locationdescription
    ORDER BY (COUNT(DISTINCT F.itemid) + COUNT(DISTINCT LST.itemid)) DESC
    '''
    columns, data = utils.query(query)
    return columns, data

def user_engagement_analysis():
    query = '''
    SELECT 
        U.userid,
        U.username,
        COUNT(DISTINCT P.itemid) AS posts_count
    FROM 
        users U
    LEFT JOIN posts P ON U.userid = P.userid
    GROUP BY U.userid, U.username
    ORDER BY posts_count DESC
    LIMIT 10;
    '''
    columns, data = utils.query(query)
    return columns, data

def item_category_trends_analysis():
    query = '''
    SELECT 
        C.categoryname,
        COUNT(DISTINCT L.itemid) AS lost_count,
        COUNT(DISTINCT F.itemid) AS found_count
    FROM 
        category C
    LEFT JOIN belongs B ON C.categoryid = B.categoryid
    LEFT JOIN lost_item L ON B.itemid = L.itemid
    LEFT JOIN found_item F ON B.itemid = F.itemid
    GROUP BY C.categoryname
    ORDER BY lost_count DESC, found_count DESC;
    '''
    columns, data = utils.query(query)
    return columns, data

# 新增失物歸還時間趨勢分析
def item_return_time_trends_analysis():
    query = '''
    SELECT 
        L.locationdescription,
        DATE_TRUNC('month', COALESCE(LST.losttime, F.foundtime)) AS month,
        AVG(EXTRACT(EPOCH FROM (COALESCE(LST.losttime, F.foundtime) - F.foundtime)) / 3600) AS avg_return_time_hours
    FROM 
        locations L
    LEFT JOIN locates LO ON L.locationid = LO.locationid
    LEFT JOIN found_item F ON LO.itemid = F.itemid
    LEFT JOIN lost_item LST ON LO.itemid = LST.itemid
    GROUP BY L.locationdescription, month
    ORDER BY month DESC, avg_return_time_hours;
    '''
    columns, data = utils.query(query)
    return columns, data

# 新增失物尋回成功率分析
def item_recovery_success_rate_analysis():
    query = '''
    SELECT 
        L.locationdescription,
        COUNT(DISTINCT F.itemid) AS found_count,
        COUNT(DISTINCT LST.itemid) AS lost_count,
        (COUNT(DISTINCT F.itemid) * 100.0 / NULLIF(COUNT(DISTINCT LST.itemid), 0)) AS recovery_success_rate
    FROM 
        locations L
    LEFT JOIN locates LO ON L.locationid = LO.locationid
    LEFT JOIN found_item F ON LO.itemid = F.itemid
    LEFT JOIN lost_item LST ON LO.itemid = LST.itemid
    GROUP BY L.locationdescription
    ORDER BY recovery_success_rate DESC
    LIMIT 10;
    '''
    columns, data = utils.query(query)
    return columns, data
