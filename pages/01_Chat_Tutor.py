import streamlit as st
from core.session_manager import initialize_session, append_chat, set_current_topic, reset_chat
from core.tutor_engine import generate_socratic_reply
from content.physics_topics import TOPICS

initialize_session()

st.title("💬 Chat Tutor")

topic = st.selectbox(
    "Seleziona l'argomento",
    options=list(TOPICS.keys()),
    format_func=lambda x: TOPICS[x]["label"],
    index=list(TOPICS.keys()).index(st.session_state.current_topic),
)

set_current_topic(topic)

col1, col2 = st.columns([3, 1])
with col1:
    st.write(f"Argomento attivo: **{TOPICS[topic]['label']}**")
with col2:
    if st.button("Reset chat"):
        reset_chat()
        st.rerun()

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Scrivi il tuo dubbio di fisica...")

if user_input:
    append_chat("user", user_input)

    result = generate_socratic_reply(
        user_input=user_input,
        student_profile=st.session_state.student_profile,
        current_topic=st.session_state.current_topic,
    )

    set_current_topic(result["topic"])
    st.session_state.last_response_mode = result["mode"]

    append_chat("assistant", result["response"])

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        st.markdown(result["response"])
