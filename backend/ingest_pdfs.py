from pdf_rag import ingest_texts

with open("data/habit_knowledge.txt", "r") as f:
    texts = [line.strip() for line in f if line.strip()]

ingest_texts(texts)
print("✅ Text knowledge ingested successfully")
