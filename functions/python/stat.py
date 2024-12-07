import utils

def run_analysis():
    print("請選擇要執行的分析：")
    print("1: 最常見的地點")
    print("2: 用戶參與度")
    print("3: 物品類別趨勢")
    print("4: 報酬獎勵效果")
    print("5: 熱門時間分析")

    selected_option = int(input("請輸入數字："))
    # 根據用戶選擇執行對應的分析
    while True:
        if selected_option == 1:
            return top_locations_analysis()
        elif selected_option == 2:
            return user_engagement_analysis()
        elif selected_option == 3:
            return item_category_trends_analysis()
        elif selected_option == 4:
            return reward_effectiveness_analysis()
        elif selected_option == 5:
            return popular_time_analysis()
        else:
            print("請輸入正確的數字！")
            selected_option = int(input("請輸入數字："))
            

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

def reward_effectiveness_analysis():
    query = '''
    SELECT 
        R.rewardname,
        R.amount,
        COUNT(DISTINCT F.itemid) AS found_with_reward,
        COUNT(DISTINCT LST.itemid) AS lost_with_reward,
        (COUNT(DISTINCT F.itemid)::FLOAT / COUNT(DISTINCT LST.itemid)) AS success_rate
    FROM 
        reward R
    LEFT JOIN found_item F ON R.itemid = F.itemid
    LEFT JOIN lost_item LST ON R.itemid = LST.itemid
    GROUP BY R.rewardname, R.amount
    ORDER BY success_rate DESC, R.amount DESC;
    '''
    columns, data = utils.query(query)
    return columns, data

def popular_time_analysis():
    query = '''
    SELECT 
        EXTRACT(HOUR FROM losttime) AS lost_hour,
        COUNT(DISTINCT L.itemid) AS lost_count,
        EXTRACT(HOUR FROM foundtime) AS found_hour,
        COUNT(DISTINCT F.itemid) AS found_count
    FROM 
        lost_item L
    FULL OUTER JOIN found_item F ON L.itemid = F.itemid
    GROUP BY lost_hour, found_hour
    ORDER BY lost_hour, found_hour;
    '''
    columns, data = utils.query(query)
    return columns, data
