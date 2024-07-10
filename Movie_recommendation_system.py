import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=46ba99765bd9c8730449453dd57eb929&language=en-US')
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(poster_url)
    
    return recommended_movies, recommended_movies_posters


# Load pickle files directly from URLs
movies_url = 'https://drive.google.com/uc?id=11KDraKlbKyd72m6qA4a1wlcgX8mEZWta'
similarity_url = 'https://drive.google.com/uc?id=1iSpaZ9E4_gcr28Bgq2cLaoYVcu6leMXc'

# Fetching movies_dict
response = requests.get(movies_url)
if response.status_code == 200:
    movies_dict = pickle.loads(response.content)
    movies = pd.DataFrame(movies_dict)
else:
    st.write("Failed to fetch movie data.")

# Fetching similarity
response = requests.get(similarity_url)
if response.status_code == 200:
    similarity = pickle.loads(response.content)
else:
    st.write("Failed to fetch similarity data.")

# Streamlit app
st.title('Movie Recommender System')
selected_movie_name = st.selectbox('What movie do you want to search?', movies['title'].values)

if st.button("RECOMMEND"):
    names, posters = recommend(selected_movie_name)
    if names and posters:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            if len(names) > 0:
                st.text(names[0])
                st.image(posters[0])
        with col2:
            if len(names) > 1:
                st.text(names[1])
                st.image(posters[1])
        with col3:
            if len(names) > 2:
                st.text(names[2])
                st.image(posters[2])
        with col4:
            if len(names) > 3:
                st.text(names[3])
                st.image(posters[3])
        with col5:
            if len(names) > 4:
                st.text(names[4])
                st.image(posters[4])
    else:
        st.write("No recommendations found.")
