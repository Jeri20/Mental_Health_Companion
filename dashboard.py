import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_questionnaire_data, get_mood, get_user_journal_history, get_user_chat_history

def dashboard_page(user_id):
    st.title("📊 MindMate Dashboard")
    
    # Retrieve data from the database
    questionnaire_data = get_questionnaire_data(user_id)
    mood_data = get_mood(user_id)
    journal_data = get_user_journal_history(user_id)
    chat_data = get_user_chat_history(user_id)

    # === GAD and PHQ Scores ===
    if len(questionnaire_data) == 0:
        st.write("No questionnaire data available yet.")
    else:
        df = pd.DataFrame(questionnaire_data, columns=["date", "gad_score", "phq_score"])
        fig = px.line(df, x="date", y=["gad_score", "phq_score"], 
                      title="GAD & PHQ Scores Over Time", 
                      labels={"value": "Score", "variable": "Score Type"})
        st.plotly_chart(fig)

    # === Mood Data ===
    if len(mood_data) > 0:
        mood_df = pd.DataFrame(mood_data, columns=["date", "mood_score"])
        mood_fig = px.line(mood_df, x="date", y="mood_score", 
                          title="Mood Tracker Over Time", 
                          labels={"mood_score": "Mood Score"})
        st.plotly_chart(mood_fig)
    else:
        st.write("No mood data available yet.")

    # === Journal Sentiment ===
    if len(journal_data) > 0:
        journal_df = pd.DataFrame(journal_data, columns=["entry", "sentiment", "date"])
        journal_fig = px.line(journal_df, x="date", y="sentiment", 
                             title="Journal Sentiment Over Time", 
                             labels={"sentiment": "Sentiment Score"})
        st.plotly_chart(journal_fig)
    else:
        st.write("No journal data available yet.")

    # === Chat Sentiment ===
    if len(chat_data) > 0:
        chat_df = pd.DataFrame(chat_data, columns=["message", "sentiment", "date"])
        chat_fig = px.line(chat_df, x="date", y="sentiment", 
                          title="Chat Sentiment Over Time", 
                          labels={"sentiment": "Sentiment Score"})
        st.plotly_chart(chat_fig)
    else:
        st.write("No chat data available yet.")