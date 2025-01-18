import streamlit as st
import pandas as pd
import random
import datetime

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

# Initialize session state variables
if "seen_flashcards" not in st.session_state:
    st.session_state.seen_flashcards = {student: set() for student in df["Student_ID"].unique()}

if "progress" not in st.session_state:
    st.session_state.progress = {student: 0 for student in df["Student_ID"].unique()}

if "review_schedule" not in st.session_state:
    st.session_state.review_schedule = {}

if "flashcards_displayed" not in st.session_state:
    st.session_state.flashcards_displayed = {student: [] for student in df["Student_ID"].unique()}

# --- Streamlit UI ---
st.set_page_config(page_title="Flashcard Trainer", layout="wide")

# --- Header ---
st.title("📝 Smart Flashcard Trainer")
st.write("Improve your grammar and vocabulary with AI-generated flashcards!")

# --- Flashcard Display ---
st.subheader("🎴 Practice Flashcards")

student_id = st.selectbox("Select Your Student ID", df["Student_ID"].unique())

# Filter data for the selected student
student_data = df[df["Student_ID"] == student_id]

# --- Check for due flashcards ---
today = datetime.date.today()
due_flashcards = student_data[student_data.index.isin(st.session_state.review_schedule.keys())]

if due_flashcards.empty:
    # Show unseen flashcards first
    unseen_flashcards = student_data[~student_data.index.isin(st.session_state.seen_flashcards[student_id])]

    if unseen_flashcards.empty:
        # If all flashcards are seen, reset the list
        st.session_state.seen_flashcards[student_id] = set()
        unseen_flashcards = student_data

    # Pick one unseen flashcard
    flashcard = unseen_flashcards.sample(1).iloc[0]
    st.session_state.seen_flashcards[student_id].add(flashcard.name)
else:
    # Pick a flashcard from the due reviews
    flashcard = due_flashcards.sample(1).iloc[0]

# --- Colorful Flashcards ---
flashcard_colors = ["#FFDDC1", "#FFABAB", "#FFC3A0", "#D5AAFF", "#85E3FF", "#B9FBC0"]
flashcard_color = random.choice(flashcard_colors)

st.markdown(
    f"""
    <div style="
        background-color: {flashcard_color}; 
        padding: 20px; 
        border-radius: 10px; 
        text-align: center; 
        font-size: 20px;
        font-weight: bold;
    ">
        <p style="color: #000;">❌ Incorrect: {flashcard.Original_Sentence}</p>
        <hr style="border: 1px solid #000;">
        <p style="color: #000;">✅ Correct: {flashcard.Corrected_Sentence}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- User Feedback ---
st.subheader("How easy was this?")
difficulty = st.radio("Rate your confidence level:", ["Difficult 😣", "Okay 😐", "Easy 😊"], horizontal=True)

# Update spaced repetition schedule
if st.button("Next Flashcard"):
    score = {"Difficult 😣": 0, "Okay 😐": 1, "Easy 😊": 2}[difficulty]
    st.session_state.review_schedule[flashcard.name] = get_next_review_date(score)
    st.session_state.progress[student_id] += 1  # Update leaderboard progress
    st.experimental_rerun()

# --- Leaderboard ---
st.subheader("🏆 Leaderboard")
leaderboard_data = pd.DataFrame(list(st.session_state.progress.items()), columns=["Student_ID", "Flashcards Reviewed"])
leaderboard_data = leaderboard_data.sort_values(by="Flashcards Reviewed", ascending=False)

st.dataframe(leaderboard_data, hide_index=True, use_container_width=True)

# --- Footer ---
st.sidebar.info("Created by AI Flashcard Trainer 🚀")
