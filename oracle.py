import os
import requests
from google import genai
from google.genai import types

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
    
    # 1. Generate the text portent
    text_prompt = (
        "Write a short, punchy hourly portent for an Oracle bot. "
        "Blend global markets, government/political shifts, and a sharp global mood. "
        "Format it nicely with Markdown bolding and emoji icons."
    )
    
    try:
        text_response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=text_prompt,
        )
        mood_message = text_response.text
        print("Successfully generated AI message text!")
    except Exception as e:
        print(f"ERROR generating text from Gemini: {e}")
        return

    # 2. Generate a matching image based on the world mood using Imagen
    image_prompt_request = (
        "Based on this Oracle mood, write a short, highly visual prompt for an AI image generator "
        "to create a dark, moody, cinematic graphic representation of it. Style: Cyberpunk, arcane, atmospheric, high contrast. "
        f"Mood text: {mood_message}"
    )
    
    try:
        prompt_response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=image_prompt_request,
        )
        visual_prompt = prompt_response.text
        print(f"Visual prompt generated: {visual_prompt}")

        # Generate the actual image using Imagen 3
        image_result = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=visual_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/jpeg",
            )
        )
        
        # Extract the image bytes
        generated_image = image_result.generated_images[0]
        image_bytes = generated_image.image.image_bytes
        print("Successfully generated AI image!")
        
    except Exception as e:
        print(f"ERROR generating image (falling back to text-only): {e}")
        # Fallback if image generation fails: send text only
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": mood_message, "parse_mode": "Markdown"}
        requests.post(url, json=payload)
        return

    # 3. Send the image and caption to Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    files = {
        'photo': ('oracle_mood.jpg', image_bytes, 'image/jpeg')
    }
    data = {
        "chat_id": CHAT_ID,
        "caption": mood_message,
        "parse_mode": "Markdown"
    }
    
    tg_response = requests.post(url, data=data, files=files)
    print("Telegram Broadcast status:", tg_response.json())

if __name__ == "__main__":
    send_update()
