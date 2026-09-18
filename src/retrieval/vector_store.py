from pathlib import Path
import json

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


CHUNKS_FILE = Path("data/processed/chunks.json")
PERSIST_DIRECTORY = "data/processed/chroma_db"

EMBEDDING_MODEL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def main():

    if not CHUNKS_FILE.exists():
        print("ERROR: chunks.json পাওয়া যায়নি।")
        return

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        chunks = json.load(file)

    print(f"মোট chunks পাওয়া গেছে: {len(chunks)}")
    print("Embedding model load হচ্ছে...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    texts = []
    metadatas = []

    for item in chunks:

        texts.append(item["text"])

        metadata = item["metadata"].copy()
        metadata["chunk_id"] = item["chunk_id"]

        metadatas.append(metadata)

    print("Vector database তৈরি হচ্ছে...")

    vector_store = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=PERSIST_DIRECTORY
    )

    print()
    print("================================")
    print("Vector database তৈরি সম্পন্ন।")
    print(f"Total chunks embedded: {len(texts)}")
    print(f"Saved to: {PERSIST_DIRECTORY}")
    print("================================")


if __name__ == "__main__":
    main()