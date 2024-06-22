# 必要なライブラリをインポートする
import pandas as pd
from sklearn import datasets
pd.set_option('display.max_columns', 50)

# アイリスのデータセットを読み込み、DataFrameに変換する
iris = datasets.load_iris()
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)

# 品種の列を追加し、0～2の番号を記入する (各番号が異なる品種を表す)
iris_df['species'] = iris.target

# 1. データの読み込みと概要
print("1. データの読み込みと概要")
print(iris_df.head(5))

# 2. データのクリーニングと検証
print("2. データのクリーニングと検証")
print("欠損値の個数")
print(iris_df.isna().sum())

print("データ型")
print(iris_df.dtypes)

# 3. 基本的な分析と基本統計量
print("3. 基本的な分析と基本統計量")
stats_df = iris_df.describe().loc[["mean", "50%", "std"], ].drop("species", axis=1).T.\
        rename(columns={"mean": "平均値", "50%": "中央値", "std": "標準偏差"})
print(stats_df)
stats_df.to_csv("./stats.csv")

# 4. 特徴量エンジニアリング
print("4. 特徴量エンジニアリング")
iris_df["sepal_area"] = iris_df["sepal length (cm)"]*iris_df["sepal width (cm)"]
iris_df["petal_area"] = iris_df["petal length (cm)"]*iris_df["petal width (cm)"]
print("特徴量追加後のiris_df")
print(iris_df.head(5))

stats_df_add = iris_df.describe().loc[["mean", "50%", "std"], ["sepal_area", "petal_area"]].T.\
        rename(columns={"mean": "平均値", "50%": "中央値", "std": "標準偏差"})
stats_df = pd.concat([stats_df, stats_df_add], axis=0)
print("特徴量追加後のstats_df")
print(stats_df)

# 5. データのフィルタリング
def filter(df, col, val, condition):
    """
    ある列（col）とvalを比較してフィルターをかけたデータフレームを返す関数
    引数：
        df: pandas.DataFrame: ターゲットのデータフレーム
        col: str: フィルタ対象の列名
        val: float or int: 閾値
        condition: str: 条件
            > : 閾値より大きい行だけを抽出
            >= : 閾値以上の行だけを抽出
            == : 閾値と等しい行だけを抽出
            <= : 閾値以下の行だけを抽出
            < : 閾値より小さい行だけを抽出
    """
    if condition==">":
        return df[df[col]>val]
    elif condition==">=":
        return df[df[col]>=val]
    elif condition=="==":
        return df[df[col]==val]
    elif condition=="<=":
        return df[df[col]<=val]
    elif condition=="<":
        return df[df[col]<val]
    else:
        raise Exception("invalid option. condition must be chosen from '>', '>=', '==', '<=' or '<'.")

df_filtered = filter(iris_df, "sepal_area", 17, ">")
print("sepal_area > 17でフィルタ")
print(df_filtered.head(5))

# 6. データのエクスポート
iris_df.to_csv("./iris_df.csv")