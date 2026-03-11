import streamlit as st


def llm_available() -> bool:
    return "OPENAI_API_KEY" in st.secrets and bool(st.secrets["OPENAI_API_KEY"])


def evaluate_with_llm(topic_label: str, question: str, student_answer: str) -> dict | None:
    """
    Stub sicuro: per ora restituisce None se non implementato.
    In seguito lo sostituiremo con una vera chiamata API.
    """
    if not llm_available():
        return None

    # Placeholder per futura integrazione reale
    return None
