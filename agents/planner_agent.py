from services.ai_service import generate_plan
from database.mongodb import plans_collection
import datetime

def create_plan(user_input):

    prompt = f"""
You are an expert AI study planner.

Create a structured, realistic study plan for:

{user_input}

Rules:
- day-wise breakdown
- simple language
- practical schedule
"""

    ai_plan = generate_plan(prompt)

    if not ai_plan:
        return "Failed to generate plan"

    plans_collection.insert_one({
        "input": user_input,
        "plan": ai_plan,
        "date": str(datetime.date.today())
    })

    return ai_plan