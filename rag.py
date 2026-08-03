import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
import streamlit as st
import time


# Load embedding model only once
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_embedding_model()

# Connect to ChromaDB
@st.cache_resource
def load_collection():
    client = chromadb.PersistentClient(path="chroma_db")
    return client.get_collection("co2_collection")

collection = load_collection()

# Create Gemini client
gemini_client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

print("===== RAG.PY LOADED =====")
print("Using model: gemini-3.6-flash")


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

Use the Context as the primary source for emission values and the better alternative.

Never invent CO₂ values.

If a value is missing from the Context, omit it instead of writing "Not Available".

Context:
{context}

User Query:
{user_query}

Generate the response in Markdown using EXACTLY this format:

## Current Emission
- Current CO₂ emission: <value> kg/day

## Better Alternative
- Better alternative: <activity>
- CO₂ emission: <value> kg/day

## Estimated Reduction
- Reduction: <percentage>

Keep the response under 120 words.

Do NOT generate eco-friendly suggestions.
"""
    # ---------- First Gemini Call (Main Answer) ----------
    response = None

    for attempt in range(3):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            break

        except Exception as e:
            print(f"Main Answer Attempt {attempt + 1} failed: {e}")

            if attempt == 2:
                raise

            time.sleep(2)

    answer = response.text

    # ---------- Second Prompt (Suggestions) ----------
    suggestion_prompt = f"""
You are an Environmental Sustainability Expert.

User Activity:
{user_query}

Generate EXACTLY 3 practical eco-friendly suggestions.

Rules:
- Suggestions must match the user's activity.
- Do NOT mention CO₂ values.
- Do NOT repeat the user's activity.
- Do NOT say "Not Available".
- Number the suggestions 1, 2, 3.
- Keep each suggestion to one sentence.
"""

    # ---------- Second Gemini Call (Suggestions) ----------
    suggestion_response = None

    for attempt in range(3):
        try:
            suggestion_response = gemini_client.models.generate_content(
                model="gemini-3.6-flash",
                contents=suggestion_prompt,
            )
            break

        except Exception as e:
            print(f"Suggestion Attempt {attempt + 1} failed: {e}")

            if attempt == 2:
                raise

            time.sleep(2)

    suggestions = suggestion_response.text

    # ---------- Combine Responses ----------
    final_answer = (
        answer
        + "\n\n## 3 Eco-Friendly Suggestions\n\n"
        + suggestions
    )

    print("Matched Activity:", activity)

    return activity, final_answer