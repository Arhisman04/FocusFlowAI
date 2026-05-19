import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")


def generate_plan(prompt):
    """
    Generates AI response using Gemini
    """

    try:
        if not prompt or prompt.strip() == "":
            return "Please enter a valid prompt."

        response = model.generate_content(prompt)

        if not response or not response.text:
            return "No response from AI."

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return f"AI service error: {str(e)}"