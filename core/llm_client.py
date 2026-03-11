import json
from typing import Optional

import streamlit as st
from openai import OpenAI


def llm_available() -> bool:
    return "OPENAI_API_KEY" in st.secrets and bool(st.secrets["OPENAI_API_KEY"])


def get_client() -> OpenAI:
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def evaluate_with_llm(
    topic_label: str,
    question: str,
    student_answer: str,
    phase: str = "diagnostic",
) -> Optional[dict]:
    if not llm_available():
        return None

    client = get_client()

    system_prompt = """
Sei un tutor universitario di Fisica Generale 1 con stile socratico.
Valuta la risposta di uno studente senza risolvere subito l'esercizio.
Devi restituire SOLO un JSON valido con questa struttura:

{
  "status": "ok" | "partial" | "recover",
  "feedback": "stringa breve e chiara in italiano",
  "next_question": "stringa breve con la prossima domanda socratica",
  "misconceptions": ["lista", "di", "errori"],
  "confidence": 0.0
}

Regole:
- "ok" se la risposta è concettualmente corretta anche se non perfetta.
- "partial" se c'è una base giusta ma mancano collegamenti importanti.
- "recover" se la risposta è errata, fuori tema, troppo vaga o mostra confusione forte.
- Mantieni tono didattico, tecnico e conciso.
- Non scrivere testo fuori dal JSON.
"""

    user_prompt = f"""
Argomento: {topic_label}
Fase: {phase}
Domanda del tutor: {question}
Risposta dello studente: {student_answer}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        content = response.choices[0].message.content
        if not content:
            return None

        parsed = json.loads(content)

        if not isinstance(parsed, dict):
            return None

        parsed.setdefault("status", "recover")
        parsed.setdefault("feedback", "Risposta non valutabile con sufficiente affidabilità.")
        parsed.setdefault("next_question", "Prova a riformulare la risposta con parole più precise.")
        parsed.setdefault("misconceptions", [])
        parsed.setdefault("confidence", 0.0)

        return parsed

    except Exception:
        return None
