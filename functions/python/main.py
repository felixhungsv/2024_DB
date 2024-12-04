import utils
import sign
import text

# 註冊/登入
while True:
    i = 1
    print(f"{i}:註冊")
    i += 1
    print(f"{i}:登入")
    str = input("請選擇功能：")
    if str == "1":
        sign.sign_up()


# homepage 三種
while True:
    if UserID[:2] == "US": # 匿名
    elif UserID[:2] == "MG": # 業務經營者
    else: # 會員


