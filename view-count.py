import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# データベースへの接続情報
db_user = 'wp_user'
db_password = 'CDSL_2024@'
db_host = 'c0a21099-ja-0701'
db_name = 'wordpress'

# データベースへの接続
try:
    cnx = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_name)
    print("Connected to the database successfully!")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    exit(1)

# 公開されている記事を取得
query_posts = """
    SELECT ID, post_name
    FROM wp_posts
    WHERE post_status = 'publish'
"""
posts_df = pd.read_sql(query_posts, cnx)

# 閲覧数を集計
query_stats = """
    SELECT uri, SUM(count) as total_count
    FROM wp_statistics_pages
    GROUP BY uri
"""
stats_df = pd.read_sql(query_stats, cnx)

# post_nameとuriを一致させる
merged_df = pd.merge(posts_df, stats_df, left_on='post_name', right_on='uri', how='left')

# NaN値をNoneに変換し、NaN値を持つ行を削除
merged_df = merged_df.where(pd.notnull(merged_df), None)
merged_df = merged_df.dropna(subset=['total_count'])

# 結果を表示
print(merged_df)

# 結果を新しいテーブルに保存するための関数
def save_to_db(dataframe, table_name, connection):
    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    create_table_query = f"""
    CREATE TABLE {table_name} (
        ID INT,
        post_name VARCHAR(255),
        uri VARCHAR(255),
        total_count INT
    )
    """
    cursor.execute(create_table_query)

    for _, row in dataframe.iterrows():
        insert_row_query = f"""
        INSERT INTO {table_name} (ID, post_name, uri, total_count)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_row_query, tuple(row))
    
    connection.commit()
    cursor.close()

# 結果を新しいテーブルに保存
save_to_db(merged_df, 'post_view_counts', cnx)

print("Data saved to post_view_counts table successfully!")

# 接続を閉じる
cnx.close()