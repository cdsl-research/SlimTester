import mysql.connector
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, urljoin, quote

# データベース接続情報
db_host = 'localhost'
db_user = 'wp_user'
db_pass = 'CDSL_2024@'
db_name = 'wordpress'
wp_url = 'http://c0a21099-ja-0701.a910.tak-cslab.org'

# 現在の日付を取得
current_date = datetime.now().strftime('%Y-%m-%d')

# ログファイルのオープン
success_log_path = f'/mnt/log/success-{current_date}.log'
fail_log_path = f'/mnt/log/fail-{current_date}.log'

success_log = open(success_log_path, 'w')
fail_log = open(fail_log_path, 'w')

# MySQL接続
db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    database=db_name
)

cursor = db.cursor()

# 公開されている記事の取得
cursor.execute("SELECT ID, post_title FROM wp_posts WHERE post_status='publish' AND post_type='post'")
posts = cursor.fetchall()

# 各記事のURLにアクセスして確認
for post_id, post_title in posts:
    post_url = f"{wp_url}/?p={post_id}"
    try:
        response = requests.get(post_url)
        if response.status_code == 200:
            success_log.write(f"[SUCCESS] {post_title} ({post_url})\n")
            print(f"[SUCCESS] {post_title} ({post_url})")
            
            # BeautifulSoupを使ってHTMLを解析
            soup = BeautifulSoup(response.content, 'html.parser')

            # コンテンツ内のURLリンク確認
            links = [a['href'] for a in soup.find_all('a', href=True)]
            for link in links:
                try:
                    # URLを正しくエンコードする
                    link = urljoin(post_url, link)
                    parsed_link = urlparse(link)
                    encoded_link = parsed_link._replace(path=quote(parsed_link.path)).geturl()
                    link_response = requests.get(encoded_link)
                    if link_response.status_code == 200:
                        success_log.write(f"  [LINK SUCCESS] {encoded_link}\n")
                        print(f"  [LINK SUCCESS] {encoded_link}")
                    else:
                        fail_log.write(f"  [LINK FAIL] {encoded_link}: HTTP {link_response.status_code}\n")
                        print(f"  [LINK FAIL] {encoded_link}: HTTP {link_response.status_code}")
                except requests.exceptions.RequestException as e:
                    fail_log.write(f"  [LINK ERROR] {encoded_link}: {e}\n")
                    print(f"  [LINK ERROR] {encoded_link}: {e}")
            
            # コンテンツ内の画像確認
            images = [img['src'] for img in soup.find_all('img', src=True)]
            for img in images:
                try:
                    img = urljoin(post_url, img)
                    parsed_img = urlparse(img)
                    encoded_img = parsed_img._replace(path=quote(parsed_img.path)).geturl()
                    img_response = requests.get(encoded_img)
                    if img_response.status_code == 200:
                        success_log.write(f"  [IMAGE SUCCESS] {encoded_img}\n")
                        print(f"  [IMAGE SUCCESS] {encoded_img}")
                    else:
                        fail_log.write(f"  [IMAGE FAIL] {encoded_img}: HTTP {img_response.status_code}\n")
                        print(f"  [IMAGE FAIL] {encoded_img}: HTTP {img_response.status_code}")
                except requests.exceptions.RequestException as e:
                    fail_log.write(f"  [IMAGE ERROR] {encoded_img}: {e}\n")
                    print(f"  [IMAGE ERROR] {encoded_img}: {e}")

        else:
            fail_log.write(f"[FAIL] {post_title} ({post_url}): HTTP {response.status_code}\n")
            print(f"[FAIL] {post_title} ({post_url}): HTTP {response.status_code}")
    except requests.exceptions.RequestException as e:
        fail_log.write(f"[ERROR] {post_title} ({post_url}): {e}\n")
        print(f"[ERROR] {post_title} ({post_url}): {e}")

# MySQL接続の終了
cursor.close()
db.close()

# ログファイルのクローズ
success_log.close()
fail_log.close()