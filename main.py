from src.retrieval.retriever import retriever
from src.generation.generator import generate_answer


def ask_question(question):
    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    answer = generate_answer(question, context)

    return answer


if __name__ == "__main__":
    question = input("আপনার প্রশ্ন: ")

    answer = ask_question(question)

    print("\nউত্তর:")
    print(answer)