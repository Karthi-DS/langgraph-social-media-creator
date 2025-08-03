from utils.rules import generate_topics

def plan_days(state):
    theme = state["theme"]
    days = state.get("days", 30)
    topics = generate_topics(theme, days)
    return {**state, "topics": topics}
