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
    {"question": "What is the output of print(2+3)?",
     "options": ["23", "5", "2+3", "Error"],
     "answer": "5"},

    {"question": "Which symbol is used for comments in Python?",
     "options": ["//", "#", "/* */", "<!-- -->"],
     "answer": "#"},

    {"question": "Which datatype is immutable?",
     "options": ["List", "Dictionary", "Tuple", "Set"],
     "answer": "Tuple"},

    {"question": "What is the output of len('Python')?",
     "options": ["5", "6", "7", "Error"],
     "answer": "6"},

    {"question": "Which is a valid variable name?",
     "options": ["1name", "_name", "name!", "for"],
     "answer": "_name"},

    {"question": "What is the output of print(type(10))?",
     "options": ["int", "<class 'int'>", "10", "number"],
     "answer": "<class 'int'>"},

    {"question": "Which function is used to take user input?",
     "options": ["input()", "get()", "scan()", "read()"],
     "answer": "input()"},

    {"question": "Which of these is a Boolean value?",
     "options": ["True", "true", "TRUE", "Yes"],
     "answer": "True"},

    {"question": "What is the correct file extension for Python files?",
     "options": [".pt", ".py", ".pyt", ".python"],
     "answer": ".py"},

    {"question": "What does the len() function do?",
     "options": ["Adds numbers", "Returns length", "Prints output", "Deletes data"],
     "answer": "Returns length"},

    {"question": "Which is a Python list?",
     "options": ["{1,2,3}", "(1,2,3)", "[1,2,3]", "<1,2,3>"],
     "answer": "[1,2,3]"},

    {"question": "What will print(10//3) output?",
     "options": ["3.33", "3", "4", "Error"],
     "answer": "3"},

    {"question": "Which keyword is used to define a function?",
     "options": ["define", "func", "def", "function"],
     "answer": "def"},

    {"question": "Which operator is used for exponentiation?",
     "options": ["^", "**", "^^", "//"],
     "answer": "**"},

    {"question": "What is the output of print('Hello' + 'World')?",
     "options": ["Hello World", "HelloWorld", "Error", "Hello+World"],
     "answer": "HelloWorld"},

    {"question": "Which data type stores True or False?",
     "options": ["int", "str", "bool", "float"],
     "answer": "bool"},

    {"question": "Which keyword is used for loops?",
     "options": ["repeat", "for", "loop", "iterate"],
     "answer": "for"},

    {"question": "What is the output of print(3*'A')?",
     "options": ["AAA", "A3", "Error", "A A A"],
     "answer": "AAA"},

    {"question": "What does print(type('10')) output?",
     "options": ["int", "string", "<class 'str'>", "<class 'int'>"],
     "answer": "<class 'str'>"},

    {"question": "Which of these is NOT a Python data type?",
     "options": ["tuple", "set", "array", "dict"],
     "answer": "array"},
]


MEDIUM_QUESTIONS = [
    {"question": "Which loop is entry-controlled?",
     "options": ["for", "while", "do-while", "loop"],
     "answer": "for"},

    {"question": "Which keyword exits a loop immediately?",
     "options": ["stop", "break", "exit", "end"],
     "answer": "break"},

    {"question": "What is the default return value of a Python function?",
     "options": ["0", "None", "Error", "Empty"],
     "answer": "None"},

    {"question": "What does lambda create?",
     "options": ["loop", "anonymous function", "variable", "module"],
     "answer": "anonymous function"},

    {"question": "Which method returns only keys of a dictionary?",
     "options": ["allkeys()", "keys()", "dict.keys()", "getkeys()"],
     "answer": "keys()"},

    {"question": "What is the output of: print([1,2,3] * 2)?",
     "options": ["[2,4,6]", "[1,2,3,1,2,3]", "Error", "None"],
     "answer": "[1,2,3,1,2,3]"},

    {"question": "Which operator checks identity?",
     "options": ["==", "!=", "is", "in"],
     "answer": "is"},

    {"question": "What is the output of: print('a' in 'apple')?",
     "options": ["False", "True", "None", "Error"],
     "answer": "True"},

    {"question": "What type of error is caused by wrong syntax?",
     "options": ["Runtime Error", "Syntax Error", "Logical Error", "Type Error"],
     "answer": "Syntax Error"},

    {"question": "Which keyword is used to handle exceptions?",
     "options": ["try", "except", "catch", "handle"],
     "answer": "except"},

    {"question": "What does list.append(x) do?",
     "options": ["Adds x at end", "Adds x at start", "Inserts x at index 0", "Sorts list"],
     "answer": "Adds x at end"},

    {"question": "Which function converts a string to an integer?",
     "options": ["string()", "toInt()", "int()", "convert()"],
     "answer": "int()"},

    {"question": "What is the output of: print(bool(''))?",
     "options": ["True", "False", "None", "Error"],
     "answer": "False"},

    {"question": "Which of the following is NOT a valid list function?",
     "options": ["append()", "remove()", "push()", "insert()"],
     "answer": "push()"},

    {"question": "What is the output of: print(type([1,2,3]))?",
     "options": ["list", "<class 'list'>", "[]", "object"],
     "answer": "<class 'list'>"},

    {"question": "What does *args allow in a function?",
     "options": ["Multiple return values", "Variable number of arguments", "String only", "List only"],
     "answer": "Variable number of arguments"},

    {"question": "Which statement is used to skip an iteration in loop?",
     "options": ["skip", "stop", "continue", "pass"],
     "answer": "continue"},

    {"question": "What is the output of: print(10 > 5 and 3 < 1)?",
     "options": ["True", "False", "None", "Error"],
     "answer": "False"},

    {"question": "What is indexing in lists?",
     "options": ["Accessing elements by position", "Sorting lists", "Deleting data", "Copying lists"],
     "answer": "Accessing elements by position"},

    {"question": "Which module is used to generate random numbers?",
     "options": ["math", "os", "random", "numbers"],
     "answer": "random"},
]

HARD_QUESTIONS = [
    {"question": "What is the purpose of the __init__ method in a class?",
     "options": ["Destructor", "Constructor", "Static Method", "Getter"],
     "answer": "Constructor"},

    {"question": "Which keyword refers to the current object instance?",
     "options": ["self", "this", "obj", "current"],
     "answer": "self"},

    {"question": "Which data structure follows LIFO?",
     "options": ["Queue", "Stack", "Linked List", "Tree"],
     "answer": "Stack"},

    {"question": "Which feature allows a function to call itself?",
     "options": ["Looping", "Recursion", "Abstraction", "Polymorphism"],
     "answer": "Recursion"},

    {"question": "What is a decorator in Python?",
     "options": ["A loop modifier", "A function that modifies another function",
                 "A class wrapper", "An error handler"],
     "answer": "A function that modifies another function"},

    {"question": "Which keyword is used to define a generator?",
     "options": ["return", "yield", "generate", "async"],
     "answer": "yield"},

    {"question": "What is the output of: len({1: 'a', 2: 'b'})?",
     "options": ["1", "2", "Error", "None"],
     "answer": "2"},

    {"question": "Which method is called when an object is deleted?",
     "options": ["__del__", "__exit__", "__finish__", "__destroy__"],
     "answer": "__del__"},

    {"question": "What does @staticmethod define?",
     "options": ["Method with no self", "Private method",
                 "Getter method", "Class-level constructor"],
     "answer": "Method with no self"},

    {"question": "What is list comprehension?",
     "options": ["A method to sort lists", "A shorthand for creating lists",
                 "A debugging tool", "A recursion technique"],
     "answer": "A shorthand for creating lists"},

    {"question": "Which of these allows multiple inheritance?",
     "options": ["Python classes", "C functions", "Java classes", "SQL tables"],
     "answer": "Python classes"},

    {"question": "What will be the output of: bool([])?",
     "options": ["True", "False", "None", "Error"],
     "answer": "False"},

    {"question": "Which method is automatically called when printing an object?",
     "options": ["__repr__", "__str__", "__show__", "__display__"],
     "answer": "__str__"},

    {"question": "What does *kwargs represent?",
     "options": ["List of arguments", "Tuple of arguments",
                 "Dictionary of keyword arguments", "Class attributes"],
     "answer": "Dictionary of keyword arguments"},

    {"question": "Which exception is raised for division by zero?",
     "options": ["TypeError", "ValueError", "ZeroDivisionError", "ArithmeticError"],
     "answer": "ZeroDivisionError"},

    {"question": "What is the output of: [i*i for i in range(3)]?",
     "options": ["[1,4,9]", "[0,1,4]", "[0,1,2]", "[2,4,6]"],
     "answer": "[0,1,4]"},

    {"question": "Which module handles dates and times?",
     "options": ["calendar", "datetime", "time", "clock"],
     "answer": "datetime"},

    {"question": "Which keyword is used to define an abstract method?",
     "options": ["@abstractmethod", "@abstract", "virtual", "private"],
     "answer": "@abstractmethod"},

    {"question": "What is the result of: 3 < 2 < 1?",
     "options": ["True", "False", "Error", "None"],
     "answer": "False"},

    {"question": "Which Python feature allows operator overloading?",
     "options": ["Magic methods", "Inheritance", "Polymorphism", "Decorators"],
     "answer": "Magic methods"},
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
    st.session_state.user = {"name": name.strip(
    ), "college": college.strip(), "reg": regid.strip()}
    st.session_state.difficulty = difficulty

    if difficulty == "Easy":
        st.session_state.questions = random.sample(EASY_QUESTIONS, 15)
        st.session_state.time_per_question = 45
    elif difficulty == "Medium":
        st.session_state.questions = random.sample(MEDIUM_QUESTIONS, 15)
        st.session_state.time_per_question = 60
    else:
        st.session_state.questions = random.sample(HARD_QUESTIONS, 15)
        st.session_state.time_per_question = 100

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

    # generate a new file name each day
    file_name = f"quiz_results_{datetime.now().strftime('%Y-%m-%d')}.csv"

    header_needed = False
    try:
        with open(file_name, "r"):
            pass
    except FileNotFoundError:
        header_needed = True

    with open(file_name, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if header_needed:
            writer.writerow([
                "Name", "College", "RegID", "Score",
                "Percentage", "Status", "Difficulty", "Timestamp"
            ])

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
/* ========================================================= */
/* ⭐ Modern Resource Buttons With Icons — Build Concepts     */
/* ========================================================= */

.resource-card {
    background: rgba(255,255,255,0.08);
    padding: 12px 18px;
    border-radius: 12px;
    margin: 8px 0;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: 0.2s ease;
    border: 1px solid rgba(255,255,255,0.12);
}

.resource-card:hover {
    transform: translateX(6px);
    background: rgba(255,255,255,0.15);
    box-shadow: 0 0 12px rgba(0,255,255,0.25);
}

.resource-icon {
    font-size: 20px;
}

.resource-text {
    font-size: 17px;
    font-weight: 600;
    color: white;
}


"""
set_background(CSS)

# -------------------------
# App Title (render after CSS)
# -------------------------
st.title("🚀 Start Your Python Quiz")
st.caption("Enter details and press Start — good luck!")


# -------------------------
# LOGIN / QUIZ / RESULTS FLOW (REPLACE YOUR CURRENT FLOW WITH THIS)
# -------------------------

# LOGIN PAGE: show when no user in session
if st.session_state.user is None:

    # layout: center column for the form
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)

        with st.form("login_form"):
            name = st.text_input("👤 Your Name")
            college = st.text_input("🏫 College Name (enter 'VJTI')")
            regid = st.text_input("🆔 Registration ID (must start with 24109)")
            difficulty = st.selectbox(
                "🎯 Difficulty", ["Easy", "Medium", "Hard"])
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
                st.rerun()   # use experimental_rerun to restart script

    # right column: resources cards (unchanged)
    with col_right:
        st.markdown("<h2 class='title' style='font-size:28px;'>📘 Build Your Concepts</h2>",
                    unsafe_allow_html=True)
        resources = [
            ("🐍", "Python Basics", "https://www.geeksforgeeks.org/python-basics/"),
            ("📦", "Data Types", "https://www.geeksforgeeks.org/python-data-types/"),
            ("⚙️", "Functions", "https://www.geeksforgeeks.org/python-functions/"),
            ("🔁", "Loops", "https://www.geeksforgeeks.org/loops-in-python/"),
            ("📚", "Lists", "https://www.geeksforgeeks.org/python-list/"),
            ("🧱", "Stacks", "https://www.geeksforgeeks.org/stack-in-python/"),
            ("📬", "Queues", "https://www.geeksforgeeks.org/queue-in-python/"),
        ]
        for icon, topic, link in resources:
            st.markdown(
                f"""
                <a href="{link}" target="_blank" style="text-decoration:none;">
                    <div class="resource-card">
                        <div class="resource-icon">{icon}</div>
                        <div class="resource-text">{topic}</div>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )

# QUIZ PAGE: user is present and quiz not finished
elif st.session_state.user is not None and not st.session_state.finished:

    user = st.session_state.user
    q_index = st.session_state.q_index
    questions = st.session_state.questions

    # safety: if question index exceeds list -> finish the quiz
    if q_index >= len(questions):
        st.session_state.finished = True
        st.rerun()

    current_q = questions[q_index]

    # Timer
    elapsed = time.time() - st.session_state.question_start
    TIME_PER_QUESTION = st.session_state.time_per_question
    time_left = max(TIME_PER_QUESTION - int(elapsed), 0)

    # Page header
    st.title(f"Question {q_index+1} / {len(questions)}")
    st.progress((q_index+1) / len(questions))

    left, right = st.columns([3, 1])

    # Right: student info + timer
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

    # Left: question + options
    with left:
        st.subheader(current_q["question"])
        option = st.radio("", current_q["options"], key=f"opt_{q_index}")

        def handle_answer(opt):
            st.session_state.answers.append(
                {"selected": opt, "correct": current_q["answer"]})
            st.session_state.time_taken.append(TIME_PER_QUESTION - time_left)

        col_submit, col_skip = st.columns([1, 1])
        if col_submit.button("Submit"):
            selected = option if time_left > 0 else None
            if selected == current_q["answer"]:
                st.session_state.score += 1
            handle_answer(selected)
            st.session_state.q_index += 1
            st.session_state.question_start = time.time()
            st.rerun()

        if col_skip.button("Skip"):
            handle_answer(None)
            st.session_state.q_index += 1
            st.session_state.question_start = time.time()
            st.rerun()

        # Handle timeout
        if time_left == 0:
            handle_answer(None)
            st.session_state.q_index += 1
            st.session_state.question_start = time.time()
            st.rerun()

    # ensure UI updates every second
    time.sleep(1)
    st.rerun()

# RESULTS PAGE: quiz finished
else:
    user = st.session_state.user
    total = len(st.session_state.questions) if st.session_state.questions else 0
    score = st.session_state.score
    percent = (score / total) * 100 if total > 0 else 0
    incorrect = total - score

    st.title("🎉 Quiz Completed!")
    st.write(f"**Score:** {score}/{total}")
    st.write(f"**Percentage:** {percent:.2f}%")
    st.write(f"**Difficulty:** {st.session_state.difficulty}")

    # Save CSV once
    if "saved" not in st.session_state:
        save_result_to_csv(user, score, percent, "Done",
                           st.session_state.difficulty)
        st.session_state.saved = True

    # -------------------------
# SIDE-BY-SIDE CHARTS
col1, col2 = st.columns([1, 1])

# ----------- LEFT: PIE CHART -----------
with col1:
    # -----------------------------------------
    # 📊 Enhanced Neon Pie Chart
    # -----------------------------------------
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    st.subheader("📊 Performance Chart")

    # Create figure
    fig, ax = plt.subplots(figsize=(5, 5), facecolor="none")

    colors = ["#00FFA3", "#FF4B4B"]   # neon green + neon red

    wedges, texts, autotexts = ax.pie(
        [score, incorrect],
        labels=["Correct", "Incorrect"],
        autopct="%1.1f%%",
        colors=colors,
        textprops={'color': "white", 'fontsize': 14, 'weight': 'bold'},
        pctdistance=0.8,
    )

    # Glow / donut effect
    centre_circle = Circle((0, 0), 0.55, fc='black')
    fig.gca().add_artist(centre_circle)

    # Improve look
    ax.set_facecolor("none")

    # Set label font style
    for t in texts:
        t.set_fontsize(14)
        t.set_color("white")

    for t in autotexts:
        t.set_fontsize(15)
        t.set_color("white")
        t.set_weight("bold")

    st.pyplot(fig)


# ----------- RIGHT: TIME GRAPH -----------
with col2:
    st.subheader("⏱️ Time Taken Per Question")

    if st.session_state.time_taken:
        df = pd.DataFrame({
            "Question": list(range(1, len(st.session_state.time_taken)+1)),
            "Time": st.session_state.time_taken
        })

        plt.style.use("dark_background")

        fig2, ax2 = plt.subplots(figsize=(6, 5))

        ax2.plot(df["Question"], df["Time"], linewidth=2, color="#00FFF7")
        ax2.set_xlabel("Question Number")
        ax2.set_ylabel("Time (sec)")
        ax2.set_title("Time Taken Per Question")

        st.pyplot(fig2)

    else:
        st.write("No timing data available.")




    # Detailed answers
    st.subheader("📝 Detailed Answers")
    for i, ans in enumerate(st.session_state.answers, 1):
        selected = ans["selected"] if ans["selected"] else "Skipped/Timeout"
        mark = "✅" if selected == ans["correct"] else "❌"
        st.write(
            f"Q{i}: Selected **{selected}**, Correct **{ans['correct']}** {mark}")

    # Restart button (clear session safely)
    if st.button("Restart Quiz"):
        # clear only the keys we set (safer than deleting everything)
        for k in ["user", "difficulty", "questions", "q_index", "score", "answers", "question_start", "finished", "time_per_question", "time_taken", "saved"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()


# footer
st.markdown("---")
st.markdown(f"<center>{APP_FOOTER}</center>", unsafe_allow_html=True)
