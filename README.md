# Spotify Genre Classification - MLOps Pipeline

Automated MLOps pipeline for Spotify music genre classification. The pipeline consists of three stages (data engineering, model engineering, deployment) orchestrated by Apache Airflow and scheduled to run every 10 minutes <br>

## Repository 
```text
.
├── code/
│    ├── config.py # Common constants (paths, features, hyperparameters)
│    ├── datasets/preprocess.py # Stage 1: loading, cleaning, splitting
│    ├── models/train.py # Stage 2: feature engineering, training, MLflow, saving
│    └── deployment/
│        ├── docker-compose.yaml # API + Streamlit
│        ├── api/ # FastAPI service
│        │ ├── main.py
│        │ └── Dockerfile
│        └── app/ # Streamlit application
│            ├── main.py
│            └── Dockerfile
├── data/
│    ├── raw/dataset.csv # Raw dataset (not in git)
│    └── processed/ # train.csv / test.csv (created automatically)
├── models/ # spotify_model.pkl (created automatically)
├── airflow/
│    ├── Dockerfile # Custom Airflow image (includes catboost, mlflow, docker CLI)
│    ├── docker-compose.yaml # Postgres + scheduler + webserver
│    ├── requirements.txt
│    └── dags/pipeline_dag.py # DAG spotify_genre_pipeline
└── requirements.txt # General dependencies
```
<br>

## Dataset

**Spotify Tracks Dataset** (114,000 tracks, 125 genres).

Download from: https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset/tree/main

After downloading, place the file at:


Features used: `danceability`, `energy`, `valence`, `tempo`, `acousticness`, `loudness`, `speechiness`, `instrumentalness`.

Target variable: `track_genre` (5 classes: rock, classical, hip-hop, k-pop, jazz).

## Requirements

- Docker Desktop 24+ (or Docker Engine + Docker Compose v2)
- 6+ GB of free RAM
- 4+ GB of free disk space
- Windows: Docker Desktop must be running, and ports 8081/8000/8502 must be free (see Troubleshooting)

## Setup

### 1. Clone the repository

```bash
git https://github.com/TereshchenkoMisha/MachineLearning_assignment1.git
cd ./MachineLearning_assignment1
```
### 2. Then you should prepare the environment
download the dataset and add it to the data/raw/dataset.csv
Add the airwlof/.env liens: AIRFLOW_UID = 50000
### 3. Then start Airflow
```bash
cd ./airflow
docker compose up -d --build
```
The first run can be executed for a long time because the images and Postgres migrations are preparing

### 4. Open Airflow UI
URL: http://localhost:8081
Login: airflow
Password: airflow

When the first run finishes the app and api will be built

### 5. Check the app
FastAPI: http://localhost:8000/docs
Streamlit UI: http://localhost:8502

In Streamlit you can drag the sliders and push button "Predict" to get prediction for the genre

# MlFlow results
You can use this commands to see the charts and metrics logged by MLFlow
```bash
pip install mlflow
mlflow ui --backend-store-uri ./mlruns
```
