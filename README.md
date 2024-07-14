# SlimTester

<p>このプログラムは, WordPressのテスト範囲を設定する際の基礎実験として調査したブログ全体の固定ページや記事の確認を行い, 確認にかかった時間を計測するものです.</p>

## 使い方

### テスト範囲を絞らない際のテスト実行
<p>file: check-all.py</p>
<p>WordPressのプラグインである, '[WP REST API](https://ja.wp-api.org/)'が導入されており, アプリケーションパスワードを生成済みの状態で実行できます.</p>


実行方法↓

```bash
# Pythonの仮想環境を読み込む.
source .venv/bin/activate
python3 check-all.py
```
<p>実行ログは, '/home/nissy/testcase/log/alllog-{date_str}.log'に現状書き込まれるように設定しています. 適宜実行する際変更してください. </p>

<p>トップページ, 固定ページ, 投稿記事のうち公開されているものをWP REST API経由で確認を行います. </p>


### 確認項目
- WordPressのブログコンテンツの確認
    - WordPressのトップページが閲覧できるか
    - 投稿内容の確認ができるか
    - 画像が表示できるか
- WordPressのブログダッシュボードの確認
    - 新しい記事が作成できるか
    - 投稿済みの記事が編集できるか
    - 投稿済みの記事が削除できるか

<p> ※ ブログのダッシュボードの確認の為, ログイン用のユーザーとログイン生成済みのアプリケーションパスワードとプログラム内に指定する必要があります. </p>

<p> 結果は, ターミナルとログファイルにそれぞれ出力されます.</p>
<p> 各項目の個数, 実行時間, Totalのプログラム実行時間が表示されます. </p>

### 結果の一部:
```bash
2024-07-14 13:09:25,592 Total number of published pages: 12
2024-07-14 13:09:25,641 Published page "Dojoの活動成果" is accessible.
2024-07-14 13:09:28,043 Execution time for check_published_pages: 2.5981905460357666 seconds
...
2024-07-14 13:10:21,723 Total execution time: 56.3378381729126 seconds

```

