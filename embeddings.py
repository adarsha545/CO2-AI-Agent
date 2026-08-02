from sentence_transformers import SentenceTransformer
import chromadb
import pandas as pd

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load dataset
df = pd.read_csv("dataset.csv")

# Create ChromaDB database
client = chromadb.PersistentClient(path="chroma_db")
try:
    client.delete_collection("co2_collection")
except:
    pass

collection = client.create_collection("co2_collection")

# Add data to ChromaDB
for i, row in df.iterrows():

    document = f"""
Activity: {row['Activity']}
Category: {row['Category']}
Current CO2: {row['Avg_CO2_Emission']} kg/day
Better Alternative: {row['Better_Alternative']}
Alternative CO2: {row['Alternative_CO2']} kg/day
"""

    embedding = model.encode(document).tolist()

    collection.add(
    ids=[str(i)],
    documents=[document],
    embeddings=[embedding],
    metadatas=[{
        "activity": row["Activity"],
        "category": row["Category"],
        "emission": float(row["Avg_CO2_Emission"])
    }]
)
print("✅ Vector Database Created Successfully!")