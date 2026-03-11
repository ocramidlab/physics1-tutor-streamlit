from content.physics_topics import TOPICS

def get_missing_prerequisites(topic_key: str, known_skills: list[str]) -> list[str]:
    topic = TOPICS.get(topic_key, {})
    prerequisites = topic.get("prerequisites", [])
    return [p for p in prerequisites if p not in known_skills]

def topic_prerequisites(topic_key: str) -> list[str]:
    return TOPICS.get(topic_key, {}).get("prerequisites", [])
