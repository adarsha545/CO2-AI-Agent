import chromadb
from sentence_transformers import SentenceTransformer
import ollama

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("co2_collection")

def retrieve_context(user_query):

    query_embedding = model.encode(user_query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    context = results["documents"][0][0]

    activity = results["metadatas"][0][0]["activity"]

    return activity, context

def generate_rag_response(user_query):

    activity, context = retrieve_context(user_query)

    prompt = f"""
You are an Environmental AI Assistant.

Use ONLY the information provided in the Context below.
Do NOT make up facts.

Context:
{context}

User Query:
{user_query}

Answer EXACTLY in this format using Markdown.

## Current Emission
- Mention the current CO₂ emission in kg/day.

## Better Alternative
- Mention the best alternative from the context.
- Mention its CO₂ emission.

## Estimated Reduction
- Mention the reduction percentage.

## 3 Eco-Friendly Suggestions
1. First suggestion.
2. Second suggestion.
3. Third suggestion.

Rules:
- ALWAYS provide exactly 3 suggestions.
- NEVER stop after suggestion 2.
- Keep the answer under 150 words.
- If information is unavailable, write "Not Available".
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": 0.2,
            "num_predict": 350
        }
    )

    print("Matched Activity:", activity)

    return activity, response["message"]["content"]