import pickle
import streamlit as st
import requests


# Function to fetch movie details
def fetch_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    return data

def fetch_keywords(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/keywords?api_key=8265bd1679663a7ea12ac168da84d2e8".format(movie_id)
    data = requests.get(url)
    data = data.json()
    keywords = data['keywords'][:5]  
    keyword_names = [keyword['name'] for keyword in keywords]
    return keyword_names


# Function to fetch movie cast
def fetch_cast(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=8265bd1679663a7ea12ac168da84d2e8".format(movie_id)
    data = requests.get(url)
    data = data.json()
    cast = data['cast'][:5] 
    return cast



# Function to fetch movie posters
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Fetch movie recommendations
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_cast = []
    recommended_movie_keywords = []
    
    for i in distances[1:11]:
         if i[0] < len(movies):  # Check if the index is within the range of movies
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_cast.append(fetch_cast(movie_id))
            recommended_movie_keywords.append(fetch_keywords(movie_id))
            
        
    return recommended_movie_names, recommended_movie_posters, recommended_movie_cast, recommended_movie_keywords



# Load movie data
movies = pickle.load(open('D:\Practice\Python_MovieRecomendationSystem_Cinemania\movie_list.pkl','rb'))
similarity = pickle.load(open('D:\Practice\Python_MovieRecomendationSystem_Cinemania\similarity.pkl','rb'))

# Set page config
st.set_page_config(
    page_title='Cinemania - Discover Your Movie Journey',
    page_icon='🎬',
    layout='wide'
)

# Page title and description
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='font-size: 3rem; color: #FFC700; text-shadow: 2px 2px #000000;'>🎥 Welcome to Cinemania 🍿</h1>
        <p>🎉 Get ready to unlock a treasure trove of cinematic gems!</p>
        <p>🔍 Uncover hidden movie masterpieces and unearth underrated classics.</p>
        <p>🌟 Expand your movie horizons and broaden your film knowledge.</p>
        <p>🍿 Grab your popcorn, sit back, and let Cinemania guide you through an unforgettable movie journey.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.title('Blockbuster Blitz')
top_15_movies = movies.sort_values(by="popularity", ascending=False).head(10)
for i, movie in top_15_movies.iterrows():
    st.sidebar.write(f" {movie['title']}")
    st.sidebar.image(fetch_poster(movie['movie_id']), width=200)


st.subheader("Select  a movie")
movie_list = movies['title'].values
selected_movie = st.selectbox("", movie_list)


# recommendations on the main screen
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_cast, recommended_movie_keywords = recommend(selected_movie)
    num_movies = min(10, len(recommended_movie_names))
    for i in range(num_movies):
        columns = st.columns([1, 3]) 
        with columns[0]:
            st.markdown(f"<h4><strong>{i+1}:  {recommended_movie_names[i]}</strong></h4>", unsafe_allow_html=True)
            st.image(recommended_movie_posters[i], width=250, caption=recommended_movie_names[i])
        with columns[1]:
            st.markdown("---")
            movie_details = fetch_movie_details(movies.iloc[i+1].movie_id)
            st.write(f"Release Year:{movie_details['release_date'][:4]}")
            st.write(f"Genres: {', '.join([genre['name'] for genre in movie_details['genres']])}")
            st.write("Cast:    " + ", ".join(actor['name'] for actor in recommended_movie_cast[i]))
            st.write(f"Keywords: {', '.join(recommended_movie_keywords[i])}")
            
            st.markdown("---") 
        st.markdown(" ")


#Footer ---
st.markdown(
    """
    <div style='text-align: center;'>
        <p style='font-size: 1.2rem; color: #666;'>Created with ❤️ by Cinemania Team</p>
        <p style='font-size: 1rem; color: #666;'>Explore. Discover. Enjoy.</p>
    </div>
    <div style='text-align:right;'>
        <p style='font-size: 1rem; color: #666;'>Vishwajeet Anekar</p>
    </div>
    """,
    unsafe_allow_html=True
)








                