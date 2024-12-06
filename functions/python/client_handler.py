import threading

# 儲存每個 client 的資料
class ClientData:
    def __init__(self, userid, role):
        self.userid = userid
        self.role = role

# 使用 thread-local 儲存每個執行緒的 client 資料
thread_local_data = threading.local()

def handle_client(userid, role):
    """
    處理單一 client 的邏輯，並將 client 資料儲存於執行緒專屬變數中
    """
    client_data = ClientData(userid, role)
    thread_local_data.client_data = client_data
    
    # 模擬處理邏輯，例如：根據 userid 和 role 執行不同的操作
    print(f"Handling client with userid: {client_data.userid}, role: {client_data.role}")
    
    # 可在此處加入其他邏輯來處理 client 的需求
    perform_action_based_on_role(client_data)

def perform_action_based_on_role(client_data):
    """
    根據 client 的 role 執行不同的動作
    """
    if client_data.role == "admin":
        print(f"Admin {client_data.userid} has full access.")
    elif client_data.role == "user":
        print(f"User {client_data.userid} has limited access.")
    else:
        print(f"Client {client_data.userid} has unknown role.")
