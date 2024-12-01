import numpy as np
import pandas as pd
import duckdb
import psycopg2
import matplotlib.pyplot as plt

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

def query(query):
    result = con.execute(query).fetchall()
    column_names = [desc[0] for desc in con.description]
    return column_names, result

query_str = '''
SELECT AnswerID, UserID, QuestionID, MissionID, 
	IsCorrect, CostTime, CreatedAT, EndedAt
FROM answers
LEFT JOIN 
(
	SELECT endedat, subscriberid
	FROM subscriptions su
) ON userid=subscriberid
WHERE createdat>=DATE'2021-5-1' and endedat<createdat
'''
columns, data = query(query_str)

for i in range(5):
    print(f"{data[i]}")

query_str = '''
SELECT UserID, Avg(CostTime) mean_CostTime, Avg(IsCorrect) mean_CorrectRate
FROM
(
	SELECT AnswerID, UserID, QuestionID, MissionID, 
		IsCorrect, CostTime, CreatedAT, EndedAt
	FROM answers
	LEFT JOIN 
	(
		SELECT endedat, subscriberid
		FROM subscriptions su
	) ON userid=subscriberid
	WHERE createdat>=DATE'2021-5-1' and endedat<createdat
)
GROUP BY UserID
'''
columns, data = query(query_str)

df = pd.DataFrame(data, columns=columns)
filtered_df = df[df['mean_CostTime'] <= 50]
median_CostTime = filtered_df['mean_CostTime'].median()
median_CorrectRate = filtered_df['mean_CorrectRate'].median()

plt.figure(figsize=(10, 6))
plt.scatter(filtered_df['mean_CostTime'], filtered_df['mean_CorrectRate'], color='green', alpha=0.35)
plt.axvline(x=median_CostTime, color='orange', linestyle='--', label=f'Median Cost Time: {median_CostTime:.2f}s')
plt.axhline(y=median_CorrectRate, color='blue', linestyle='--', label=f'Median Correct Rate: {median_CorrectRate:.2%}')

plt.title('Scatter Plot of Avg Cost Time vs. Correct Rate')
plt.xlabel('Average Cost Time (seconds)')
plt.ylabel('Correct Rate')
plt.legend()
plt.show()