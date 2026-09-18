from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


EMBEDDING_MODEL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

DB_A = "data/processed/chroma_db"
DB_B = "data/processed/chroma_db_500"


BENCHMARK = [
    {
        "question": "নবকুমার কপালকুণ্ডলাকে কোথায় প্রথম দেখেছিল?",
        "evidence": ["কপালকুণ্ডলা", "নবকুমার"],
    },
    {
        "question": "কপালকুণ্ডলার সঙ্গে নবকুমারের বিবাহ হয়েছিল কি?",
        "evidence": ["বিবাহ", "নবকুমার", "কপালকুণ্ডলা"],
    },
    {
        "question": "লুৎফ্-উন্নিসা কপালকুণ্ডলার সঙ্গে দেখা করেছিল কি?",
        "evidence": ["লুৎফ", "উন্নিসা", "কপালকুণ্ডলা"],
    },
    {
        "question": "কাপালিকের সঙ্গে নবকুমারের দেখা হয়েছিল কি?",
        "evidence": ["কাপালিক", "নবকুমার"],
    },
    {
        "question": "কপালকুণ্ডলা ব্রাহ্মণবেশীর সঙ্গে কথা বলেছিল কি?",
        "evidence": ["ব্রাহ্মণবেশী", "কপালকুণ্ডলা"],
    },
    {
        "question": "নবকুমারের সঙ্গে কপালকুণ্ডলার সম্পর্ক কী ছিল?",
        "evidence": ["নবকুমার", "কপালকুণ্ডলা"],
    },
    {
        "question": "কপালিক কপালকুণ্ডলাকে কী করতে বলেছিল?",
        "evidence": ["কাপালিক", "কপালকুণ্ডলা"],
    },
    {
        "question": "কপালকুণ্ডলার পিতার পরিচয় কী?",
        "evidence": ["কপালকুণ্ডলা", "পিতা"],
    },
]


def test_database(db_path):

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    hits = 0

    print("\n" + "=" * 70)
    print(f"Database: {db_path}")
    print("=" * 70)

    for i, item in enumerate(BENCHMARK, 1):

        docs = retriever.invoke(item["question"])

        retrieved_text = "\n".join(
            doc.page_content for doc in docs
        )

        matched_evidence = [
            phrase
            for phrase in item["evidence"]
            if phrase in retrieved_text
        ]

        hit = len(matched_evidence) >= 2

        if hit:
            hits += 1

        print(f"\n{i}. {item['question']}")
        print(
            "Evidence:",
            ", ".join(item["evidence"])
        )
        print(
            "Matched:",
            ", ".join(matched_evidence)
            if matched_evidence
            else "None"
        )
        print(
            "Result:",
            "HIT" if hit else "MISS"
        )

    hit_rate = (
        hits / len(BENCHMARK)
    ) * 100

    print("\n" + "-" * 70)
    print(
        f"Correct Hits: "
        f"{hits} / {len(BENCHMARK)}"
    )
    print(
        f"Hit Rate: "
        f"{hit_rate:.1f}%"
    )
    print("-" * 70)

    return hit_rate


if __name__ == "__main__":

    print(
        "\nBONUS: CHUNKING STRATEGY "
        "EVIDENCE RETRIEVAL COMPARISON"
    )

    rate_a = test_database(DB_A)

    rate_b = test_database(DB_B)

    print("\n" + "=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)

    print(
        f"Approach A (800/100): "
        f"{rate_a:.1f}%"
    )

    print(
        f"Approach B (500/100): "
        f"{rate_b:.1f}%"
    )

    difference = rate_b - rate_a

    print(
        f"Difference: "
        f"{difference:+.1f} percentage points"
    )

    print("=" * 70)
