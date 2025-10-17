import streamlit as st
import pickle
import pandas as pd
import requests
import os

def fetch_poster(movies_id):
    '''
    fetching poster URL from TMDB website using API

    '''
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=9477836ab3d83c78f9f8f1a644a0797a&language=en-US".format(movies_id))
    data = response.json()

    return  "https://image.tmdb.org/t/p/w500/"+data['poster_path']

# similarity = pickle.load(open("similarity.pkl", "rb"))
hybrid_similarity =pickle.load(open('hybrid_similarity.pkl','rb'))

def recommend(movie):
    '''
    Recommend 5 movies and There Poster path 

    '''
    movie_index = movies[movies['title'] == movie].index[0]
    # distance = similarity[movie_index]
    distance = hybrid_similarity[movie_index]
    recommend_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_poster =[]
    for i in recommend_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movie_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movie_poster


movies = pickle.load(open("movies.pkl", "rb"))

select_movies = movies['title'].values


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select Your movie',
    select_movies )


if st.button("Recommend Movie"):
    names, poster = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    # Custom CSS to fix the height of the title box and handle overflow

    TITLE_CSS = """
    <style>
        .fixed-height-title {
            height: 4.5em; /* Example height to accommodate 3 lines of text */
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 3; /* Show maximum of 3 lines */
            -webkit-box-orient: vertical;
            text-overflow: ellipsis;
            margin-bottom: 5px; /* Small gap between title and poster */
        }
    </style>
    """
    st.markdown(TITLE_CSS, unsafe_allow_html=True)


    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            # 1. Title Container with Fixed Height
            st.markdown(
                f"""
                <div class='fixed-height-title'>
                    <strong>{names[i]}</strong>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.image(poster[i], use_container_width=True)



