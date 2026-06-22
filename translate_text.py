import requests
import json
import httpx
import asyncio

def translate_text_with_deepl(text, target_lang):
    api_key = "728e3f58-bb3e-ec7a-f558-04b3c9160daf:fx"
    # Define the API endpoint
    api_url = "https://api-free.deepl.com/v2/translate"

    # Create the request payload
    payload = {
        "text": [text],
        "target_lang": target_lang,
    }

    # Create the headers with your API key
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "User-Agent": "YourApp/1.2.3",
        "Content-Type": "application/json",
    }

    # Send the POST request to DeepL API
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code == 200:
        translation_response = json.loads(response.text)
        translations = translation_response.get("translations")
        if translations:
            translation = translations[0]
            translated_text = translation.get("text")
            return translated_text
        else:
            return None
    else:
        return None

async def translate_text_with_deepl_async(text, target_lang, client=None):
    api_key = "728e3f58-bb3e-ec7a-f558-04b3c9160daf:fx"
    api_url = "https://api-free.deepl.com/v2/translate"

    payload = {
        "text": [text],
        "target_lang": target_lang,
    }

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "User-Agent": "YourApp/1.2.3",
        "Content-Type": "application/json",
    }

    if client is None:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, headers=headers, json=payload)
    else:
        response = await client.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        translation_response = response.json()
        translations = translation_response.get("translations")
        if translations:
            return translations[0].get("text")
    return None
