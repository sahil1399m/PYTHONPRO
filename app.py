import streamlit as st
import random
import csv
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# CONFIG
# -------------------------
RESULTS_CSV = "quiz_results.csv"
APP_FOOTER = "Built by SAHIL DESAI | VJTI"

# -------------------------
# QUESTION BANKS (SMALL SET)
# -------------------------
EASY_QUESTIONS = [
    {"question": "What is the output of print(2+3)?", "options": ["23", "5", "2+3", "Error"], "answer": "5"},
    {"question": "Which symbol is used for comments?", "options": ["//", "#", "/* */", "<!-- -->"], "answer": "#"},
    {"question": "Which datatype is immutable?", "options": ["List", "Dictionary", "Tuple", "Set"], "answer": "Tuple"},
    {"question": "What is the output of len('Python')?", "options": ["5", "6", "7", "Error"], "answer": "6"},
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
# SESSION STATE INIT
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
    st.session_state.user = {"name": name.strip(), "college": college.strip(), "reg": regid.strip()}
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
        with open(RESULTS_CSV, "r"):
            pass
    except FileNotFoundError:
        header_needed = True

    with open(RESULTS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header_needed:
            writer.writerow(["Name", "College", "RegID", "Score", "Percentage", "Status", "Difficulty", "Timestamp"])

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
# GLOBAL BACKGROUND & UI CSS
# -------------------------
def set_background(css_code):
    st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

CSS = r"""
/* ============================= */
/* 🔥 ANIMATED BACKGROUND THEME  */
/* ============================= */

@keyframes gradientShift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes floatBlob {
  0%   { transform: translateY(0px) translateX(0px) scale(1); opacity: .9; }
  50%  { transform: translateY(-30px) translateX(20px) scale(1.05); opacity: .8; }
  100% { transform: translateY(0px) translateX(0px) scale(1); opacity: .9; }
}

@keyframes slowPan {
  from { transform: translateX(-25%); }
  to   { transform: translateX(25%); }
}

/* Main Animated Background applied to streamlit app container */
.stApp {
  position: relative;
  overflow: hidden;
  background: linear-gradient(-45deg,
             rgba(6,10,34,1) 0%,
             rgba(11,20,43,1) 30%,
             rgba(22,36,58,1) 60%,
             rgba(11,12,30,1) 100%);
  background-size: 300% 300%;
  animation: gradientShift 18s ease-in-out infinite;
  min-height: 100vh;
}

/* Layer 1: Floating Neon Blobs */
.stApp::before{
  content: "";
  position: absolute;
  inset: -20%;
  z-index: 0;
  background:
    radial-gradient(30% 30% at 10% 20%, rgba(54,142,255,0.12), transparent 18%),
    radial-gradient(35% 35% at 75% 30%, rgba(59,211,178,0.10), transparent 20%),
    radial-gradient(28% 28% at 50% 80%, rgba(150,99,255,0.08), transparent 16%);
  filter: blur(40px) saturate(1.05);
  transform: translateZ(0);
  pointer-events: none;
  animation: floatBlob 14s ease-in-out infinite;
}

/* Layer 2: Moving Grid Overlay */
.stApp::after{
  content: "";
  position: absolute;
  inset: 0;
  z-index: 0;
  background-image:
    linear-gradient(120deg, rgba(255,255,255,0.01) 1px, transparent 1px),
    linear-gradient(30deg, rgba(255,255,255,0.01) 1px, transparent 1px);
  background-size: 260px 260px, 260px 260px;
  opacity: 0.20;
  transform-origin: center;
  transform: translateX(-5%);
  mix-blend-mode: overlay;
  pointer-events: none;
  animation: slowPan 40s linear infinite;
}

/* Ensure app content is above decorative layers */
.stApp > header,
.stApp > div,
.stApp > main,
.stApp .block-container {
  position: relative;
  z-index: 1;
}

/* Make block container wider for better UX */
.block-container {
    max-width: 1400px !important;
    padding-top: 2rem !important;
}

/* Glass card used for login */
.glass {
    width: 85% !important;
    max-width: 920px !important;
    margin: 0 auto 18px auto !important;
    padding: 34px !important;
    border-radius: 16px !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.55) !important;
    backdrop-filter: blur(10px) !important;
}

/* Title glow */
h1, h2, .title {
  color: #ffffff !important;
  text-shadow: 0 4px 18px rgba(0, 200, 255, 0.08), 0 1px 3px rgba(0,0,0,0.6);
}

/* Inputs and selects - larger and readable */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextInput input,
.stSelectbox select {
    font-size: 17px !important;
    padding: 12px 14px !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    background: rgba(0,0,0,0.45) !important;
}

/* Labels bigger */
.stTextInput label,
.stSelectbox label {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #d1d5db !important;
}

/* Buttons bigger & vibrant */
.stButton > button {
    padding: 12px 22px !important;
    font-size: 16px !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg,#ff8a00,#e52e71) !important;
    color: white !important;
    border: none !important;
    transition: transform .12s ease, box-shadow .12s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(229,46,113,0.18) !important;
}

/* Radio larger */
.stRadio label {
    font-size: 16px !important;
}

/* ============================= */
/* ✅ SELECTBOX FIXES (important) */
/* ============================= */

/* baseweb select wrapper — selected value visible */
div[data-baseweb="select"] span,
.stSelectbox > div > div {
    color: #ffffff !important;
    font-size: 16px !important;
}

/* dropdown menu style + ensure it shows on top */
div[data-baseweb="menu"] {
    background-color: rgba(10,12,20,0.98) !important;
    border-radius: 8px !important;
    z-index: 9999 !important;
    box-shadow: 0 10px 30px rgba(2,6,23,0.6) !important;
}

/* each option */
div[role="option"] {
    color: #ffffff !important;
    padding: 10px 14px !important;
    font-size: 16px !important;
}

/* ensure menu items aren't hidden behind other elements */
div[role="option"]:hover {
    background: rgba(255,255,255,0.03) !important;
}

/* For the underlying select container */
div[data-baseweb="select"] {
    z-index: 9998 !important;
}

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  .stApp, .stApp::before, .stApp::after {
    animation: none !important;
  }
}
/* ============================= */
/* 🔥 BIGGER QUESTION + OPTIONS  */
/* ============================= */

/* Increase size of main question text */
.question-text, .stMarkdown h2, .stMarkdown h3 {
    font-size: 32px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin-bottom: 20px !important;
}

/* Increase radio button text */
.stRadio > div > label {
    font-size: 22px !important;
    padding: 10px 4px !important;
    color: #fff !important;
}

/* Make radio circle bigger */
.stRadio > div > div[role="radiogroup"] > label > div:first-child {
    width: 22px !important;
    height: 22px !important;
    border-width: 3px !important;
}

/* Increase spacing between options */
.stRadio > div > div[role="radiogroup"] > label {
    margin-bottom: 12px !important;
}

/* Submit + Skip buttons bigger */
.stButton > button {
    padding: 16px 30px !important;
    font-size: 20px !important;
    border-radius: 12px !important;
}

/* Enlarge progress bar */
.stProgress > div > div {
    height: 12px !important;
    border-radius: 20px !important;
}

"""

set_background(CSS)

# -------------------------
# App Title (render after CSS)
# -------------------------
st.title("🚀 Start Your Python Quiz")
st.caption("Enter details and press Start — good luck!")


# -------------------------
# LOGIN / QUIZ / RESULTS
# -------------------------
# centered layout for login
if st.session_state.user is None:

    # place login in center column
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)

        with st.form("login_form"):
            name = st.text_input("👤 Your Name")
            college = st.text_input("🏫 College Name (enter 'VJTI')")
            regid = st.text_input("🆔 Registration ID (must start with 24109)")
            # selectbox -> CSS above fixes selected text & dropdown visibility
            difficulty = st.selectbox("🎯 Difficulty", ["Easy", "Medium", "Hard"])
            submitted = st.form_submit_button("🔥 Start Quiz")

        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if not name or not college or not regid:
                st.warning("⚠ Fill all fields.")
            elif not verify_college(college):
                st.error("❌ Only VJTI students allowed.")
            elif not verify_regid(regid):
                st.error("❌ Reg ID must start with 24109.")
            else:
                start_quiz(name, college, regid, difficulty)
                st.rerun()

    # resources on the right
    with col_right:
        st.markdown("<h3 class='title' style='font-size:20px;'>📘 Build Your Concepts</h3>", unsafe_allow_html=True)
        resources = {
            "Python Basics": "https://www.geeksforgeeks.org/python-basics/",
            "Data Types": "https://www.geeksforgeeks.org/python-data-types/",
            "Functions": "https://www.geeksforgeeks.org/python-functions/",
            "Loops": "https://www.geeksforgeeks.org/loops-in-python/",
            "Lists": "https://www.geeksforgeeks.org/python-list/",
            "Stacks": "https://www.geeksforgeeks.org/stack-in-python/",
            "Queues": "https://www.geeksforgeeks.org/queue-in-python/",
        }
        for topic, link in resources.items():
            st.markdown(f"[🔗 {topic}]({link})")

# -------------------------
# QUIZ PAGE
# -------------------------
elif not st.session_state.finished:

    user = st.session_state.user
    q_index = st.session_state.q_index
    questions = st.session_state.questions

    # safety: if question index exceeds list -> finish
    if q_index >= len(questions):
        st.session_state.finished = True
        st.rerun()

    current_q = questions[q_index]

    # compute timer
    elapsed = time.time() - st.session_state.question_start
    TIME_PER_QUESTION = st.session_state.time_per_question
    time_left = max(TIME_PER_QUESTION - int(elapsed), 0)

    st.header(f"Question {q_index+1} / {len(questions)}")
    st.progress((q_index+1)/len(questions))

    left, right = st.columns([3, 1])
    with right:
        st.subheader("👤 Student Info")
        st.write(f"**{user['name']}**")
        st.write(f"Reg ID: **{user['reg']}**")
        st.write(f"Difficulty: **{st.session_state.difficulty}**")
        st.write(f"Score: **{st.session_state.score}**")
        st.markdown("---")
        st.subheader("⏳ Time Left")
        st.progress(time_left / TIME_PER_QUESTION)
        st.write(f"**{time_left} seconds**")

    with left:
        st.markdown(f"<div class='question-text'>{current_q['question']}</div>", unsafe_allow_html=True)
        option = st.radio("", current_q["options"], key=f"opt_{q_index}")

        def handle_answer(opt):
            st.session_state.answers.append({"selected": opt, "correct": current_q["answer"]})
            st.session_state.time_taken.append(TIME_PER_QUESTION - time_left)

        if st.button("Submit"):
            selected = option if time_left > 0 else None
            if selected == current_q["answer"]:
                st.session_state.score += 1
            handle_answer(selected)
            st.session_state.q_index += 1
            st.session_state.question_start = time.time()
            st.rerun()

        # Skip button (counts as unanswered)
        if st.button("Skip"):
            handle_answer(None)
            st.session_state.q_index += 1
            st.session_state.question_start = time.time()
            st.rerun()

        # Timeout handling
        if time_left == 0:
            handle_answer(None)
            st.session_state.q_index += 1
            st.session_state.question_start = time.time()
            st.rerun()

    # refresh for timer
    time.sleep(1)
    st.rerun()

# -------------------------
# RESULTS PAGE
# -------------------------
else:
    user = st.session_state.user
    total = len(st.session_state.questions)
    score = st.session_state.score
    percent = (score/total)*100 if total > 0 else 0
    incorrect = total - score

    st.success("🎉 Quiz Completed!")
    st.write(f"**Score:** {score}/{total}")
    st.write(f"**Percentage:** {percent:.2f}%")
    st.write(f"**Difficulty:** {st.session_state.difficulty}")

    if "saved" not in st.session_state:
        save_result_to_csv(user, score, percent, "Done", st.session_state.difficulty)
        st.session_state.saved = True

    st.subheader("📊 Performance Pie Chart")
    fig, ax = plt.subplots(figsize=(4,4))
    ax.pie([score, incorrect], labels=["Correct", "Incorrect"], autopct="%1.1f%%", colors=["#4CAF50","#FF5252"])
    ax.axis("equal")
    st.pyplot(fig)

    st.subheader("📈 Time Taken Per Question")
    if st.session_state.time_taken:
        df = pd.DataFrame({"Question": list(range(1, len(st.session_state.time_taken)+1)), "Time": st.session_state.time_taken})
        st.line_chart(df.set_index("Question"))
    else:
        st.info("No timing data recorded.")

    st.subheader("📝 Detailed Answers")
    for i, ans in enumerate(st.session_state.answers, 1):
        selected = ans["selected"] if ans["selected"] else "Skipped/Timeout"
        mark = "✅" if selected == ans["correct"] else "❌"
        st.write(f"Q{i}: Selected **{selected}**, Correct **{ans['correct']}** {mark}")

    if st.button("Restart Quiz"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# footer
st.markdown("---")
st.markdown(f"<center>{APP_FOOTER}</center>", unsafe_allow_html=True)
