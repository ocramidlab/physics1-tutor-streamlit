import streamlit as st
from core.session_manager import initialize_session

initialize_session()

st.title("👤 Profilo Studente")

profile = st.session_state.student_profile

profile["name"] = st.text_input("Nome", value=profile["name"])
profile["course_progress"] = st.text_input(
    "A che punto sei del corso?",
    value=profile["course_progress"],
    placeholder="Es. sto iniziando dinamica, ho difficoltà con i vettori...",
)

st.markdown("## Stato attuale")
st.write(f"**Nome:** {profile['name'] or 'Non impostato'}")
st.write(f"**Progresso dichiarato:** {profile['course_progress'] or 'Non impostato'}")

st.markdown("## Argomenti completati")
if profile["completed_topics"]:
    for topic in profile["completed_topics"]:
        st.markdown(f"- {topic}")
else:
    st.write("Nessun argomento segnato come completato.")

st.markdown("## Risultati diagnostici")
if profile["diagnostic_results"]:
    st.json(profile["diagnostic_results"])
else:
    st.write("Nessuna diagnostica registrata.")

st.markdown("## Esercizi svolti")
if profile["exercise_results"]:
    st.json(profile["exercise_results"])
else:
    st.write("Nessun esercizio registrato.")
