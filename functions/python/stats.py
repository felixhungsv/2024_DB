import utils

def run_analysis():
    while True:
        print("請選擇要執行的分析：")
        print("1: 最常見的地點")
        print("2: 用戶參與度")
        print("3: 物品類別趨勢")
        print("4: 報酬獎勵效果")
        print("5: 熱門時間分析")
        print("6: 返回")

        selected_option = int(input("請輸入數字："))
        # 根據用戶選擇執行對應的分析
        if selected_option == 1:
            print(top_locations_analysis())
        elif selected_option == 2:
            print(user_engagement_analysis())
        elif selected_option == 3:
            print(item_category_trends_analysis())
        elif selected_option == 4:
            print(reward_effectiveness_analysis())
        elif selected_option == 5:
            print(popular_time_analysis())
        elif selected_option == 6:
            break
        else:
            print("輸入錯誤！請輸入正確的數字！")
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
    limit 10;
    '''
    columns, data = utils.query(query)
    return utils.pd.DataFrame(data, columns=columns)

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
    return utils.pd.DataFrame(data, columns=columns)

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
    return utils.pd.DataFrame(data, columns=columns)

def reward_effectiveness_analysis():
    query = '''
    SELECT 
        R.rewardname,
        R.amount,
        COUNT(DISTINCT LST.itemid) AS number_of_lost_with_reward
    FROM 
        reward R
    LEFT JOIN lost_item LST ON R.itemid = LST.itemid
    GROUP BY R.rewardname, R.amount
    ORDER BY number_of_lost_with_reward DESC
    limit 10;
    '''
    columns, data = utils.query(query)
    return utils.pd.DataFrame(data, columns=columns)

def popular_time_analysis():
    query = '''
    SELECT 
        hour AS time_hour,
        SUM(lost_count) AS total_lost_count,
        SUM(found_count) AS total_found_count,
        SUM(lost_count + found_count) AS total_items_count
    FROM (
        SELECT 
            EXTRACT(HOUR FROM losttime) AS hour,
            COUNT(DISTINCT L.itemid) AS lost_count,
            0 AS found_count
        FROM 
            lost_item L
        GROUP BY hour

        UNION ALL

        SELECT 
            EXTRACT(HOUR FROM foundtime) AS hour,
            0 AS lost_count,
            COUNT(DISTINCT F.itemid) AS found_count
        FROM 
            found_item F
        GROUP BY hour
    ) AS combined_data
    GROUP BY time_hour
    ORDER BY total_items_count DESC;
    '''
    columns, data = utils.query(query)
    return utils.pd.DataFrame(data, columns=columns)
