def calculate_recovery_metrics(
    study_hours,
    stress,
    confidence,
    consistency,
    backlog
):

    score = 50

    # Study Hours
    score += study_hours * 4

    # Confidence
    score += confidence * 3

    # Consistency
    score += consistency * 4

    # Stress Penalty
    score -= stress * 3

    # Backlog Penalty
    if backlog == "High":
        score -= 20

    elif backlog == "Medium":
        score -= 10

    score = max(0, min(score, 100))

    # Burnout Risk
    if stress >= 8:
        burnout = "High 🔴"

    elif stress >= 5:
        burnout = "Medium 🟠"

    else:
        burnout = "Low 🟢"

    return {
        "recovery_score": score,
        "burnout_risk": burnout
    }
def generate_insight(score, burnout):

    if score >= 80:
        return "Excellent momentum detected 🔥"

    elif burnout == "High 🔴":
        return "Burnout indicators rising rapidly ⚠"

    elif score >= 50:
        return "Recovery progressing steadily 📈"

    else:
        return "Consistency needs improvement 📉"