from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.generation.generator import generate_answer


PERSIST_DIRECTORY = "data/processed/chroma_db"

EMBEDDING_MODEL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def main():

    print("Embedding model load হচ্ছে...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 3
        }
    )

    query = input(
        "\nকপালকুণ্ডলা সম্পর্কে প্রশ্ন লিখুন: "
    )

    docs = retriever.invoke(query)

    print(
        "\nRetrieved documents:",
        len(docs)
    )

    context_parts = []

    for doc in docs:

        volume = doc.metadata.get(
            "volume",
            ""
        )

        chapter = doc.metadata.get(
            "chapter",
            ""
        )

        source = doc.metadata.get(
            "source",
            ""
        )

        context_parts.append(
            f"""
খণ্ড: {volume}
পরিচ্ছেদ: {chapter}
Source: {source}

{doc.page_content}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    if not context.strip():

        print()
        print("================================")
        print("উত্তর")
        print("================================")
        print(
            "দুঃখিত, প্রদত্ত কপালকুণ্ডলা বইয়ের "
            "তথ্যের মধ্যে এই প্রশ্নের উত্তর পাওয়া যায়নি।"
        )
        return

    answer = generate_answer(
        query,
        context
    )

    print()
    print("================================")
    print("উত্তর")
    print("================================")
    print(answer)


if __name__ == "__main__":
    main()