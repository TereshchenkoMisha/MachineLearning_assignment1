import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
from sklearn.model_selection import train_test_split
from config import FEATURES, TARGET, RAW_DATA_PATH, TRAIN_DATA_PATH, TEST_DATA_PATH

def preprocess():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Fail {RAW_DATA_PATH} isn't found.")

    df = pd.read_csv(RAW_DATA_PATH)
    
    selected_cols = FEATURES + [TARGET]
    df = df[selected_cols].dropna()

    top_genres = ["rock", "classical", "hip-hop", "k-pop", 'jazz']
    df = df[df[TARGET].isin(top_genres)]

    df = df[(df["tempo"] >= 50) & (df["tempo"] <= 220)]

    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df[TARGET])

    os.makedirs("data/processed", exist_ok=True)
    train_df.to_csv(TRAIN_DATA_PATH, index=False)
    test_df.to_csv(TEST_DATA_PATH, index=False)
    print("Preprocessing finished. Train and test saved to data/processed/")

if __name__ == "__main__":
    preprocess()