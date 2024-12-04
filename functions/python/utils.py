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

role = ""