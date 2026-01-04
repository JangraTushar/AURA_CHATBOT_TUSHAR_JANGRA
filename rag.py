import json
import chromadb
#from chromadb.config import Settings
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

from config import (
    KB_FILE,
    CHROMA_DB_DIR,
    GROQ_API_KEY,
    GROQ_MODEL,
)

_client = None          # Chroma client
_collection = None      # Chroma collection
_embedding_model = None # SentenceTransformers model
_llm_client = None      # Groq client


def init_llm():
    global _llm_client
    if _llm_client is None:
        _llm_client = Groq(api_key=GROQ_API_KEY)
    return _llm_client


def init_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model


def init_chroma():
    global _client, _collection
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        _collection = _client.get_or_create_collection("agriculture_kb")
    return _client, _collection


def load_knowledge_base():
    with open(KB_FILE, "r", encoding="utf-8") as f:
        kb = json.load(f)
    return kb


def setup_knowledge_base(force_rebuild: bool = False):
    """
    Build Chroma vector DB from agricultural_knowledge_base.json.
    Call once at startup.
    """
    _, collection = init_chroma()
    model = init_embedding_model()

    if not force_rebuild and collection.count() > 0:
        return collection, model

    kb = load_knowledge_base()

    if force_rebuild and collection.count() > 0:
        collection.delete(where={})

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for entry in kb:
        eid = str(entry["id"])
        text = entry["question"] + " " + entry["answer"]
        emb = model.encode(text)

        ids.append(eid)
        embeddings.append(emb.tolist())
        documents.append(entry["answer"])
        metadatas.append(
            {
                "question": entry["question"],
                "category": entry.get("category", ""),
                "tags": ",".join(entry.get("tags", [])),
            }
        )

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    return collection, model


def search_knowledge_base(question: str, collection, model, n_results: int = 3):
    """
    Semantic search over KB using Chroma.
    """
    query_emb = model.encode(question)
    results = collection.query(
        query_embeddings=[query_emb.tolist()],
        n_results=n_results,
    )
    return results


def generate_llm_answer(question: str, context: str) -> str:
    """
    Use Groq chat completion to answer based on retrieved context.
    """
    client = init_llm()
    prompt = f"""
You are an expert agronomist. Answer the farmer's question using ONLY the knowledge below.

Context:
{context}

Question: {question}

Provide a helpful, clear, concise answer for a non-technical farmer.
"""

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert agronomist."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    return completion.choices[0].message.content.strip()


def level_1_answer(question: str) -> str:
    """
    Level 1: RAG answer using KB + Chroma + Groq.
    """
    _, collection = init_chroma()
    model = init_embedding_model()

    results = search_knowledge_base(question, collection, model, n_results=3)
    top_docs = results["documents"][0]  # list of strings
    context = "\n".join(top_docs)

    answer = generate_llm_answer(question, context)
    return answer
