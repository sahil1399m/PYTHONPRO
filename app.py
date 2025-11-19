import streamlit as st
import random
import csv
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# CONFIGURATION
# -------------------------
RESULTS_CSV = "quiz_results.csv"
APP_FOOTER = "Built by SAHIL DESAI | VJTI"

# -------------------------
# QUESTION BANKS
# -------------------------

EASY_QUESTIONS = [
    {"question": "What is the output of print(2+3)?", "options": ["23", "5", "2+3", "Error"], "answer": "5"},
    {"question": "Which symbol is used for comments?", "options": ["//", "#", "/* */", "<!-- -->"], "answer": "#"},
    {"question": "Which datatype is immutable?", "options": ["List", "Dictionary", "Tuple", "Set"], "answer": "Tuple"},
    {"question": "What is the output of print(len('Python'))?", "options": ["5", "6", "7", "Error"], "answer": "6"},
    {"question": "Which is a valid variable name?", "options": ["1name", "_name", "name!", "for"], "answer": "_name"},
]

MEDIUM_QUESTIONS = [
    {"question": "Which loop is entry-controlled?", "options": ["for", "while", "do-while", "loop"], "answer": "for"},
    {"question": "Which keyword breaks loop?", "options": ["stop", "break", "exit", "end"], "answer": "break"},
    {"question": "Default return value of a function?", "options": ["0", "None", "Error", "Empty"], "answer": "None"},
    {"question": "What does lambda define?", "options": ["loop", "anonymous function", "variable", "module"], "answer": "anonymous function"},
    {"question": "Which returns list of dictionary keys?", "options": ["keys()", "allkeys()", "dict.keys()", "getkeys()"], "answer": "dict.keys()"},
]

HARD_QUESTIONS = [
    {"question": "What is __init__ in Python?", "options": ["Destructor", "Constructor", "Function", "Variable"], "answer": "Constructor"},
    {"question": "Which refers to current object?", "options": ["self", "this", "obj", "me"], "answer": "self"},
    {"question": "Stack follows:", "options": ["FIFO", "LIFO", "Random", "Priority"], "answer": "LIFO"},
    {"question": "Queue follows:", "options": ["LIFO", "FIFO", "FILO", "Random"], "answer": "FIFO"},
    {"question": "Linked list consists of:", "options": ["Nodes", "Arrays", "Stacks", "Queues"], "answer": "Nodes"},
]

# -------------------------
# SESSION INITIALIZATION
# -------------------------
def init_session():
    defaults = {
        "user": None,
        "difficulty": None,
        "questions": [],
        "q_index": 0,
        "score": 0,
        "answers": [],
        "question_start": None,
        "finished": False,
        "time_per_question": 30,
        "time_taken": []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def verify_college(c):
    return c.strip().lower() == "vjti"

def verify_regid(r):
    return r.strip().startswith("24109")

# -------------------------
# START QUIZ
# -------------------------
def start_quiz(name, college, regid, difficulty):

    st.session_state.user = {
        "name": name.strip(),
        "college": college.strip(),
        "reg": regid.strip()
    }

    st.session_state.difficulty = difficulty

    if difficulty == "Easy":
        st.session_state.questions = random.sample(EASY_QUESTIONS, 5)
        st.session_state.time_per_question = 30

    elif difficulty == "Medium":
        st.session_state.questions = random.sample(MEDIUM_QUESTIONS, 5)
        st.session_state.time_per_question = 60

    else:
        st.session_state.questions = random.sample(HARD_QUESTIONS, 5)
        st.session_state.time_per_question = 120

    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.time_taken = []
    st.session_state.finished = False
    st.session_state.question_start = time.time()

# -------------------------
# SAVE RESULT
# -------------------------
def save_result_to_csv(user, score, percent, status, difficulty):
    header_needed = False
    try:
        with open(RESULTS_CSV, "r"): pass
    except FileNotFoundError:
        header_needed = True

    with open(RESULTS_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        if header_needed:
            writer.writerow(["Name","College","RegID","Score","Percentage","Status","Difficulty","Timestamp"])

        writer.writerow([
            user["name"], user["college"], user["reg"],
            score, f"{percent:.2f}%", status, difficulty,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

# -------------------------
# PAGE SETUP
# -------------------------
st.set_page_config(page_title="VJTI Python Quiz", page_icon="🧠", layout="wide")
init_session()

# -------------------------
# LOGIN PAGE
# -------------------------
if st.session_state.user is None:

    st.title("🚀 Start Your Python Quiz")
    st.caption("Enter your details to begin the challenge")

    col1, col2 = st.columns([2, 2])

    with col1:
        with st.form("login_form"):

            name = st.text_input("👤 Your Name")
            college = st.text_input("🏫 College Name (enter 'VJTI')")
            regid = st.text_input("🆔 Registration ID (must start with 24109)")
            difficulty = st.selectbox("🎯 Select Difficulty Level", ["Easy","Medium","Hard"])

            submitted = st.form_submit_button("🔥 Start Quiz")

        if submitted:
            if not name or not college or not regid:
                st.warning("⚠ Fill all fields.")
            elif not verify_college(college):
                st.error("❌ Only VJTI students allowed.")
            elif not verify_regid(regid):
                st.error("❌ Registration ID must start with 24109.")
            else:
                start_quiz(name, college, regid, difficulty)
                st.rerun()

    with col2:
        st.subheader("📘 Build Concepts")
        st.write("Click any topic to open GeeksForGeeks:")

        topics = {
            "Python Basics": "https://www.geeksforgeeks.org/python-basics/",
            "Data Types": "https://www.geeksforgeeks.org/python-data-types/",
            "Functions": "https://www.geeksforgeeks.org/python-functions/",
            "Loops": "https://www.geeksforgeeks.org/loops-in-python/",
            "Lists": "https://www.geeksforgeeks.org/python-list/",
            "Stacks": "https://www.geeksforgeeks.org/stack-in-python/",
            "Queues": "https://www.geeksforgeeks.org/queue-in-python/",
        }

        for topic, link in topics.items():
            st.markdown(f"[🔗 {topic}]({link})")

# -------------------------
# QUIZ PAGE
# -------------------------
elif not st.session_state.finished:

    user = st.session_state.user
    q_index = st.session_state.q_index
    TIME_PER_QUESTION = st.session_state.time_per_question
    questions = st.session_state.questions
    current_q = questions[q_index]

    # Timer
    elapsed = time.time() - st.session_state.question_start
    time_left = max(TIME_PER_QUESTION - int(elapsed), 0)

    st.title(f"Question {q_index+1} / {len(questions)}")
    st.progress((q_index + 1) / len(questions))

    col1, col2 = st.columns([3, 1])

    with col2:
        st.subheader("⏳ Time Left")
        st.progress(time_left / TIME_PER_QUESTION)
        st.write(f"**{time_left} seconds**")

        st.markdown("---")
        st.write(f"👤 **{user['name']}**")
        st.write(f"🆔 **{user['reg']}**")
        st.write(f"🎯 **{st.session_state.difficulty}**")
        st.write(f"🏆 Score: **{st.session_state.score}**")

    with col1:
        st.subheader(current_q["question"])

        option = st.radio("Select option:", current_q["options"])

        def handle_answer(opt):
            st.session_state.answers.append(
                {"selected": opt, "correct": current_q["answer"]}
            )
            st.session_state.time_taken.append(TIME_PER_QUESTION - time_left)

        if st.button("Submit"):
            if option == current_q["answer"]:
                st.session_state.score += 1
            handle_answer(option)
            st.session_state.q_index += 1
            st.session_state.question_start = time.time()
            st.rerun()

        if time_left == 0:
            handle_answer(None)
            st.session_state.q_index += 1
            st.session_state.question_start = time.time()
            st.rerun()

    time.sleep(1)
    st.rerun()

# -------------------------
# RESULTS PAGE
# -------------------------
else:
    user = st.session_state.user
    total = len(st.session_state.questions)
    score = st.session_state.score
    percent = (score / total) * 100
    incorrect = total - score

    st.title("🎉 Quiz Completed!")

    st.write(f"**Score:** {score}/{total}")
    st.write(f"**Percentage:** {percent:.2f}%")
    st.write(f"**Difficulty:** {st.session_state.difficulty}")

    # Save CSV once
    if "saved" not in st.session_state:
        save_result_to_csv(user, score, percent, "Done", st.session_state.difficulty)
        st.session_state.saved = True

    # Pie chart
    st.subheader("📊 Performance Pie Chart")
    fig, ax = plt.subplots()
    ax.pie([score, incorrect], labels=["Correct", "Incorrect"], autopct="%1.1f%%")
    st.pyplot(fig)

    # Time Chart
    st.subheader("📈 Time Taken per Question")
    df = pd.DataFrame({"Question": list(range(1, total+1)), "Time": st.session_state.time_taken})
    st.line_chart(df.set_index("Question"))

    # Detailed answers
    st.subheader("📝 Detailed Answers")
    for i, ans in enumerate(st.session_state.answers, 1):
        sel = ans["selected"] if ans["selected"] else "Skipped/Timeout"
        mark = "✅" if sel == ans["correct"] else "❌"
        st.write(f"Q{i}: Selected **{sel}**, Correct **{ans['correct']}** {mark}")

    if st.button("Restart Quiz"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

st.markdown("---")
st.markdown(APP_FOOTER)
