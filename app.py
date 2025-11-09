import streamlit as st
import random
import csv
import time
from datetime import datetime

# -------------------------
# Configuration
# -------------------------
TIME_PER_QUESTION = 30  # ✅ 30 seconds per question
RESULTS_CSV = "quiz_results.csv"
APP_FOOTER = "Built by SAHIL DESAI  |  VJTI"

# -------------------------
# Question bank
# -------------------------
QUESTION_BANK = [
    {"question": "What is the output of print(2**3)?", "options": ["6", "8", "9", "5"], "answer": "8"},
    {"question": "Which keyword defines a function in Python?", "options": ["func", "def", "define", "function"], "answer": "def"},
    {"question": "Which data type is immutable?", "options": ["List", "Dictionary", "Tuple", "Set"], "answer": "Tuple"},
    {"question": "What does len([1,2,3]) return?", "options": ["2", "3", "1", "Error"], "answer": "3"},
    {"question": "Which of these is a valid variable name?", "options": ["1num", "_num", "num-1", "for"], "answer": "_num"},
    {"question": "Which of the following is used for comments?", "options": ["//", "/* */", "#", "<!-- -->"], "answer": "#"},
    {"question": "What is the result of [1,2,3] + [4,5]?", "options": ["[1,2,3,4,5]", "[5,7,8]", "Error", "[1,2,3][4,5]"], "answer": "[1,2,3,4,5]"},
    {"question": "Tuples are:", "options": ["Mutable", "Immutable", "Temporary", "Dynamic"], "answer": "Immutable"},
    {"question": "How to get all keys of dictionary d?", "options": ["d.keys()", "d.allkeys()", "keys(d)", "d.getkeys()"], "answer": "d.keys()"},
    {"question": "Duplicate keys in a dictionary are:", "options": ["Allowed", "Ignored", "Error", "Overwritten"], "answer": "Overwritten"},
    {"question": "Stack follows which principle?", "options": ["FIFO", "LIFO", "FILO", "LOFI"], "answer": "LIFO"},
    {"question": "Queue follows which principle?", "options": ["FIFO", "LIFO", "FILO", "Random"], "answer": "FIFO"},
    {"question": "Which module in Python supports queue implementation?", "options": ["os", "collections", "math", "time"], "answer": "collections"},
    {"question": "Which method adds an item to a stack implemented using list?", "options": ["append()", "push()", "add()", "insert()"], "answer": "append()"},
    {"question": "Which method removes last element in a stack?", "options": ["pop()", "remove()", "delete()", "discard()"], "answer": "pop()"},
]

# -------------------------
# Helpers
# -------------------------
def init_session():
    """Initialize Streamlit session state"""
    defaults = {
        "user": None,
        "questions": [],
        "q_index": 0,
        "score": 0,
        "answers": [],
        "question_start": None,
        "finished": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def verify_college(college_input):
    c = college_input.strip().lower()
    return c in ["vjti", "veermata jijabai technological institute"]

def verify_regid(regid):
    return regid.strip().startswith("24109")

def start_quiz(name, college, regid):
    """Setup quiz"""
    st.session_state.user = {"name": name.strip(), "college": college.strip(), "reg": regid.strip()}
    qs = QUESTION_BANK.copy()
    random.shuffle(qs)
    st.session_state.questions = qs
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.finished = False
    st.session_state.question_start = time.time()

def save_result_to_csv(user, score, percent, status):
    """Save results"""
    header_needed = False
    try:
        with open(RESULTS_CSV, "r"):
            pass
    except FileNotFoundError:
        header_needed = True

    with open(RESULTS_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        if header_needed:
            writer.writerow(["Name", "College", "RegID", "Score", "Percentage", "Status", "Timestamp"])
        writer.writerow([user["name"], user["college"], user["reg"], score, f"{percent:.2f}%", status,
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

# -------------------------
# UI Setup
# -------------------------
st.set_page_config(page_title="VJTI Python Quiz", page_icon="🧠", layout="centered")
st.title("🧠 VJTI Python Quiz")
st.caption("Quiz covers Python lab topics up to Stacks & Queues")

init_session()

# -------------------------
# Login Form
# -------------------------
if st.session_state.user is None:
    with st.form("login_form"):
        name = st.text_input("Your Name")
        college = st.text_input("College Name (enter 'VJTI' or full name)")
        regid = st.text_input("Registration ID (must start with 24109)")
        submitted = st.form_submit_button("Request Access")

    if submitted:
        if not name or not college or not regid:
            st.warning("Please fill all fields.")
        elif not verify_college(college):
            st.error("Access Denied — Only VJTI students allowed.")
        elif not verify_regid(regid):
            st.error("Access Denied — Reg ID must start with 24109.")
        else:
            start_quiz(name, college, regid)
            st.rerun()

# -------------------------
# Quiz Interface
# -------------------------
elif not st.session_state.finished:
    user = st.session_state.user
    q_index = st.session_state.q_index
    questions = st.session_state.questions

    if q_index >= len(questions):
        st.session_state.finished = True
        st.rerun()

    current_q = questions[q_index]

    st.markdown(f"**Student:** {user['name']}  |  **Reg ID:** {user['reg']}")
    st.markdown("---")
    st.subheader(f"Question {q_index + 1} of {len(questions)}")
    st.write(current_q["question"])

    # --- Timer logic ---
    if st.session_state.question_start is None:
        st.session_state.question_start = time.time()

    elapsed = time.time() - st.session_state.question_start
    time_left = max(int(TIME_PER_QUESTION - elapsed), 0)

    # Timer UI
    timer_col1, timer_col2 = st.columns([3, 1])
    with timer_col1:
        progress = time_left / TIME_PER_QUESTION
        st.progress(progress)
    with timer_col2:
        st.markdown(f"⏱️ **{time_left}s left**")

    # Options
    option = st.radio("Choose an option:", current_q["options"], key=f"opt_{q_index}")

    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        submit = st.button("✅ Submit", key=f"submit_{q_index}")
    with col2:
        skip = st.button("⏭ Skip", key=f"skip_{q_index}")

    # Actions
    if submit and time_left > 0:
        selected = option
        correct = current_q["answer"]
        st.session_state.answers.append({"selected": selected, "correct": correct})
        if selected == correct:
            st.session_state.score += 1
        st.session_state.q_index += 1
        st.session_state.question_start = time.time()
        st.rerun()

    if skip:
        st.session_state.answers.append({"selected": None, "correct": current_q["answer"]})
        st.session_state.q_index += 1
        st.session_state.question_start = time.time()
        st.rerun()

    # Timeout auto-skip
    if time_left == 0:
        st.warning("⏰ Time's up! Moving to next question...")
        st.session_state.answers.append({"selected": None, "correct": current_q["answer"]})
        st.session_state.q_index += 1
        st.session_state.question_start = time.time()
        st.rerun()

    # Live countdown refresh every 1 second
    time.sleep(1)
    st.rerun()

# -------------------------
# Result Page
# -------------------------
else:
    user = st.session_state.user
    total = len(st.session_state.questions)
    score = st.session_state.score
    percent = (score / total) * 100
    if percent == 100:
        status = "Excellent 🌟"
    elif percent >= 60:
        status = "Above Average 👍"
    else:
        status = "Below Average ⚠️"

    st.success("🎉 Quiz Completed!")
    st.write(f"**Name:** {user['name']}")
    st.write(f"**Reg ID:** {user['reg']}")
    st.write(f"**Score:** {score} / {total}")
    st.write(f"**Percentage:** {percent:.2f}%")
    st.write(f"**Performance:** {status}")

    save_result_to_csv(user, score, percent, status)

    st.info("Your result has been saved to quiz_results.csv")

    st.markdown("### Detailed Answers")
    for i, ans in enumerate(st.session_state.answers, start=1):
        sel = ans["selected"] if ans["selected"] else "— (timeout)"
        corr = ans["correct"]
        mark = "✅" if ans["selected"] == corr else "❌"
        st.write(f"Q{i}: Selected: **{sel}** | Correct: **{corr}** {mark}")

    if st.button("Restart Quiz"):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.finished = False
        st.session_state.question_start = time.time()
        st.rerun()

    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:gray;'>{APP_FOOTER}</div>", unsafe_allow_html=True)
