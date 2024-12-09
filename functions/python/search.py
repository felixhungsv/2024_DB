import utils

def search():
    utils.print_bold(f"您好，{utils.username}！")
    print("請問您要搜尋「遺失物」或「尋獲物」呢？")
    print("1: 遺失物  2: 尋獲物")
    while True:
        type = input("請輸入數字：")
        if type == "1":
            utils.list_category()
            item_category = input("您要搜尋的物品數屬於哪個類別（請填數字，可不填）：")
            if item_category:
                item_category_name = utils.category_names[int(item_category)-1]
            item_start_time = input("您要搜尋的開始時間（格式為YYYY-MM-DD HH:MM:SS，可不填）：")
            if item_start_time:
                item_end_time = input("您要搜尋的結束時間（格式為YYYY-MM-DD HH:MM:SS）：")
            utils.list_location()
            item_location = input("您要搜尋的物品遺失地點（請填數字，可不填）：")
            if item_location:
                item_location_name = utils.locations[int(item_location)-1]

            # 顯示出貼文
            query_str = '''
            SELECT         
            c.categoryname, i.description, lt.locationdescription, p.posttime
            FROM posts p
            JOIN lost_item li ON li.itemid = p.itemid
            JOIN locates lo ON lo.itemid = p.itemid
            JOIN locations lt ON lt.locationid = lo.locationid
            JOIN belongs b ON b.itemid = p.itemid
            JOIN category c ON c.categoryid = b.categoryid
            LEFT JOIN members m ON m.memberid = p.userid
            JOIN item i ON i.itemid = p.itemid
            WHERE 1=1
            '''

            params = []

            if item_category:
                query_str += ''' AND c.categoryname=%s'''
                params.append(item_category_name)
            if item_start_time:
                query_str += ''' AND li.losttime>=%s AND li.losttime<=%s'''
                params.append(item_start_time)
                params.append(item_end_time)
            if item_location:
                query_str += ''' AND lt.locationdescription=%s'''
                params.append(item_location_name)
            columns, data = utils.query(query_str, tuple(params))
            dataframe = utils.pd.DataFrame(data, columns=columns)
            dataframe.rename(columns={"categoryname": '類別名稱', "description":"描述", "locationdescription":"地點", "posttime":"發文時間"}, inplace=True)

            print(dataframe)
            
            break
        elif type == "2":
            utils.list_category()
            item_category = input("您要搜尋的物品數屬於哪個類別（請填數字，可不填）：")
            if item_category:
                item_category_name = utils.category_names[int(item_category)-1]
            item_start_time = input("您要搜尋的開始時間（格式為YYYY-MM-DD HH:MM:SS，可不填）：")
            if item_start_time:
                item_end_time = input("您要搜尋的結束時間（格式為YYYY-MM-DD HH:MM:SS）：")
            utils.list_location()
            item_location = input("您要搜尋的物品尋獲地點（請填數字，可不填）：")
            if item_location:
                item_location_name = utils.locations[int(item_location)-1]
            # item_store = input("您要搜尋的物品存放地點（請填數字，可不填）：")
            # if item_store:
            #     item_store_name = utils.locations[int(item_location)-1]

            # 顯示出貼文
            query_str = '''
            SELECT 	    
            c.categoryname, i.description, lt.locationdescription, p.posttime
            FROM posts p
            JOIN lost_item li ON li.itemid = p.itemid
            JOIN locates lo ON lo.itemid = p.itemid
            JOIN locations lt ON lt.locationid = lo.locationid
            JOIN belongs b ON b.itemid = p.itemid
            JOIN category c ON c.categoryid = b.categoryid
            JOIN members m ON m.memberid = p.userid
            JOIN item i ON i.itemid = p.itemid
            WHERE 1=1
            '''

            params = []

            if item_category:
                query_str += ''' AND c.categoryname=%s'''
                params.append(item_category_name)
            if item_start_time:
                query_str += ''' AND li.losttime>=%s AND li.losttime<=%s'''
                params.append(item_start_time)
                params.append(item_end_time)
            if item_location:
                query_str += ''' AND lt.locationdescription=%s'''
                params.append(item_location_name)
            # if item_store:
            #     query_str += ''' AND s.locationdescription=%s'''
            #     params.append(item_store_name)
            columns, data = utils.query(query_str, tuple(params))
            dataframe = utils.pd.DataFrame(data, columns=columns)
            dataframe.rename(columns={"categoryname": '類別名稱', "description":"描述", "locationdescription":"地點", "posttime":"發文時間"}, inplace=True)
            print(dataframe)

            break
        else:
            print("輸入錯誤！請重新再試！")
            utils.delete_terminal_content(1.5,2)

search()