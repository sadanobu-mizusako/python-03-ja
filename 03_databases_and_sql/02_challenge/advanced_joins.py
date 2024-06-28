
# SQLとPython＋Chinookデータベース: 高度な結合

import sqlite3

# chinook.dbデータベースに接続
conn = sqlite3.connect('../data/chinook.db')
db = conn.cursor()

# 楽曲の詳細
def detailed_tracks(db):
    query = """
                select 
                    a.name as track_name, 
                    b.title as album_title, 
                    c.name as artist_name
                from tracks as a
                left join albums as b
                on a.albumid = b.albumid
                left join artists as c
                on b.artistid = c.artistid
"""  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    print(results[:10])
    return results

# 未購入の楽曲
def tracks_not_bought(db):
    query = """
                -- invoiceにないtrack_idを未購入とみなす
                with 
                    purchased_tbl as (
                        select
                            distinct (b.trackid) as trackid
                        from invoices as a
                        left join invoice_items as b
                        on a.invoiceid = b.invoiceid
                    )
                select
                    a.name
                from tracks as a
                left join purchased_tbl as b
                on a.trackid = b.trackid
                where b.trackid is NULL
"""  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    print(results[:10])
    return results

# ジャンルの統計情報
def genre_stats(db, genre_name):
    query = f"""
            select
                count(*) as number_of_tracks,
                avg(a.Milliseconds) as avg_track_length
            from tracks as a
            left join genres as b
            on a.genreid = b.genreid
            where b.name == "{genre_name}"
"""  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    results_dict = {"genre":genre_name}
    results_dict["number_of_tracks"] = results[0][0]
    results_dict["avg_track_length"] = results[0][1]
    print(results_dict)
    return results_dict

# ジャンル別のトップ5アーティスト
def top_five_artists_by_genre(db, genre_name):
    query = f"""
            select
                d.name as artist_name,
                count(*) as number_of_tracks
            from tracks as a
            left join genres as b
            on a.genreid = b.genreid
            left join albums as c
            on a.albumid = c.albumid
            left join artists as d
            on c.artistid = d.artistid
            where b.name == "{genre_name}"
            group by d.name
            order by number_of_tracks desc
            limit 5
"""  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    print(results)
    return results



# スクリプトの最後で必ずデータベース接続を閉じる
conn.close()
