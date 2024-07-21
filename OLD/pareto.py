import mysql.connector

# データベース接続の設定
config = {
    'user': 'wp_user',
    'password': 'CDSL_2024@',
    'host': 'c0a21099-ja-0701',
    'database': 'wordpress',
}

# データベースに接続
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# 上位20%の閲覧数が全体の80%を占めているかを確認するクエリ
query_top_20_percent_views_ratio = """
WITH ranked_articles AS (
    SELECT
        cleaned_uri,
        total_count,
        post_title,
        SUM(total_count) OVER (ORDER BY total_count DESC) AS cumulative_count,
        SUM(total_count) OVER () AS total_views,
        ROW_NUMBER() OVER (ORDER BY total_count DESC) AS row_num,
        COUNT(*) OVER () AS total_articles
    FROM
        wp_nissy_kekka_new
),
percentiles AS (
    SELECT
        cleaned_uri,
        total_count,
        post_title,
        cumulative_count,
        total_views,
        row_num,
        total_articles,
        (cumulative_count * 1.0 / total_views) AS cumulative_percent,
        (row_num * 1.0 / total_articles) AS article_percent
    FROM
        ranked_articles
),
top_20_percent AS (
    SELECT
        cleaned_uri,
        total_count,
        post_title,
        cumulative_percent,
        article_percent
    FROM
        percentiles
    WHERE
        article_percent <= 0.2
),
total_views AS (
    SELECT SUM(total_count) AS total_views
    FROM wp_nissy_kekka_new
)
SELECT
    (SUM(top_20_percent.total_count) * 1.0 / total_views.total_views) AS top_20_percent_views_ratio
FROM
    top_20_percent,
    total_views;
"""

# クエリを実行して結果を取得
try:
    cursor.execute(query_top_20_percent_views_ratio)
    top_20_percent_views_ratio = cursor.fetchone()[0]
    print(f"Top 20% Views Ratio: {top_20_percent_views_ratio:.2f}")

    if top_20_percent_views_ratio >= 0.8:
        print("上位20%の記事が全体の80%以上の閲覧数を占めています。")
    else:
        print("上位20%の記事が全体の80%未満の閲覧数しか占めていません。")

finally:
    cursor.close()
    conn.close()