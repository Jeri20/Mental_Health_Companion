import streamlit as st
from database import store_questionnaire
from datetime import datetime  # Added for date handling

def questionnaire_page(user_id):
    st.subheader("📝 Mental Health Questionnaire")

    # GAD-7 Section
    st.markdown("#### Generalized Anxiety Disorder 7 (GAD-7)")
    gad_questions = [
        "Feeling nervous, anxious or on edge",
        "Not being able to stop or control worrying",
        "Worrying too much about different things",
        "Trouble relaxing",
        "Being so restless that it is hard to sit still",
        "Becoming easily annoyed or irritable",
        "Feeling afraid as if something awful might happen"
    ]

    st.markdown("""
    **Rate the following from 0 (Not at all) to 3 (Nearly every day):**
    - 0 = Not at all
    - 1 = Several days
    - 2 = More than half the days
    - 3 = Nearly every day
    """)
    gad_answers = []
    for i, q in enumerate(gad_questions):
        gad_answers.append(st.slider(q, 0, 3, key=f"gad_{i}"))  # Unique key for each slider

    st.markdown("---")
    
    # PHQ-9 Section
    st.markdown("#### Patient Health Questionnaire 9 (PHQ-9)")
    phq_questions = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself — or that you are a failure or have let yourself or your family down",
        "Trouble concentrating on things, such as reading the newspaper or watching television",
        "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual",
        "Thoughts that you would be better off dead or of hurting yourself in some way"
    ]

    st.markdown("""
    **Rate the following from 0 (Not at all) to 3 (Nearly every day):**
    - 0 = Not at all
    - 1 = Several days
    - 2 = More than half the days
    - 3 = Nearly every day
    """)
    phq_answers = []
    for i, q in enumerate(phq_questions):
        phq_answers.append(st.slider(q, 0, 3, key=f"phq_{i}"))  # Unique key for each slider

    if st.button("Submit"):
        gad_score = sum(gad_answers)
        phq_score = sum(phq_answers)
        current_date = datetime.now().date()  # Get current date
        store_questionnaire(user_id, gad_score, phq_score, current_date)  # Pass date
        st.success(f"Responses submitted! GAD Score: {gad_score}, PHQ Score: {phq_score}")