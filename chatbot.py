import google.generativeai as genai
import os
from dotenv import load_dotenv
from .prompts import SYSTEM_PROMPT

load_dotenv()

def load_gemini_model(api_key=None):
    """
    Initializes the Gemini 1.5 Flash model.
    """
    if api_key:
        genai.configure(api_key=api_key)
    else:
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        else:
            return None
            
    return genai.GenerativeModel("gemini-1.5-flash")

def generate_response(model, resume_text, question):
    """
    Generates a response from Gemini based on the resume and question.
    """
    if not model:
        return "Model not initialized. Please check your API key."

    # Creating the user-specific prompt
    full_prompt = f"{SYSTEM_PROMPT}\n\nUSER RESUME DATA:\n{resume_text}\n\nQUESTION: {question}"
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"
