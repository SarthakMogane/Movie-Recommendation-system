import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movies_id):

    # url = "https://api.themoviedb.org/3/trending/movie/{movie_id}".format(movie_id=movies_id)
    #
    # headers = {
    #     "accept": "application/json",
    #     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5NDc3ODM2YWIzZDgzYzc4ZjlmOGYxYTY0NGEwNzk3YSIsIm5iZiI6MTc0MzE1NTY2OC45ODEsInN1YiI6IjY3ZTY3MWQ0NWU4ZTVjOWJhY2JhNzUzMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.O2Ryaeu4k2p4Kwcsp-QZOepMAVeXlm3f74NyuyXlpag"
    # }


    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=9477836ab3d83c78f9f8f1a644a0797a&language=en-US".format(movies_id))
    data = response.json()
    # st.text(data)
    # st.text("https://api.themoviedb.org/3/movie/{}?api_key=9477836ab3d83c78f9f8f1a644a0797a&language=en-US".format(movies_id))

    return  "https://image.tmdb.org/t/p/w500/"+data['poster_path']

similarity = pickle.load(open("similarity.pkl", "rb"))

def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distance = similarity[movie_index]
    recommend_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_poster =[]
    for i in recommend_list:

        movie_id = movies_list.iloc[i[0]].movie_id

        recommended_movies.append(movies_list.iloc[i[0]].title)
        # fetch poster from API
        recommended_movie_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movie_poster

movies_list = pickle.load(open("movies.pkl", "rb"))

select_movies = movies_list['title'].values


def save_feedback( movie_id, liked):
    feedback_file = 'feedback.csv'

    new_entry = pd.DataFrame([[ movie_id, liked]], columns=[ 'movie_id', 'liked'])

    if os.path.exists(feedback_file):
        df = pd.read_csv(feedback_file)
        df = pd.concat([df, new_entry], ignore_index=True)
    else:
        df = new_entry

    df.to_csv(feedback_file, index=False)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select Your movie',
    select_movies )

if st.button("Recommend Movie"):
    names,poster= recommend(selected_movie_name)

    col1, col2 ,col3,col4,col5 = st.columns(5)
    # with col1:
    #     st.markdown(names[0])
    #     st.image(poster[0])
    # with col2:
    #     st.markdown(names[1])
    #     st.image(poster[1])
    # with col3:
    #     st.markdown(names[2])
    #     st.image(poster[2])
    # with col4:
    #     st.markdown(names[3])
    #     st.image(poster[3])
    # with col5:
    #     st.text(names[4])
    #     st.image(poster[4])
    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            # Using HTML with text overflow for long titles and horizontal scrolling
            st.markdown(
                f"""
                <div style='width; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>
                    <div style="overflow-x: auto; white-space: nowrap;">
                        {names[i]}
                    </div>
                </div>
                """, unsafe_allow_html=True
            )
            st.image(poster[i])

    for movie in recommended_movies:
        st.write(movie['title'])

        # Feedback buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"👍 Like {movie['title']}", key=f"like_{movie['movie_id']}"):
                st.success(f"You liked {movie['title']}")
                # Log feedback
                save_feedback(movie['movie_id'],1)
        with col2:
            if st.button(f"👎 Dislike {movie['title']}", key=f"dislike_{movie['movie_id']}"):
                st.warning(f"You disliked {movie['title']}")
                save_feedback( movie['movie_id'],0)

        import pandas as pd
        import os



