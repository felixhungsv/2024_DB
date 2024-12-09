import utils
import sign
import view
import search
import post
import feedback
import message
import stats

# 註冊/登入
sign_features = {
    1: ("註冊", sign.sign_up),
    2: ("登入", sign.sign_in),
    3: ("訪客註冊", sign.anonymous_sign_up),
    4: ("訪客登入", sign.anonymous_sign_in)
}
utils.print_bold("功能選單")
for feature_id, (description, _) in sign_features.items():
    print(f"{feature_id}: {description}")
while True:
    try:
        choice = int(input("請選擇功能："))
        if choice in sign_features:
            print("")
            description, function = sign_features[choice]
            utils.userid, utils.username = function()
            if utils.userid != "" and utils.username != "":
                break
            utils.time.sleep(2)
        else:
            raise ValueError("輸入無效")
    except ValueError as e:
        print(f"格式錯誤！請輸入正確數字！{e}")
        # utils.delete_terminal_content(1.5, 2)

if utils.userid:
    if utils.userid[:2] == "US": # 匿名
        utils.role = "anonym"
    elif utils.userid[:2] == "MG": # 業務經營者
        utils.role = "manager"
    else: # 會員
        utils.role = "member"


# homepage 三種

member_features = {
    1: ("發文", post.post),
    2: ("搜尋", search.search),
    3: ("檢視貼文", view.type_of_posts),
    4: ("私訊", message.message_view),
    5: ("回饋", feedback.post_feedback),
    6: ("登出", sign.log_out)
}
anonym_features = {
    1: ("發文", post.post),
    2: ("搜尋", search.search),
    3: ("檢視貼文", view.type_of_posts),
    4: ("回饋", feedback.post_feedback),
    5: ("登出", sign.log_out)
}
manager_features = {
    1: ("搜尋", search.search),
    2: ("檢視貼文", view.type_of_posts),
    3: ("檢視回饋", feedback.feedback_view),
    4: ("統計數據", stats.run_analysis),
    5: ("登出", sign.log_out)
}

def member_homepage():
    while True:
        utils.print_bold("功能選單")
        for feature_id, (description, _) in member_features.items():
            print(f"{feature_id}: {description}")
        try:
            choice = int(input("請選擇功能："))
            if choice in member_features:
                print("")
                description, function = member_features[choice]
                function()
                utils.time.sleep(2)
            else:
                raise ValueError("輸入無效")
            if choice == 6:
                break
        except ValueError as e:
            print("格式錯誤！請輸入正確數字！")
            utils.delete_terminal_content(1.5, 2)
    

def anonym_homepage():
    while True:
        utils.print_bold("功能選單")
        for feature_id, (description, _) in anonym_features.items():
            print(f"{feature_id}: {description}")
        try:
            choice = int(input("請選擇功能："))
            if choice in anonym_features:
                print("")
                description, function = anonym_features[choice]
                function()
                utils.time.sleep(2)
            else:
                raise ValueError("輸入無效")
            if choice == 5:
                break
        except ValueError as e:
            print("格式錯誤！請輸入正確數字！")
            utils.delete_terminal_content(1.5, 2)

def manager_homepage():
    while True:
        utils.print_bold("功能選單")
        for feature_id, (description, _) in manager_features.items():
            print(f"{feature_id}: {description}")
        try:
            choice = int(input("請選擇功能："))
            if choice in manager_features:
                print("")
                description, function = manager_features[choice]
                function()
                utils.time.sleep(2)
            else:
                raise ValueError("輸入無效")
            if choice == 5:
                break
        except ValueError as e:
            print("格式錯誤！請輸入正確數字！")
            utils.delete_terminal_content(1.5, 2)


if utils.role == "anonym": # 匿名
    anonym_homepage()
elif utils.role == "manager": # 業務經營者
    manager_homepage()
else: # 會員
    member_homepage()

# post格式 要過濾被認領的
# 編號: accountname itemdes 類別：itemcategoty 地點：location （懸賞：reward x amount）
# 請輸入數字：編號
# 貼文內包含：發文時間、留言、上一頁下一頁
