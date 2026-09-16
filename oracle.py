import os
import random
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

world_moods = [
    "🔮 **The Oracle's Hourly Portent**\n\n*Markets:* Global financial currents are shifting erratically.\n*Governments:* New decrees ripple through international borders.\n*World Mood:* Highly volatile and electric. Proceed with caution across all sectors.",
    
    "🔮 **The Oracle's Hourly Portent**\n\n*Markets:* Capital flows steady into safe havens today.\n*Governments:* Diplomatic talks show faint signs of alignment.\n*World Mood:* Quietly observant. A period of heavy preparation.",
    
    "🔮 **The Oracle's Hourly Portent**\n\n*Markets:* Aggressive spikes detected in regional trade metrics.\n*Governments:* Policy shifts spark intense debate among state powers.\n*World Mood:* Driven, restless, and hungry for disruption.",
    
    "🔮 **The Oracle speaks**\n\nThe next hour favours those who stay calm under pressure.\nSomething small is about to matter more than it should.",
    
    "🔮 **Hourly Vision**\n\nOld patterns are breaking. Watch the quiet movements — they carry the real signal."
]

def send_update():
    if not TOKEN or not CHAT_ID:
        print("Error: Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID")
        return

    # Random picture
    seed = random.randint(1, 999999)
    image_url = f"https://picsum.photos/seed/{seed}/800/600"

    caption = random.choice(world_moods)

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=20)
        print("Broadcast status:", response.json())
    except Exception as e:
        print("Error sending:", e)

if __name__ == "__main__":
    send_update()
