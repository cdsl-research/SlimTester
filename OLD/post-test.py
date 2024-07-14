import requests
from requests.auth import HTTPBasicAuth
import logging
from datetime import datetime

# WordPressサイトのログイン情報
url = 'http://c0a21099-ja-0701.a910.tak-cslab.org/wp-json/wp/v2/posts'  # 実際のURLに変更
username = 'test'  # 実際のユーザー名に変更
password = 'k67Y 8TaS wGs5 3f4c o5E2 ncYy'  # 実際のパスワードに変更

auth = HTTPBasicAuth(username, password)

# 日付を取得
date_str = datetime.now().strftime("%Y-%m-%d")

# ログファイルの設定
log_file = f'/home/nissy/testcase/log/log-{date_str}.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

# 記事の投稿
def create_post(title, content):
    post_data = {
        'title': title,
        'content': content,
        'status': 'publish'
    }
    response = requests.post(url, json=post_data, auth=auth)  # URLを修正
    if response.status_code == 201:
        logging.info('Post created successfully: %s', title)
        return response.json()['id']
    else:
        logging.error('Failed to create post: %s', response.content)
        logging.error('Status Code: %s', response.status_code)
        logging.error('Response Headers: %s', response.headers)
        return None

# 記事の編集
def edit_post(post_id, new_content):
    post_data = {
        'content': new_content
    }
    response = requests.post(f'{url}/{post_id}', json=post_data, auth=auth)  # URLを修正
    if response.status_code == 200:
        logging.info('Post edited successfully: ID %s', post_id)
    else:
        logging.error('Failed to edit post: ID %s, %s', post_id, response.content)
        logging.error('Status Code: %s', response.status_code)
        logging.error('Response Headers: %s', response.headers)

# 記事の削除
def delete_post(post_id):
    response = requests.delete(f'{url}/{post_id}?force=true', auth=auth)  # URLを修正
    if response.status_code == 200:
        logging.info('Post deleted successfully: ID %s', post_id)
    else:
        logging.error('Failed to delete post: ID %s, %s', post_id, response.content)
        logging.error('Status Code: %s', response.status_code)
        logging.error('Response Headers: %s', response.headers)

if __name__ == "__main__":
    # 記事の作成
    post_id = create_post('テスト記事', 'これはテスト記事です。')

    if post_id:
        # 記事の編集
        edit_post(post_id, 'これは編集されたテスト記事です。追加文章を含みます。')

        # 記事の削除
        # delete_post(post_id)
