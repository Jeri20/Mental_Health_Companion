# mood_tracker.py
import streamlit as st
import datetime
from database import store_mood, get_mood

def mood_calendar(user_id):
    st.subheader("📅 Mood Calendar")
    mood = st.selectbox("How are you feeling today?", ["Happy", "Neutral", "Sad", "Anxious"])
    date = st.date_input("Select Date", datetime.date.today())

    if st.button("Save Mood"):
        store_mood(user_id, str(date), mood)
        st.success("Mood saved!")

    st.markdown("### Past Mood Entries:")
    data = get_mood(user_id)
    for row in data:
        st.text(f"{row[0]}: {row[1]}")
