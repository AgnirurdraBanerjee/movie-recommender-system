import pickle
import streamlit as st
import requests
import pandas as pd

# ----------------------------------------
# Safe function to fetch movie poster
# ----------------------------------------
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"  # fallback
    except Exception as e:
        print(f"[ERROR] Poster fetch failed for movie_id={movie_id} -> {e}")
        return "https://via.placeholder.com/300x450?text=Error"

# ----------------------------------------
# Recommend similar movies
# ----------------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ----------------------------------------
# Load model and data
# ----------------------------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# ----------------------------------------
# Streamlit App Layout
# ----------------------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "🔍 Type or select a movie from the dropdown:",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx], width=200)

