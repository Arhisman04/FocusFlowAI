def calculate_recovery_metrics(
    study_hours,
    stress,
    confidence,
    consistency,
    backlog
):

    # ---------------- BASE SCORE ----------------
    score = 50

    # Study hours impact
    score += study_hours * 4

    # Confidence impact
    score += confidence * 3

    # Consistency impact
    score += consistency * 2

    # Stress penalty
    score -= stress * 4

    # Backlog penalty
    if backlog == "High":
        score -= 20
    elif backlog == "Medium":
        score -= 10

    score = max(0, min(score, 100))

    # ---------------- BURNOUT ----------------
    if stress >= 8:
        burnout = "High 🔴"
    elif stress >= 5:
        burnout = "Medium 🟠"
    else:
        burnout = "Low 🟢"

    # ---------------- MOMENTUM ----------------
    if consistency >= 8:
        momentum = "Excellent 🔥"
    elif consistency >= 5:
        momentum = "Improving 🚀"
    else:
        momentum = "Weak 📉"

    # ---------------- CONFIDENCE ----------------
    if confidence >= 8:
        confidence_trend = "Strong 💪"
    elif confidence >= 5:
        confidence_trend = "Recovering 📈"
    else:
        confidence_trend = "Low ⚠"

    return {
        "recovery_score": score,
        "burnout": burnout,
        "momentum": momentum,
        "confidence_trend": confidence_trend
    }