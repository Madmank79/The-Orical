import os
requests_installed = True
try:
    import requests
    from io import BytesIO
    from google import genai
    from google.genai import types
except ImportError:
    requests_installed = False

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

def send_update():
    if not TOKEN or not CHAT_ID or not GEMINI_KEY:
        print("Error: Missing required environment variables.")
        return

    client = genai.Client(api_key=GEMINI_KEY)
    
    # 1. Generate the text portent via Gemini 3.6 Flash
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

    # 2. Derive a clean visual prompt and generate image via Imagen 3
    image_bytes = None
    try:
        image_prompt_request = (
            "Write a short, highly visual prompt for an image generator to create a dark, "
            "moody, cinematic graphic representation of this mood: " + mood_message
        )
        prompt_response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=image_prompt_request,
        )
        visual_prompt = prompt_response.text
        print(f"Visual prompt generated: {visual_prompt}")

        # Correct method for Google GenAI SDK image generation
        image_result = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=visual_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/jpeg",
            )
        )
        
        if image_result and image_result.generated_images:
            image_bytes = image_result.generated_images[0].image.image_bytes
            print("Successfully generated AI image via Imagen 3!")
            
    except Exception as e:
        print(f"WARNING: Image generation encountered an issue, posting text-only: {e}")

    # 3. Broadcast to Telegram (Photo with caption if available, fallback to text)
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
