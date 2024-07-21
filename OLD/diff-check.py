import mysql.connector
from mysql.connector import Error

# データベース接続の設定
config_main = {
    'user': 'wp_user',
    'password': 'CDSL_2024@',
    'host': 'c0a21099-ja-0701.a910.tak-cslab.org',
    'database': 'wordpress'
}

config_sub = {
    'user': 'wp_user',
    'password': 'CDSL_2024@',
    'host': 'c0a21099-ja-0708.a910.tak-cslab.org',
    'database': 'wordpress'
}

try:
    # メインデータベースに接続
    connection_main = mysql.connector.connect(**config_main)
    # サブデータベースに接続
    connection_sub = mysql.connector.connect(**config_sub)
    
    if connection_main.is_connected() and connection_sub.is_connected():
        cursor_main = connection_main.cursor(dictionary=True)
        cursor_sub = connection_sub.cursor(dictionary=True)
        
        # メインデータベースからデータを取得
        cursor_main.execute("SELECT cleaned_uri, total_count, post_title FROM wp_nissy_kekka_new")
        main_data = cursor_main.fetchall()
        
        # サブデータベースからデータを取得
        cursor_sub.execute("SELECT cleaned_uri, total_count, post_title FROM wp_nissy_kekka_new")
        sub_data = cursor_sub.fetchall()
        
        # データを辞書に変換して比較
        main_dict = {row['cleaned_uri']: row for row in main_data}
        sub_dict = {row['cleaned_uri']: row for row in sub_data}
        
        # 差分を計算
        diffs = []
        all_keys = set(main_dict.keys()).union(set(sub_dict.keys()))
        for key in all_keys:
            main_row = main_dict.get(key)
            sub_row = sub_dict.get(key)
            if main_row != sub_row:
                diffs.append((main_row, sub_row))
        
        # 差分を表示
        for main_row, sub_row in diffs:
            print("Main:", main_row)
            print("Sub:", sub_row)
            print("---")
            
except Error as e:
    print(f"Error: {e}")
    
finally:
    # データベース接続を閉じる
    if connection_main.is_connected():
        cursor_main.close()
        connection_main.close()
        print("Main MySQL connection is closed")
        
    if connection_sub.is_connected():
        cursor_sub.close()
        connection_sub.close()
        print("Sub MySQL connection is closed")