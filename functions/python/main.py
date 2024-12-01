import numpy as np
import pandas as pd
import duckdb
import psycopg2
import matplotlib.pyplot as plt
import re
from colorama import Cursor, init
import sys
import time
import psycopg2

import sign

# 初始化 colorama
init()

with open('db_password.txt', 'r') as file:
    db_password = file.read().strip()

psql_conn = psycopg2.connect("port = '5433' dbname = 'OnlineLearning2024' user = 'postgres' host = 'localhost' password = " + db_password)

table_names = ['Subscriptions', 'StateChanges', 'UserMissions', 'Answers']
con = duckdb.connect()

for table_name in table_names:
    query_str = "SELECT * FROM " + table_name
    df = pd.read_sql_query(query_str, psql_conn)
    con.register(table_name, df)

psql_conn.close()

def query(query, param):
    result = con.execute(query, param).fetchall()
    column_names = [desc[0] for desc in con.description]
    return column_names, result