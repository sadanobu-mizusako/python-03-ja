# ここにコードを書いてください
import pandas as pd
from sklearn.datasets import load_wine

wine_data = load_wine()

df = pd.DataFrame(
    columns=wine_data.feature_names,
    data=wine_data.data
)

df["class"] = wine_data.target

# カスタムインデックスでソートする
print("カスタムインデックスでソートする")
print(df.set_index("alcohol").sort_index().head(5))

# クラスごとの平均をとる
print("クラスごとの平均をとる")
print(df.groupby("class").mean())

# アルコールが平均よりも高いものだけをフィルタして抽出する
print("アルコールが平均よりも高いものだけをフィルタして抽出する")
print(df[df.alcohol>df.alcohol.mean()].head(5))

# アルコール度数とポリフェノールの比率を列として追加する
print("アルコール度数とポリフェノールの比率を列として追加する")
df["ash_alcohol_ratio"] = df.ash/df.alcohol
print(df["ash_alcohol_ratio"].head(5))
