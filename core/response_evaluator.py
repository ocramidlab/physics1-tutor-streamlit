import re


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s=/^+-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def count_concept_hits(answer: str, expected_concepts: list[str]) -> int:
    normalized = normalize_text(answer)
    hits = 0

    for concept in expected_concepts:
        concept_norm = normalize_text(concept)
        if concept_norm in normalized:
            hits += 1

    return hits


def count_marker_hits(answer: str, good_answer_markers: list[str]) -> int:
    normalized = normalize_text(answer)
    hits = 0

    for marker in good_answer_markers:
        marker_norm = normalize_text(marker)
        if marker_norm in normalized:
            hits += 1

    return hits


def evaluate_open_answer(
    answer: str,
    expected_concepts: list[str],
    good_answer_markers: list[str],
) -> dict:
    normalized = normalize_text(answer)

    if len(normalized) < 8:
        return {
            "status": "too_short",
            "score": 0,
            "feedback": "La risposta è troppo breve per capire bene il tuo ragionamento.",
        }

    uncertain_markers = [
        "non so",
        "non ricordo",
        "forse",
        "non ho capito",
        "non bene",
        "non saprei",
    ]
    if any(m in normalized for m in uncertain_markers):
        return {
            "status": "recover",
            "score": 0,
            "feedback": "Mi sembra che il prerequisito non sia ancora stabile. Facciamo un mini-ripasso.",
        }

    concept_hits = count_concept_hits(answer, expected_concepts)
    marker_hits = count_marker_hits(answer, good_answer_markers)

    score = concept_hits + (2 * marker_hits)

    if score >= 4:
        return {
            "status": "ok",
            "score": score,
            "feedback": "La tua risposta contiene gli elementi giusti. Possiamo procedere.",
        }

    if score >= 2:
        return {
            "status": "partial",
            "score": score,
            "feedback": "La risposta è sulla strada giusta, ma manca ancora qualche collegamento importante.",
        }

    return {
        "status": "recover",
        "score": score,
        "feedback": "La risposta non mostra ancora con chiarezza i concetti attesi. Conviene consolidare il prerequisito.",
    }
