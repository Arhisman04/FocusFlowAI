def detect_persona(stress, consistency, study_hours, confidence):

    if stress >= 8 and confidence <= 4:
        return "Burnout Student 🔥"

    elif consistency <= 4:
        return "Inconsistent Learner ⚠"

    elif study_hours >= 6 and stress >= 7:
        return "Overworked Achiever 🚀"

    elif confidence <= 3:
        return "Low Confidence Student 📉"

    else:
        return "Balanced Learner ✅"