from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3",
    temperature=0.3
)

def create_study_plan(branch, semester, exam_date, weak_subjects):
    prompt = f"""
    Create a personalized study plan.

    Branch: {branch}
    Semester: {semester}
    Exam Date: {exam_date}
    Weak Subjects: {weak_subjects}

    Give daily schedule and revision strategy.
    """

    return llm.predict(prompt)
