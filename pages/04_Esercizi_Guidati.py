import streamlit as st
from core.session_manager import initialize_session
from content.guided_exercises import GUIDED_EXERCISES
from content.physics_topics import TOPICS

initialize_session()

st.title("📝 Esercizi Guidati")

available_topics = list(GUIDED_EXERCISES.keys())

topic = st.selectbox(
    "Scegli un argomento",
    options=available_topics,
    format_func=lambda x: TOPICS[x]["label"],
)

exercises = GUIDED_EXERCISES[topic]

for i, ex in enumerate(exercises):
    with st.container(border=True):
        st.subheader(ex["title"])
        st.caption(f"Difficoltà: {ex['level']}")
        st.write(ex["problem"])

        show_steps = st.checkbox("Mostra guida passo-passo", key=f"steps_{topic}_{i}")
        if show_steps:
            for idx, step in enumerate(ex["steps"], start=1):
                st.markdown(f"**Passo {idx}.** {step}")

        if st.button("Segna come svolto", key=f"done_{topic}_{i}"):
            st.session_state.student_profile["exercise_results"].append({
                "topic": topic,
                "title": ex["title"],
                "status": "completed",
            })
            st.success("Esercizio salvato nel profilo.")
