import sqlite3
import pandas as pd
import datetime

# SQLiteデータベースに接続する
conn = sqlite3.connect('../data/northwind.db')

def emplployee_age_analysis():
    print("emplployee_age_analysis")
    df = pd.read_sql_query("SELECT * FROM Employees;", conn)
    df["Age"] = (pd.to_datetime(datetime.date.today()).year - pd.to_datetime(df.BirthDate).dt.year)
    print(df.Age.mean())
    print(df.Age.median())
    print(df.Age.mode())
    print(df.Age.std())
    print()

emplployee_age_analysis()

def customer_analysis():
    print("customer_analysis")
    print()
    df = pd.read_sql_query("SELECT * FROM Customers;", conn)
    print(df.groupby("Country").CustomerID.count())
    # print("max", df.groupby("Country", as_index=False)["CustomerID"].count().sort_values(by="CustomerID").iloc[-1])
    # print("min", df.groupby("Country", as_index=False)["CustomerID"].count().sort_values(by="CustomerID").iloc[0])
    # print("max", df.groupby("Country")["CustomerID"].count().idxmax())
    # print("min", df.groupby("Country")["CustomerID"].count().idxmin())
    perCountry = df.groupby("Country")["CustomerID"].count()
    print(perCountry[perCountry==perCountry.max()])
    print(perCountry[perCountry==perCountry.min()])
    print()

customer_analysis()

def order_analysis():
    print("order_analysis")
    df = pd.read_sql_query("SELECT * FROM Orders;", conn)
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    df.sort_values(by="OrderDate", inplace=True)
    df["diffence_date"] = df["OrderDate"].diff().dt.days
    print(df["diffence_date"].mean())
    print(df["diffence_date"].describe())
    print()

order_analysis()

def supplier_price_analysis():
    print("supplier_price_analysis")
    df = pd.read_sql_query("""
                           SELECT * 
                           FROM Products as a
                           left join Suppliers as b
                           on a.SupplierID=b.SupplierID;""", conn) 
    print(df.groupby("SupplierName").Price.mean())
    print()

supplier_price_analysis()

def order_date_analysis():
    print("order_date_analysis")
    df = pd.read_sql_query("""
                           SELECT * 
                           FROM Orders as a
                           left join OrderDetails as b
                           on a.OrderID=b.OrderID;""", conn) 
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    df["year"] = df["OrderDate"].dt.year
    df["month"] = df["OrderDate"].dt.month
    print(df.groupby(["year","month"]).Quantity.sum())
    print()

order_date_analysis()