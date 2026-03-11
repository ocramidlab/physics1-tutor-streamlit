from content.physics_topics import TOPICS
from content.diagnostic_questions import DIAGNOSTIC_QUESTIONS
from core.prerequisite_checker import get_missing_prerequisites

KEYWORD_MAP = {
    "moto": "cinematica",
    "velocità": "cinematica",
    "accelerazione": "cinematica",
    "forza": "dinamica",
    "newton": "dinamica",
    "energia": "lavoro_energia",
    "lavoro": "lavoro_energia",
    "urto": "quantita_moto",
    "quantità di moto": "quantita_moto",
    "momento angolare": "rotazioni",
    "rotazione": "rotazioni",
    "gravitazione": "gravitazione",
    "orbita": "gravitazione",
    "termodinamica": "termodinamica",
    "gas": "termodinamica",
    "pressione": "fluidi",
    "fluido": "fluidi",
    "oscillazione": "oscillazioni",
    "molla": "oscillazioni",
}

def detect_topic(user_input: str, fallback_topic: str = "cinematica") -> str:
    text = user_input.lower()
    for keyword, topic in KEYWORD_MAP.items():
        if keyword in text:
            return topic
    return fallback_topic

def get_diagnostic_question(topic_key: str) -> str:
    questions = DIAGNOSTIC_QUESTIONS.get(topic_key, [])
    if questions:
        return questions[0]
    return "Quale parte dell'argomento ti sembra più difficile?"

def generate_socratic_reply(user_input: str, student_profile: dict, current_topic: str):
    detected_topic = detect_topic(user_input, fallback_topic=current_topic)
    topic_info = TOPICS[detected_topic]

    known_skills = student_profile.get("completed_topics", [])
    missing = get_missing_prerequisites(detected_topic, known_skills)

    if missing:
        response = (
            f"Prima di affrontare **{topic_info['label']}**, conviene verificare alcuni prerequisiti: "
            f"**{', '.join(missing)}**.\n\n"
            f"Cominciamo con una domanda diagnostica: {get_diagnostic_question(detected_topic)}"
        )
        mode = "diagnostic"
        next_question = get_diagnostic_question(detected_topic)
    else:
        response = (
            f"Stai lavorando su **{topic_info['label']}**.\n\n"
            f"Non ti do subito la soluzione completa: iniziamo dal primo passo utile.\n\n"
            f"**Domanda guida:** {topic_info['starter_question']}"
        )
        mode = "socratic"
        next_question = topic_info["starter_question"]

    return {
        "topic": detected_topic,
        "mode": mode,
        "response": response,
        "next_question": next_question,
        "prerequisites_missing": missing,
    }

def evaluate_diagnostic_answer(topic_key: str, answer: str) -> dict:
    answer = answer.lower().strip()

    positive_markers = ["sì", "si", "penso di sì", "certo", "ok", "conosco", "so"]
    uncertain_markers = ["non so", "forse", "non ricordo", "poco", "non bene"]

    if any(m in answer for m in uncertain_markers):
        return {
            "status": "recover",
            "feedback": (
                "Va bene: prima di procedere conviene fare un mini-ripasso del prerequisito."
            )
        }

    if any(m in answer for m in positive_markers) or len(answer) > 20:
        return {
            "status": "ok",
            "feedback": (
                "Buon punto di partenza. Possiamo procedere con una guida socratica sull'argomento."
            )
        }

    return {
        "status": "unclear",
        "feedback": (
            "La risposta è un po' troppo breve per capire il tuo livello. "
            "Prova a spiegare il concetto con parole tue."
        )
    }
