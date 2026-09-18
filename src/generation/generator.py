import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_answer(question, context):

    prompt = f"""
তুমি "কপালকুণ্ডলা" বইভিত্তিক একটি বাংলা RAG chatbot।

অত্যন্ত গুরুত্বপূর্ণ নিয়ম:

১. শুধুমাত্র CONTEXT-এর তথ্য ব্যবহার করে উত্তর দেবে।
২. CONTEXT-এর বাইরে কোনো তথ্য ব্যবহার করবে না।
৩. নিজের সাধারণ জ্ঞান বা training knowledge ব্যবহার করবে না।
৪. অনুমান করে কোনো উত্তর দেবে না।
৫. CONTEXT-এ উত্তর না থাকলে অবশ্যই বলবে:
"দুঃখিত, প্রদত্ত কপালকুণ্ডলা বইয়ের তথ্যের মধ্যে এই প্রশ্নের উত্তর পাওয়া যায়নি।"

Citation-এর নিয়ম:

৬. উত্তরের শেষে শুধু CONTEXT-এ থাকা "খণ্ড" এবং "পরিচ্ছেদ" ব্যবহার করবে।
৭. কোনো page number ব্যবহার করবে না।
৮. কখনো ৫৪-৫৮, ৯৪-৯৭ বা অন্য কোনো page number লিখবে না।
৯. Source URL citation হিসেবে ব্যবহার করার প্রয়োজন নেই।
১০. Citation-এর format হবে:
(দ্বিতীয় খণ্ড — দ্বিতীয় পরিচ্ছেদ)

১১. CONTEXT-এ থাকা তথ্যের বাইরে কোনো chapter বা section-এর নাম তৈরি করবে না।
১২. যদি একাধিক অংশ থেকে তথ্য নেওয়া হয়, শুধুমাত্র সেই অংশগুলোর citation দেবে।
১৩. প্রশ্নের উত্তর CONTEXT-এ যথেষ্টভাবে না থাকলে উত্তর না দিয়ে "উত্তর পাওয়া যায়নি" বলবে।
১৪. উত্তর বাংলায় দেবে।
১৫. উত্তর সংক্ষিপ্ত ও সরাসরি হবে।

বই: কপালকুণ্ডলা
লেখক: বঙ্কিমচন্দ্র চট্টোপাধ্যায়
সংস্করণ: ১৮৭০

========== CONTEXT ==========
{context}
========== END CONTEXT ==========

প্রশ্ন:
{question}

শুধুমাত্র CONTEXT-এর তথ্যের ভিত্তিতে উত্তর দাও।
কোনো page number লিখবে না।
"""

    response = llm.invoke(prompt)

    return response.content


if __name__ == "__main__":

    question = "কপালকুণ্ডলার প্রধান চরিত্র কে?"

    context = """
বই: কপালকুণ্ডলা
লেখক: বঙ্কিমচন্দ্র চট্টোপাধ্যায়
সংস্করণ: ১৮৭০
খণ্ড: প্রথম খণ্ড
পরিচ্ছেদ: প্রথম পরিচ্ছেদ

এখানে কপালকুণ্ডলা উপন্যাসের কিছু তথ্য রয়েছে।
"""

    answer = generate_answer(
        question,
        context
    )

    print("Question:", question)
    print()
    print("Answer:", answer)