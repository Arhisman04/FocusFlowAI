from flask import Flask, render_template, request, jsonify
import datetime

from services.ai_agent import ask_ai
from database.mongodb import (
    sessions_collection,
    tasks_collection,
    plans_collection
)

app = Flask(__name__)

# =========================
# 🏠 LANDING PAGE
# =========================
@app.route("/")
def landing():
    return render_template("landing.html")


# =========================
# 📊 DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():

    sessions = list(sessions_collection.find({}, {"_id": 0}))
    tasks = list(tasks_collection.find({}, {"_id": 0}))

    total_time = sum(s["duration"] for s in sessions) if sessions else 0

    score = min(
        100,
        int((total_time * 1.5) + (len(sessions) * 3))
    )

    xp = total_time * 5
    level = (xp // 100) + 1

    pending_tasks = len([t for t in tasks if not t["done"]])

    burnout = (
        "High 🔴" if total_time > 300
        else "Medium 🟠" if total_time > 150
        else "Low 🟢"
    )

    momentum = (
        "Excellent 🔥" if total_time > 250
        else "Improving 🚀" if total_time > 100
        else "Needs Consistency 📉"
    )

    ai_insight = (
        "You're building strong momentum 🚀"
        if total_time > 120
        else "Consistency is your biggest upgrade path 📈"
    )

    return render_template(
        "dashboard.html",
        total_sessions=len(sessions),
        total_time=total_time,
        avg_time=(total_time / len(sessions)) if sessions else 0,
        score=score,
        xp=xp,
        level=level,
        burnout=burnout,
        pending_tasks=pending_tasks,
        momentum=momentum,
        ai_insight=ai_insight
    )

    sessions = list(sessions_collection.find({}, {"_id": 0}))
    tasks = list(tasks_collection.find({}, {"_id": 0}))

    total_time = sum(s["duration"] for s in sessions) if sessions else 0

    score = min(
        100,
        int((total_time * 1.5) + (len(sessions) * 3))
    )

    xp = total_time * 5
    level = (xp // 100) + 1

    pending_tasks = len([t for t in tasks if not t["done"]])

    burnout = (
        "High 🔴" if total_time > 300
        else "Medium 🟠" if total_time > 150
        else "Low 🟢"
    )

    momentum = (
        "Excellent 🔥" if total_time > 250
        else "Improving 🚀" if total_time > 100
        else "Needs Consistency 📉"
    )

    return render_template(
        "dashboard.html",
        total_sessions=len(sessions),
        total_time=total_time,
        avg_time=(total_time / len(sessions)) if sessions else 0,
        score=score,
        xp=xp,
        level=level,
        burnout=burnout,
        pending_tasks=pending_tasks,
        momentum=momentum
    )

# =========================
# 💬 AI CHAT (AGENT CORE)
# =========================
@app.route("/chat", methods=["POST"])
def chat():

    msg = request.json.get("message", "")

    prompt = f"""
You are FocusFlowAI.

You are an elite AI tutor and academic mentor.

Student Message:
{msg}

Reply:
- clearly
- intelligently
- supportively
- practically

Keep the answer concise but useful.
"""

    reply = ask_ai(prompt, mode="chat")

    return jsonify({
        "response": reply
    })

# =========================
# 🧠 AI RECOVERY PLANNER
# =========================
@app.route("/planner")
def planner():
    return render_template("planner.html")
@app.route("/generate-plan", methods=["POST"])
def generate_plan():

    data = request.get_json()
    user_input = data.get("input", "")

    if not user_input:
        return jsonify({
            "status": "error",
            "plan": "No input provided"
        })

    enhanced_prompt = f"""
You are FocusFlowAI,
an elite AI Academic Recovery Coach.

Analyze the student's academic situation deeply.

Student Input:
{user_input}

Generate:

1. 📊 Recovery Analysis
2. 🎯 Readiness Score (0-100)
3. ⚠ Burnout Risk
4. 📚 Weakness Detection
5. 🚀 High ROI Topics
6. ⏰ Daily Study Strategy
7. 🔁 Revision Plan
8. 🧠 Productivity Advice
9. 💡 Motivation Guidance

Your response must:
- feel highly personalized
- be emotionally intelligent
- avoid generic advice
- prioritize realistic recovery
- optimize marks vs time

Keep formatting clean and visually readable.
"""

    plan = ask_ai(enhanced_prompt, mode="plan")

    plans_collection.insert_one({
        "type": "manual",
        "input": user_input,
        "plan": plan,
        "date": str(datetime.date.today())
    })

    return jsonify({
        "status": "success",
        "plan": plan
    })

# =========================
# ⚡ AUTO DAILY PLAN
# =========================
@app.route("/auto-plan")
def auto_plan():

    sessions = list(sessions_collection.find({}, {"_id": 0}))
    plans = list(plans_collection.find({}, {"_id": 0}))
    tasks = list(tasks_collection.find({}, {"_id": 0}))

    context = f"""
You are FocusFlowAI.

You are an autonomous academic optimization AI.

Past Sessions:
{sessions}

Past Plans:
{plans}

Pending Tasks:
{tasks}

Generate today's optimized study recovery plan.

Requirements:
- focus weak areas
- realistic workload
- include revision
- include breaks
- avoid burnout
- prioritize important topics
"""

    plan = ask_ai(context, mode="plan")

    plans_collection.insert_one({
        "type": "auto",
        "plan": plan,
        "date": str(datetime.date.today())
    })

    return jsonify({
        "plan": plan
    })

# =========================
# 📊 PERFORMANCE PREDICTION
# =========================
@app.route("/predict-performance")
def predict_performance():

    sessions = list(sessions_collection.find({}, {"_id": 0}))

    if not sessions:
        return jsonify({
            "risk": "unknown",
            "message": "Not enough data"
        })

    total = sum(s["duration"] for s in sessions)
    avg = total / len(sessions)

    readiness = min(100, int(avg * 1.8))

    if avg < 20:
        risk = "high 🔴"
    elif avg < 50:
        risk = "medium 🟠"
    else:
        risk = "low 🟢"

    return jsonify({
        "total_time": total,
        "avg_session": avg,
        "risk_level": risk,
        "readiness_score": readiness
    })

# =========================
# 🧠 RECOMMENDATION ENGINE
# =========================
@app.route("/recommend")
def recommend():

    sessions = list(sessions_collection.find({}, {"_id": 0}))
    tasks = list(tasks_collection.find({}, {"_id": 0}))

    total = sum(s["duration"] for s in sessions)
    pending = len([t for t in tasks if not t["done"]])

    prompt = f"""
You are an elite AI academic strategist.

Student Stats:
- Total Study Time: {total}
- Pending Tasks: {pending}

Generate:

1. Next Best Action
2. Focus Recommendation
3. Weakness Advice
4. Motivation
5. Productivity Improvement

Keep advice practical and personalized.
"""

    advice = ask_ai(prompt, mode="chat")

    return jsonify({
        "recommendation": advice
    })

# =========================
# 🔁 FEEDBACK LOOP
# =========================
@app.route("/feedback-loop")
def feedback_loop():

    sessions = list(sessions_collection.find({}, {"_id": 0}))

    total = sum(s["duration"] for s in sessions)

    prompt = f"""
Analyze student behavior deeply.

Stats:
- Total Study Time: {total}
- Total Sessions: {len(sessions)}

Return:
1. Biggest Weakness
2. Improvement Area
3. Recovery Suggestion
4. Burnout Analysis
5. Next Step
"""

    feedback = ask_ai(prompt, mode="chat")

    return jsonify({
        "feedback": feedback
    })

# =========================
# 📈 INSIGHT ENGINE
# =========================
@app.route("/insight")
def insight():

    sessions = list(sessions_collection.find({}, {"_id": 0}))
    total = sum(s["duration"] for s in sessions)

    if total < 50:
        msg = "You need more consistency 📉"

    elif total < 150:
        msg = "Good momentum 🚀"

    elif total < 300:
        msg = "Excellent discipline 🔥"

    else:
        msg = "Be careful of burnout ⚠"

    return jsonify({
        "insight": msg
    })

# =========================
# 📊 ADD SESSION
# =========================
@app.route("/add_session", methods=["POST"])
def add_session():

    duration = request.json.get("duration", 0)

    sessions_collection.insert_one({
        "date": str(datetime.date.today()),
        "duration": duration
    })

    return jsonify({
        "status": "ok"
    })

# =========================
# 📊 GET SESSIONS
# =========================
@app.route("/api/sessions")
def api_sessions():

    sessions = list(sessions_collection.find({}, {"_id": 0}))
    return jsonify(sessions)

# =========================
# ✅ ADD TASK
# =========================
@app.route("/add_task", methods=["POST"])
def add_task():

    task = request.json.get("task")

    tasks_collection.insert_one({
        "task": task,
        "done": False,
        "date": str(datetime.date.today())
    })

    return jsonify({
        "status": "ok"
    })

# =========================
# 📋 GET TASKS
# =========================
@app.route("/get_tasks")
def get_tasks():

    tasks = list(tasks_collection.find({}, {"_id": 0}))
    return jsonify(tasks)

# =========================
# 🔁 TOGGLE TASK
# =========================
@app.route("/toggle_task", methods=["POST"])
def toggle_task():

    task_name = request.json.get("task")

    task = tasks_collection.find_one({
        "task": task_name
    })

    if task:
        tasks_collection.update_one(
            {"task": task_name},
            {"$set": {"done": not task["done"]}}
        )

    return jsonify({
        "status": "updated"
    })

# =========================
# ❌ DELETE TASK
# =========================
@app.route("/delete_task", methods=["POST"])
def delete_task():

    task_name = request.json.get("task")

    tasks_collection.delete_one({
        "task": task_name
    })

    return jsonify({
        "status": "deleted"
    })

# =========================
# 📊 ANALYTICS
# =========================
@app.route("/analytics")
def analytics():

    sessions = list(sessions_collection.find({}, {"_id": 0}))
    tasks = list(tasks_collection.find({}, {"_id": 0}))

    total_time = sum(s["duration"] for s in sessions) if sessions else 0

    score = min(
        100,
        int((total_time * 1.5) + (len(sessions) * 3))
    )

    xp = total_time * 5
    level = (xp // 100) + 1

    completed = len([t for t in tasks if t["done"]])

    return jsonify({
        "sessions": len(sessions),
        "total_time": total_time,
        "score": score,
        "xp": xp,
        "level": level,
        "completed_tasks": completed
    })

# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)