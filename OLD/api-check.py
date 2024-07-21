import requests

# WordPress REST APIベースURL
base_url = "http://c0a21099-ja-0701.a910.tak-cslab.org/wp-json"  # あなたのサイトのURLに変更してください

# すべてのREST APIエンドポイントを取得
response = requests.get(base_url)

if response.status_code != 200:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)
else:
    try:
        api_endpoints = response.json()
        print("Available API Endpoints:")
        for key, value in api_endpoints.items():
            print(f"{key}: {value}")
    except requests.exceptions.JSONDecodeError as e:
        print("Failed to parse JSON response")
        print(e)