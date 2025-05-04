import streamlit as st
import pandas as pd

import pickle
import requests

def fetch_poster(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=18d5718aba7dfc22eeab9cc58cf015e8".format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w185/"+ data["poster_path"]


movie_dict=pickle.load(open("movie_dict.pkl","rb"))
movie=pd.DataFrame(movie_dict)

similarity=pickle.load(open("similarity.pkl","rb"))

movie_list=movie["title"].values
st.title("Movie Recommender System")

select_movie=st.selectbox(
    "Which movie you like to watch?",
    (movie_list)
)
def recommend(select_movie):
    movie_index=movie[movie["title"]==select_movie].index[0]
    distance= similarity[movie_index]
    top_five_similar_movie=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_sim_movie=[]
    recommend_poster_movie=[]

    for i in top_five_similar_movie:
        movie_id=movie.iloc[i[0]].movie_id
        recommend_sim_movie.append(movie.iloc[i[0]].title)
        recommend_poster_movie.append(fetch_poster(movie_id))

    return recommend_sim_movie,recommend_poster_movie



if st.button("Recommend"): 
    name,poster=recommend(select_movie)
    movie1, movie2, movie3, movie4, movie5=st.columns(5)

    with movie1:
        st.text(name[0])
        st.image(poster[0])

    with movie2:
        st.text(name[1])
        st.image(poster[1])
    
    with movie3:
        st.text(name[2])
        st.image(poster[2])
    
    with movie4:
        st.text(name[3])
        st.image(poster[3])

    with movie5:
        st.text(name[4])
        st.image(poster[4])

