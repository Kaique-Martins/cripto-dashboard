import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_trends(df):
    df["day_index"] = np.arange(len(df))
    model = LinearRegression()
    model.fit(df[["day_index"]], df["current_price"])
    next_day = len(df)
    predicted_price = model.predict([[next_day]])
    return predicted_price[0]
