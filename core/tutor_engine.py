from content.physics_topics import TOPICS
from content.diagnostic_questions import DIAGNOSTIC_QUESTIONS
from core.prerequisite_checker import get_missing_prerequisites
from core.response_evaluator import evaluate_open_answer
from core.llm_client import evaluate_with_llm


KEYWORD_MAP = {
    "moto": "cinematica",
    "velocita": "cinematica",
    "velocità": "cinematica",
    "accelerazione": "cinematica",
    "forza": "dinamica",
    "newton": "dinamica",
    "energia": "lavoro_energia",
    "lavoro": "lavoro_energia",
    "urto": "quantita_moto",
    "quantita di moto": "quantita_moto",
    "quantità di moto": "quantita_moto",
    "impulso": "quantita_moto",
    "momento angolare": "rotazioni",
    "rotazione": "rotazioni",
    "momento torcente": "rotazioni",
    "gravitazione": "gravitazione",
    "gravita": "gravitazione",
    "gravità": "gravitazione",
    "orbita": "gravitazione",
    "termodinamica": "termodinamica",
    "gas": "termodinamica",
    "temperatura": "termodinamica",
    "calore": "termodinamica",
    "pressione": "fluidi",
    "fluido": "fluidi",
    "bernoulli": "fluidi",
    "archimede": "fluidi",
    "oscillazione": "oscillazioni",
    "oscillazioni": "oscillazioni",
    "molla": "oscillazioni",
    "pendolo": "oscillazioni",
}


def detect_topic(user_input: str, fallback_topic: str = "cinematica") -> str:
    """
    Prova a identificare l'argomento a partire da keyword semplici.
    Se non trova nulla, usa l'argomento corrente come fallback.
    """
    text = user_input.lower()

    for keyword, topic in KEYWORD_MAP.items():
        if keyword in text:
            return topic

    return fallback_topic


def build_diagnostic_step(topic_key: str) -> dict:
    """
    Costruisce il primo passo diagnostico per l'argomento scelto.
    """
    diag = DIAGNOSTIC_QUESTIONS[topic_key]

    return {
        "phase": "diagnostic",
        "question": diag["question"],
        "expected_concepts": diag["expected_concepts"],
        "response": (
            f"Prima di procedere con **{TOPICS[topic_key]['label']}**, "
            f"verifichiamo un prerequisito importante.\n\n"
            f"**Domanda diagnostica:** {diag['question']}"
        ),
    }


def build_guided_step(topic_key: str, custom_question: str | None = None) -> dict:
    """
    Costruisce il passo di guida socratica.
    Se custom_question è presente, usa quella al posto della starter_question del topic.
    """
    starter = custom_question or TOPICS[topic_key]["starter_question"]

    return {
        "phase": "guided",
        "question": starter,
        "expected_concepts": [],
        "response": (
            f"Bene, possiamo passare a **{TOPICS[topic_key]['label']}**.\n\n"
            f"Non ti do subito la soluzione completa.\n\n"
            f"**Prima domanda guida:** {starter}"
        ),
    }


def build_recovery_step(topic_key: str) -> dict:
    """
    Costruisce un passo di recupero/ripasso quando la diagnostica non è sufficiente.
    """
    diag = DIAGNOSTIC_QUESTIONS[topic_key]

    return {
        "phase": "review",
        "question": diag["question"],
        "expected_concepts": diag["expected_concepts"],
        "response": (
            f"{diag['recovery_message']}\n\n"
            f"Prova ora a rispondere di nuovo con parole tue, in modo un po' più esplicito."
        ),
    }


def _evaluate_diagnostic_answer(topic_key: str, user_input: str, conversation_state: dict) -> dict:
    """
    Valuta la risposta dello studente nella fase diagnostica o review.
    Prova prima con LLM; se non disponibile, usa il fallback locale.
    """
    diag = DIAGNOSTIC_QUESTIONS[topic_key]
    current_question = conversation_state.get("current_question", diag["question"])
    use_llm = conversation_state.get("use_llm", False)

    llm_result = None
    if use_llm:
        llm_result = evaluate_with_llm(
            topic_label=TOPICS[topic_key]["label"],
            question=current_question,
            student_answer=user_input,
            phase=conversation_state.get("phase", "diagnostic"),
        )

    if llm_result is not None:
        evaluation = llm_result
    else:
        evaluation = evaluate_open_answer(
            answer=user_input,
            expected_concepts=diag["expected_concepts"],
            good_answer_markers=diag["good_answer_markers"],
        )
        evaluation.setdefault("next_question", TOPICS[topic_key]["starter_question"])
        evaluation.setdefault("misconceptions", [])
        evaluation.setdefault("confidence", 0.0)

    return evaluation


def _format_misconceptions(evaluation: dict, prefix: str) -> str:
    """
    Restituisce una stringa pronta da mostrare con eventuali nodi concettuali emersi.
    """
    misconceptions = evaluation.get("misconceptions", [])

    if misconceptions:
        return f"\n\n{prefix}: " + ", ".join(misconceptions)

    return ""


def process_user_message(
    user_input: str,
    student_profile: dict,
    current_topic: str,
    conversation_state: dict,
) -> dict:
    """
    Funzione principale del tutor.

    Input:
    - user_input: messaggio dello studente
    - student_profile: profilo dello studente in sessione
    - current_topic: topic attualmente selezionato
    - conversation_state: stato corrente della conversazione

    Output:
    Dizionario con:
    - topic
    - mode
    - response
    - phase
    - current_question
    - expected_concepts
    - prerequisites_missing
    - evaluation (opzionale)
    - mark_topic_completed (opzionale)
    """
    phase = conversation_state.get("phase", "initial")

    # ---------------------------
    # FASE INIZIALE
    # ---------------------------
    if phase == "initial":
        detected_topic = detect_topic(user_input, fallback_topic=current_topic)
        known_skills = student_profile.get("completed_topics", [])
        missing = get_missing_prerequisites(detected_topic, known_skills)

        if missing:
            step = build_diagnostic_step(detected_topic)
            return {
                "topic": detected_topic,
                "mode": "diagnostic",
                "response": step["response"],
                "phase": step["phase"],
                "current_question": step["question"],
                "expected_concepts": step["expected_concepts"],
                "prerequisites_missing": missing,
            }

        step = build_guided_step(detected_topic)
        return {
            "topic": detected_topic,
            "mode": "guided",
            "response": step["response"],
            "phase": step["phase"],
            "current_question": step["question"],
            "expected_concepts": step["expected_concepts"],
            "prerequisites_missing": [],
        }

    # ---------------------------
    # FASE DIAGNOSTICA / REVIEW
    # ---------------------------
    if phase in ("diagnostic", "review"):
        topic_key = current_topic
        evaluation = _evaluate_diagnostic_answer(topic_key, user_input, conversation_state)

        if evaluation["status"] == "ok":
            next_question = evaluation.get("next_question") or TOPICS[topic_key]["starter_question"]

            step = build_guided_step(topic_key, custom_question=next_question)

            return {
                "topic": topic_key,
                "mode": "guided",
                "response": (
                    f"{evaluation['feedback']}\n\n"
                    f"{step['response']}"
                ),
                "phase": step["phase"],
                "current_question": step["question"],
                "expected_concepts": step["expected_concepts"],
                "prerequisites_missing": [],
                "evaluation": evaluation,
                "mark_topic_completed": True,
            }

        if evaluation["status"] == "partial":
            next_question = evaluation.get("next_question") or TOPICS[topic_key]["starter_question"]
            misconception_text = _format_misconceptions(
                evaluation,
                prefix="Possibili punti da chiarire",
            )

            return {
                "topic": topic_key,
                "mode": "hint",
                "response": (
                    f"{evaluation['feedback']}"
                    f"{misconception_text}\n\n"
                    f"**Domanda successiva:** {next_question}"
                ),
                "phase": "hint",
                "current_question": next_question,
                "expected_concepts": [],
                "prerequisites_missing": [],
                "evaluation": evaluation,
            }

        misconception_text = _format_misconceptions(
            evaluation,
            prefix="Vedo questi nodi concettuali",
        )
        step = build_recovery_step(topic_key)

        return {
            "topic": topic_key,
            "mode": "review",
            "response": (
                f"{evaluation['feedback']}"
                f"{misconception_text}\n\n"
                f"{step['response']}"
            ),
            "phase": step["phase"],
            "current_question": step["question"],
            "expected_concepts": step["expected_concepts"],
            "prerequisites_missing": [],
            "evaluation": evaluation,
        }

    # ---------------------------
    # FASE HINT
    # ---------------------------
    if phase == "hint":
        current_question = conversation_state.get("current_question") or TOPICS[current_topic]["starter_question"]

        return {
            "topic": current_topic,
            "mode": "guided",
            "response": (
                "Proviamo ad avanzare di un passo.\n\n"
                f"**Domanda guida:** {current_question}\n\n"
                "Rispondi concentrandoti sul primo principio fisico utile, "
                "oppure scrivi dati, incognite e legge che vuoi usare."
            ),
            "phase": "guided",
            "current_question": current_question,
            "expected_concepts": [],
            "prerequisites_missing": [],
        }

    # ---------------------------
    # FASE GUIDED
    # ---------------------------
    if phase == "guided":
        return {
            "topic": current_topic,
            "mode": "guided",
            "response": (
                "Sto seguendo la tua risposta nella fase guidata.\n\n"
                "Adesso prova a esplicitare il primo passo del ragionamento:\n"
                "- quali sono i dati,\n"
                "- qual è l'incognita,\n"
                "- quale legge fisica collegheresti a questi elementi?"
            ),
            "phase": "guided",
            "current_question": "Quali sono dati, incognita e legge fisica utile?",
            "expected_concepts": [],
            "prerequisites_missing": [],
        }

    # ---------------------------
    # FALLBACK
    # ---------------------------
    return {
        "topic": current_topic,
        "mode": "fallback",
        "response": (
            "Ripartiamo dall'argomento corrente.\n\n"
            "Descrivimi il dubbio in una frase e dimmi anche se vuoi:"
            "\n- capire la teoria,"
            "\n- risolvere un esercizio,"
            "\n- fare un ripasso dei prerequisiti."
        ),
        "phase": "initial",
        "current_question": None,
        "expected_concepts": [],
        "prerequisites_missing": [],
    }
