# 📚 Bangla RAG Chatbot

## 📖 Book Information

* **Book Title:** কপালকুণ্ডলা
* **Author:** বঙ্কিমচন্দ্র চট্টোপাধ্যায়
* **Edition:** ১৮৭০
* **Bengali Wikisource:** https://bn.wikisource.org/wiki/কপালকুণ্ডলা

**Brief Description:**
কপালকুণ্ডলা বঙ্কিমচন্দ্র চট্টোপাধ্যায় রচিত একটি বাংলা prose novel। এই project-এ বইটির সম্পূর্ণ ৩২টি পরিচ্ছেদ সংগ্রহ করে একটি RAG-based Knowledge Base Chatbot তৈরি করা হয়েছে।

---

# ⚙️ Setup & Running Instructions

## Required Python Version

```text
Python 3.14.3
```

## Installation

Create a virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file and add the Groq API key:

```text
GROQ_API_KEY=your_api_key_here
```

## Run the Chatbot

```powershell
streamlit run app.py
```

---

# 🛠️ Technical Details

## Embedding Model

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### Why this model?

The book and user questions are in Bengali. Therefore, a multilingual embedding model was selected instead of an English-only embedding model.

`paraphrase-multilingual-MiniLM-L12-v2` supports multilingual semantic representation and is suitable for Bengali text retrieval.

## Chunking

### Main Chunking Strategy

* **Chunk Size:** 800 characters
* **Chunk Overlap:** 100 characters
* **Total Chunks:** 50

The book text is divided into smaller overlapping chunks so that relevant passages can be efficiently retrieved while maintaining contextual continuity.

## Preprocessing

The complete book was collected chapter by chapter from Bengali Wikisource.

During preprocessing:

* Chapter text was cleaned.
* Book metadata was preserved.
* Volume and chapter information was preserved.
* Source URL was preserved.
* Unnecessary metadata was removed from the text used for embeddings.

## Vector Database

**ChromaDB** is used as the vector database.

The generated embeddings are stored in ChromaDB and used for semantic similarity search.

## Retriever Configuration

The project uses a LangChain retriever with ChromaDB.

```python
retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 3
    }
)
```

The system retrieves the top 3 relevant chunks for each user question.

## LLM

The project uses:

```text
openai/gpt-oss-20b
```

through the Groq API.

The LLM is instructed to answer only from the retrieved book context and to clearly state when the requested information is not available in the book.

---

# 🔗 RAG Pipeline

The overall workflow is:

```text
Wikisource
    ↓
Crawling
    ↓
Cleaning
    ↓
Chunking
    ↓
Embeddings
    ↓
Chroma Vector DB
    ↓
Retrieval
    ↓
LLM
    ↓
Answer + Citation
```

The chatbot retrieves relevant passages from the selected book and generates answers using only the retrieved context. Each answer includes the relevant volume/chapter citation.

---

## Chunking Strategy Comparison

As a bonus experiment, two different chunking strategies were compared to evaluate their effect on evidence retrieval.

## Approach A

* **Chunk Size:** 800 characters
* **Chunk Overlap:** 100 characters
* **Total Chunks:** 50
* **Vector Database:** ChromaDB
* **Evidence Retrieval Hit Rate:** 50.0%

## Approach B

* **Chunk Size:** 500 characters
* **Chunk Overlap:** 100 characters
* **Total Chunks:** 73
* **Vector Database:** ChromaDB
* **Evidence Retrieval Hit Rate:** 87.5%

## Comparison Result

| Strategy   |     Chunk Size | Overlap | Total Chunks | Hit Rate |
| ---------- | -------------: | ------: | -----------: | -------: |
| Approach A | 800 characters |     100 |           50 |    50.0% |
| Approach B | 500 characters |     100 |           73 |    87.5% |

**Difference:** +37.5 percentage points in favor of Approach B in this benchmark.

The evaluation used 8 Bengali benchmark questions and checked
