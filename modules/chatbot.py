from langchain_ollama import ChatOllama
from modules.rag_engine import RAGEngine

# Load once globally
llm = ChatOllama(
    model="llama3",
    temperature=0.7
)

rag_engine = RAGEngine()


# ==================================
# GENERAL CHAT
# ==================================
def general_chat(prompt):

    response = llm.invoke(prompt)

    return response.content


# ==================================
# LECTURE SUMMARIZER
# ==================================
def lecture_summarizer(notes):

    prompt = f"""
    You are a university lecture assistant.

    Summarize the following lecture notes clearly
    using headings and bullet points.

    Lecture Notes:
    {notes}
    """

    response = llm.invoke(prompt)

    return response.content


# ==================================
# STUDY PLANNER
# ==================================
def study_planner(goal):

    prompt = f"""
    Create a smart university study plan.

    Goal: {goal}

    Provide:
    - Daily schedule
    - Weekly milestones
    - Revision strategy
    """

    response = llm.invoke(prompt)

    return response.content


# ==================================
# UNIVERSITY KNOWLEDGE QA (RAG)
# ==================================
def university_qa(question):

    return rag_engine.query(question)


# ==================================
# AI MODE ROUTER ⭐
# ==================================
def ask_ai(prompt, mode="General AI"):

    if mode == "Lecture Summarizer":
        return lecture_summarizer(prompt)

    elif mode == "Study Planner":
        return study_planner(prompt)

    elif mode == "University QA":
        return university_qa(prompt)

    else:
        return general_chat(prompt)
