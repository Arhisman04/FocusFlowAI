def detect_conversation_mode(message):

    msg = message.lower().strip()

    # Casual Conversation
    casual_words = [
        "hi", "hello", "hey", "yo",
        "lol", "lmao", "thanks",
        "ok", "okay", "hmm"
    ]

    if msg in casual_words:
        return "casual"

    # Emotional / Stress
    emotional_keywords = [
        "tired", "burnout", "stressed",
        "sad", "depressed", "hopeless",
        "can't", "failure", "pressure"
    ]

    for word in emotional_keywords:
        if word in msg:
            return "emotional"

    # Deep Thinking
    deep_keywords = [
        "meaning", "future", "purpose",
        "life", "mindset", "thinking",
        "philosophy"
    ]

    for word in deep_keywords:
        if word in msg:
            return "deep"

    # Technical
    technical_keywords = [
        "code", "python", "bug",
        "error", "flask", "api",
        "ai", "system"
    ]

    for word in technical_keywords:
        if word in msg:
            return "technical"

    return "normal"