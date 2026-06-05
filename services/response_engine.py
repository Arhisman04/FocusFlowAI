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
IMPORTANT:

When writing mathematics:

Always use LaTeX.

Wrap all equations inside $$ $$

Examples:

$$
\int x dx = \frac{x^2}{2}+C
$$

$$
\frac{d}{dx}(x^3)=3x^2
$$

$$
a^2+b^2=c^2
$$

Never use:

[ equation ]

Never use:

( equation )

Always use proper LaTeX between $$ symbols.
Mathematical expressions must be displayed in LaTeX.

Every formula, derivation, fraction, matrix, integral, derivative and equation should be wrapped inside $$ $$.

Show derivations.

Verify calculations before answering.

For JEE-level questions:
- identify concepts
- derive equations
- solve systematically
- check final answer
For mathematics, physics and chemistry:

Always write formulas using LaTeX.

Example:

$$
\int x\,dx=\frac{x^2}{2}+C
$$

Use $$ $$ for display equations.
"""
    }

    return styles.get(length_mode, styles["adaptive"])