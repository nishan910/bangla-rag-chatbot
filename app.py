import streamlit as st

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.generation.generator import generate_answer


PERSIST_DIRECTORY = "data/processed/chroma_db"

EMBEDDING_MODEL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


st.set_page_config(
    page_title="কপালকুণ্ডলা RAG Chatbot",
    page_icon="📚"
)


st.title("📚 Bangla RAG Chatbot")

st.write(
    "বঙ্কিমচন্দ্র চট্টোপাধ্যায়ের "
    "কপালকুণ্ডলা (১৮৭০) বইভিত্তিক প্রশ্ন করুন।"
)


@st.cache_resource
def load_vector_store():

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    return Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )


vector_store = load_vector_store()

retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 3
    }
)


question = st.chat_input(
    "কপালকুণ্ডলা সম্পর্কে প্রশ্ন লিখুন..."
)


if question:

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "বই থেকে তথ্য খোঁজা হচ্ছে..."
        ):

            docs = retriever.invoke(
                question
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

            if context.strip():

                answer = generate_answer(
                    question,
                    context
                )

            else:

                answer = (
                    "দুঃখিত, প্রদত্ত কপালকুণ্ডলা "
                    "বইয়ের তথ্যের মধ্যে এই প্রশ্নের "
                    "উত্তর পাওয়া যায়নি।"
                )

        st.write(answer)