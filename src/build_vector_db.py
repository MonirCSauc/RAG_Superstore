import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load documents
df = pd.read_csv("data/sales_documents.csv")

# Initialize ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(name="sales_data")


# def chunk_text(text, chunk_size=500):
#     chunks = []
#     for i in range(0, len(text), chunk_size):
#         chunks.append(text[i:i + chunk_size])
#     return chunks

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into chunks at sentence boundaries where possible.
    overlap: number of characters to repeat at the start of the next chunk
    for continuity.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:])
            break
        # Try to break at the last sentence boundary (. ! ?) within the window
        boundary = max(
            text.rfind(". ", start, end),
            text.rfind("! ", start, end),
            text.rfind("? ", start, end),
        )
        if boundary != -1 and boundary > start:
            chunks.append(text[start:boundary + 1])
            start = boundary + 1 - overlap  # step back slightly for overlap
        else:
            chunks.append(text[start:end])
            start = end - overlap
        start = max(start, 0)
    return chunks

ids = []
documents = []
metadatas = []

counter = 0

for _, row in tqdm(df.iterrows(), total=len(df)):
    chunks = chunk_text(row["text"], chunk_size=500, overlap=50)

    for chunk in chunks:
        ids.append(str(counter))
        documents.append(chunk)

        metadata = {
            "doc_type": row["doc_type"],
            "year": int(row["year"]),
            "month": int(row["month"]),
            "category": row["category"],
            "region": row["region"]
        }

        metadatas.append(metadata)
        counter += 1

# Generate embeddings
embeddings = model.encode(documents, show_progress_bar=True)

# Store in ChromaDB
embeddings = embeddings.tolist()

batch_size = 5000

for start in range(0, len(documents), batch_size):
    end = start + batch_size

    collection.add(
        ids=ids[start:end],
        documents=documents[start:end],
        embeddings=embeddings[start:end],
        metadatas=metadatas[start:end]
    )

    print(f"Added chunks {start} to {min(end, len(documents))}")

print(f"Stored {len(documents)} chunks in vector DB")
