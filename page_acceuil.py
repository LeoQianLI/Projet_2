import streamlit as st
import pandas as pd
import time
import uuid

df = pd.read_csv(r"C:\Users\leo12\Documents\Projet_2\data\\movies.csv")

st.set_page_config(
    layout= 'wide',
    initial_sidebar_state= "collapsed"
)
# Utilisation d'une image externe pour le fond
page_bg_css = """
<style>
[data-testid="stAppViewContainer"] {
    background: url('https://images.unsplash.com/photo-1621791554700-35b52803f596?q=80&w=1770&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
}
[data-testid="stSidebar"] {
    background-color: rgba(30, 30, 47, 0.9);
}
.css-1cpxqw2 a {
    color: white;
}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)
# read mon csv data film
col1, col2, col3 = st.columns([0.5, 10, 0.5])
with col2:
    st.title("🎉 Welcome to Big Pandas recommandation film world 🎥")
    # Dropdown for film selection
    film_title = df.originalTitle 
    choice = st.selectbox('**Veuillez** **trouver** **votre** **film** **préféré**:', film_title)
    selected_movie = df[df['originalTitle'] == choice].reset_index(drop = True)
    if st.button('Détails du film selectionné'):
        st.session_state['title'] = choice 
        st.switch_page("pages\page1.py")

if 'averageRating' in df.columns and 'poster_path' in df.columns:
    st.header(":orange[⭐ Top 50 Films by Rating]")
    placeholder = st.empty()

    # Sort films by average rating
    rat_movies = df.sort_values(by='averageRating', ascending=False).head(50)

    # Initialize carousel movies in session state if not already done
    if 'carousel_start_idx' not in st.session_state:
        st.session_state.carousel_start_idx = 0  # Start index for the carousel

    # Function to display carousel
    def display_carousel():
        with placeholder.container():
            start_idx = st.session_state.carousel_start_idx
            end_idx = start_idx + 8
            movies = rat_movies.iloc[start_idx:end_idx]
            cols = st.columns(8)
            for i, movie in enumerate(movies.itertuples()):
                with cols[i]:
                    st.image(movie.poster_path, caption=movie.originalTitle)

    # Display the initial carousel
    display_carousel()

    # Create aligned buttons for navigation
    button_cols = st.columns([1, 6, 1])  # Adjust column proportions for alignment

    with button_cols[0]:
        if st.button('⬅️ Previous Page'):
            # Move to the previous set of films, looping back if at the start
            st.session_state.carousel_start_idx = (st.session_state.carousel_start_idx - 8) % 50
            display_carousel()

    with button_cols[2]:
        if st.button('Next Page ➡️'):
            # Move to the next set of films, looping back if at the end
            st.session_state.carousel_start_idx = (st.session_state.carousel_start_idx + 8) % 50
            display_carousel()


if 'originalTitle' in df.columns and 'poster_path' in df.columns:
    st.header(":orange[🎬 Films]")

    placeholder = st.empty()

    # Function to display carousel
    def display_carousel():
        with placeholder.container():
            st.markdown(
                """
                <style>
                .custom-carousel .movie-title {
                    width: 100px; /* Set a fixed width for captions */
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    text-align: center;
                }
                .custom-carousel .stButton button {
                    width: 100%; /* Ensure buttons take full width */
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                }
                </style>
                <div class="custom-carousel">
                """,
                unsafe_allow_html=True,
            )
                # Sample 8 random movies
            movies = df.sample(8)
            cols = st.columns(8)
            for i, movie in enumerate(movies.itertuples()):
                with cols[i]:
                    st.image(movie.poster_path)
                    # Generate a truly unique key for the button
                    unique_key = f"btn_{movie.Index}_{str(uuid.uuid4())}"
                    if st.button(f"{movie.originalTitle}", key=unique_key):
                        st.session_state['selected_film'] = movie.originalTitle
                        #st.switch_page("pages\page1.py")  # Replace with your page name

    # Carousel logic
    while True:
        display_carousel()
        time.sleep(8)  # Refresh the carousel every 8 seconds

    