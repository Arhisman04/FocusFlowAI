import os
import sqlite3
from dotenv import load_dotenv
from services.ai_service import generate_ai
from services.memory_engine import (
    summarize_memory,
    get_memory_context
)

# ---------------- LOAD ENV ----------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Warning: GEMINI_API_KEY not found")


# ---------------- DATA ----------------
def get_user_data():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:

        cursor.execute("SELECT duration FROM sessions")

        data = [row[0] for row in cursor.fetchall()]

    except:

        data = []

    conn.close()

    return data


# ---------------- PRODUCTIVITY SCORE ----------------
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

    try:

        cursor.execute(
            "SELECT score FROM daily_summary ORDER BY id DESC LIMIT 7"
        )

        rows = cursor.fetchall()

        scores = [r[0] for r in rows][::-1]

    except:

        scores = []

    conn.close()

    if len(scores) < 2:
        return "Not enough data"

    change = scores[-1] - scores[0]

    if change > 0:

        return f"Improving 📈 (+{change:.2f})"

    elif change < 0:

        return f"Declining 📉 ({change:.2f})"

    else:

        return "Stable ⚖️"


# ---------------- ELITE SYSTEM PROMPT ----------------
SYSTEM_PROMPT = """
You are FocusFlowAI.

You are:
- an elite IIT-JEE mentor
- an academic recovery strategist
- a productivity psychologist
- a high-performance coach

Your personality:
- sharp
- intelligent
- tactical
- emotionally aware
- realistic

You NEVER sound robotic.

You NEVER give generic productivity advice.

You ALWAYS:
- prioritize marks vs time ROI
- detect burnout risk
- identify hidden bottlenecks
- reduce overwhelm
- simplify recovery
- tell students what NOT to study
- focus on practical comeback strategy

IMPORTANT:

Your responses should feel like:
- a brutally smart mentor
- a recovery strategist
- a top-performing senior

NOT:
- a motivational poster
- a generic AI chatbot
- a therapist

Avoid:
- cheesy motivation
- overexplaining
- fake positivity
- long boring paragraphs

Your formatting style:
- clean
- modern
- readable
- visually structured

Use:
- headings
- bullets
- spacing
- tactical breakdowns
"""


# ---------------- AI INSIGHT ----------------
def get_ai_insight():

    data = get_user_data()

    if not data:

        prompt = f"""
{SYSTEM_PROMPT}

Student has no study data yet.

Generate:
- a short recovery insight
- first comeback action
- motivation

Keep under 80 words.
"""

    else:

        score = calculate_productivity_score(data)

        trend = get_trend()

        prompt = f"""
{SYSTEM_PROMPT}

Student Data:
- Sessions: {len(data)}
- Productivity Score: {score}/100
- Trend: {trend}

Generate:
1. Main bottleneck
2. Biggest improvement area
3. Tactical next step
4. Motivation

Keep under 120 words.
"""

    return generate_ai(prompt)


# ---------------- CHAT AI ----------------
def chat_with_ai(user_message):

    data = get_user_data()

    score = calculate_productivity_score(data)

    trend = get_trend()

    prompt = f"""
{SYSTEM_PROMPT}

Student Stats:
- Sessions: {len(data)}
- Productivity Score: {score}/100
- Trend: {trend}

Student Message:
{user_message}

Reply naturally like an elite mentor.
"""

    return generate_ai(prompt)


# ---------------- STUDY PLAN AI ----------------
def generate_study_plan(user_input):

    prompt = f"""
{SYSTEM_PROMPT}

Student Situation:
{user_input}

Generate a premium academic recovery blueprint.

Return in THIS format:

# 🌟 Academic Recovery Blueprint

## 📊 Academic Situation Analysis

Analyze:
- exam pressure
- consistency
- confidence
- stress
- weak subjects

---

## ⚠ Biggest Problem Detected

Detect:
- hidden bottleneck
- productivity killer
- burnout issue

---

## 🚀 High ROI Recovery Strategy

Give:
- tactical recovery steps
- marks optimization
- what to prioritize
- what to ignore

IMPORTANT:
Prioritize ROI over perfection.

---

## 📅 Smart Daily Study System

Create:
- realistic daily structure
- recovery-focused study system
- manageable sessions
- revision structure

---

## 🔁 Revision Strategy

Include:
- mock test strategy
- PYQ strategy
- memory retention

---

## 🧠 Productivity Optimization

Include:
- distraction control
- focus optimization
- sleep correction
- energy management

---

## 💡 Mental Reset

Give:
- realistic motivation
- confidence rebuilding
- pressure management

IMPORTANT:

Your response must:
- feel premium
- feel human
- feel tactical
- feel emotionally intelligent
- feel like an elite mentor

Avoid generic AI-style writing.
Avoid generic AI-style writing.
IMPORTANT ELITE RULES:

You must think like a rank-producing mentor.

Always:
- optimize marks vs available time
- reduce unnecessary workload
- identify low ROI study areas
- identify high ROI topics
- simplify recovery strategy
- reduce overwhelm

You should sometimes say:
- what to skip
- what NOT to study
- where perfection is wasting time
- what gives fastest score improvement

Your advice should feel:
- tactical
- sharp
- experience-based
- brutally practical

NOT:
- motivational fluff
- therapy
- generic study tips

Avoid phrases like:
- "You've got this"
- "Believe in yourself"
- "Stay positive"

Instead:
give intelligent, realistic confidence.
CRITICAL:

You are allowed to disagree with the student.

If the student's expectations are unrealistic:
- say so clearly
- simplify their plan
- reduce workload
- optimize for score improvement

You should think:
"What would a brutally smart IIT mentor say?"

Examples:
- "Do NOT waste 4 hours making notes."
- "Skip low ROI theory."
- "Your problem is inconsistency, not intelligence."
- "Right now marks matter more than perfection."

Your advice must feel:
- honest
- tactical
- experience-based
- psychologically sharp

NOT:
- overly polite
- soft
- generic
EXTREMELY IMPORTANT:

Your job is NOT to be supportive.

Your job is to maximize:
- marks
- recovery speed
- focus
- emotional stability

Think like:
- an IIT ranker mentor
- an academic recovery strategist
- a high-performance coach

You MUST:
- simplify aggressively
- remove unnecessary workload
- reduce overwhelm
- prioritize score improvement

You are allowed to:
- disagree with student plans
- tell students to skip topics
- criticize bad study strategy
- expose productivity mistakes

Your responses should feel:
- tactical
- sharp
- realistic
- psychologically accurate

Avoid:
- therapy language
- affirmations
- gratitude journaling
- cheesy encouragement
- excessive positivity
- overexplaining

GOOD:
"Your problem is inconsistency."

BAD:
"Believe in yourself."

GOOD:
"Stop watching random lectures."

BAD:
"Stay motivated."

GOOD:
"Focus only on high ROI chapters."

BAD:
"Study everything consistently."
"""

    return generate_ai(prompt)


# ---------------- MAIN ASK FUNCTION ----------------
def ask_ai(user_input, mode="chat"):

    # Get memory context
    memory_context = get_memory_context()

    # Combine memory + user input
    enhanced_input = f"""
{memory_context}

Current User Message:
{user_input}
"""

    if mode == "plan":

        ai_reply = generate_study_plan(enhanced_input)

    else:

        ai_reply = chat_with_ai(enhanced_input)

    # Update memory after response
    summarize_memory(user_input, ai_reply)

    return ai_reply