import os
import requests
from google import genai

# Pull credentials from environment variables
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

def send_update():
    if not TOKEN or not CHAT_ID or not GEMINI_KEY:
        print("Error: Missing required environment variables.")
        return

    # Initialize the Google GenAI client
    client = genai.Client(api_key=GEMINI_KEY)
    
    # Prompt the AI to generate a unique hourly briefing
    prompt = (
        "Write a short, punchy hourly portent for an Oracle bot. "
        "Blend global markets, government/political shifts, and a sharp global mood. "
        "Format it nicely with Markdown bolding and emoji icons."
    )
    
    try:
        # Generate the content using Gemini 3.6 Flash
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        mood_message = response.text
        print("Successfully generated AI message!")
    except Exception as e:
        print(f"ERROR generating content from Gemini: {e}")
        return
    
    # Send the generated message to Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mood_message,
        "parse_mode": "Markdown"
    }
    
    tg_response = requests.post(url, json=payload)
    print("Telegram Broadcast status:", tg_response.json())

if __name__ == "__main__":
    send_update()
