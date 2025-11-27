import streamlit as st
import random
import csv
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------------------
#  PROJECT: Interactive Python Quiz Web App (Streamlit)
#  PURPOSE: Validate basic → advanced Python concepts through
#           an animated, modern, user-friendly quiz interface.
#  AUTHOR:  KGS(Krish,Ganesh,Sahil)(VJTI)
# -----------------------------------------------------------


# -----------------------------------------------------------
# CONFIGURATION VALUES
# -----------------------------------------------------------
RESULTS_CSV = "quiz_results.csv"   # Default CSV name
APP_FOOTER = "Built by KGS | VJTI" # Footer text


# -----------------------------------------------------------
# EASY QUESTIONS — 20 beginner-level MCQs
# -----------------------------------------------------------
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

    {"question": "Correct extension for Python files?",
     "options": [".pt", ".py", ".pyt", ".python"],
     "answer": ".py"},

    {"question": "What does len() do?",
     "options": ["Adds numbers", "Returns length", "Prints output", "Deletes data"],
     "answer": "Returns length"},

    {"question": "Which is a Python list?",
     "options": ["{1,2,3}", "(1,2,3)", "[1,2,3]", "<1,2,3>"],
     "answer": "[1,2,3]"},

    {"question": "Output of print(10//3)?",
     "options": ["3.33", "3", "4", "Error"],
     "answer": "3"},

    {"question": "Keyword used to define a function?",
     "options": ["define", "func", "def", "function"],
     "answer": "def"},

    {"question": "Operator for exponentiation?",
     "options": ["^", "**", "^^", "//"],
     "answer": "**"},

    {"question": "Output of print('Hello' + 'World')?",
     "options": ["Hello World", "HelloWorld", "Error", "Hello+World"],
     "answer": "HelloWorld"},

    {"question": "Which datatype stores True/False?",
     "options": ["int", "str", "bool", "float"],
     "answer": "bool"},

    {"question": "Keyword used for loops?",
     "options": ["repeat", "for", "loop", "iterate"],
     "answer": "for"},

    {"question": "Output of print(3*'A')?",
     "options": ["AAA", "A3", "Error", "A A A"],
     "answer": "AAA"},

    {"question": "type('10') returns?",
     "options": ["int", "string", "<class 'str'>", "<class 'int'>"],
     "answer": "<class 'str'>"},

    {"question": "Which is NOT a Python datatype?",
     "options": ["tuple", "set", "array", "dict"],
     "answer": "array"},
]

# -----------------------------------------------------------
# MEDIUM QUESTIONS — 20 MCQs for intermediate users
# -----------------------------------------------------------
MEDIUM_QUESTIONS = [
    {"question": "Which loop is entry-controlled?",
     "options": ["for", "while", "do-while", "loop"],
     "answer": "for"},

    {"question": "Keyword to exit loop immediately?",
     "options": ["stop", "break", "exit", "end"],
     "answer": "break"},

    {"question": "Default return value of Python function?",
     "options": ["0", "None", "Error", "Empty"],
     "answer": "None"},

    {"question": "Lambda creates?",
     "options": ["loop", "anonymous function", "variable", "module"],
     "answer": "anonymous function"},

    {"question": "Method for dictionary keys?",
     "options": ["allkeys()", "keys()", "dict.keys()", "getkeys()"],
     "answer": "keys()"},

    {"question": "Output of [1,2,3] * 2?",
     "options": ["[2,4,6]", "[1,2,3,1,2,3]", "Error", "None"],
     "answer": "[1,2,3,1,2,3]"},

    {"question": "Identity operator?",
     "options": ["==", "!=", "is", "in"],
     "answer": "is"},

    {"question": "'a' in 'apple' gives?",
     "options": ["False", "True", "None", "Error"],
     "answer": "True"},

    {"question": "Wrong syntax causes?",
     "options": ["Runtime Error", "Syntax Error", "Type Error", "Logical Error"],
     "answer": "Syntax Error"},

    {"question": "Keyword to handle exceptions?",
     "options": ["try", "except", "catch", "handle"],
     "answer": "except"},

    {"question": "list.append(x) does?",
     "options": ["Adds x at end", "Adds x at start", "Insert at index 0", "Sorts list"],
     "answer": "Adds x at end"},

    {"question": "Convert string → integer?",
     "options": ["string()", "toInt()", "int()", "convert()"],
     "answer": "int()"},

    {"question": "bool('') gives?",
     "options": ["True", "False", "None", "Error"],
     "answer": "False"},

    {"question": "NOT a list function?",
     "options": ["append()", "remove()", "push()", "insert()"],
     "answer": "push"},

    {"question": "Type of [1,2,3]?",
     "options": ["list", "<class 'list'>", "[]", "object"],
     "answer": "<class 'list'>"},

    {"question": "*args allows?",
     "options": ["Multiple return", "Variable arguments", "String only", "List only"],
     "answer": "Variable arguments"},

    {"question": "Skip loop iteration?",
     "options": ["skip", "stop", "continue", "pass"],
     "answer": "continue"},

    {"question": "10 > 5 and 3 < 1?",
     "options": ["True", "False", "None", "Error"],
     "answer": "False"},

    {"question": "Indexing means?",
     "options": ["Access by position", "Sorting", "Deleting", "Copying"],
     "answer": "Access by position"},

    {"question": "Module for random numbers?",
     "options": ["math", "os", "random", "numbers"],
     "answer": "random"},
]

# -----------------------------------------------------------
# HARD QUESTIONS — 20 advanced MCQs
# -----------------------------------------------------------
HARD_QUESTIONS = [
    {"question": "Purpose of __init__?",
     "options": ["Destructor", "Constructor", "Static Method", "Getter"],
     "answer": "Constructor"},

    {"question": "Keyword referring to current object?",
     "options": ["self", "this", "obj", "current"],
     "answer": "self"},

    {"question": "Which follows LIFO?",
     "options": ["Queue", "Stack", "Linked List", "Tree"],
     "answer": "Stack"},

    {"question": "Function calling itself?",
     "options": ["Looping", "Recursion", "Polymorphism", "Abstraction"],
     "answer": "Recursion"},

    {"question": "What is a decorator?",
     "options": ["Loop modifier", "Function that modifies another function",
                 "Class wrapper", "Error handler"],
     "answer": "Function that modifies another function"},

    {"question": "Keyword for generator?",
     "options": ["return", "yield", "generate", "async"],
     "answer": "yield"},

    {"question": "len({1:'a', 2:'b'}) = ?",
     "options": ["1", "2", "Error", "None"],
     "answer": "2"},

    {"question": "Method when object deleted?",
     "options": ["__del__", "__exit__", "__finish__", "__destroy__"],
     "answer": "__del__"},

    {"question": "@staticmethod defines?",
     "options": ["No self", "Private", "Getter", "Constructor"],
     "answer": "No self"},

    {"question": "List comprehension is?",
     "options": ["Sorting", "Shorthand list creation", "Debugging", "Recursion"],
     "answer": "Shorthand list creation"},

    {"question": "Allows multiple inheritance?",
     "options": ["Python classes", "C functions", "Java classes", "SQL tables"],
     "answer": "Python classes"},

    {"question": "bool([]) → ?",
     "options": ["True", "False", "None", "Error"],
     "answer": "False"},

    {"question": "Method called when printing object?",
     "options": ["__repr__", "__str__", "__show__", "__display__"],
     "answer": "__str__"},

    {"question": "*kwargs stands for?",
     "options": ["List", "Tuple", "Dict of keyword args", "Attributes"],
     "answer": "Dict of keyword args"},

    {"question": "Exception for division by zero?",
     "options": ["TypeError", "ValueError", "ZeroDivisionError", "ArithmeticError"],
     "answer": "ZeroDivisionError"},

    {"question": "[i*i for i in range(3)]?",
     "options": ["[1,4,9]", "[0,1,4]", "[0,1,2]", "[2,4,6]"],
     "answer": "[0,1,4]"},

    {"question": "Module for dates & times?",
     "options": ["calendar", "datetime", "time", "clock"],
     "answer": "datetime"},

    {"question": "Keyword for abstract method?",
     "options": ["@abstractmethod", "@abstract", "virtual", "private"],
     "answer": "@abstractmethod"},

    {"question": "Result of 3 < 2 < 1?",
     "options": ["True", "False", "Error", "None"],
     "answer": "False"},

    {"question": "Feature enabling operator overloading?",
     "options": ["Magic methods", "Inheritance", "Polymorphism", "Decorators"],
     "answer": "Magic methods"},
]

# -----------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------
# Streamlit re-runs the script on every interaction.  
# Therefore we store the entire quiz progress in session_state.
# This ensures the quiz continues without resetting values.
# -----------------------------------------------------------

def init_session():
    defaults = {
        "user": None,              # stores user details
        "difficulty": None,        # Easy / Medium / Hard
        "questions": [],           # selected 15 questions
        "q_index": 0,              # current question index
        "score": 0,                # total correct answers
        "answers": [],             # list of {"selected","correct"}
        "question_start": None,    # timestamp when question started
        "finished": False,         # quiz finished flag
        "time_per_question": 30,   # dynamic based on difficulty
        "time_taken": []           # list storing time spent on each question
    }

    # Create missing session_state keys
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val



# -----------------------------------------------------------
# BASIC VALIDATION FUNCTIONS
# -----------------------------------------------------------
# Used on login page to ensure correct college + reg ID.
# -----------------------------------------------------------

def verify_college(college_name: str) -> bool:
    """Returns True only if user enters 'VJTI' """
    return college_name.strip().lower() == "vjti"


def verify_regid(reg_id: str) -> bool:
    """Valid Reg ID must start with 24109"""
    return reg_id.strip().startswith("24109")



# -----------------------------------------------------------
# START QUIZ FUNCTION
# -----------------------------------------------------------
# Called only AFTER user enters valid credentials.
# This function:
#   - stores user info
#   - selects 15 random questions from correct difficulty
#   - sets timer per question
#   - resets all quiz tracking values
# -----------------------------------------------------------

def start_quiz(name, college, regid, difficulty):

    # Store user details in session
    st.session_state.user = {
        "name": name.strip(),
        "college": college.strip(),
        "reg": regid.strip()
    }

    st.session_state.difficulty = difficulty

    # Select 15 random questions from correct difficulty bank
    if difficulty == "Easy":
        st.session_state.questions = random.sample(EASY_QUESTIONS, 15)
        st.session_state.time_per_question = 45

    elif difficulty == "Medium":
        st.session_state.questions = random.sample(MEDIUM_QUESTIONS, 15)
        st.session_state.time_per_question = 60

    else:  # Hard
        st.session_state.questions = random.sample(HARD_QUESTIONS, 15)
        st.session_state.time_per_question = 100

    # Reset tracking variables
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.time_taken = []
    st.session_state.finished = False
    st.session_state.question_start = time.time()  # start timer for Q1



# -----------------------------------------------------------
# SAVE RESULTS TO CSV
# -----------------------------------------------------------
# Every quiz attempt is saved in a dated CSV file:
#       quiz_results_2025-11-28.csv
#
# If the file for that day doesn't exist → add headers.
# If it exists → append result.
# -----------------------------------------------------------

def save_result_to_csv(user, score, percent, status, difficulty):

    # Create daily file
    file_name = f"quiz_results_{datetime.now().strftime('%Y-%m-%d')}.csv"

    # Check if headers required
    header_needed = False
    try:
        with open(file_name, "r"):
            pass    # file exists → skip header
    except FileNotFoundError:
        header_needed = True    # new file → add header row

    # Append result
    with open(file_name, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        # Insert header once
        if header_needed:
            writer.writerow([
                "Name", "College", "RegID", "Score",
                "Percentage", "Status", "Difficulty", "Timestamp"
            ])

        # Insert actual quiz record
        writer.writerow([
            user["name"],
            user["college"],
            user["reg"],
            score,
            f"{percent:.2f}%",
            status,
            difficulty,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])


# -------------------------
# PAGE SETUP & CSS
# -------------------------
st.set_page_config(page_title="VJTI Python Quiz", page_icon="🧠", layout="wide")
init_session()

def set_background(css_code: str):
    """Inject CSS into Streamlit page."""
    st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

# Full CSS: animated background, UI tweaks and important selectbox fixes
CSS = r"""
/* ============================
   Animated background + UI
   ============================ */

/* Animated gradient and decorative layers */
@keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes floatBlob { 0% { transform: translateY(0) translateX(0) scale(1); opacity:.9 } 50% { transform: translateY(-30px) translateX(20px) scale(1.05); opacity:.8 } 100% { transform: translateY(0) translateX(0) scale(1); opacity:.9 } }
@keyframes slowPan { from { transform: translateX(-25%); } to { transform: translateX(25%); } }

.stApp {
  position: relative;
  overflow: hidden;
  background: linear-gradient(-45deg, rgba(6,10,34,1) 0%, rgba(11,20,43,1) 30%, rgba(22,36,58,1) 60%, rgba(11,12,30,1) 100%);
  background-size: 300% 300%;
  animation: gradientShift 18s ease-in-out infinite;
  min-height: 100vh;
}

/* Soft neon blobs */
.stApp::before {
  content: "";
  position: absolute;
  inset: -20%;
  z-index: 0;
  background:
    radial-gradient(30% 30% at 10% 20%, rgba(54,142,255,0.12), transparent 18%),
    radial-gradient(35% 35% at 75% 30%, rgba(59,211,178,0.10), transparent 20%),
    radial-gradient(28% 28% at 50% 80%, rgba(150,99,255,0.08), transparent 16%);
  filter: blur(40px) saturate(1.05);
  animation: floatBlob 14s ease-in-out infinite;
  pointer-events: none;
}

/* Faint moving grid overlay */
.stApp::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 0;
  background-image:
    linear-gradient(120deg, rgba(255,255,255,0.01) 1px, transparent 1px),
    linear-gradient(30deg, rgba(255,255,255,0.01) 1px, transparent 1px);
  background-size: 260px 260px, 260px 260px;
  opacity: 0.20;
  mix-blend-mode: overlay;
  animation: slowPan 40s linear infinite;
  pointer-events: none;
}

/* Ensure app content sits above decorative layers */
.stApp > header,
.stApp > div,
.stApp > main,
.stApp .block-container {
  position: relative;
  z-index: 1;
}

/* Wider app container for better UX */
.block-container {
  max-width: 1400px !important;
  padding-top: 2rem !important;
}

/* Glass card for login */
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

/* Titles */
h1, h2, .title { color: #fff !important; text-shadow: 0 4px 18px rgba(0,200,255,0.08); }

/* Inputs & selects — larger + readable */
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

/* Labels */
.stTextInput label,
.stSelectbox label { font-size: 15px !important; font-weight: 600 !important; color: #d1d5db !important; }

/* Buttons */
.stButton > button {
  padding: 12px 22px !important;
  font-size: 16px !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  background: linear-gradient(90deg,#ff8a00,#e52e71) !important;
  color: white !important;
  border: none !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 10px 30px rgba(229,46,113,0.18) !important; }

/* Radio size */
.stRadio label { font-size: 16px !important; }

/* =============================
   Selectbox (baseweb) fixes — ensures selected value is visible
   ============================= */
div[data-baseweb="select"] span,
.stSelectbox > div > div { color: #ffffff !important; font-size: 16px !important; }

/* Dropdown menu z-index so it appears above other elements */
div[data-baseweb="menu"] { background-color: rgba(10,12,20,0.98) !important; border-radius: 8px !important; z-index: 9999 !important; box-shadow: 0 10px 30px rgba(2,6,23,0.6) !important; }
div[role="option"] { color: #ffffff !important; padding: 10px 14px !important; font-size: 16px !important; }

/* Bigger question & options styling */
.question-text, .stMarkdown h2, .stMarkdown h3 { font-size: 28px !important; font-weight: 700 !important; color: #ffffff !important; margin-bottom: 12px !important; }
.stRadio > div > label { font-size: 20px !important; padding: 8px 4px !important; color: #fff !important; }
.stRadio > div > div[role="radiogroup"] > label { margin-bottom: 10px !important; }

/* Progress bar height */
.stProgress > div > div { height: 12px !important; border-radius: 20px !important; }

/* Resource card */
.resource-card { background: rgba(255,255,255,0.08); padding: 12px 18px; border-radius: 12px; margin: 8px 0; display:flex; align-items:center; gap:10px; border:1px solid rgba(255,255,255,0.12); }
.resource-card:hover { transform: translateX(6px); background: rgba(255,255,255,0.12); box-shadow: 0 0 12px rgba(0,255,255,0.08); }
.resource-icon { font-size: 20px; }
.resource-text { font-size: 16px; font-weight: 600; color: white; }

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  .stApp, .stApp::before, .stApp::after { animation: none !important; }
}
"""
set_background(CSS)

# -------------------------
# APP TITLE
# -------------------------
st.title("🚀 Start Your Python Quiz")
st.caption("Enter details and press Start — good luck!")

# -------------------------
# LOGIN PAGE
# -------------------------
if st.session_state.user is None:
    # center the form with columns
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        # glass card wrapper (CSS class 'glass' is defined above)
        st.markdown("<div class='glass'>", unsafe_allow_html=True)

        # login form (keeps selection in widget state)
        with st.form("login_form"):
            name = st.text_input("👤 Your Name")
            college = st.text_input("🏫 College Name (enter 'VJTI')")
            regid = st.text_input("🆔 Registration ID (must start with 24109)")
            difficulty = st.selectbox("🎯 Difficulty", ["Easy", "Medium", "Hard"])
            # default number of questions is 15; you can pass a different number if desired
            submitted = st.form_submit_button("🔥 Start Quiz")

        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            # basic validation
            if not name or not college or not regid:
                st.warning("⚠ Please fill all fields.")
            elif not verify_college(college):
                st.error("❌ Only VJTI students allowed.")
            elif not verify_regid(regid):
                st.error("❌ Reg ID must start with 24109.")
            else:
                # start the quiz & set up questions + timer
                start_quiz(name, college, regid, difficulty, num_questions=15)
                # rerun to move to quiz page
                st.experimental_rerun()

    # resources on right column
    with col_right:
        st.markdown("<h2 class='title' style='font-size:26px;'>📘 Build Your Concepts</h2>", unsafe_allow_html=True)
        resources = [
            ("🐍", "Python Basics", "https://www.geeksforgeeks.org/python-basics/"),
            ("📦", "Data Types", "https://www.geeksforgeeks.org/python-data-types/"),
            ("⚙️", "Functions", "https://www.geeksforgeeks.org/python-functions/"),
            ("🔁", "Loops", "https://www.geeksforgeeks.org/loops-in-python/"),
            ("📚", "Lists", "https://www.geeksforgeeks.org/python-list/"),
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
                """, unsafe_allow_html=True
            )

# -------------------------
# QUIZ PAGE
# -------------------------
elif st.session_state.user is not None and not st.session_state.finished:
    user = st.session_state.user
    q_index = st.session_state.q_index
    questions = st.session_state.questions

    # safety: if questions exhausted -> finish
    if q_index >= len(questions):
        st.session_state.finished = True
        st.experimental_rerun()

    current_q = questions[q_index]

    # compute remaining time for current question
    elapsed = time.time() - st.session_state.question_start
    TIME_PER_QUESTION = st.session_state.time_per_question
    time_left = max(TIME_PER_QUESTION - int(elapsed), 0)

    # header with progress
    st.title(f"Question {q_index+1} / {len(questions)}")
    st.progress((q_index + 1) / len(questions))

    left, right = st.columns([3, 1])

    # Right column: student info + timer
    with right:
        st.subheader("👤 Student Info")
        st.write(f"**{user['name']}**")
        st.write(f"Reg ID: **{user['reg']}**")
        st.write(f"Difficulty: **{st.session_state.difficulty}**")
        st.write(f"Score: **{st.session_state.score}**")
        st.markdown("---")
        st.subheader("⏳ Time Left")
        # progress bar expects 0..1 — protect divide by zero
        st.progress(time_left / TIME_PER_QUESTION if TIME_PER_QUESTION else 0)
        st.write(f"**{time_left} sec**")

    # Left column: question + options
    with left:
        # larger question visual (CSS targets .question-text class)
        st.markdown(f"<div class='question-text'>{current_q['question']}</div>", unsafe_allow_html=True)

        # unique key per question prevents selection bleed-over
        option = st.radio("", current_q["options"], key=f"opt_{q_index}")

        # helper to record answer and time taken
        def handle_answer(selected_value):
            st.session_state.answers.append({"selected": selected_value, "correct": current_q["answer"]})
            st.session_state.time_taken.append(TIME_PER_QUESTION - time_left)

        # Submit and Skip buttons (placed horizontally)
        col_submit, col_skip = st.columns([1, 1])
        if col_submit.button("Submit"):
            selected = option if time_left > 0 else None
            if selected == current_q["answer"]:
                st.session_state.score += 1
            handle_answer(selected)
            st.session_state.q_index += 1
            st.session_state.question_start = time.time()
            st.experimental_rerun()

        if col_skip.button("Skip"):
            handle_answer(None)
            st.session_state.q_index += 1
            st.session_state.question_start = time.time()
            st.experimental_rerun()

        # If timer expired, count as skipped/timeout and proceed
        if time_left == 0:
            handle_answer(None)
            st.session_state.q_index += 1
            st.session_state.question_start = time.time()
            st.experimental_rerun()

    # small delay to let timer update each second and re-render
    time.sleep(1)
    st.experimental_rerun()

# -------------------------
# RESULTS PAGE
# -------------------------
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

    # Save results to daily CSV one time
    if "saved" not in st.session_state:
        save_result_to_csv(user, score, percent, "Done", st.session_state.difficulty)
        st.session_state.saved = True

    # -------------------------
    # SIDE-BY-SIDE CHARTS (Pie | Time)
    # -------------------------
    col1, col2 = st.columns([1, 1])

    # LEFT: enhanced neon donut pie chart
    with col1:
        st.subheader("📊 Performance Chart")
        # build figure
        fig, ax = plt.subplots(figsize=(5, 5), facecolor="none")
        colors = ["#00FFA3", "#FF4B4B"]  # neon palette

        # handle case when total is zero (avoid zero-length pie)
        pie_values = [score, incorrect] if total > 0 else [1, 0]

        wedges, texts, autotexts = ax.pie(
            pie_values,
            labels=["Correct", "Incorrect"],
            autopct="%1.1f%%",
            colors=colors,
            textprops={'color': "white", 'fontsize': 13, 'weight': 'bold'},
            pctdistance=0.78,
            startangle=90
        )
        # donut center
        centre_circle = Circle((0, 0), 0.55, fc='black')
        ax.add_artist(centre_circle)
        ax.set_facecolor("none")
        ax.set_title("Performance", color="white", fontsize=16, weight="bold")

        for t in texts:
            t.set_color("white")
            t.set_fontsize(13)
        for t in autotexts:
            t.set_color("white")
            t.set_fontsize(13)
            t.set_weight("bold")

        st.pyplot(fig)

    # RIGHT: time taken line chart (dark style)
    with col2:
        st.subheader("⏱️ Time Taken Per Question")
        if st.session_state.time_taken:
            df = pd.DataFrame({
                "Question": list(range(1, len(st.session_state.time_taken) + 1)),
                "Time": st.session_state.time_taken
            })
            plt.style.use("dark_background")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            ax2.plot(df["Question"], df["Time"], linewidth=3, color="#00FFF7", marker="o")
            ax2.set_xlabel("Question Number")
            ax2.set_ylabel("Time (sec)")
            ax2.set_title("Time Taken per Question")
            ax2.grid(alpha=0.25)
            st.pyplot(fig2)
        else:
            st.write("No timing data available.")

    # Detailed answers list
    st.subheader("📝 Detailed Answers")
    for i, ans in enumerate(st.session_state.answers, 1):
        selected = ans["selected"] if ans["selected"] else "Skipped/Timeout"
        mark = "✅" if selected == ans["correct"] else "❌"
        st.write(f"Q{i}: Selected **{selected}**, Correct **{ans['correct']}** {mark}")

    # Restart quiz button: clear only known keys and rerun
    if st.button("Restart Quiz"):
        for k in ["user", "difficulty", "questions", "q_index", "score", "answers", "question_start", "finished", "time_per_question", "time_taken", "saved"]:
            if k in st.session_state:
                del st.session_state[k]
        st.experimental_rerun()

# -------------------------
# FOOTER
# ------------------------- 
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:gray;'>{APP_FOOTER}</div>", unsafe_allow_html=True)
