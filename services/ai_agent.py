from services.gemini_service import generate_plan
from agents.memory import get_context, save_event

def ask_ai(user_input, mode="chat"):

    memory = get_context()

    base_context = f"""
You are FocusFlow AI, a smart student learning agent.

User Memory:
{memory}

User Input:
{user_input}
"""

    if mode == "plan":
        prompt = base_context + """

TASK: Create a structured study plan.
- day-wise breakdown
- realistic workload
- based on user memory if available
"""
        result = generate_plan(prompt)

        save_event("plan_generated", {
            "input": user_input,
            "plan": result
        })

        return result

    else:
        prompt = base_context + """

TASK: Act as a personal AI tutor.
- give short helpful answer
- adapt based on past memory
"""

        result = generate_plan(prompt)

        save_event("chat", {
            "input": user_input,
            "response": result
        })

        return result