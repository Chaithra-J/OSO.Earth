# app/chatbot.py
import os
import textwrap
from typing import List

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

load_dotenv()

# CONFIG
#PDF_FOLDER = os.path.join(os.path.dirname(__file__), "pdfs")
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(APP_DIR, "pdfs")
EMBED_MODEL = os.getenv("EMBED_MODEL", "mxbai-embed-large")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1")
CHROMA_PERSIST_DIR = os.path.join(APP_DIR, "chroma_db")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 900))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 150))
K_RETRIEVE = int(os.getenv("K_RETRIEVE", 4))


def load_all_pdfs(folder: str = PDF_FOLDER):
    docs = []
    if not os.path.isdir(folder):
        return docs
    for fname in os.listdir(folder):
        if not fname.lower().endswith(".pdf"):
            continue
        path = os.path.join(folder, fname)
        loader = PyPDFLoader(path)
        pdf_docs = loader.load()
        for d in pdf_docs:
            d.metadata.setdefault("source", fname)
            if "page" not in d.metadata:
                if "page_number" in d.metadata:
                    d.metadata["page"] = d.metadata["page_number"]
                else:
                    d.metadata["page"] = "?"
            docs.append(d)
    return docs


def create_or_load_vectordb(documents: List, embed_model: str = EMBED_MODEL):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    # If existing DB present, load it
    if os.path.isdir(CHROMA_PERSIST_DIR) and os.listdir(CHROMA_PERSIST_DIR):
        embeddings = OllamaEmbeddings(model=embed_model)
        vectordb = Chroma(embedding_function=embeddings, persist_directory=CHROMA_PERSIST_DIR)
        return vectordb

    # Otherwise split and build
    chunks = text_splitter.split_documents(documents)
    embeddings = OllamaEmbeddings(model=embed_model)
    vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_PERSIST_DIR)
    return vectordb


def build_rag_runnable(retriever, llm_model_name: str = LLM_MODEL):
    llm = ChatOllama(model=llm_model_name)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",
             "You are a helpful assistant. Use ONLY the provided context to answer the question. "
             "If the answer is not present in the context, reply: 'I don't know from the provided documents.' "
             "Be concise (max 3 sentences). Include inline citations like (source.pdf p.4)."),
            ("user", "Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:")
        ]
    )

    rag = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    return rag



def format_context_with_citations(documents):
    parts = []
    for d in documents:
        meta = d.metadata or {}
        source = meta.get("source", "unknown.pdf")
        page = meta.get("page", "?")
        header = f"[source: {source} | page: {page}]"
        text = d.page_content if hasattr(d, "page_content") else str(d)
        snippet = textwrap.shorten(text, width=2000, placeholder=" ...")
        parts.append(f"{header}\n{snippet}")
    return "\n\n".join(parts)


def build_citation_links(documents, server_base="/pdf"):
    """
    Return HTML-friendly citation links (markdown-like).
    Example: [file.pdf p.4](/pdf/file.pdf#page=4)
    """
    out = []
    for d in documents:
        meta = d.metadata or {}
        src = meta.get("source", "unknown.pdf")
        page = meta.get("page", "?")
        link = f"{server_base}/{src}#page={page}"
        out.append({"text": f"{src} p.{page}", "link": link})
    return out


# High-level API function used by the web server
def answer_question(query: str):
    docs = load_all_pdfs()
    if not docs:
        return {"error": "No PDFs found. Put PDFs into app/pdfs/ and restart."}

    vectordb = create_or_load_vectordb(docs)
    retriever = vectordb.as_retriever(search_kwargs={"k": K_RETRIEVE})

    rag = build_rag_runnable(retriever)

    try:
        result = rag.invoke(query)
        answer = result.content
    except Exception as e:
        return {"error": str(e)}

    return {"answer": answer}

