from services.persona_engine import detect_persona
from services.recovery_engine import calculate_recovery_metrics
from services.insight_engine import generate_insight
from services.evolution_engine import evolve_plan


def build_ai_brain(
    study_hours,
    stress,
    confidence,
    consistency,
    backlog,
    score_history
):

    # ---------------- PERSONA ----------------

    persona = detect_persona(
        stress=stress,
        consistency=consistency,
        study_hours=study_hours,
        confidence=confidence
    )

    # ---------------- RECOVERY ----------------

    recovery = calculate_recovery_metrics(
        study_hours=study_hours,
        stress=stress,
        confidence=confidence,
        consistency=consistency,
        backlog=backlog   
    )

    recovery_score = recovery["recovery_score"]
    burnout_risk = recovery["burnout_risk"]

    # ---------------- EVOLUTION ----------------

    evolution = evolve_plan(score_history)

    # ---------------- INSIGHT ----------------

    insight = generate_insight(
        recovery_score,
        burnout_risk
    )

    # ---------------- AI STATE ----------------

    ai_state = {

        "persona": persona,

        "recovery_score": recovery_score,

        "burnout_risk": burnout_risk,

        "evolution_state": evolution,

        "insight": insight
    }

    return ai_state