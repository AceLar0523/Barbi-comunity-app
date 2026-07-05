import os
import chromadb
from chromadb.config import Settings

# Initialize the ChromaDB persistent client
CHROMA_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'chroma_db')

try:
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name="barbies_collection")
except Exception as e:
    print(f"Error initializing ChromaDB: {e}")
    client = None
    collection = None

def get_barbie_text_representation(barbie):
    """
    Creates a detailed text representation of a Barbie for vector embeddings.
    """
    parts = []
    parts.append(f"Nombre: {barbie.name}")
    if barbie.collection:
        parts.append(f"Colección: {barbie.collection}")
    if barbie.release_year:
        parts.append(f"Año: {barbie.release_year}")
    if barbie.manufacturer:
        parts.append(f"Fabricante: {barbie.manufacturer}")
    if barbie.barbie_type:
        parts.append(f"Tipo: {barbie.barbie_type}")
    if barbie.hair_color:
        parts.append(f"Color de pelo: {barbie.hair_color}")
    if barbie.eye_color:
        parts.append(f"Color de ojos: {barbie.eye_color}")
    if barbie.description:
        parts.append(f"Descripción: {barbie.description}")
    if barbie.notes:
        parts.append(f"Notas: {barbie.notes}")
    
    return " | ".join(parts)

def add_barbie_to_index(barbie):
    """
    Adds or updates a Barbie in the ChromaDB index.
    """
    if collection is None:
        return
        
    text_rep = get_barbie_text_representation(barbie)
    
    collection.add(
        documents=[text_rep],
        metadatas=[{
            "barbie_id": barbie.id,
            "name": barbie.name,
            "collection": barbie.collection or "N/A"
        }],
        ids=[str(barbie.id)]
    )

def search_similar_barbies(query_text, n_results=3):
    """
    Searches for similar Barbies given a query text.
    """
    if collection is None:
        return []
        
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    similar_barbies = []
    if results['documents'] and len(results['documents']) > 0:
        docs = results['documents'][0]
        metas = results['metadatas'][0]
        for doc, meta in zip(docs, metas):
            similar_barbies.append({
                "text": doc,
                "name": meta["name"],
                "collection": meta["collection"]
            })
            
    return similar_barbies
