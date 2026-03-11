DIAGNOSTIC_QUESTIONS = {
    "cinematica": {
        "question": "Sai distinguere tra posizione, velocità e accelerazione?",
        "expected_concepts": [
            "posizione",
            "velocità",
            "accelerazione",
            "variazione nel tempo",
        ],
        "good_answer_markers": [
            "posizione indica dove si trova il corpo",
            "velocità è la variazione della posizione",
            "accelerazione è la variazione della velocità",
        ],
        "recovery_message": "Facciamo un mini-ripasso: posizione, velocità e accelerazione descrivono aspetti diversi del moto.",
    },
    "dinamica": {
        "question": "Sai spiegare perché una forza risultante non nulla implica accelerazione?",
        "expected_concepts": [
            "forza risultante",
            "accelerazione",
            "seconda legge di newton",
            "massa",
        ],
        "good_answer_markers": [
            "f uguale ma",
            "f = ma",
            "la forza risultante produce accelerazione",
        ],
        "recovery_message": "Ripasso: la seconda legge di Newton collega forza risultante, massa e accelerazione.",
    },
    "lavoro_energia": {
        "question": "Quando è più conveniente usare la conservazione dell'energia invece di F = m a?",
        "expected_concepts": [
            "energia meccanica",
            "stato iniziale",
            "stato finale",
            "forze conservative",
        ],
        "good_answer_markers": [
            "quando confronto stato iniziale e finale",
            "quando si conserva l'energia meccanica",
            "forze conservative",
        ],
        "recovery_message": "Idea chiave: l'energia è utile quando vuoi collegare stato iniziale e finale senza descrivere tutto il moto nel dettaglio.",
    },
    "quantita_moto": {
        "question": "In quale condizione la quantità di moto totale di un sistema si conserva?",
        "expected_concepts": [
            "sistema isolato",
            "forze esterne nulle",
            "quantità di moto totale",
        ],
        "good_answer_markers": [
            "sistema isolato",
            "forze esterne nulle",
            "assenza di forza esterna risultante",
        ],
        "recovery_message": "Mini-ripasso: la quantità di moto totale si conserva se il sistema è isolato o la risultante delle forze esterne è trascurabile.",
    },
    "rotazioni": {
        "question": "Che cosa rappresenta il momento di una forza rispetto a un asse?",
        "expected_concepts": [
            "asse",
            "rotazione",
            "braccio",
            "momento della forza",
        ],
        "good_answer_markers": [
            "tendenza a far ruotare",
            "dipende dal braccio",
            "dipende dalla distanza dall'asse",
        ],
        "recovery_message": "Ripasso: il momento misura quanto una forza tende a produrre rotazione rispetto a un asse.",
    },
    "gravitazione": {
        "question": "Come dipende la forza gravitazionale dalla distanza tra due masse?",
        "expected_concepts": [
            "inverso del quadrato",
            "distanza",
            "masse",
            "legge di gravitazione",
        ],
        "good_answer_markers": [
            "inversamente proporzionale al quadrato della distanza",
            "1 su r quadro",
            "1/r^2",
        ],
        "recovery_message": "Mini-ripasso: la forza gravitazionale decresce con l'inverso del quadrato della distanza.",
    },
    "oscillazioni": {
        "question": "Nel moto armonico, come è legata la forza di richiamo allo spostamento?",
        "expected_concepts": [
            "forza di richiamo",
            "spostamento",
            "proporzionale",
            "verso opposto",
        ],
        "good_answer_markers": [
            "proporzionale allo spostamento",
            "verso opposto",
            "f = -kx",
        ],
        "recovery_message": "Ripasso: nel moto armonico la forza di richiamo è proporzionale allo spostamento e diretta in verso opposto.",
    },
    "fluidi": {
        "question": "Come definisci la pressione in fisica?",
        "expected_concepts": [
            "forza",
            "superficie",
            "area",
            "pressione",
        ],
        "good_answer_markers": [
            "forza su unità di superficie",
            "forza diviso area",
            "p = f/a",
        ],
        "recovery_message": "Mini-ripasso: la pressione è la forza esercitata per unità di superficie.",
    },
    "termodinamica": {
        "question": "Sai distinguere tra calore, temperatura ed energia interna?",
        "expected_concepts": [
            "calore",
            "temperatura",
            "energia interna",
            "trasferimento di energia",
        ],
        "good_answer_markers": [
            "il calore è energia trasferita",
            "la temperatura misura lo stato termico",
            "l'energia interna è energia microscopica del sistema",
        ],
        "recovery_message": "Ripasso: temperatura, calore ed energia interna non sono la stessa cosa.",
    },
}
