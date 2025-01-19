import streamlit as st
import pandas as pd
import random
import datetime

# --- Set page configuration (MUST be first Streamlit command) ---
st.set_page_config(page_title="Flashcard Trainer", layout="wide")

# --- Spaced Repetition Logic ---
def get_next_review_date(score):
    """Determine the next review date based on the score"""
    if score == 0:
        return datetime.date.today() + datetime.timedelta(days=1)  # Review tomorrow
    elif score == 1:
        return datetime.date.today() + datetime.timedelta(days=3)  # Review in 3 days
    elif score == 2:
        return datetime.date.today() + datetime.timedelta(days=7)  # Review in 7 days
    else:
        return datetime.date.today() + datetime.timedelta(days=14)  # Review in 2 weeks

# --- Hide Sidebar (Move this below set_page_config) ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stAppViewContainer"] {margin-left: 0px;}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Load Mistake Data ---
data = {
    "Student_ID": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5],
    "Mistake_Type": ["Grammar", "Vocabulary", "Grammar", "Vocabulary", "Grammar", "Grammar",
                     "Vocabulary", "Grammar", "Vocabulary", "Grammar", "Grammar", "Vocabulary",
                     "Vocabulary", "Grammar", "Grammar"],
    "Original_Sentence": ["I goes to school", "She took the wrong bus", "They is my friends",
                           "He miss the bus", "She were late", "They doesn't know",
                           "He don't have any", "She are happy", "We doesn't like it",
                           "He has car", "They has a house", "He bringed the book",
                           "I taked the bus", "She have been there", "They was there"],
    "Corrected_Sentence": ["I go to school", "She missed the bus", "They are my friends",
                            "He missed the bus", "She was late", "They don't know",
                            "He doesn't have any", "She is happy", "We don't like it",
                            "He has a car", "They have a house", "He brought the book",
                            "I took the bus", "She has been there", "They were there"]
}

df = pd.DataFrame(data)

# --- Initialize session state variables ---
if "seen_flashcards" not in st.session_state:
    st.session_state.seen_flashcards = {student: set() for student in df["Student_ID"].unique()}

if "progress" not in st.session_state:
    st.session_state.progress = {student: 0 for student in df["Student_ID"].unique()}

if "review_schedule" not in st.session_state:
    st.session_state.review_schedule = {}

if "flashcards_displayed" not in st.session_state:
    st.session_state.flashcards_displayed = {student: [] for student in df["Student_ID"].unique()}

# --- Streamlit UI ---
st.title("📝 Smart Flashcard Trainer")
st.write("Improve your grammar and vocabulary with AI-generated flashcards!")

# --- Flashcard Display ---
st.subheader("🎴 Practice Flashcards")

student_id = st.selectbox("Select Your Student ID", df["Student_ID"].unique())

# Filter data for the selected student
student_data = df[df["Student_ID"] == student_id]

# --- Flashcard Selection ---
today = datetime.date.today()
due_flashcards = student_data[student_data.index.isin(st.session_state.review_schedule.keys())]

if due_flashcards.empty:
    unseen_flashcards = student_data[~student_data.index.isin(st.session_state.seen_flashcards[student_id])]
    if unseen_flashcards.empty:
        st.session_state.seen_flashcards[student_id] = set()
        unseen_flashcards = student_data

    flashcard = unseen_flashcards.sample(1).iloc[0]
    st.session_state.seen_flashcards[student_id].add(flashcard.name)
else:
    flashcard = due_flashcards.sample(1).iloc[0]

# --- Flip Flashcard UI ---
flashcard_colors = ["#FFDDC1", "#FFABAB", "#FFC3A0", "#D5AAFF", "#85E3FF", "#B9FBC0"]
flashcard_color = random.choice(flashcard_colors)

st.markdown(
    f"""
    <style>
        .flip-card {{
            background-color: transparent;
            width: 450px;
            height: 300px;
            perspective: 1000px;
            display: flex;
            justify-content: center;
        }}
        .flip-card-inner {{
            position: relative;
            width: 450px;
            height: 300px;
            text-align: center;
            transform-style: preserve-3d;
            transition: transform 0.6s;
        }}
        .flip-card:hover .flip-card-inner {{
            transform: rotateY(180deg);
        }}
        .flip-card-front, .flip-card-back {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
        }}
        .flip-card-front {{
            background-color: {flashcard_color};
            color: black;
        }}
        .flip-card-back {{
            background-color: #D5AAFF;
            color: black;
            transform: rotateY(180deg);
        }}
    </style>

    <div class="flip-card">
        <div class="flip-card-inner">
            <div class="flip-card-front">
                ❌ Incorrect: {flashcard.Original_Sentence}
            </div>
            <div class="flip-card-back">
                ✅ Correct: {flashcard.Corrected_Sentence}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- "Next Flashcard" Button ---
if st.button("Next Flashcard"):
    difficulty = st.radio("Rate your confidence level:", ["Difficult 😣", "Okay 😐", "Easy 😊"], horizontal=True)

    # Update spaced repetition schedule
    score = {"Difficult 😣": 0, "Okay 😐": 1, "Easy 😊": 2}[difficulty]
    st.session_state.review_schedule[flashcard.name] = get_next_review_date(score)
    
    # Ensure that the data in session_state is serializable (convert numpy.int64 to int)
    st.session_state.progress[student_id] = int(st.session_state.progress[student_id] + 1)  # Update leaderboard progress

    # Update session state for new flashcard
    st.session_state.flashcards_displayed[student_id].append(flashcard.name)

# --- Leaderboard ---
st.subheader("🏆 Leaderboard")
leaderboard_data = pd.DataFrame(list(st.session_state.progress.items()), columns=["Student_ID", "Flashcards Reviewed"])
leaderboard_data = leaderboard_data.sort_values(by="Flashcards Reviewed", ascending=False)

st.dataframe(leaderboard_data, hide_index=True, use_container_width=True)

# --- Footer ---
st.markdown("Designed for Efficient Learning 🚀")
