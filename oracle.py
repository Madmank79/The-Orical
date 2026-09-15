import os
import random
import requests

# These pull securely from your GitHub repository settings
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# The Oracle's worldview templates blending money, government, and global mood
world_moods = [
    "🔮 **The Oracle's Hourly Portent**\n\n*Markets:* Global financial currents are shifting erratically.\n*Governments:* New decrees ripple through international borders.\n*World Mood:* Highly volatile and electric. Proceed with caution across all sectors.",
    "🔮 **The Oracle's Hourly Portent**\n\n*Markets:* Capital flows steady into safe havens today.\n*Governments:* Diplomatic talks show faint signs of alignment.\n*World Mood:* Quietly observant. A period of heavy preparation.",
    "🔮 **The Oracle's Hourly Portent**\n\n*Markets:* Aggressive spikes detected in regional trade metrics.\n*Governments:* Policy shifts spark intense debate among state powers.\n*World Mood:* Driven, restless, and hungry for disruption."
]

def send_update():
    if not TOKEN or not CHAT_ID:
        print("Error: Missing Telegram token or chat ID environment variables.")
        return

    mood_message = random.choice(world_moods)
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mood_message,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=payload)
    print("Broadcast status:", response.json())

if __name__ == "__main__":
    send_update()

