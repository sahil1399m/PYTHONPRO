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
# QUESTION BANKS (EASY / MEDIUM / HARD)
# -------------------------

EASY_QUESTIONS = [
    {"question": "What is the output of print(2+3)?",
     "options": ["23", "5", "2+3", "Error"], "answer": "5"},
    {"question": "Which symbol is used for comments?",
     "options": ["//", "#", "/* */", "<!-- -->"], "answer": "#"},
    {"question": "Which datatype is immutable?",
     "options": ["List", "Dictionary", "Tuple", "Set"], "answer": "Tuple"},
    {"question": "What is the output of print(len('Python'))?",
     "options": ["5", "6", "7", "Error"], "answer": "6"},
    {"question": "Which is a valid variable name?",
     "options": ["1name", "_name", "name!", "for"], "answer": "_name"},
    {"question": "What is the output of print(10//3)?",
     "options": ["3.33", "3", "4", "0"], "answer": "3"},
    {"question": "Which operator is used for exponent?",
     "options": ["^", "**", "exp()", "%"], "answer": "**"},
    {"question": "Output of print(10 % 3)?",
     "options": ["1", "3", "0", "10"], "answer": "1"},
    {"question": "Which function converts data to string?",
     "options": ["str()", "int()", "float()", "ord()"], "answer": "str()"},
    {"question": "What is the output of print('A' * 3)?",
     "options": ["AAA", "A3", "Error", "A*A*A"], "answer": "AAA"},
    {"question": "Which removes last element from list?",
     "options": ["remove()", "del()", "pop()", "discard()"], "answer": "pop()"},
    {"question": "Which is a list?",
     "options": ["(1,2,3)", "[1,2,3]", "{1,2,3}", "<1,2,3>"], "answer": "[1,2,3]"},
    {"question": "Output of print([1,2]*2)?",
     "options": ["[1,2,1,2]", "[2,4]", "Error", "[1,2][1,2]"],
     "answer": "[1,2,1,2]"},
    {"question": "Which creates an empty dictionary?",
     "options": ["[]", "{}", "dict()", "()"], "answer": "{}"},
    {"question": "What is output of print(3*'Hi')?",
     "options": ["HiHiHi", "Hi3", "Error", "Hi"], "answer": "HiHiHi"},
    {"question": "Which method splits a string?",
     "options": ["join()", "cut()", "split()", "strip()"], "answer": "split()"},
    {"question": "Which method removes whitespace?",
     "options": ["strip()", "trim()", "clean()", "rstrip()"], "answer": "strip()"},
    {"question": "Output of print(type([]))?",
     "options": ["list", "<class 'list'>", "[]", "<list>"], "answer": "<class 'list'>"},
    {"question": "What does len([1,2,3]) return?",
     "options": ["1", "2", "3", "Error"], "answer": "3"},
    {"question": "Which is a boolean value?",
     "options": ["TRUE", "Yes", "True", "1"], "answer": "True"},
    {"question": "What is the output of print(5 > 3)?",
     "options": ["True", "False", "5>3", "None"], "answer": "True"},
    {"question": "Which datatype stores unique values?",
     "options": ["List", "Tuple", "Dictionary", "Set"], "answer": "Set"},
    {"question": "What is the output of print(None == 0)?",
     "options": ["True", "False", "None", "0"], "answer": "False"},
    {"question": "Output of print('2' + '3')?",
     "options": ["23", "5", "Error", "None"], "answer": "23"},
    {"question": "Output of print(10 < 20 < 30)?",
     "options": ["True", "False", "Error", "None"], "answer": "True"},
    {"question": "Output of print(ord('A'))?",
     "options": ["65", "97", "A", "Error"], "answer": "65"},
    {"question": "Which function returns max value?",
     "options": ["big()", "max()", "largest()", "high()"], "answer": "max()"},
    {"question": "Which creates tuple?",
     "options": ["(1,)", "(1)", "[1]", "{1}"], "answer": "(1,)"},
    {"question": "Which keyword is used for else-if?",
     "options": ["elseif", "elif", "else_if", "elif()"], "answer": "elif"},
]

# MEDIUM_QUESTIONS and HARD_QUESTIONS continue...
# (Your full set exactly as you already wrote)
# I am NOT rewriting here to save space — your code uses them 100% correctly.

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
        "time_taken": []        # <<< NEW for line chart
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

    # Select question bank
    if difficulty == "Easy":
        st.session_state.questions = random.sample(EASY_QUESTIONS, 15)
        st.session_state.time_per_question = 30

    elif difficulty == "Medium":
        st.session_state.questions = random.sample(MEDIUM_QUESTIONS, 15)
        st.session_state.time_per_question = 60

    else:
        st.session_state.questions = random.sample(HARD_QUESTIONS, 15)
        st.session_state.time_per_question = 120

    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.time_taken = []   # Reset time taken list
    st.session_state.finished = False
    st.session_state.question_start = time.time()

# -------------------------
# SAVE RESULT
# -------------------------


def save_result_to_csv(user, score, percent, status, difficulty):
    header_needed = False

    try:
        with open(RESULTS_CSV, "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        header_needed = True

    with open(RESULTS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header_needed:
            writer.writerow(["Name", "College", "RegID",
                             "Score", "Percentage", "Status", "Difficulty",
                             "Timestamp"])

        writer.writerow([
            user["name"], user["college"], user["reg"],
            score, f"{percent:.2f}%", status, difficulty,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

# -------------------------
# PAGE SETUP
# -------------------------


st.set_page_config(page_title="VJTI Python Quiz", page_icon="🧠", layout="wide")
st.title("🧠 VJTI Python Quiz")
st.caption("Quiz with Difficulty Levels • Python MCQs • 15 Questions")

init_session()

# -------------------------
# LOGIN PAGE
# -------------------------

if st.session_state.user is None:
    with st.form("login_form"):
        name = st.text_input("Your Name")
        college = st.text_input("College Name (enter 'VJTI')")
        regid = st.text_input("Registration ID (must start with 24109)")
        difficulty = st.selectbox(
            "Select Difficulty Level:", ["Easy", "Medium", "Hard"])

        submitted = st.form_submit_button("Start Quiz")

    if submitted:
        if not name or not college or not regid:
            st.warning("Please fill all fields.")
        elif not verify_college(college):
            st.error("Only VJTI students allowed.")
        elif not verify_regid(regid):
            st.error("RegID must start with 24109.")
        else:
            start_quiz(name, college, regid, difficulty)
            st.rerun()

# -------------------------
# QUIZ PAGE
# -------------------------

elif not st.session_state.finished:

    user = st.session_state.user
    q_index = st.session_state.q_index
    TIME_PER_QUESTION = st.session_state.time_per_question
    questions = st.session_state.questions

    if q_index >= len(questions):
        st.session_state.finished = True
        st.rerun()

    current_q = questions[q_index]

    # Sidebar
    with st.sidebar:
        st.header("📘 Student Info")
        st.write(f"**Name:** {user['name']}")
        st.write(f"**Reg ID:** {user['reg']}")
        st.write(f"**Difficulty:** {st.session_state.difficulty}")
        st.write("---")
        st.subheader("📊 Progress")
        st.write(f"Question: {q_index+1}/15")
        st.write(f"Score: {st.session_state.score}")

    # Timer
    elapsed = time.time() - st.session_state.question_start
    time_left = max(TIME_PER_QUESTION - int(elapsed), 0)

    st.write(f"⏳ **Time Left: {time_left}s**")
    st.progress(time_left / TIME_PER_QUESTION)

    st.subheader(f"Question {q_index+1}")
    st.write(current_q["question"])

    option = st.radio(
        "Choose an option:",
        current_q["options"],
        key=f"opt_{q_index}_{abs(hash(current_q['question']))}"
    )

    col1, col2 = st.columns(2)
    submit = col1.button("Submit")
    skip = col2.button("Skip")

    # Process Answer
    def handle_answer(selected):
        st.session_state.answers.append(
            {"selected": selected, "correct": current_q["answer"]})

        # Store time taken
        st.session_state.time_taken.append(
            TIME_PER_QUESTION - time_left
        )

    if submit:
        selected = option if time_left > 0 else None

        if selected == current_q["answer"]:
            st.session_state.score += 1

        handle_answer(selected)
        st.session_state.q_index += 1
        st.session_state.question_start = time.time()
        st.rerun()

    if skip or time_left == 0:
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
    score = st.session_state.score
    percent = (score / 15) * 100
    incorrect = 15 - score
    diff = st.session_state.difficulty

    st.success("🎉 QUIZ COMPLETED!")
    st.write(f"**Score:** {score}/15")
    st.write(f"**Percentage:** {percent:.2f}%")
    st.write(f"**Difficulty:** {diff}")

    # Save Results
    if "saved" not in st.session_state:
        save_result_to_csv(user, score, percent, "Done", diff)
        st.session_state.saved = True

    # -------------------------
    # PIE CHART
    # -------------------------

    st.subheader("📊 Performance Pie Chart")

    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie([score, incorrect],
           labels=["Correct", "Incorrect"],
           autopct="%1.1f%%",
           colors=["#4CAF50", "#FF5252"],
           startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    # -------------------------
    # LINE CHART (CODECHEF STYLE)
    # -------------------------

    st.subheader("📈 Time Taken per Question (Sec)")

    q_nums = list(range(1, len(st.session_state.time_taken)+1))
    df_time = pd.DataFrame({
        "Question": q_nums,
        "Time (sec)": st.session_state.time_taken
    })

    st.line_chart(df_time.set_index("Question"))

    # -------------------------
    # Detailed Answers
    # -------------------------

    st.markdown("### Detailed Answers")

    for i, ans in enumerate(st.session_state.answers, 1):
        sel = ans["selected"] if ans["selected"] else "(timeout/skip)"
        corr = ans["correct"]
        mark = "✅" if sel == corr else "❌"
        st.write(f"Q{i}: Selected **{sel}**, Correct **{corr}** {mark}")

    if st.button("Restart Quiz"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# FOOTER
st.markdown("---")
st.markdown(
    f"<div style='text-align:center; color:gray;'>{APP_FOOTER}</div>",
    unsafe_allow_html=True)
