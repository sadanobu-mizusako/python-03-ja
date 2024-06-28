
# SQLとPython＋Chinookデータベース: 楽曲の再生時間に応じたバケット分類

import sqlite3

# chinook.dbデータベースに接続
conn = sqlite3.connect('../data/chinook.db')
db = conn.cursor()

# 楽曲の再生時間に応じたバケット
def track_length_buckets(db):
    query = """
                select
                    cast(Milliseconds/60000+1 as integer) as max_duration_in_minutes,
                    count(*) as track_count
                from tracks
                group by 1
"""
    db.execute(query)
    results = db.fetchall()
    print(results)
    return results

# スクリプトの最後で必ずデータベース接続を閉じる
conn.close()
