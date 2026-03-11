import streamlit as st
from typing import Optional


def llm_available() -> bool:
    return "OPENAI_API_KEY" in st.secrets and bool(st.secrets["OPENAI_API_KEY"])


def evaluate_with_llm(topic_label: str, question: str, student_answer: str) -> Optional[dict]:
    """
    Stub sicuro: per ora restituisce None se non implementato.
    """
    if not llm_available():
        return None

    return None
