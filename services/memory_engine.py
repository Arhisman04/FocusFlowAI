from services.ai_agent import ask_ai


def summarize_memory(user_message, ai_reply):

    prompt = f"""
You are an AI memory compression engine.

Summarize ONLY important long-term user traits.

IGNORE:
- greetings
- casual chat
- temporary statements

Extract:
- academic weaknesses
- stress patterns
- learning style
- productivity problems
- emotional patterns

Keep memory under 80 words.

Conversation:
User: {user_message}

AI: {ai_reply}
"""

    return ask_ai(prompt, mode="chat")
def summarize_memory(message, reply):

    return {
        "student_issue": message[:120],
        "ai_response": reply[:200]
    }
