import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from chromadb import Client
from chromadb.config import Settings
import chromadb

# Load the dataset
df_m = pd.read_csv(r"C:\Users\leo12\Documents\Projet_2\data\\movies.csv")

# Streamlit UI
st.title("Assistant de Recherche de Films")
st.markdown("**Comment puis-je vous aider ?**")

# Input for the search query
query = st.text_input("Entrez une description ou un genre de film à rechercher:")

# Button to perform search
if st.button("Recherche"):
    if query.strip():  # Check if query is not empty
        with st.spinner("Chargement du modèle et préparation des données..."):
            # Load the embedding model
            model = SentenceTransformer("all-MiniLM-L6-v2")

            # Create a descriptive column
            df_m['all_text'] = (
                "Nom de film: " + df_m['originalTitle'].fillna("") + ". "
                "Genre: " + df_m['genres'].fillna("") + ". "
                "Overview: " + df_m['overview'].fillna("") + ". "
                "Keyword: " + df_m['key_words'].fillna("")
            )

            # Encode the column into embeddings
            embeddings = model.encode(df_m['all_text'].tolist())

            # Define ChromaDB persistent storage location
            CHROMA_DB_DIR = "chromadb_storage"
            # Initialize ChromaDB with persistent storage
            #chroma_client = chromadb.Client(
                #Settings(
                    #chroma_api_impl="local",
                    #persist_directory=CHROMA_DB_DIR # Use DuckDB with Parquet for persistence
             #))
            client = chromadb.PersistentClient(
            path="/path/to/persist/directory",
            settings=Settings(anonymized_telemetry=False))
            collection = client.create_collection(
                name="films_db",
                metadata={"hnsw:space": "cosine"}
            )
            # Add data to ChromaDB
            collection.add(
                documents=df_m['all_text'].tolist(),
                metadatas=[
                    {
                        'tconst': row['tconst'],
                        'runtimeMinutes': row['runtimeMinutes'],
                        'genres': row['genres']
                    }
                    for _, row in df_m.iterrows()
                ],
                ids=[f"id{i}" for i in range(len(df_m))]
            )

        with st.spinner("Recherche en cours..."):
            # Query ChromaDB
            results = collection.query(
                query_texts=[query],
                n_results=5,
                include=['documents', 'metadatas', 'distances']
            )

        # Display results
        st.markdown("### Résultats de la recherche :")
        for i, result in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            st.markdown(f"""
            **Film {i+1}:**
            - **Description:** {result}
            - **Genre:** {metadata['genres']}
            - **Durée:** {metadata['runtimeMinutes']} minutes
            """)
    else:
        st.warning("Veuillez entrer une description ou un genre pour rechercher.")
