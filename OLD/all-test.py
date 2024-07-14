import requests
from requests.auth import HTTPBasicAuth
import logging
from datetime import datetime
import time
import re

# WordPressサイトのログイン情報
url_base = 'http://c0a21099-ja-0701.a910.tak-cslab.org'
api_url = f'{url_base}/wp-json/wp/v2'
username = 'test'
application_password = 'k67Y 8TaS wGs5 3f4c o5E2 ncYy'
auth = HTTPBasicAuth(username, application_password)

# 日付を取得
date_str = datetime.now().strftime("%Y-%m-%d")

# ログファイルの設定
log_file = f'/home/nissy/testcase/log/log-{date_str}.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

# キャッシュ無効化のヘッダー
headers = {
    'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0',
    'Pragma': 'no-cache'
}

# 実行時間を計測するデコレーター
def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info('Execution time for %s: %s seconds', func.__name__, elapsed_time)
        print(f'Execution time for {func.__name__}: {elapsed_time} seconds')
        return result
    return wrapper

# トップページが閲覧できるか
@log_time
def check_top_page():
    response = requests.get(url_base, headers=headers)
    if response.status_code == 200:
        logging.info('Top page is accessible.')
        print('Top page is accessible.')
    else:
        logging.error('Failed to access top page. Status Code: %s', response.status_code)
        print(f'Failed to access top page. Status Code: {response.status_code}')

# Publishになっている固定ページと記事がすべて表示できるか
@log_time
def check_published_pages_and_posts():
    def fetch_all_items(endpoint):
        items = []
        page = 1
        while True:
            response = requests.get(f'{api_url}/{endpoint}', params={'per_page': 100, 'page': page}, auth=auth, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                items.extend(data)
                page += 1
            else:
                logging.error('Failed to fetch %s. Status Code: %s', endpoint, response.status_code)
                print(f'Failed to fetch {endpoint}. Status Code: {response.status_code}')
                break
        return items

    pages = fetch_all_items('pages')
    posts = fetch_all_items('posts')
    
    logging.info('Total number of published pages: %s', len(pages))
    logging.info('Total number of published posts: %s', len(posts))
    print(f'Total number of published pages: {len(pages)}')
    print(f'Total number of published posts: {len(posts)}')
    
    for page in pages:
        if page['status'] == 'publish':
            response = requests.get(page['link'], headers=headers)
            if response.status_code == 200:
                logging.info('Published page "%s" is accessible.', page['title']['rendered'])
                print(f'Published page "{page["title"]["rendered"]}" is accessible.')
            else:
                logging.error('Failed to access published page "%s". Status Code: %s', page['title']['rendered'], response.status_code)
                print(f'Failed to access published page "{page["title"]["rendered"]}". Status Code: {response.status_code}')
    
    for post in posts:
        if post['status'] == 'publish':
            response = requests.get(post['link'], headers=headers)
            if response.status_code == 200:
                logging.info('Published post "%s" is accessible.', post['title']['rendered'])
                print(f'Published post "{post["title"]["rendered"]}" is accessible.')
            else:
                logging.error('Failed to access published post "%s". Status Code: %s', post['title']['rendered'], response.status_code)
                print(f'Failed to access published post "{post["title"]["rendered"]}". Status Code: {response.status_code}')

# 記事に紐づいている画像が表示されているか
@log_time
def check_images():
    posts = requests.get(f'{api_url}/posts', params={'per_page': 100}, auth=auth, headers=headers).json()
    for post in posts:
        if post['status'] == 'publish':
            content = post['content']['rendered']
            image_urls = set(re.findall(r'<img.*?src="(.*?)"', content))
            for image_url in image_urls:
                response = requests.get(image_url, headers=headers)
                if response.status_code == 200:
                    logging.info('Image "%s" is accessible.', image_url)
                    print(f'Image "{image_url}" is accessible.')
                else:
                    logging.error('Failed to access image "%s". Status Code: %s', image_url, response.status_code)
                    print(f'Failed to access image "{image_url}". Status Code: {response.status_code}')

# ログインページにアクセスできるか
@log_time
def check_login_page():
    response = requests.get(f'{url_base}/10gin_cds1', headers=headers)
    if response.status_code == 200:
        logging.info('Login page is accessible.')
        print('Login page is accessible.')
    else:
        logging.error('Failed to access login page. Status Code: %s', response.status_code)
        print(f'Failed to access login page. Status Code: {response.status_code}')

# 新しい記事が作成できるか
@log_time
def create_post(title, content):
    post_data = {
        'title': title,
        'content': content,
        'status': 'private'  # 記事のステータスをprivateに設定
    }
    response = requests.post(f'{api_url}/posts', json=post_data, auth=auth, headers=headers)
    if response.status_code == 201:
        logging.info('Post created successfully: %s', title)
        print(f'Post created successfully: {title}')
        return response.json()['id']
    else:
        logging.error('Failed to create post: %s', response.content)
        logging.error('Status Code: %s', response.status_code)
        print(f'Failed to create post: {response.content}')
        print(f'Status Code: {response.status_code}')
        return None

# 作成された記事が編集できるか
@log_time
def edit_post(post_id, new_content):
    post_data = {
        'content': new_content
    }
    response = requests.post(f'{api_url}/posts/{post_id}', json=post_data, auth=auth, headers=headers)
    if response.status_code == 200:
        logging.info('Post edited successfully: ID %s', post_id)
        print(f'Post edited successfully: ID {post_id}')
    else:
        logging.error('Failed to edit post: ID %s, %s', post_id, response.content)
        logging.error('Status Code: %s', response.status_code)
        print(f'Failed to edit post: ID {post_id}, {response.content}')
        print(f'Status Code: {response.status_code}')

# 作成した記事が削除できるか
@log_time
def delete_post(post_id):
    response = requests.delete(f'{api_url}/posts/{post_id}?force=true', auth=auth, headers=headers)
    if response.status_code == 200:
        logging.info('Post deleted successfully: ID %s', post_id)
        print(f'Post deleted successfully: ID {post_id}')
    else:
        logging.error('Failed to delete post: ID %s, %s', post_id, response.content)
        logging.error('Status Code: %s', response.status_code)
        print(f'Failed to delete post: ID {post_id}, {response.content}')
        print(f'Status Code: {response.status_code}')

if __name__ == "__main__":
    start_time = time.time()
    
    check_top_page()
    check_published_pages_and_posts()
    check_images()
    check_login_page()
    
    # 新しい記事の作成、編集、削除のテスト
    post_id = create_post('テスト記事', 'これはテスト記事です。')
    if post_id:
        edit_post(post_id, 'これは編集されたテスト記事です。追加文章を含みます。')
        delete_post(post_id)
    
    end_time = time.time()
    total_time = end_time - start_time
    logging.info('Total execution time: %s seconds', total_time)
    print(f'Total execution time: {total_time} seconds')
