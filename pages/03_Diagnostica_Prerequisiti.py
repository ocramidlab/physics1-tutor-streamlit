import streamlit as st
from core.session_manager import initialize_session
from core.tutor_engine import evaluate_diagnostic_answer
from content.physics_topics import TOPICS
from content.diagnostic_questions import DIAGNOSTIC_QUESTIONS

initialize_session()

st.title("🧪 Diagnostica Prerequisiti")

topic = st.selectbox(
    "Per quale argomento vuoi fare la diagnostica?",
    options=list(TOPICS.keys()),
    format_func=lambda x: TOPICS[x]["label"],
)

question = DIAGNOSTIC_QUESTIONS[topic][0]
st.markdown(f"**Domanda diagnostica:** {question}")

answer = st.text_area("Scrivi la tua risposta")

if st.button("Valuta risposta"):
    result = evaluate_diagnostic_answer(topic, answer)
    st.info(result["feedback"])

    st.session_state.student_profile["diagnostic_results"][topic] = result["status"]

    if result["status"] == "ok":
        if topic not in st.session_state.student_profile["completed_topics"]:
            st.session_state.student_profile["completed_topics"].append(topic)
