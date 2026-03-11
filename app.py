import streamlit as st
from core.session_manager import initialize_session
from content.physics_topics import TOPICS

st.set_page_config(
    page_title="Tutor di Fisica 1 - UniBo",
    page_icon="🧲",
    layout="wide",
)

initialize_session()

st.title("🧲 Tutor di Fisica 1 - UniBo")
st.subheader("Tutor virtuale socratico per Fisica Generale 1")

st.markdown(
    """
Benvenuto. Questa app ti aiuta a studiare Fisica 1 con un approccio guidato:
non dà subito la soluzione completa, ma ti accompagna con domande progressive,
verifica dei prerequisiti e mini-esercizi.
"""
)

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"Argomento corrente: **{st.session_state.current_topic_label}**"
    )

with col2:
    st.success(
        f"Messaggi in sessione: **{len(st.session_state.chat_history)}**"
    )

st.markdown("## Scegli come iniziare")
st.page_link("pages/01_Chat_Tutor.py", label="Vai al Chat Tutor", icon="💬")
st.page_link("pages/02_Mappa_Argomenti.py", label="Apri la Mappa Argomenti", icon="🗺️")
st.page_link("pages/03_Diagnostica_Prerequisiti.py", label="Diagnostica Prerequisiti", icon="🧪")
st.page_link("pages/04_Esercizi_Guidati.py", label="Esercizi Guidati", icon="📝")
st.page_link("pages/05_Profilo_Studente.py", label="Profilo Studente", icon="👤")

st.markdown("## Argomenti disponibili")
for key, value in TOPICS.items():
    st.markdown(f"- **{value['label']}** — {value['short_description']}")
