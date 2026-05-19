from flask import Flask, render_template, request, jsonify
import datetime

from services.ai_agent import ask_ai
from database.mongodb import sessions_collection, tasks_collection, plans_collection

app = Flask(__name__)

# =========================
# 🏠 DASHBOARD
# =========================
@app.route("/")
def dashboard():

    sessions = list(sessions_collection.find({}, {"_id": 0}))
    total_time = sum(s["duration"] for s in sessions) if sessions else 0

    return render_template(
        "dashboard.html",
        total_sessions=len(sessions),
        total_time=total_time,
        avg_time=(total_time / len(sessions)) if sessions else 0,
        score=min(100, total_time * 2),
        xp=total_time * 5,
        level=(total_time * 5) // 100 + 1
    )

# =========================
# 💬 AI CHAT (AGENT CORE)
# =========================
@app.route("/chat", methods=["POST"])
def chat():

    msg = request.json.get("message", "")

    prompt = f"""
You are a personal AI tutor.

Reply clearly and helpfully:

{msg}
"""

    reply = ask_ai(prompt, mode="chat")

    return jsonify({
        "response": reply
    })

# =========================
# 🧠 AI PLANNER
# =========================
@app.route("/generate-plan", methods=["POST"])
def generate_plan():

    data = request.get_json()
    user_input = data.get("input", "")

    if not user_input:
        return jsonify({
            "status": "error",
            "plan": "No input provided"
        })

    plan = ask_ai(user_input, mode="plan")

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
# ⚡ AUTO DAILY PLAN (AGENT FEATURE)
# =========================
@app.route("/auto-plan")
def auto_plan():

    sessions = list(sessions_collection.find({}, {"_id": 0}))
    plans = list(plans_collection.find({}, {"_id": 0}))

    context = f"""
You are an autonomous learning AI.

Past sessions:
{sessions}

Past plans:
{plans}

Generate today's optimized study plan:
- focus weak areas
- realistic workload
- include revision + breaks
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

    if avg < 20:
        risk = "high"
    elif avg < 50:
        risk = "medium"
    else:
        risk = "low"

    return jsonify({
        "total_time": total,
        "avg_session": avg,
        "risk_level": risk
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
You are an AI study advisor.

Student stats:
- total study time: {total}
- pending tasks: {pending}

Give:
1. next action
2. focus advice
3. motivation
"""

    advice = ask_ai(prompt, mode="chat")

    return jsonify({
        "recommendation": advice
    })

# =========================
# 🔁 FEEDBACK LOOP (LEARNING ENGINE)
# =========================
@app.route("/feedback-loop")
def feedback_loop():

    sessions = list(sessions_collection.find({}, {"_id": 0}))

    total = sum(s["duration"] for s in sessions)

    prompt = f"""
Analyze student behavior:

Total study time: {total}
Sessions: {len(sessions)}

Return:
- weakness
- improvement
- next step
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
        msg = "You need consistency 📉"
    elif total < 150:
        msg = "Good progress 🚀"
    else:
        msg = "Excellent discipline 🔥"

    return jsonify({
        "insight": msg
    })

# =========================
# 📊 SESSIONS
# =========================
@app.route("/add_session", methods=["POST"])
def add_session():

    duration = request.json.get("duration", 0)

    sessions_collection.insert_one({
        "date": str(datetime.date.today()),
        "duration": duration
    })

    return jsonify({"status": "ok"})

@app.route("/api/sessions")
def api_sessions():

    sessions = list(sessions_collection.find({}, {"_id": 0}))
    return jsonify(sessions)

# =========================
# ✅ TASK SYSTEM
# =========================
@app.route("/add_task", methods=["POST"])
def add_task():

    task = request.json.get("task")

    tasks_collection.insert_one({
        "task": task,
        "done": False,
        "date": str(datetime.date.today())
    })

    return jsonify({"status": "ok"})

@app.route("/get_tasks")
def get_tasks():

    tasks = list(tasks_collection.find({}, {"_id": 0}))
    return jsonify(tasks)

@app.route("/toggle_task", methods=["POST"])
def toggle_task():

    task_name = request.json.get("task")

    task = tasks_collection.find_one({"task": task_name})

    if task:
        tasks_collection.update_one(
            {"task": task_name},
            {"$set": {"done": not task["done"]}}
        )

    return jsonify({"status": "updated"})

@app.route("/delete_task", methods=["POST"])
def delete_task():

    task_name = request.json.get("task")

    tasks_collection.delete_one({"task": task_name})

    return jsonify({"status": "deleted"})

# =========================
# 📊 ANALYTICS
# =========================
@app.route("/analytics")
def analytics():

    sessions = list(sessions_collection.find({}, {"_id": 0}))
    total_time = sum(s["duration"] for s in sessions) if sessions else 0

    return jsonify({
        "sessions": len(sessions),
        "total_time": total_time,
        "score": min(100, total_time * 2),
        "xp": total_time * 5,
        "level": (total_time * 5) // 100 + 1
    })

# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)