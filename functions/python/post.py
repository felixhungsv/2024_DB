import utils
from datetime import datetime

def post():
    utils.print_bold(f"您好，{utils.username}！")
    print("請問您是「遺失」或「尋獲」物品呢？")
    print("1: 遺失  2: 尋獲")
    while True:
        utils.sys.stdout.write("\033[s")
        type = input("請輸入數字：")
        utils.query("BEGIN;")
        try:
            if type == "1":
                item_name = input("您遺失的物品名稱：")
                utils.list_category()
                item_category = input("您遺失的物品數屬於哪個類別（請填數字）：")
                item_category_name = utils.category_names[int(item_category)-1]
                item_time = input("您遺失的大致時間（格式為YYYY-MM-DD HH:MM:SS，可不填）：") # 要把它轉換成timestamp格式存進資料庫
                utils.list_location()
                item_location = input("您遺失的大致地點（請填數字，可不填）：")
                if item_location:
                    item_location_name = utils.locations[int(item_location)-1]
                item_description = input("您對物品的詳細描述：")
                item_image = input("物品照片的網址（可不填）：")
                if item_image == "":
                    item_image = None
                item_reward = input("您提出的懸賞物品名稱（可不填）：")
                item_reward_amount = input("您提出的懸賞物品數量（請填數字，可不填）：")

                # 找ID
                query_str = '''
                WITH items_with_numbers AS (
                    SELECT ItemID,
                        CAST(SUBSTRING(ItemID FROM 3) AS INTEGER) AS number_part
                    FROM item
                    WHERE ItemID LIKE 'IT%'
                )
                SELECT 'IT' || LPAD((MAX(number_part) + 1)::TEXT, 8, '0') AS next_ItemID
                FROM items_with_numbers;
                '''
                columns, data = utils.query(query_str)
                ItemID =  data[0]

                # insert item
                query_str = '''
                INSERT INTO item(ItemID, Description, imageURL)
                VALUES (%s, %s, %s);
                '''
                utils.query(query_str, (ItemID, item_description, item_image))

                # insert lost_item
                query_str = '''
                INSERT INTO lost_item(ItemID, losttime)
                VALUES (%s, %s);
                '''
                utils.query(query_str, (ItemID, item_time))

                # insert reward
                if item_reward:
                    query_str = '''
                    INSERT INTO reward(ItemID, rewardname, amount)
                    VALUES (%s, %s, %s);
                    '''
                    utils.query(query_str, (ItemID, item_reward, item_reward_amount))

                # find category
                query_str = '''
                SELECT CategoryID
                FROM category
                WHERE CategoryName=%s;
                '''
                columns, data = utils.query(query_str, (item_category_name,))
                item_category_id = data[0]

                # insert belongs
                query_str = '''
                INSERT INTO belongs(ItemID, categoryid)
                VALUES (%s, %s);
                '''
                utils.query(query_str, (ItemID, item_category_id))

                # insert posts
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                query_str = '''
                INSERT INTO posts(UserID, ItemID, posttime)
                VALUES (%s, %s, %s);
                '''
                utils.query(query_str, (utils.userid, ItemID, formatted_time))

                if item_location != "\n":
                    # find location
                    query_str = '''
                    SELECT LocationID
                    FROM locations
                    WHERE LocationDescription=%s;
                    '''
                    columns, data = utils.query(query_str, (item_location_name,))
                    item_location_id = data[0]

                    # insert locates
                    query_str = '''
                    INSERT INTO locates(ItemID, locationid)
                    VALUES (%s, %s);
                    '''
                    utils.query(query_str, (ItemID, item_location_id))

                utils.query("COMMIT;")

                print("發文成功！感謝您的參與！") # 可以接回饋
                break
            elif type == "2":
                item_name = input("您尋獲的物品名稱：")
                utils.list_category()
                item_category = input("您尋獲的物品數屬於哪個類別（請填數字）：")
                item_category_name = utils.category_names[int(item_category)-1]
                item_time = input("您尋獲的大致時間（格式為YYYY-MM-DD HH:MM:SS）：") # 要把它轉換成timestamp格式存進資料庫
                utils.list_location()
                item_location = input("您尋獲的大致地點（請填數字）：")
                item_location_name = utils.locations[int(item_location)-1]
                item_store = input("您將物品存放在哪個地點（請填數字）：")
                item_store_name = utils.locations[int(item_store)-1]
                item_description = input("您對物品的詳細描述：")
                item_image = input("物品照片的網址（可不填）：")
                if item_image == "\n":
                    item_image = None

                # 找ID
                query_str = '''
                WITH items_with_numbers AS (
                    SELECT ItemID,
                        CAST(SUBSTRING(ItemID FROM 3) AS INTEGER) AS number_part
                    FROM item
                    WHERE ItemID LIKE 'IT%'
                )
                SELECT 'IT' || LPAD((MAX(number_part) + 1)::TEXT, 8, '0') AS next_ItemID
                FROM items_with_numbers;
                '''
                columns, data = utils.query(query_str)
                ItemID =  data[0]

                # insert item
                query_str = '''
                INSERT INTO item(ItemID, Description, imageURL)
                VALUES (%s, %s, %s);
                '''
                utils.query(query_str, (ItemID, item_description, item_image))

                # insert found_item
                query_str = '''
                INSERT INTO found_item(ItemID, foundtime)
                VALUES (%s, %s);
                '''
                utils.query(query_str, (ItemID, item_time))

                # find store
                query_str = '''
                SELECT LocationID
                FROM locations
                WHERE LocationDescription=%s;
                '''
                columns, data = utils.query(query_str, (item_store_name,))
                item_store_id = data[0]

                # insert stores
                query_str = '''
                INSERT INTO stores(ItemID, locationid, starttime)
                VALUES (%s, %s, %s);
                '''
                utils.query(query_str, (ItemID, item_store_id, item_time))

                # find category
                query_str = '''
                SELECT CategoryID
                FROM category
                WHERE CategoryName=%s;
                '''
                columns, data = utils.query(query_str, (item_category_name,))
                item_category_id = data[0]

                # insert belongs
                query_str = '''
                INSERT INTO belongs(ItemID, categoryid)
                VALUES (%s, %s);
                '''
                utils.query(query_str, (ItemID, item_category_id))

                # insert posts
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                query_str = '''
                INSERT INTO posts(UserID, ItemID, posttime)
                VALUES (%s, %s, %s);
                '''
                utils.query(query_str, (utils.userid, ItemID, formatted_time))

                # find location
                query_str = '''
                SELECT LocationID
                FROM locations
                WHERE LocationDescription=%s;
                '''
                columns, data = utils.query(query_str, (item_location_name,))
                item_location_id = data[0]

                # insert locates
                query_str = '''
                INSERT INTO locates(ItemID, locationid)
                VALUES (%s, %s);
                '''
                utils.query(query_str, (ItemID, item_location_id))

                utils.query("COMMIT;")

                print("發文成功！感謝您的參與！") # 可以接回饋
                break
            else:
                print("輸入錯誤！請重新再試！")
                utils.delete_terminal_content(1.5,2)
        except Exception as e:
            print(f"發生問題，請重新再試！{e}")
            utils.query("ROLLBACK;")
            utils.time.sleep(2)
            utils.sys.stdout.write("\033[u\033[J")

# post()