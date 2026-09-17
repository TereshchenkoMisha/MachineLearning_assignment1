import os

FEATURES = ["danceability", "energy", "valence", "tempo", "acousticness", "loudness", "speechiness", "instrumentalness"]
TARGET = "track_genre"

GRID = {'learning_rate': [0.01, 0.03, 0.05, 0.1, 0.15, 0.2],
        'depth': [i for i in range(2, 10, 2)],
        'l2_leaf_reg': [1, 3, 5]
        }

RAW_DATA_PATH = "data/raw/dataset.csv"
TRAIN_DATA_PATH = "data/processed/train.csv"
TEST_DATA_PATH = "data/processed/test.csv"

MODEL_OUTPUT_DIR = "models"
MODEL_PATH = os.path.join(MODEL_OUTPUT_DIR, "spotify_model.pkl")