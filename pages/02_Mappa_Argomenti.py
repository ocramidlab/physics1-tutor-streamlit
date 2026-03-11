import streamlit as st
from core.session_manager import initialize_session, set_current_topic
from content.physics_topics import TOPICS

initialize_session()

st.title("🗺️ Mappa Argomenti")

for topic_key, topic in TOPICS.items():
    with st.expander(topic["label"]):
        st.markdown(f"**Descrizione:** {topic['short_description']}")
        st.markdown(f"**Prerequisiti:** {', '.join(topic['prerequisites'])}")
        st.markdown("**Sottoargomenti:**")
        for item in topic["subtopics"]:
            st.markdown(f"- {item}")

        if st.button(f"Imposta come argomento corrente: {topic['label']}", key=topic_key):
            set_current_topic(topic_key)
            st.success(f"Argomento corrente impostato su {topic['label']}")
