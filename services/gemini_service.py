import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_plan(prompt):

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response:
            return "No response from AI"

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return "AI service error"