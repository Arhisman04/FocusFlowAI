import re


def route_agent(user_message):

    msg = user_message.lower().strip()

    # =========================
    # KEYWORD GROUPS
    # =========================

    stress_keywords = [
        "stress", "burnout", "tired", "overwhelmed",
        "can't study", "demotivated", "exhausted",
        "anxious", "panic", "pressure", "depressed",
        "drained", "frustrated", "lost"
    ]

    planner_keywords = [
        "plan", "schedule", "routine",
        "timetable", "study plan",
        "roadmap", "strategy",
        "how should i study",
        "organize", "manage time"
    ]

    tutor_keywords = [
        "explain", "teach", "solve",
        "what is", "how does",
        "derive", "formula",
        "understand", "example",
        "question", "physics",
        "math", "chemistry",
        "biology", "english"
    ]

    productivity_keywords = [
        "focus", "productive", "discipline",
        "consistency", "dopamine",
        "procrastination", "lazy",
        "distraction", "phone addiction",
        "time waste"
    ]

    motivation_keywords = [
        "motivate", "motivation",
        "sad", "failure", "hopeless",
        "give up", "can't do",
        "not good enough",
        "fear", "self doubt"
    ]

    analytics_keywords = [
        "progress", "performance",
        "analytics", "report",
        "improvement", "score",
        "weakness", "strength",
        "track", "analysis"
    ]

    memory_keywords = [
        "remember", "memory",
        "save this", "note this",
        "don't forget"
    ]

    recovery_keywords = [
        "backlog", "exam soon",
        "syllabus not completed",
        "failed", "low marks",
        "recovery", "comeback",
        "behind schedule"
    ]

    # =========================
    # SCORING SYSTEM
    # =========================

    scores = {
        "recovery": 0,
        "planner": 0,
        "tutor": 0,
        "motivation": 0,
        "productivity": 0,
        "analytics": 0,
        "memory": 0
    }

    for w in stress_keywords:
        if w in msg:
            scores["recovery"] += 3

    for w in recovery_keywords:
        if w in msg:
            scores["recovery"] += 4

    for w in planner_keywords:
        if w in msg:
            scores["planner"] += 3

    for w in tutor_keywords:
        if w in msg:
            scores["tutor"] += 2

    for w in productivity_keywords:
        if w in msg:
            scores["productivity"] += 2

    for w in motivation_keywords:
        if w in msg:
            scores["motivation"] += 3

    for w in analytics_keywords:
        if w in msg:
            scores["analytics"] += 2

    for w in memory_keywords:
        if w in msg:
            scores["memory"] += 5

    # QUESTION BOOST
    if "?" in msg:
        scores["tutor"] += 1

    # LONG TEXT BOOST
    word_count = len(re.findall(r"\w+", msg))
    if word_count > 80:
        scores["recovery"] += 1
        scores["planner"] += 1

    # =========================
    # FINAL SELECTION
    # =========================

    best_mode = max(scores, key=scores.get)

    if scores[best_mode] == 0:
        return "chat"

    # =========================
    # SAFE MAPPING (CRITICAL FIX)
    # =========================

    mode_map = {
        "recovery": "chat",
        "planner": "plan",
        "tutor": "chat",
        "motivation": "chat",
        "productivity": "chat",
        "analytics": "chat",
        "memory": "chat"
    }

    return mode_map.get(best_mode, "chat")