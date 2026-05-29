def detect_response_length(user_input):

    text = user_input.lower().strip()

    # Very Short / Casual
    short_inputs = [
        "hi", "hello", "hey",
        "ok", "okay", "lol",
        "thanks", "hmm"
    ]

    if text in short_inputs:
        return "short"

    # Deep / Serious
    if len(text.split()) > 40:
        return "long"

    # Technical
    technical_words = [
        "code",
        "error",
        "bug",
        "api",
        "flask",
        "python"
    ]

    for word in technical_words:

        if word in text:
            return "medium"

    return "adaptive"
def get_response_style(length_mode):

    styles = {

        "short": """
Keep response:
- short
- conversational
- natural
- 1-3 sentences maximum

Avoid:
- overexplaining
- bullet points
- structured plans
""",

        "medium": """
Keep response:
- practical
- clear
- concise

Use:
- short explanations
- readable formatting

Avoid:
- unnecessary paragraphs
""",

        "long": """
Respond deeply and thoughtfully.

Structure ideas clearly.
Prioritize insight and clarity.

Still sound human and natural.
""",

        "adaptive": """
Adapt response length naturally.

Do not force long answers.
Keep pacing human-like.
"""
    }

    return styles.get(length_mode, styles["adaptive"])