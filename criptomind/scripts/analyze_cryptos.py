import pandas as pd

def analyze_data(df):
    print("\n📊 Estatísticas básicas:")
    print(df.describe())

    top = df.sort_values(by="price_change_percentage_24h", ascending=False).head(3)
    print("\n🚀 Top 3 Criptos do Dia:")
    print(top[["name", "price_change_percentage_24h"]])
