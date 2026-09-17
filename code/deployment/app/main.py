import streamlit as st
import requests

st.title("Spotify Genre Predictor")
st.write("Настройте параметры трека для определения его жанра:")

danceability = st.slider("Danceability (Танцевальность)", 0.0, 1.0, 0.5)
energy = st.slider("Energy (Энергичность)", 0.0, 1.0, 0.5)
valence = st.slider("Valence (Позитивность)", 0.0, 1.0, 0.5)
tempo = st.slider("Tempo (Темп, BPM)", 50.0, 220.0, 120.0)
acousticness = st.slider("Acousticness (Акустичность)", 0.0, 1.0, 0.5)
loudness = st.slider("Loundness", -60.0, 0.0, -10.0)
speechiness = st.slider("Speechiness", 0.0, 1.0, 0.1)
instrumentalness = st.slider("Instrumentalness", 0.0, 1.0, 0.0)

if st.button("Предсказать жанр"):
    payload = {
        "danceability": danceability,
        "energy": energy,
        "valence": valence,
        "tempo": tempo,
        "acousticness": acousticness,
        "loudness": loudness,
        "speechiness": speechiness,
        "instrumentalness": instrumentalness
    }
    
    try:
        response = requests.post("http://api:8000/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Предсказанный жанр: **{result['prediction']}**")
        else:
            st.error(f"Ошибка API: {response.json().get('detail')}")
    except Exception as e:
        st.error(f"Не удалось связаться с API: {e}")