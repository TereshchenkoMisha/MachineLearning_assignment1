import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"

import joblib
import pandas as pd
import mlflow
import numpy as np
import mlflow.catboost
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import RandomizedSearchCV

from config import TRAIN_DATA_PATH, TEST_DATA_PATH, MODEL_PATH, MODEL_OUTPUT_DIR
from config import TARGET, FEATURES, GRID

np.random.seed(42)

def train():
    if not os.path.exists(TRAIN_DATA_PATH) or not os.path.exists(TEST_DATA_PATH):
        raise FileNotFoundError("There is no data! Firstly execute the preprocessing")

    train_df = pd.read_csv(TRAIN_DATA_PATH)
    test_df = pd.read_csv(TEST_DATA_PATH)

    X_train, y_train = train_df[FEATURES], train_df[TARGET]
    X_test, y_test = test_df[FEATURES], test_df[TARGET]

    # Adding ML Flow tracking
    mlflow.set_experiment("Spotify_Genre_Classification")

    with mlflow.start_run():
        model = CatBoostClassifier(iterations=500, learning_rate=0.1, depth=6, random_state=42, logging_level='Silent', thread_count=-1)
        search = RandomizedSearchCV(estimator=model, param_distributions=GRID, n_iter=17, scoring='f1_weighted', n_jobs=2, cv=3, random_state=42)
        search.fit(X_train, y_train)
        print(search.best_estimator_, search.best_params_, sep='\n')

        best_model = search.best_estimator_

        mlflow.log_params(search.best_params_)

        # Evaluation of model
        predictions = best_model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        f1 = f1_score(y_test, predictions, average="weighted")

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)

        print(f"Model was learned succesfully! Accuracy: {acc:.4f}, F1-score: {f1:.4f}")

        # Model saving
        os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)
        joblib.dump(best_model, MODEL_PATH)
        mlflow.catboost.log_model(best_model, artifact_path="catboost")
        
        print(f"Model is saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()