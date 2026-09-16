import os
import random
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

    prompt = (
        "Write a short, punchy hourly portent for an Oracle bot. "
        "Blend global markets, government shifts, and a sharp global mood. "
        "Format with Markdown and emojis. Keep it under 300 characters. "
        "Make it dark, cinematic and mysterious."
    )

    mood_message = ""

    try:
        # Free text model
        response = client.models.generate_content(
            model="gemini-2.0-flash",          # Free model
            contents=prompt
        )
        
        mood_message = response.text.strip()
        print("Successfully generated AI text!")
    except Exception as e:
        print(f"ERROR generating content from Gemini: {e}")
        # Fallback text if Gemini fails
        mood_message = "🔮 **The Oracle speaks**\n\nThe currents are shifting. Stay alert."

    # Free random high-quality image from Picsum
    seed = random.randint(1, 999999)
    image_url = f"https://picsum.photos/seed/{seed}/800/800"

    # Send photo with caption to Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": mood_message,
        "parse_mode": "Markdown"
    }

    try:
        tg_response = requests.post(url, json=payload, timeout=20)
        print("Telegram Broadcast status:", tg_response.json())
    except Exception as e:
        print("Error sending to Telegram:", e)

if __name__ == "__main__":
    send_update()
