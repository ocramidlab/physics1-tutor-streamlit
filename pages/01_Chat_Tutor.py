import streamlit as st
from core.session_manager import initialize_session, append_chat, set_current_topic, reset_chat
from core.tutor_engine import process_user_message
from content.physics_topics import TOPICS

initialize_session()

st.session_state.conversation_state["use_llm"] = st.toggle(
    "Usa valutazione LLM",
    value=st.session_state.conversation_state.get("use_llm", False),
)

st.title("💬 Chat Tutor")

topic = st.selectbox(
    "Seleziona l'argomento",
    options=list(TOPICS.keys()),
    format_func=lambda x: TOPICS[x]["label"],
    index=list(TOPICS.keys()).index(st.session_state.current_topic),
)

set_current_topic(topic)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.write(f"Argomento attivo: **{TOPICS[topic]['label']}**")

with col2:
    st.write(f"Fase: **{st.session_state.conversation_state['phase']}**")

with col3:
    if st.button("Reset chat"):
        reset_chat()
        st.rerun()

st.divider()

with st.expander("Debug stato conversazione"):
    st.json(st.session_state.conversation_state)

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Scrivi il tuo dubbio di fisica o rispondi alla domanda del tutor...")

if user_input:
    append_chat("user", user_input)

    st.session_state.conversation_state["last_user_message"] = user_input

    result = process_user_message(
        user_input=user_input,
        student_profile=st.session_state.student_profile,
        current_topic=st.session_state.current_topic,
        conversation_state=st.session_state.conversation_state,
    )

    set_current_topic(result["topic"])

    st.session_state.conversation_state["phase"] = result["phase"]
    st.session_state.conversation_state["current_question"] = result["current_question"]
    st.session_state.conversation_state["expected_concepts"] = result["expected_concepts"]
    st.session_state.conversation_state["last_tutor_action"] = result["mode"]

    if "evaluation" in result:
        st.session_state.conversation_state["last_evaluation"] = result["evaluation"]

    if result.get("mark_topic_completed"):
        topic_key = result["topic"]
        if topic_key not in st.session_state.student_profile["completed_topics"]:
            st.session_state.student_profile["completed_topics"].append(topic_key)

    append_chat("assistant", result["response"])

    st.rerun()
