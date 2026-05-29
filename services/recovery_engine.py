def calculate_recovery_metrics(

    study_hours,
    stress,
    confidence,
    consistency,
    backlog,
    sleep_hours=7,
    focus_level=5

):

    # =========================
    # BASE RECOVERY SCORE
    # =========================

    score = 50

    # Study Hours
    score += study_hours * 4

    # Confidence
    score += confidence * 3

    # Consistency
    score += consistency * 5

    # Focus Quality
    score += focus_level * 4

    # Sleep Quality
    if sleep_hours >= 7:
        score += 10

    elif sleep_hours <= 4:
        score -= 15

    # Stress Penalty
    score -= stress * 4

    # Backlog Penalty
    if backlog == "High":
        score -= 25

    elif backlog == "Medium":
        score -= 12

    # Clamp Score
    score = max(0, min(score, 100))

    # =========================
    # BURNOUT DETECTION
    # =========================

    if stress >= 8 and sleep_hours <= 5:
        burnout = "Critical 🔴"

    elif stress >= 7:
        burnout = "High 🟠"

    elif stress >= 5:
        burnout = "Moderate 🟡"

    else:
        burnout = "Low 🟢"

    # =========================
    # MOMENTUM DETECTION
    # =========================

    if consistency >= 8 and confidence >= 7:
        momentum = "Peak Momentum 🔥"

    elif consistency >= 5:
        momentum = "Recovery Building 📈"

    else:
        momentum = "Unstable ⚠"

    # =========================
    # WORKLOAD STATUS
    # =========================

    if study_hours >= 8 and stress >= 7:
        workload = "Overloaded"

    elif study_hours <= 2:
        workload = "Underperforming"

    else:
        workload = "Balanced"

    # =========================
    # ACADEMIC STABILITY
    # =========================

    if score >= 80:
        stability = "Stable & Improving ✅"

    elif score >= 60:
        stability = "Recovering 📈"

    elif score >= 40:
        stability = "Fragile ⚠"

    else:
        stability = "Critical Recovery Needed 🔴"

    # =========================
    # AI RECOMMENDATIONS
    # =========================

    recommendations = []

    if burnout == "Critical 🔴":
        recommendations.append(
            "Reduce workload immediately and prioritize recovery."
        )

    if consistency <= 4:
        recommendations.append(
            "Focus on rebuilding consistency before increasing intensity."
        )

    if confidence <= 4:
        recommendations.append(
            "Prioritize small achievable wins to rebuild confidence."
        )

    if backlog == "High":
        recommendations.append(
            "Focus only on high ROI chapters first."
        )

    if sleep_hours <= 5:
        recommendations.append(
            "Improve sleep stability to restore cognitive performance."
        )

    # =========================
    # FINAL OUTPUT
    # =========================

    return {

        "recovery_score": score,

        "burnout_risk": burnout,

        "momentum_status": momentum,

        "workload_status": workload,

        "academic_stability": stability,

        "recommendations": recommendations
    }