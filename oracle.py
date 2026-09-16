import os
import random
import requests
from google import genai

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

# Strong fallback messages (used when Gemini fails)
FALLBACKS = [
    "🔮 **The Oracle speaks**\n\nThe currents are shifting. Stay alert.",
    "🔮 **Hourly Vision**\n\nOld patterns are breaking. Watch the quiet movements — they carry the real signal.",
    "🔮 **The Oracle's Portent**\n\nSomething small is about to matter more than it should. Proceed with calm awareness.",
    "🔮 **Whisper from the Void**\n\nThe markets hold their breath. Governments move in shadows. The mood is electric.",
    "🔮 **Oracle Transmission**\n\nA subtle realignment is underway. Those who notice early will gain advantage.",
    "🔮 **The Oracle observes**\n\nVolatility gathers like storm clouds. Remain steady. The next hour favours the prepared.",
    "🔮 **Portent**\n\nInvisible forces are rearranging the board. Watch carefully. Act only when the signal is clear.",
    "🔮 **The Oracle's Hour**\n\nSilence before the shift. The world is listening. So should you."
]

def get_ai_message(client):
    """Try free Gemini models. Return text or None if both fail."""
    models = ["gemini-2.0-flash", "gemini-2.5-flash"]
    
    prompt = (
        "Write a short, punchy hourly portent for an Oracle bot. "
        "Blend global markets, government shifts, and a sharp global mood. "
        "Use Markdown and one or two emojis. "
        "Keep it under 280 characters. "
        "Make it dark, cinematic, mysterious and slightly prophetic."
    )

    for model in models:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            text = response.text.strip()
            if text:
                print(f"Successfully generated with {model}")
                return text
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue
    return None

def send_update():
    if not TOKEN or not CHAT_ID or not GEMINI_KEY:
        print("Error: Missing required environment variables.")
        return

    client = genai.Client(api_key=GEMINI_KEY)

    # Try AI first, then fall back
    mood_message = get_ai_message(client)
    if not mood_message:
        mood_message = random.choice(FALLBACKS)
        print("Using fallback message")

    # Free random image
    seed = random.randint(1, 999999)
    image_url = f"https://picsum.photos/seed/{seed}/800/800"

    # Send to Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": mood_message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=20)
        print("Telegram status:", response.json())
    except Exception as e:
        print("Telegram error:", e)

if __name__ == "__main__":
    send_update()
