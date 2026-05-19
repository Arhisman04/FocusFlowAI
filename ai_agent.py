import os
import sqlite3
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"


# ---------------- DATA ----------------
def get_user_data():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT duration FROM sessions")
    data = [r[0] for r in cursor.fetchall()]
    conn.close()
    return data


# ---------------- SCORE ----------------
def calculate_productivity_score(data):
    if not data:
        return 0

    sessions = len(data)
    total_time = sum(data)
    avg_time = total_time / sessions

    score = (
        min(sessions * 5, 40) +
        min(total_time / 60, 40) +
        min(avg_time / 10, 20)
    )

    return round(min(score, 100), 2)


# ---------------- TREND ----------------
def get_trend():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM daily_summary ORDER BY id DESC LIMIT 7")
    rows = cursor.fetchall()
    conn.close()

    scores = [r[0] for r in rows][::-1]

    if len(scores) < 2:
        return "Not enough data"

    change = scores[-1] - scores[0]

    if change > 0:
        return f"Improving 📈 (+{change:.2f})"
    elif change < 0:
        return f"Declining 📉 ({change:.2f})"
    return "Stable ⚖️"


# ---------------- AI INSIGHT (DASHBOARD) ----------------
def get_ai_insight():
    data = get_user_data()

    if not data:
        prompt = "User has no data. Encourage starting with 5 min focus session."
    else:
        score = calculate_productivity_score(data)
        trend = get_trend()

        prompt = f"""
You are FocusFlow AI productivity coach.

DATA:
- Sessions: {len(data)}
- Score: {score}/100
- Trend: {trend}

Give:
1 insight
1 bottleneck
1 action
1 motivation

Keep under 120 words.
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"AI Error: {str(e)}"


# ---------------- CHAT AI ----------------
def chat_with_ai(user_message):
    data = get_user_data()
    score = calculate_productivity_score(data)
    trend = get_trend()

    context = f"""
You are FocusFlow AI — a personal productivity assistant.

User stats:
- Sessions: {len(data)}
- Score: {score}/100
- Trend: {trend}

You help with:
- studying
- focus
- planning
- productivity improvement

Be natural, clear, and helpful.
"""

    prompt = context + "\nUser: " + user_message

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"