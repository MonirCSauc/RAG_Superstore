````markdown
# RAG Superstore Sales Analyst

## 📌 Project Overview

RAG Superstore Sales Analyst is a Python-based Retrieval-Augmented Generation system designed to answer business questions about the **Sample Superstore** sales dataset.

The system converts structured sales data into natural-language business documents, stores them in a vector database, retrieves the most relevant context for a user question, and uses a local LLM to generate clear analytical answers.

This project demonstrates how RAG can be applied to business intelligence and data analysis tasks, allowing users to ask questions about sales, profit, regions, product categories, discounts, seasonality, and trends in natural language.

## 🎯 Project Goal

The main goal of this project is to build a local AI-powered sales analyst that can answer questions such as:

- What is the sales trend over the 4-year period?
- Which months show the highest sales?
- Which product category generates the most revenue?
- Which region has the best sales performance?
- Which cities are the top performers?
- What products are frequently sold at a discount?
- How does the West region compare to the East in terms of profit?

Instead of manually querying the dataset, the user can ask questions directly and receive interpreted answers supported by retrieved data context.

## 🧠 What is RAG?

Retrieval-Augmented Generation, or RAG, combines information retrieval with text generation.

In this project, the system works as follows:

1. The Superstore dataset is converted into text documents.
2. Each document is embedded using a sentence-transformer model.
3. The embeddings are stored in ChromaDB.
4. When the user asks a question, the system retrieves the most relevant documents.
5. The retrieved context is passed to a local LLM.
6. The LLM generates a business-style answer based on the retrieved data.

## 📊 Dataset

The project uses the **Sample Superstore** dataset.

The dataset contains sales transaction records with information such as:

- Order date
- Ship date
- Customer name
- Segment
- Product name
- Category
- Sub-category
- Ship mode
- City
- State
- Region
- Sales
- Quantity
- Discount
- Profit

The dataset is stored in:

```text
data/Sample_Superstore.csv
````

## 🧾 Document Generation

The raw CSV data is transformed into multiple types of text documents to make retrieval more effective.

The generated documents include:

* Transaction-level records
* Monthly sales summaries
* Category and sub-category summaries
* Region and state performance summaries
* Yearly sales trend summaries
* Seasonality summaries
* Product discount summaries
* City performance summaries
* Category yearly trend summaries

The processed text documents are saved as:

```text
data/sales_documents.csv
```

## 🏗️ System Architecture

```text
Sample_Superstore.csv
        |
        v
prepare_data.py
        |
        v
sales_documents.csv
        |
        v
build_vector_db.py
        |
        v
ChromaDB Vector Store
        |
        v
rag_app.py
        |
        v
User Question → Retrieved Context → LLM Answer
```

## 📁 Project Structure

```text
RAG_Superstore/
│
├── data/
│   ├── Sample_Superstore.csv          # Original Superstore dataset
│   └── sales_documents.csv            # Generated text documents
│
├── chroma_db/                         # Persistent ChromaDB vector database
│
├── src/
│   ├── prepare_data.py                # Converts CSV rows and summaries into text documents
│   ├── build_vector_db.py             # Creates embeddings and stores them in ChromaDB
│   ├── rag_app.py                     # Main RAG application for question answering
│   └── test_queries.py                # Runs predefined evaluation questions
│
├── test_results_20260428_184354.json  # Saved test output
├── test_results_20260428_191402.json  # Saved test output
├── requierments.txt                   # Project dependencies
└── README.md
```

> Note: The dependency file is currently named `requierments.txt`. A recommended improvement is to rename it to `requirements.txt`.

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* ChromaDB
* Sentence Transformers
* LangChain
* LangChain Community
* LangChain Ollama
* Ollama
* Llama 3.2 3B
* tqdm

## 🤖 Models Used

### Embedding Model

```text
all-MiniLM-L6-v2
```

This model is used to convert the generated sales documents and user questions into vector embeddings.

### Language Model

```text
llama3.2:3b
```

The project uses Ollama to run the local language model.

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MonirCSauc/RAG_Superstore.git
cd RAG_Superstore
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

The repo currently contains a file named `requierments.txt`.

```bash
pip install -r requierments.txt
```

If you rename it to the standard spelling, use:

```bash
pip install -r requirements.txt
```

### 4. Install and Run Ollama

Make sure Ollama is installed on your machine.

Then pull the required model:

```bash
ollama pull llama3.2:3b
```

## 🚀 How to Run the Project

### Step 1: Prepare the Data

Convert the structured Superstore CSV into natural-language documents:

```bash
python src/prepare_data.py
```

This creates:

```text
data/sales_documents.csv
```

### Step 2: Build the Vector Database

Generate embeddings and store the document chunks in ChromaDB:

```bash
python src/build_vector_db.py
```

This creates or updates the persistent vector database in:

```text
chroma_db/
```

### Step 3: Run the RAG App

Start the interactive question-answering system:

```bash
python src/rag_app.py
```

You can then ask questions such as:

```text
Which region has the best sales performance?
```

```text
Compare Technology vs Furniture sales trends.
```

```text
Which cities are the top performers?
```

To stop the app, type:

```text
exit
```

To clear conversation history, type:

```text
reset
```

## 🧪 Running Test Queries

The project includes a testing script with predefined business questions.

Run:

```bash
python src/test_queries.py
```

The script asks several questions, generates answers, and saves the results in a timestamped JSON file.

Example tested questions include:

* What is the sales trend over the 4-year period?
* Which months show the highest sales?
* Which product category generates the most revenue?
* What sub-categories have the highest profit margins?
* Which products are frequently sold at a discount?
* Which region has the best sales performance?
* Compare sales performance across different states.
* Which cities are the top performers?
* Compare Technology vs Furniture sales trends.
* How does the West region compare to the East in terms of profit?

## 🔍 Retrieval Logic

The system includes basic query routing and filtering.

It can detect keywords related to:

* Years from 2014 to 2017
* Regions such as West, East, Central, and South
* Categories such as Furniture, Technology, and Office Supplies
* Document types such as city summaries, state summaries, monthly summaries, yearly trends, discount summaries, and category summaries

This improves retrieval by selecting more relevant documents from the vector database before generating the final answer.

## 📌 Example Questions

```text
What is the sales trend over the 4-year period?
```

```text
Which months show the highest sales? Is there seasonality?
```

```text
Which product category generates the most revenue?
```

```text
What sub-categories have the highest profit margins?
```

```text
Which products are frequently sold at a discount?
```

```text
Which region has the best sales performance?
```

```text
Compare sales performance across different states.
```

```text
Which cities are the top performers?
```

```text
Compare Technology vs Furniture sales trends.
```

```text
How does the West region compare to the East in terms of profit?
```

## 📈 Key Features

* Converts structured CSV data into natural-language documents
* Generates transaction-level and summary-level documents
* Uses ChromaDB for persistent vector storage
* Uses sentence-transformer embeddings for semantic search
* Uses Ollama with Llama 3.2 3B for local response generation
* Supports interactive question answering
* Maintains short conversation history
* Includes query filtering for years, categories, regions, and document types
* Includes a test script for evaluating multiple business questions

## ✅ Strengths of the Project

* Runs locally using Ollama
* Does not require a paid API key
* Combines structured data analysis with natural-language querying
* Uses multiple document types to improve retrieval quality
* Demonstrates a practical business intelligence use case for RAG
* Stores the vector database persistently using ChromaDB

## ⚠️ Limitations

* Some answers may depend heavily on retrieval quality.
* The system may occasionally retrieve incomplete context for broad comparison questions.
* The LLM may need stronger prompting or post-processing for precise numerical analysis.
* The current system does not directly run SQL or Pandas calculations at query time.
* The dependency file name is misspelled as `requierments.txt`.
* The project currently runs through the command line and does not include a web interface.


## 👥 Authors

* Ahmed M. Monir

