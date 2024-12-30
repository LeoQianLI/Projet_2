import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

df_intervenant = pd.read_csv(r"C:\Users\leo12\Documents\Projet_2\data\\df_interv.csv")

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

# Ensure session state variables are initialized
if "reco_film" not in st.session_state:
    st.session_state["reco_film"] = None

if "selected_artist" not in st.session_state:
    st.session_state["selected_artist"] = None

# Load movie recommendation data
if st.session_state.get("info_reco") is not None:
    movie_reco = st.session_state["info_reco"].reset_index(drop=True)
else:
    st.error("No recommendation data available.")
    st.stop()

# Display recommended movies
col = st.columns(5)  # Adjust number of columns if necessary
for cols, (_, movie_info) in zip(col, movie_reco.iterrows()):
    with cols:
        st.image(movie_info["poster_path"])
        if st.button(movie_info["originalTitle"]):  # Button for movie title
            st.session_state["reco_film"] = movie_info.to_dict()
            st.session_state["selected_artist"] = None  # Clear previous artist selection

# Display selected movie details if a movie is clicked
if st.session_state["reco_film"]:
    reco_f = st.session_state["reco_film"]
    st.markdown("### Selected Film Information")
    st.markdown(f"**{reco_f['originalTitle']}**")
    col1, col2 = st.columns([4, 6])
    with col1:
        st.image(reco_f["poster_path"], width=550)
    with col2:
        # Display additional film details
        st.metric(label="Genre", value=reco_f["genres"])
        st.write(f"**Start Year:** {reco_f['startYear']}")
        st.write(f"**Runtime (minutes):** {reco_f['runtimeMinutes']}")
        st.write(f"**Popularity:** {reco_f['popularity_film']}")
        st.write(f"**Average Rating:** {reco_f['averageRating']}")
        st.write(f"**Number of Votes:** {reco_f['numVotes']}")
        st.write(f"**Description:** {reco_f['overview']}")
    st.video(reco_f["b_annonce"])

    # Display artist information related to the selected movie
    st.markdown("### Artists Information")
    film_tconst = reco_f["tconst"]
    person_info = df_intervenant[df_intervenant["tconst"] == film_tconst].head(6)
    artist_columns = st.columns(6)  # Columns for artists

    for col, (_, info) in zip(artist_columns, person_info.iterrows()):
        with col:
            st.image(info["profile_path"])
            if st.button(info["primaryName"]):  # Button for artist's name
                st.session_state["selected_artist"] = info.to_dict()

# Display selected artist details if an artist is clicked
if st.session_state["selected_artist"]:
    selected_artist = st.session_state["selected_artist"]
    st.markdown("### Selected Artist Information")
    col1, col2 = st.columns([4, 6])
    with col1:
        st.image(selected_artist["profile_path"], width=300)
    with col2:
        st.write(f"**Name:** {selected_artist['primaryName']}")
        st.write(f"**Role:** {selected_artist['primaryProfession']}")
        st.write(f"**Birthday:** {selected_artist['birthday']}")
        st.write(f"**Place of Birth:** {selected_artist['place_of_birth']}")
        st.write(f"**Biography:** {selected_artist['biography']}")

        
#if st.button("Retour à la page d'accueil"):
    #st.session_state['selected_film']
    #st.swtich.page(page_acceuil.py)
