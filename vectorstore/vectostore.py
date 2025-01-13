import pandas as pd  # Pour la manipulation des données
from langchain_community.vectorstores import Chroma  # Base de données vectorielle
from langchain_openai import OpenAIEmbeddings  # Pour créer les embeddings
from langchain.schema import Document  # Structure de données pour les documents
from typing import List  # Pour le typage des fonctions
import os
from dotenv import load_dotenv  # Pour gérer les variables d'environnement
import shutil  # Pour les opérations sur les fichiers
from openai import OpenAI

# Chargement des variables d'environnement (clés API)
load_dotenv()

def create_documents_from_csv(csv_path: str) -> List[Document]:
    """
    Crée une liste de documents à partir d'un fichier CSV de film.
    
    Cette fonction:
    1. Lit le fichier CSV contenant les recettes
    2. Pour chaque recette, crée un document structuré avec:
       - Le contenu (texte de la recette)
       - Les métadonnées (temps de cuisson, nombre de personnes, etc.)
    
    Args:
        csv_path (str): Chemin vers le fichier CSV des recettes
        
    Returns:
        List[Document]: Liste des documents structurés prêts à être vectorisés
    """
    # Lecture du fichier CSV
    #csv_path = os.path.join("data", "movies.csv")
    df = pd.read_csv(csv_path)
    documents = []
    print(f"Reading CSV from: {csv_path}")
    print(f"Number of rows in CSV: {len(df)}")
    # Traitement de chaque ligne du CSV
    for i, r in df.iterrows():
         # Combinaison des champs textuels pour créer le contenu
        content = f"Nom de film: {r['originalTitle']}\n\nDescription: {str(r['overview'])}\n\nKeyword: {str(r['key_words'])}\n\nGenre: {str(r['genres'])}"

        # Création des métadonnées associées
        metadata={            
                'Start year': r['startYear'],
                'Average rating': r[ 'averageRating'],
                'Run time minutes': r['runtimeMinutes'],
                'Types': r['genres'],
                'Poster': r['poster_path'],
                'Popularity': r['popularity_film'],
                'Budget': r['budget']
                    }
        # Création du document structuré
        doc = Document(
            page_content=content,
            metadata=metadata
        )
        documents.append(doc)
    
    return documents

def main():
    """
    Fonction principale qui gère la création de la base de données vectorielle.
    
    Cette fonction:
    1. Vérifie la présence de la clé API OpenAI
    2. Initialise le modèle d'embedding
    3. Crée les documents à partir du CSV
    4. Génère et sauvegarde la base de données vectorielle
    """
    # Vérification de la clé API
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Clé API OpenAI non trouvée dans les variables d'environnement")
    
    # Possibilité de nettoyer la base existante (actuellement commenté)
    #if os.path.exists("./chroma_db"):
    #    shutil.rmtree("./chroma_db")
    
    # Initialisation du modèle d'embedding
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",  # Utilisation du modèle plus léger et économique
        openai_api_key=os.getenv("OPENAI_API_KEY") # Use the API key from .env
    )

    # Création des documents à partir du CSV
    documents = create_documents_from_csv("data/movies.csv")
    
    # Création de la base de données vectorielle
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_db"  # Dossier où sera sauvegardée la base
    )
    
    # Sauvegarde permanente de la base
    vectorstore.persist()
    print(f"Base de données vectorielle créée avec {len(documents)} documents et sauvegardée dans ./chroma_db")

if __name__ == "__main__":
    main()

    