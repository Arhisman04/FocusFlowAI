def evolve_plan(score_history):

    if not score_history:
        return "Starting Recovery Journey 🚀"

    latest = score_history[-1]

    if latest >= 85:
        return "Peak Momentum Mode 🔥"

    elif latest >= 65:
        return "Strong Recovery Progress 📈"

    elif latest >= 40:
        return "Stabilizing Academic Performance ⚖"

    else:
        return "Recovery Needed Immediately ⚠"