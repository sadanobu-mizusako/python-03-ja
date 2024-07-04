# SQLとPython＋Northwindデータベース

import sqlite3

# northwind.dbデータベースに接続
conn = sqlite3.connect('../data/northwind.db')
db = conn.cursor()

# サプライヤーのリスト
def list_of_suppliers(db):
    query = "select suppliername from suppliers;"  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    results = [r[0] for r in results]
    return results

# 少量の注文
def count_small_orders(db):
    query = """
            select count(*)
            from(
                select orderid, sum(quantity) as quantity
                from orderdetails
                group by orderid
                having quantity < 5
            )
    """  # ここにSQLクエリを書いてください
    db.execute(query)
    result = db.fetchone()
    return result[0] if result else 0

# 最初の10商品
def first_ten_products(db):
    query = "select * from products limit 10;"  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    return results

# キーワードを含む商品
def products_with_keyword(db, keyword):
    query = f"""
            select * 
            from products as a
            left join suppliers as b
            on a.supplierid = b.supplierid
            where a.ProductName like "%{keyword}%";
            """  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    return results

# 商品数が多いトップ5のカテゴリー
def top_five_categories_by_product_count(db):
    query = """
            with top_5_tbl as (
                select categoryid, count(*) as productcnt
                from products
                group by categoryid
                order by productcnt desc
                limit 5
            )
            select * from top_5_tbl as a
            left join categories as b
            on a.categoryid = b.categoryid
    """  # ここにSQLクエリを書いてください
    db.execute(query)
    results = db.fetchall()
    return results

# 関数呼び出しの例 (提出する前にこれらをコメントアウトしてください)
# print("List of Suppliers:")
# print(list_of_suppliers(db))

# print("\Count Small Orders:")
# print(count_small_orders(db))

# print("\nFirst Ten Products:")
# print(first_ten_products(db))

# print("\nProducts with a Keyword 'Chai':")
# print(products_with_keyword(db, 'Chai'))

# print("\nTop 5 Categories by Product Count:")
# print(top_five_categories_by_product_count(db))

# スクリプトの最後で必ずデータベース接続を閉じる
conn.close()