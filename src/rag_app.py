import re
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_ollama import OllamaLLM

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "sales_data"
MODEL_NAME = "llama3.2:3b"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name=COLLECTION_NAME)
llm = OllamaLLM(model=MODEL_NAME)

YEAR_PATTERN = re.compile(r'\b(201[4-7])\b')

DOC_TYPE_ROUTING = {
    "cities": "city_total_summary",
    "city": "city_total_summary",
    "states": "state_total_summary",
    "state": "state_total_summary",
    "monthly": "monthly_summary",
    "month": "seasonality_summary",
    "profit": "yearly_summary",
    "seasonality": "seasonality_summary",
    "seasonal": "seasonality_summary",
    "season": "seasonality_summary",
    "yearly": "yearly_summary",
    "trend": "yearly_summary",
    "annual": "yearly_summary",
    "discount": "product_discount_summary",
    "discounted": "product_discount_summary",
    "sub-categor": "category_summary",
    "subcategor": "category_summary",
    "profit margin": "category_summary",
}

CATEGORY_KEYWORDS = ["furniture", "technology", "office supplies"]
REGION_KEYWORDS = ["west", "east", "central", "south"]


def extract_filters(question):
    q = question.lower()
    filters = []

    year_match = YEAR_PATTERN.search(question)
    if year_match:
        filters.append({"year": {"$eq": int(year_match.group())}})

    for region in REGION_KEYWORDS:
        if region in q:
            filters.append({"region": {"$eq": region.title()}})
            break

    for cat in CATEGORY_KEYWORDS:
        if cat in q:
            filters.append({"category": {"$eq": cat.title()}})
            break

    for keyword, doc_type in DOC_TYPE_ROUTING.items():
        if keyword in q:
            return {"doc_type": {"$eq": doc_type}}

    if len(filters) == 1:
        return filters[0]
    elif len(filters) > 1:
        return {"$and": filters}
    return None


def retrieve_context(question, top_k=15):
    q = question.lower()
    is_comparison = any(w in q for w in ["compare", "vs", "versus", "difference between"])

    if is_comparison:
        top_k = 25
        where_filter = None
        year_match = YEAR_PATTERN.search(question)
        if year_match:
            where_filter = {"year": {"$eq": int(year_match.group())}}
    else:
        where_filter = extract_filters(question)

    question_embedding = embedding_model.encode([question]).tolist()[0]

    query_kwargs = {
        "query_embeddings": [question_embedding],
        "n_results": top_k,
    }
    if where_filter:
        query_kwargs["where"] = where_filter

    try:
        results = collection.query(**query_kwargs)
    except Exception:
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=top_k
        )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []
    for doc, meta in zip(documents, metadatas):
        context_parts.append(f"[{meta.get('doc_type', 'unknown')}] {doc}")

    return "\n\n".join(context_parts)


def generate_answer(question, conversation_history=None):
    context = retrieve_context(question)

    history_text = ""
    if conversation_history:
        for turn in conversation_history[-3:]:
            history_text += f"User: {turn['question']}\nAssistant: {turn['answer']}\n\n"

    prompt = f"""You are a professional data analyst.

Rules:
- Always interpret the numbers, not just list them.
- If numbers show a trend, describe it clearly (increase, decrease, peak, etc.).
- Always include units ($ for sales, % for margins).
- Never confuse sales with profit.
- Format answers clearly using bullet points or rankings.
- Do NOT say "not enough data" if relevant numbers exist in the context.

{f"Previous conversation:{chr(10)}{history_text}" if history_text else ""}
Context:
{context}

Question: {question}

Answer:"""

    return llm.invoke(prompt).strip()


def main():
    print("RAG Sales Data Analyst")
    print("Type 'exit' to stop, 'reset' to clear history.\n")

    conversation_history = []

    while True:
        question = input("Ask a question: ").strip()

        if question.lower() == "exit":
            break
        if question.lower() == "reset":
            conversation_history = []
            print("Conversation history cleared.\n")
            continue
        if not question:
            continue

        answer = generate_answer(question, conversation_history)
        conversation_history.append({"question": question, "answer": answer})

        print("\nAnswer:")
        print(answer)
        print("-" * 80)


if __name__ == "__main__":
    main()