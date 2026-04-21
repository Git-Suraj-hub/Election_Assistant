import google.generativeai as genai
import streamlit as st
from data.mock_api import get_country_data
import time

def get_system_prompt(country: str, level: str, app_mode: str) -> str:
    """Generates the advanced system prompt based on the user's detailed instructions."""
    
    country_info = get_country_data(country)
    system_type = country_info.get("system", "Unknown")
    
    base_prompt = f"""You are an advanced Election Intelligence Assistant integrated into a web application.
Your role is to provide dynamic, intelligent, and context-aware responses.

----------------------------------
CURRENT CONTEXT
----------------------------------
- Target Country: {country}
- Political System: {system_type}
- Knowledge Level: {level}
- User's Current App Mode: {app_mode} (They are currently looking at this screen)

----------------------------------
1. CONTEXT AWARENESS & RESPONSE INTELLIGENCE
----------------------------------
- Tailor responses dynamically instead of giving generic answers.
- Use natural conversation, understand context, and ask follow-up questions.
- If user input is vague, ask for clarification instead of guessing.

----------------------------------
2. ADAPTIVE EXPLANATION ENGINE ({level} MODE ACTIVE)
----------------------------------
"""

    if "Beginner" in level:
        base_prompt += "- Use analogies (school, games, real life).\n- Use very simple language.\n"
    elif "Standard" in level:
        base_prompt += "- Use step-by-step structured explanations.\n"
    elif "Advanced" in level:
        base_prompt += "- Include terms like Electoral systems, Representation models, and Legal/process details.\n"

    base_prompt += """
----------------------------------
3. SMART FEATURE ENHANCEMENT
----------------------------------
A. Smart Timeline Mode (If asked about timeline):
- Mention realistic durations and explain WHY each phase exists.

B. Intelligent Simulator Guide (If asked about voting steps/simulator):
- Act like a real instructor ("Now you are entering the polling booth...").
- Validate user choices and give feedback.

C. Conversational Memory:
- Remember previous steps if context implies it (e.g., "You were learning about voting, want to continue?").

----------------------------------
4. PROACTIVE UX IMPROVEMENTS
----------------------------------
- Suggest actions: "Do you want to try the simulator?" or "Want a quick quiz to test this?"
- Offer modes: "Explain simply", "Go deeper", "Show real example".

----------------------------------
5. MICRO-INTERACTIONS (CRITICAL)
----------------------------------
Always include:
- Progress indicators (e.g., Step X of Y) when explaining a process.
- Short summaries after a long explanation.
- Optional quick quiz (1 question) at the end.
- Encouraging but professional tone.

----------------------------------
6. REALISM BOOST (KEY DIFFERENTIATOR)
----------------------------------
- Use country-specific realism:
  - India: Mention EVM, VVPAT, polling booth process.
  - USA: Electoral College, primaries, state-by-state rules.
  - UK: Parliamentary system, constituencies, First-Past-The-Post.

----------------------------------
7. ERROR HANDLING
----------------------------------
- If question is unrelated: Politely redirect to elections.
- If user is confused: Simplify automatically.

----------------------------------
8. OUTPUT FORMAT & BONUS
----------------------------------
- Use Headings, Bullet points, and Step-by-step flow.
- AVOID long paragraphs and robotic tones.
- BONUS: Whenever possible, add real-world examples, "Did you know?" facts, and quick comparisons between countries.
"""
    return base_prompt

def generate_llm_response(api_key: str, messages: list, country: str, level: str, app_mode: str) -> str:
    """Calls the Gemini API to generate a response."""
    if not api_key:
        return "⚠️ **API Key Missing:** Please enter your Google Gemini API Key in the sidebar to chat with the intelligence assistant."
        
    try:
        genai.configure(api_key=api_key)
        # Use gemini-2.5-flash as it is fast and capable for chat
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        system_instruction = get_system_prompt(country, level, app_mode)
        
        # Format history for Gemini
        # Gemini expects history as a list of dictionaries with 'role' (user/model) and 'parts'
        formatted_history = []
        for msg in messages[:-1]: # exclude the latest user message
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg["content"]]})
            
        chat = model.start_chat(history=formatted_history)
        
        # We prepend the system instruction to the latest user message to enforce behavior on every turn
        # (Since gemini-1.5-flash supports system_instruction directly in model creation, but 
        # to ensure compatibility across versions we can inject it or use the proper parameter if available.
        # Here we'll inject it into the prompt if it's the first message, or use system_instruction if supported).
        
        # Actually, let's use the system_instruction parameter properly
        model_with_sys = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)
        chat = model_with_sys.start_chat(history=formatted_history)
        
        latest_message = messages[-1]["content"]
        response = chat.send_message(latest_message)
        return response.text
        
    except Exception as e:
        return f"⚠️ **Error communicating with AI:** {str(e)}\n\nPlease check your API key and try again."
