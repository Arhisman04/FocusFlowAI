from services.coach_engine import generate_coach_message
from services.intelligence_layer import build_ai_brain
from services.persona_engine import detect_persona
from services.insight_engine import generate_insight
from services.evolution_engine import evolve_plan
from services.memory_engine import summarize_memory
from services.recovery_engine import calculate_recovery_metrics
from flask import Flask, render_template, request, jsonify, session, redirect

import datetime
import bcrypt

from flask_jwt_extended import JWTManager

from services.ai_agent import ask_ai

from database.mongodb import (
    sessions_collection,
    tasks_collection,
    plans_collection,
    memory_collection,
    users_collection
)
# ---------------- APP INIT ----------------
app = Flask(__name__)

# secret key for sessions (Flask login/session)
app.secret_key = "focusflow_super_secret"

# JWT config
app.config["JWT_SECRET_KEY"] = "your_secret_key_change_this"

jwt = JWTManager(app)
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]

    users_collection.insert_one({
        "name": name,
        "email": email,
        "password_hash": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
        "created_at": str(datetime.date.today())
    })

    return jsonify({"status": "success"})
@app.route("/login", methods=["POST"])
def login():

    data = request.json
    email = data["email"]
    password = data["password"]

    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
        return jsonify({"error": "Wrong password"}), 401
    session["user"] = email

    return jsonify({
        "status": "success",
    })
# =========================
# 🏠 LANDING PAGE
# =========================
@app.route("/")
def landing():
    return render_template("landing.html")
@app.route("/login-page")
def login_page():
    return render_template("login.html")


@app.route("/signup")
def signup_page():
    return render_template("signup.html")
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login-page")
# =========================
# 📊 DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login-page")

    sessions = list(
        sessions_collection.find(
            {"user": session["user"]}
        )
    )

    tasks = list(
        tasks_collection.find(
            {"user": session["user"]},
            {"_id": 0}
        )
    )

    total_time = sum(
        s["duration"] for s in sessions
    ) if sessions else 0

    score = min(
        100,
        int((total_time * 1.5) + (len(sessions) * 3))
    )

    xp = total_time * 5

    level = (xp // 100) + 1

    pending_tasks = len([
        t for t in tasks if not t["done"]
    ])

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

    # =========================
    # 🧠 AI BRAIN
    # =========================
    ai_brain = build_ai_brain(

        study_hours=3,

        stress=8,

        confidence=3,

        consistency=4,

        backlog="High",

        score_history=[45, 52, 61]

    )

    # =========================
    # 🤖 AUTONOMOUS AI COACH
    # =========================
    coach_message = generate_coach_message(
        ai_brain
    )

    return render_template(

        "dashboard.html",

        total_sessions=len(sessions),

        total_time=total_time,

        avg_time=(
            total_time / len(sessions)
        ) if sessions else 0,

        score=score,

        xp=xp,

        level=level,

        burnout=burnout,

        pending_tasks=pending_tasks,

        momentum=momentum,

        ai_insight=ai_insight,

        ai_brain=ai_brain,

        coach_message=coach_message

    )
# =========================
# 💬 AI CHAT (AGENT CORE)
# =========================
@app.route("/chat", methods=["POST"])
def chat():

    if "user" not in session:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    msg = request.json.get("message", "")

    memories = list(
        memory_collection.find(
            {"user": session["user"]},
            {"_id": 0}
        )
    )

    prompt = f"""
You are FocusFlowAI.

You are an elite AI tutor and academic mentor.

Student Memory:
{memories}

Student Message:
{msg}

Reply intelligently using memory context.
"""

    reply = ask_ai(prompt, mode="chat")

    compressed_memory = {
        "message": msg,
        "reply": reply[:300]
    }

    memory_collection.insert_one({
        "user": session["user"],
        "memory": compressed_memory,
        "date": str(datetime.date.today())
    })

    return jsonify({
        "response": reply
    })
@app.route("/save-memory", methods=["POST"])
def save_memory():

    data = request.json

    memory_collection.insert_one({

        "user": session["user"],

        "memory": data["memory"],

        "date": str(datetime.date.today())

    })

    return jsonify({
        "status":"saved"
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

    metrics = calculate_recovery_metrics(

        study_hours=3,
        stress=8,
        confidence=3,
        consistency=4,
        backlog="High"

    )

    brain = build_ai_brain(

        study_hours=3,
        stress=8,
        confidence=3,
        consistency=4,
        backlog="High",
        score_history=[45, 52, 61]

    )

    enhanced_prompt = f"""

You are FocusFlowAI,
an elite AI Academic Recovery Coach.

Analyze the student's academic situation deeply.

Student Input:
{user_input}

Recovery Metrics:
- Recovery Score: {metrics['recovery_score']}
- Burnout: {metrics['burnout']}
- Momentum: {metrics['momentum']}
- Confidence Trend: {metrics['confidence_trend']}

AI Brain State:
{brain}

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

    plan = ask_ai(
        enhanced_prompt,
        mode="plan"
    )

    plans_collection.insert_one({

        "user": session["user"],

        "type": "auto",

        "plan": plan,

        "date": str(datetime.date.today())

    })

    return jsonify({

        "status": "success",

        "plan": plan,

        "metrics": metrics

    })

# =========================
# ⚡ AUTO DAILY PLAN
# =========================
@app.route("/auto-plan")
def auto_plan():

    sessions = list(
    sessions_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    )
)
    plans = list(
    plans_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    )
)
    tasks = list(
    tasks_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    )
)

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
    "user": session["user"],
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

    sessions = list(
    sessions_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    )
)

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

    sessions = list(
    sessions_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    )
)
    tasks = list(
    tasks_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    )
)

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

    sessions = list(
    sessions_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    )
)

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

    sessions = list(
    sessions_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    )
)
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
    "user": session["user"],
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

    sessions = list(sessions_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    ))
    return jsonify(sessions) 

# =========================
# ✅ ADD TASK
# =========================
@app.route("/add_task", methods=["POST"])
def add_task():

    task = request.json.get("task")

    tasks_collection.insert_one({
    "user": session["user"],
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

    tasks = list(
    tasks_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    )
)
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

    sessions = list(
    sessions_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    )
)
    tasks = list(
    tasks_collection.find(
        {"user": session["user"]},
        {"_id": 0}
    )
)

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