import streamlit as st
from datetime import datetime
from database import init_db, store_journal_entry, get_user_journal_history, register_user, login_user
from questionnaire import questionnaire_page
from mood_tracker import mood_calendar
from journal_analysis import analyze_sentiment
from chatbot import therapist_chat, user_histories
from dashboard import dashboard_page

# Initialize the database
init_db()

# Initialize session state
if "signed_in" not in st.session_state:
    st.session_state.signed_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sign In / Sign Up Page
def show_login_signup():
    st.title("🧠 MindMate Login / Sign Up")
    mode = st.radio("Choose Action", ["Login", "Sign Up"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Sign Up":
        if st.button("Register"):
            if register_user(email, password):
                st.success("✅ Registered successfully! You can now log in.")
            else:
                st.error("❌ Email already registered.")
    else:
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.signed_in = True
                st.session_state.user_id = user[0]  # Store user ID from DB
                st.success("✅ Logged in successfully.")
                st.rerun()
            else:
                st.error("❌ Invalid email or password.")

# Landing Page
def landing_page():
    st.title("Welcome to MindMate 💙")
    st.markdown("""
        ### You're not alone.
        MindMate is your emotional support app to help track, reflect, and get help when needed.

        **About Anxiety & Depression:**
        - Anxiety is your body's response to stress.
        - Depression causes a persistent feeling of sadness.

        ### 📞 Mental Health Helplines:

        #### India 🇮🇳
        - **iCall (TISS)**: +91 9152987821  
        - **Vandrevala Foundation**: 1860 266 2345 / 1800 233 3330  
        - **AASRA**: +91 9820466726

        #### United States 🇺🇸
        - **National Suicide Prevention Lifeline**: 988  
        - **Crisis Text Line**: Text HOME to 741741

        #### United Kingdom 🇬🇧
        - **Samaritans**: 116 123  
        - **SHOUT Crisis Text Line**: Text SHOUT to 85258

        ---
        If you’re in crisis, please reach out to a professional. You matter. 💙
    """)

# Journal Page
def journal_page(user_id):
    st.subheader("📔 Your Daily Journal")
    text = st.text_area("Write your thoughts...")
    if st.button("Save Entry"):
        score = analyze_sentiment(text)
        current_date = datetime.now().date()
        store_journal_entry(user_id, text, score, current_date)
        st.success(f"Journal saved. Sentiment Score: {score:.2f}")

# Chatbot Page
def chatbot_page(user_id):
    st.subheader("🤖 24/7 Therapist")
    st.markdown("### Chat with your Therapist")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Type your message...")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        history = get_user_journal_history(user_id)
        response = therapist_chat(user_id, prompt, history)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

    if st.button("Reset Conversation"):
        user_histories[user_id] = None
        st.session_state.chat_history = []
        st.info("Conversation reset.")

# Main App Logic
if not st.session_state.signed_in:
    show_login_signup()
else:
    st.sidebar.title("MindMate Menu")
    pages = ["Landing", "Questionnaire", "Journal", "Mood Calendar", "Chatbot", "Dashboard"]
    choice = st.sidebar.radio("Go to", pages)
    st.sidebar.markdown(f"👤 Logged in as User ID: `{st.session_state.user_id}`")

    if st.sidebar.button("Logout"):
        st.session_state.signed_in = False
        st.session_state.user_id = None
        st.session_state.chat_history = []
        st.rerun()

    user_id = st.session_state.user_id

    if choice == "Landing":
        landing_page()
    elif choice == "Questionnaire":
        questionnaire_page(user_id)
    elif choice == "Journal":
        journal_page(user_id)
    elif choice == "Mood Calendar":
        mood_calendar(user_id)
    elif choice == "Chatbot":
        chatbot_page(user_id)
    elif choice == "Dashboard":
        dashboard_page(user_id)
