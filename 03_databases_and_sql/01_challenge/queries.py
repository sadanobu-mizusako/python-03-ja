
# SQLとPython＋Chinookデータベース

import sqlite3

# chinook.dbデータベースに接続
conn = sqlite3.connect('../data/chinook.db')
db = conn.cursor()

# アーティストの数
def number_of_artists(db):
    query = "select count(*) from artists"  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    results = results[0][0]
    print(results)
    return results

# アーティストのリスト
def list_of_artists(db):
    query = "select Name from artists order by Name asc"  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    results = [r[0] for r in results]
    print(results)
    return results


# 「愛」をテーマにしたアルバムのリスト
def albums_about_love(db):
    query = "select Title from albums where Title LIKE '%love%' order by Title asc"  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    results = [r[0] for r in results]
    print(results)
    return results

# 指定された再生時間よりも長い楽曲数
def tracks_longer_than(db, duration):
    query = f"select count(*) from tracks where Milliseconds > {duration}"  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    results = results[0][0]
    return results

# 最も楽曲数が多いジャンルのリスト
def genres_with_most_tracks(db):
    query = """
    select 
        b.name as genre, a.count as count
    from 
    (
        select GenreId, count(*) as count
        from tracks
        group by GenreId
    ) as a
    left join genres as b
    on a.GenreId = b.GenreId
    order by a.count desc
    """  # ここにSQLクエリを書いてください

    db.execute(query)
    results = db.fetchall()
    results = [[r[0], r[1]] for r in results]
    print(results)
    return results

# スクリプトの最後で必ずデータベース接続を閉じる
conn.close()