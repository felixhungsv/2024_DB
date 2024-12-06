import utils
import sign
import text
import search

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
            if utils.userid & utils.username:
                break
            utils.time.sleep(2)
        else:
            raise ValueError("輸入無效")
    except ValueError as e:
        print("格式錯誤！請輸入正確數字！")
        utils.delete_terminal_content(1.5, 2)

if utils.userid:
    if utils.userid[:2] == "US": # 匿名
        utils.role = "anonym"
    elif utils.userid[:2] == "MG": # 業務經營者
        utils.role = "manager"
    else: # 會員
        utils.role = "member"


# # homepage 三種
# while True:
#     if UserID[:2] == "US": # 匿名
#     elif UserID[:2] == "MG": # 業務經營者
#     else: # 會員

