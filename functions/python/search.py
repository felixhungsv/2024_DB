import utils

def search():
    utils.print_bold(f"您好，{utils.username}！")
    print("請問您要搜尋「遺失物」或「尋獲物」呢？")
    print("1: 遺失物  2: 尋獲物")
    while True:
        type = input("請輸入數字：")
        if type == 1:
            item_name = input("您遺失的物品名稱：")
            utils.list_category()
            item_category = input("您遺失的物品數屬於哪個類別（請填數字）：")
            item_time = input("您遺失的大致時間（格式為YYYY-MM-DD HH:MM:SS，可不填）：") # 要把它轉換成timestamp格式存進資料庫
            utils.list_location()
            item_location = input("您遺失的大致地點（請填數字，可不填）：")
            print("發文成功！感謝您的參與！") # 可以接回饋
            break
        elif type == 2:
            item_name = input("您尋獲的物品名稱：")
            utils.list_category()
            item_category = input("您尋獲的物品數屬於哪個類別（請填數字）：")
            item_time = input("您尋獲的大致時間（格式為YYYY-MM-DD HH:MM:SS，可不填）：") # 要把它轉換成timestamp格式存進資料庫
            utils.list_location()
            item_location = input("您尋獲的大致地點（請填數字，可不填）：")
            item_store = input("您將物品存放在哪個地點（請填數字）：")
            print("發文成功！感謝您的參與！") # 可以接回饋
            break
        else:
            print("輸入錯誤！請重新再試！")
            utils.delete_terminal_content(1.5,2)