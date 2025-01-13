import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

df_intervenant = pd.read_csv(r"C:\Users\leo12\Documents\Projet_2\data\\df_interv.csv")

# Utilisation d'une image externe pour le fond écran
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
st.title(":orange[Recommandations]")
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
    st.header(f":orange[Détails de:] {reco_f['originalTitle']}")
     # Display additional film details
    st.write(":orange[Genre:]", reco_f["genres"].replace(",", " "))
    st.write(":orange[Description:]", reco_f['overview'])
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric(label=":orange[Start Year]", value= reco_f['startYear'])
    with c2:
        st.metric(label=":orange[minutes]", value= reco_f['runtimeMinutes'])
    with c3:    
        st.metric(label=":orange[Popularity]", value= reco_f['popularity_film'])
    with c4:
        st.metric(label=":orange[Average Rating]", value= reco_f['averageRating'])
    with c5:
        st.metric(label=":orange[Number of Votes]", value= reco_f['numVotes'])
    col1, col2 = st.columns([2.9, 7.6])
    with col1:
        st.image(reco_f["poster_path"], width=550)
    with col2:
        st.video(reco_f["b_annonce"])
    st.write(":orange[________________________________________________________________________________________________________________________________________________________________]")
    # Display artist information related to the selected movie
    st.subheader(":orange[Quelques intervenants]")
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
    st.write(":orange[______________________________________________________________________________________________________________________________________________________________]")
    st.subheader(":orange[Informations de la personne]")
    col1, col2 = st.columns([3,7.5])
    with col1:
        st.image(selected_artist["profile_path"], width=300)
    with col2:
        st.write(":orange[Name:]", selected_artist['primaryName'])
        st.write(":orange[Role:]", selected_artist['primaryProfession'].replace(",", " - "))
        st.write(":orange[Birthday:]", selected_artist['birthday'])
        st.write(":orange[Place of Birth:]", selected_artist['place_of_birth'])
        st.write(":orange[Biography:]",  selected_artist['biography'])

# Bouton pour sélectionner un autre film et revenir à la page d'accueil
st.write(":orange[____________________________________________________________________________________________________________________________________________________________]")
col3, col4, col5=st.columns(3)
with col4:
    #if st.button(":orange[Voulez-vous sélectionner un autre film?]", key="reset_button"):
        #st.session_state['button_clicked'] = "reset"  # Réinitialise l'état
        #st.switch_page("page_acceuil.py")  # Redirige vers la page d'accueil
        if st.button(":orange[Plus de fimls par Chatbot]"):
            #st.session_state['info_reco'] = resultat
            st.switch_page('pages\page3.py')

