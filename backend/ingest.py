from rag import ingest_sources

with open("data/habit_knowledge.txt") as f:
    texts = [l.strip() for l in f if l.strip()]

ingest_sources(texts)
print("✅ Habit knowledge ingested")
