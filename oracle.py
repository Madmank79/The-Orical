import os
import requests
from io import BytesIO
from google import genai
from google.genai import types

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

def send_update():
    if not TOKEN or not CHAT_ID or not GEMINI_KEY:
        print("Error: Missing required environment variables.")
        return

    client = genai.Client(api_key=GEMINI_KEY)
    
    # Prompt requesting both the text portent and the actual generated image
    prompt = (
        "Write a short, punchy hourly portent for an Oracle bot blending global markets, "
        "government shifts, and a sharp global mood, formatted with Markdown and emojis. "
        "Also generate a dark, moody, cinematic cyberpunk visual graphic representing this exact mood."
    )
    
    mood_message = ""
    image_bytes = None

    try:
        # Use gemini-3.1-flash-image to natively generate text and image contents
        response = client.models.generate_content(
            model="gemini-3.1-flash-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            )
        )
        
        # Parse through the response parts
        for part in response.candidates[0].content.parts:
            if part.text:
                mood_message += part.text
            elif part.inline_data:
                image_bytes = part.inline_data.data
                
        print("Successfully generated AI content and image!")
    except Exception as e:
        print(f"ERROR generating content from Gemini: {e}")
        return

    # Broadcast to Telegram: sendPhoto with the graphic, or fallback to text if missing
    if image_bytes:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        files = {'photo': ('oracle_mood.jpg', BytesIO(image_bytes), 'image/jpeg')}
        data = {"chat_id": CHAT_ID, "caption": mood_message, "parse_mode": "Markdown"}
        tg_response = requests.post(url, data=data, files=files)
    else:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": mood_message, "parse_mode": "Markdown"}
        tg_response = requests.post(url, json=payload)
        
    print("Telegram Broadcast status:", tg_response.json())

if __name__ == "__main__":
    send_update()
