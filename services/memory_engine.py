long_term_memory = {
    "weak_subjects": [],
    "stress_patterns": [],
    "learning_style": [],
    "productivity_issues": [],
    "emotional_patterns": []
}


def summarize_memory(user_message, ai_reply):

    text = user_message.lower()

    # Weak Subjects
    subjects = [
        "math",
        "physics",
        "chemistry",
        "biology",
        "computer"
    ]

    for subject in subjects:

        if f"weak in {subject}" in text:

            if subject not in long_term_memory["weak_subjects"]:
                long_term_memory["weak_subjects"].append(subject)

    # Stress Patterns
    stress_words = [
        "stress",
        "burnout",
        "pressure",
        "tired"
    ]

    for word in stress_words:

        if word in text:
            long_term_memory["stress_patterns"].append(word)

    # Productivity Issues
    productivity_words = [
        "procrastination",
        "can't focus",
        "distracted",
        "lazy"
    ]

    for word in productivity_words:

        if word in text:
            long_term_memory["productivity_issues"].append(word)

    # Emotional Patterns
    emotional_words = [
        "hopeless",
        "failure",
        "low confidence",
        "anxiety"
    ]

    for word in emotional_words:

        if word in text:
            long_term_memory["emotional_patterns"].append(word)

    return long_term_memory


def get_memory_context():

    return f"""

Long Term Student Memory:

Weak Subjects:
{long_term_memory['weak_subjects']}

Stress Patterns:
{long_term_memory['stress_patterns']}

Productivity Issues:
{long_term_memory['productivity_issues']}

Emotional Patterns:
{long_term_memory['emotional_patterns']}
"""