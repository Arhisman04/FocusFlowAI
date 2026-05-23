def generate_coach_message(brain):

    burnout = brain.get("burnout_risk", "Medium")
    score = brain.get("recovery_score", 50)
    momentum = brain.get("evolution_state", "Stable")

    if burnout == "High":
        return "⚠ Burnout risk detected. Reduce workload immediately."

    if score < 50:
        return "📉 Low recovery score. Focus on consistency over intensity."

    if momentum == "Declining":
        return "🔻 Momentum dropping. Fix routine and sleep cycle."

    return "🧠 You are stable. Maintain current system and improve gradually."