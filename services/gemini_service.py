import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# ✅ correct client init
client = genai.Client(api_key=os.getenv("AIzaSyBPRdyX_GMz495c5zWbElj3Y2Vpdbdof18"))


def generate_plan(prompt):
    """
    Generates AI response using Gemini
    """

    try:
        if not prompt or prompt.strip() == "":
            return "Please enter a valid prompt."

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            return "No response from AI."

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return f"AI service error: {str(e)}"