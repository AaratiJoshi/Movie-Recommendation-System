import streamlit as st
import pickle
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")


# Fetch poster from OMDb
def fetch_poster(movie_name):

    api_key = "62e51c6"

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"

    data = requests.get(url).json()

    if data["Response"] == "True":
        return data["Poster"]
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"


def recommend(movie):
    movie_index = movies_list[movies_list["title"] == movie].index[0]

    distances = similarity[movie_index]

    similar_movies = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for i in similar_movies:

        movie_name = movies_list.iloc[i[0]].title

        recommend_movies.append(movie_name)

        # Fetch poster
        recommend_movies_posters.append(fetch_poster(movie_name))

    return recommend_movies, recommend_movies_posters


movies_list = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# st.title("Movie Recommender System")
st.markdown(
    "<h1 style='text-align:center;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>

.stApp{
    background-color: #0E1117;
}

.movie-title{
    text-align:center;
    font-size:18px;
    font-weight:bold;
    height:60px;
    color:white;
}

img{
    border-radius:10px;
}

</style>
""",
    unsafe_allow_html=True,
)


option = st.selectbox("Select Movie", movies_list["title"].values)

if st.button("Recommend"):

    names, posters = recommend(option)

    cols = st.columns(5)

    for idx, col in enumerate(cols):

        with col:

            st.markdown(
                f"<div class='movie-title'>{names[idx]}</div>", unsafe_allow_html=True
            )

            st.image(posters[idx], use_container_width=True)
