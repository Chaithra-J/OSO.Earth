import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# client = chromadb.Client(
#     Settings(
#         persist_directory="./chroma",
#         anonymized_telemetry=False
#     )
# )

# collection = client.get_or_create_collection("habit_knowledge")
# model = SentenceTransformer("all-MiniLM-L6-v2")

# def ingest_sources(texts):
#     if collection.count() > 0:
#         return

#     embeddings = model.encode(texts)
#     for i, text in enumerate(texts):
#         collection.add(
#             ids=[str(i)],
#             documents=[text],
#             embeddings=[embeddings[i]]
#         )

#     client.persist()

# def retrieve_knowledge(query: str) -> str:
#     if collection.count() == 0:
#         return ""

#     embedding = model.encode([query])
#     results = collection.query(
#         query_embeddings=embedding,
#         n_results=3
#     )

#     return "\n".join(results["documents"][0])



# VECTOR_DB = None

# def build_vector_db(pdf_dir="data/pdfs"):
#     global VECTOR_DB

#     docs = []
#     for file in os.listdir(pdf_dir):
#         if file.endswith(".pdf"):
#             loader = PyPDFLoader(os.path.join(pdf_dir, file))
#             docs.extend(loader.load())

#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     chunks = splitter.split_documents(docs)

#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )

#     VECTOR_DB = FAISS.from_documents(chunks, embeddings)


# def retrieve_pdf_context(query, k=4):
#     if VECTOR_DB is None:
#         raise RuntimeError("Vector DB not initialized")

#     docs = VECTOR_DB.similarity_search(query, k=k)
#     if not docs:
#         return "", False

#     text = "\n\n".join(d.page_content for d in docs)
#     return text, True



import os
from functools import lru_cache
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

@lru_cache(maxsize=1)
def get_vector_db(pdf_dir="data/pdfs"):
    # Path relative to the habit_builder folder
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
        raise RuntimeError(f"PDF directory {pdf_dir} was missing and has been created. Add PDFs and restart.")

    docs = []
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_dir, file))
            docs.extend(loader.load())

    if not docs:
        # Create a dummy index or return error to prevent crash
        raise RuntimeError("No PDF documents found in data/pdfs. Please add documents.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.from_documents(chunks, embeddings)

def retrieve_pdf_context(query, k=4):
    try:
        vectordb = get_vector_db()
        docs = vectordb.similarity_search(query, k=k)
        if not docs:
            return "", False
        return "\n\n".join(d.page_content for d in docs), True
    except Exception as e:
        print(f"RAG Error: {e}")
        return "", False

def retrieve_knowledge(query: str) -> str:
    """Standard wrapper for main.py"""
    context, found = retrieve_pdf_context(query)
    return context if found else ""

