import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# ---------------- LOAD DATA ----------------
def load_data():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql_query("SELECT * FROM sessions", conn)
    conn.close()
    return df

# ---------------- FEATURE ENGINEERING ----------------
def prepare_data(df):
    df["session_number"] = np.arange(len(df))
    return df

# ---------------- TRAIN MODEL ----------------
def train_model():
    df = load_data()

    if len(df) < 5:
        return None  # not enough data

    df = prepare_data(df)

    X = df[["session_number"]]
    y = df["duration"]

    model = LinearRegression()
    model.fit(X, y)

    return model

# ---------------- PREDICT NEXT SESSION ----------------
def predict_next_session():
    model = train_model()

    if model is None:
        return "Not enough data yet for ML prediction"

    next_session = np.array([[100]])  # future session index
    prediction = model.predict(next_session)[0]

    return round(prediction, 2)


# ---------------- TEST ----------------
if __name__ == "__main__":
    print("Next session prediction:", predict_next_session())