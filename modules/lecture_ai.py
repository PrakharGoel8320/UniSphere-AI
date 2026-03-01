from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3",
    temperature=0.3
)

def summarize_notes(text):
    prompt = f"""
    Summarize the lecture.
    Give revision notes.
    List important topics.
    Create exam questions.

    Lecture:
    {text}
    """

    return llm.predict(prompt)
