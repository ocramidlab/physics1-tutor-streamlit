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

    if "last_response_mode" not in st.session_state:
        st.session_state.last_response_mode = "diagnostic"

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
