import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_posters(movie_id):
    api_key = "4ba6713d26e8bd3fd0ec92017812a475"  # Replace with your API key
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
        if response.status_code == 200:
            data = response.json()
            return "https://image.tmdb.org/t/p/w500" + data.get('poster_path', "")
        else:
            return ""
    except Exception as e:
        return ""

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Ensure 'movie_id' exists
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('C:/Users/pooja/OneDrive/Desktop/django/my_venv/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('C:/Users/pooja/OneDrive/Desktop/django/my_venv/similarity.pkl', 'rb'))

st.title('Movie Recommendation System')
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)  # Create columns for displaying movies
    for i in range(len(names)):
        with cols[i % 5]:  # Spread across five columns
            st.image(posters[i], caption=names[i], use_container_width=True)  # Combine title and poster
