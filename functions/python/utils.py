import numpy as np
import pandas as pd
import duckdb
import psycopg2
import matplotlib.pyplot as plt
from colorama import Cursor, init
import psycopg2
import warnings
import re
import sys
import time

# 初始化 colorama
init()

warnings.filterwarnings('ignore')

with open('db_password.txt', 'r') as file:
    db_port = file.readline().strip()
    db_password = file.readline().strip()
    db_name = file.readline().strip()

psql_conn = psycopg2.connect(f"port = '{db_port}' dbname = '{db_name}' user = 'postgres' host = 'localhost' password = '{db_password}'")


table_names = ['item', 'lost_item', 'found_item', 'users', 'locations', 'locates', 'stores', 'returns_or_claims', 'category', 'belongs', 'posts', 'members', 'comments', 'message', 'feedback', 'notifies', 'reward']
cursor = psql_conn.cursor()

# con = duckdb.connect()

# for table_name in table_names:
#     query_str = "SELECT * FROM " + table_name
#     df = pd.read_sql_query(query_str, psql_conn)
#     con.register(table_name, df)

# def query(query, param):
#     result = con.execute(query, (param)).fetchall()
#     column_names = [desc[0] for desc in con.description]
#     return column_names, result

def query(query, param=None):
    cursor.execute(query, param)
    if query.strip().lower().startswith("select") or query.strip().lower().startswith("with"):
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        return column_names, result
    else:
        psql_conn.commit()
        return None

def print_bold(str):
    print(f"\033[1m{str}\033[0m")

def delete_terminal_content(sleep_time, lines):
    time.sleep(sleep_time)
    sys.stdout.write(Cursor.UP(lines)) 
    sys.stdout.write("\033[1G\033[J")   
    sys.stdout.flush()

userid = ""
role = ""
username = ""

category_names = [
    "文具", "衣物", "配件", "電子產品", "交通工具", "居家用品", "個人護理", "運動用品", "收藏品", "其他"
]

locations = [
    # campus
    "台大正門", "椰林大道", "台大校史館", "總圖書館", "電機一館", "電機二館", "管理學院一館", "管理學院二館", 
    "教研館", "計算機及資訊網路中心", "思亮館", "新月台", "理學院", "普通教學館", "綜合體育館", "小福樓", "台大農場", 
    "學生活動中心", "化學系館", "舟山路前段", "舟山路後段", "學新館", "第二學生活動中心", "鹿鳴堂", "游泳池", 
    "博雅教學館", "國青宿舍", "醉月湖", "德田館", "女九舍", "駐警隊",
    # nearby
    "公館夜市", "溫州街", "羅斯福路四段", "台電大樓捷運站", "科技大樓捷運站", "和平東路", "基隆路", 
    "公館捷運站一號出口", "公館捷運站二號出口", "公館捷運站三號出口", "公館捷運站四號出口", "新生南路", 
    "師大夜市", "公館水岸公園", "水源市場", "公館捷運站"
]

def list_category():
    for i, name in enumerate(category_names, 1):
        print(f"{i:>2}: {name:<{10 - len(name)}}", end="\n" if i % 3 == 0 else "")
    print("")

def list_location():
    for i, name in enumerate(locations, 1):
        print(f"{i:>2}: {name:<{22 - len(name)}}", end="\n" if i % 3 == 0 else "")
    print("")

page = 1
def print_page(page_num):
    print("U: 上一頁   D: 下一頁")
    command = input("請輸入U或D：")
    if command.upper() == "U":
        if page <= 1:
            print("已是第一頁！")
            delete_terminal_content(1.5,2)
        else:
            page -= 1
    elif command.upper() == "D":
        if page >= page_num:
            print("已是最後一頁！")
            delete_terminal_content(1.5,2)
        else:
            page += 1
    else:
        print("輸入錯誤！請重新再試！")
        delete_terminal_content(1.5,2)