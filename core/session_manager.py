import streamlit as st
from content.physics_topics import TOPICS

DEFAULT_TOPIC = "cinematica"


def initialize_session():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "student_profile" not in st.session_state:
        st.session_state.student_profile = {
            "name": "",
            "course_progress": "",
            "weaknesses": [],
            "completed_topics": [],
            "diagnostic_results": {},
            "exercise_results": [],
        }

    if "current_topic" not in st.session_state:
        st.session_state.current_topic = DEFAULT_TOPIC

    if "current_topic_label" not in st.session_state:
        st.session_state.current_topic_label = TOPICS[DEFAULT_TOPIC]["label"]

    if "conversation_state" not in st.session_state:
        st.session_state.conversation_state = {
            "phase": "initial",
            "current_question": None,
            "expected_concepts": [],
            "last_evaluation": None,
            "last_user_message": None,
            "last_tutor_action": None,
            "use_llm": False,
        }


def set_current_topic(topic_key: str):
    if topic_key in TOPICS:
        st.session_state.current_topic = topic_key
        st.session_state.current_topic_label = TOPICS[topic_key]["label"]


def append_chat(role: str, content: str):
    st.session_state.chat_history.append({
        "role": role,
        "content": content,
    })


def reset_chat():
    st.session_state.chat_history = []
    st.session_state.conversation_state = {
        "phase": "initial",
        "current_question": None,
        "expected_concepts": [],
        "last_evaluation": None,
        "last_user_message": None,
        "last_tutor_action": None,
        "use_llm": st.session_state.conversation_state.get("use_llm", False)
        if "conversation_state" in st.session_state
        else False,
    }
