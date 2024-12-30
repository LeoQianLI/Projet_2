import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

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

df = pd.read_csv(r"C:\Users\leo12\Documents\Projet_2\data\\movies.csv")
copy_df = pd.read_csv(r"C:\Users\leo12\Documents\Projet_2\data\\movies.csv")
df_intervenant = pd.read_csv(r"C:\Users\leo12\Documents\Projet_2\data\\df_interv.csv")


# Ensure session state variables are initialized
if "selected_person" not in st.session_state: 
    st.session_state["selected_person"] = None

if 'title' not in st.session_state:
    st.session_state['title'] = 'No movies selected'

if 'info_reco' not in st.session_state:
    st.session_state['info_reco'] = None  # Initialize it as None or an appropriate default value

# Layout
col1, col2, col3 = st.columns([1, 10, 1])
with col2:
    st.title(st.session_state['title'])

    # Retrieve the selected movie
    selected = st.session_state['title']
    selected_movie = df[df['originalTitle'] == selected].reset_index(drop=True)
    st.write(selected_movie)

    if not selected_movie.empty:
        tconst_selected_movie = selected_movie.loc[0, 'tconst']
        film_description = selected_movie.loc[0, 'overview']
        st.markdown(f"**Description du film**: {film_description}")
    else:
        st.markdown("**No movie selected or found.**")


    # Display poster and trailer if available
    if not selected_movie.empty:
        col1, col2 = st.columns([2.9, 7.6])
        with col1:
            poster = selected_movie.loc[0, 'poster_path']
            st.image(poster, caption=f"Poster of {selected}")
        with col2:
            st.video(selected_movie.loc[0, 'b_annonce'])

        # Display metrics if 'selected_movie' is not None
        if  not selected_movie.empty:
            col1, col2, col3 = st.columns([6, 3, 3])
            with col1:
                st.metric(label="Genre", value=selected_movie.loc[0, 'genres'])
                st.metric(label="Average Rating", value=selected_movie.loc[0, 'averageRating'])
            with col2:
                st.metric(label="Start Year", value=selected_movie.loc[0, 'startYear'])
                st.metric(label="Popularity", value=selected_movie.loc[0, 'popularity_film'])
            with col3:
                st.metric(label="Runtime (minutes)", value=selected_movie.loc[0, 'runtimeMinutes'])
                st.metric(label="Number of Votes", value=selected_movie.loc[0, 'numVotes'])
        else:
            st.markdown("**Metrics unavailable for this movie.**")
    
    # Add custom styling for the button
    st.markdown(
        """
        <style>
        .custom-button {
            display: inline-block;
            background-color: transparent; /* Transparent background */
            color: #007BFF; /* Text color (adjust as needed) */
            border: 1px solid #007BFF; /* Border styling */
            border-radius: 5px; /* Optional: rounded corners */
            padding: 5px 10px; /* Padding for button size */
            text-align: center; /* Center the text */
            font-size: 12px; /* Adjust font size */
            text-decoration: none; /* Remove underline */
            cursor: pointer; /* Pointer cursor on hover */
            transition: all 0.3s ease; /* Smooth transition for hover effect */
        }
        .custom-button:hover {
            background-color: #007BFF; /* Change background on hover */
            color: white; /* Change text color on hover */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Artiste:")
    # Initialize selected_person to None
    if "selected_person" in st.session_state:
        st.session_state["selected_person"] = None

    df_name = df_intervenant[df_intervenant.tconst == tconst_selected_movie].reset_index(drop=True)
    # Extract data for display
    top_names = df_name['primaryName'].head(6).fillna("")
    top_profession = df_name['primaryProfession'].head(6).fillna("")
    top_images = df_name['profile_path'].head(6).fillna("")
    top_bio = df_name['biography'].head(6).fillna("No biography available.")
    columns = st.columns(len(top_names))  # Create one column for each person

    # Display artistes in a row with 6 images and buttons
    for col, name, profession, image, bio in zip(columns, top_names, top_profession, top_images, top_bio):
        with col:
             # Display image only if it's not empty
            if image:
                st.image(image, caption=name)
            else:
                st.warning("No image available.")  # Fallback for missing images

            # Display name button
            if st.button(name):  # If the button is clicked, set the selected person
                st.session_state["selected_person"] = {
                    "name": name,
                    "profession": profession,
                    "bio": bio,
                    "image": image,
                }
                

    # Display selected person's information in a large section below
    if st.session_state["selected_person"]:
        selected_person = st.session_state["selected_person"]
        st.markdown("### Selected Person Information")
        st.metric(label = "Profession", value = selected_person['profession'])

        # Display image only if it's not empty
        if selected_person["image"]:
            st.image(selected_person["image"], width=200)
        else:
            st.warning("No image available.")

        st.markdown(f"**Name:** {selected_person['name']}")
        st.write(selected_person["bio"])
    else:
        st.write(" ")


def recommandation(alpha):
    # cette fonction prend en argument l'id d'un film de imdb (tconst) et retourne la liste des films que notre modèle recommande
    cols = ['tconst', 'startYear', 'runtimeMinutes', 'averageRating', 'numVotes', 'budget', 'popularity_film', 'revenue']
    df_num = df[cols]

    scaler = MinMaxScaler()
    df_num[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes', 'budget', 'popularity_film', 'revenue']] = scaler.fit_transform(df_num[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes', 'budget', 'popularity_film', 'revenue']])

    df.genres.str.split(",").explode().nunique()
    dummies = df.genres.str.get_dummies(',')
    df_concat = pd.concat([df, dummies], axis = 1)
    cols_drop = ['originalTitle', 'genres', 'id_TMDB', 'origin_country','original_language', 'overview', 'poster_path',
        'spoken_languages', 'tagline', 'b_annonce', 'key_words']
    df_movie = df_concat.drop(columns = cols_drop)

    X_ami = df_movie[df_movie['tconst'] == alpha].reset_index(drop=True)
    df_num = df_movie[df_num['tconst'] != alpha].reset_index(drop=True)

    model = NearestNeighbors(n_neighbors= 5).fit(df_num.drop(columns= ['tconst']))
    distance, indice = model.kneighbors(X_ami.drop(columns=['tconst']))

    df1 = df_num.iloc[indice[0],:]

    l_final = []
    for x in df1['tconst']:
        film = copy_df[copy_df['tconst'] == x ]
        l_final.append(film)
    result = pd.concat(l_final)

    return result

col1, col2 = st.columns([0.8, 9])

# Add the button to the right column (col2)
with col2:
# Place the button inside the custom class
    with st.markdown('<div class="small-transparent-button">', unsafe_allow_html=True):
        if st.button("Aller voir plus de films similaires"):
            resultat = recommandation(tconst_selected_movie)
            st.session_state['info_reco'] = resultat
            st.switch_page('pages\page2.py')
