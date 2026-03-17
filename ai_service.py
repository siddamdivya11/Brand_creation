import os
import requests
import base64
import time
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Core AI call
def ask_ai(prompt: str):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# ============================
# Project AI Functions
# ============================

def generate_brand_names(data):
    prompt = f"""
    Generate 10 sophisticated, premium, and luxury brand names.
    Industry: {data['industry']}
    Keywords: {data['keywords']} (Focus on elegance, prestige, modern luxury)
    Tone: {data['tone']} (High-end, Exclusive)
    """
    return ask_ai(prompt)


def generate_content(data):
    prompt = f"""
    Write high-quality, professional, and sophisticated marketing content.
    Description: {data['description']}
    Tone: {data['tone']} (Professional, Persuasive, Elegant)
    Content Type: {data['content_type']}
    Ensure vocabulary is refined and impactful.
    """
    return ask_ai(prompt)


def analyze_sentiment(text):
    prompt = f"""
    Analyze the sentiment of this text.
    Respond only with Positive, Negative or Neutral.

    Text: {text}
    """
    return {"sentiment": ask_ai(prompt)}


def chatbot_reply(message):
    prompt = f"You are Creovate, a luxury AI assistant. Respond politely, professionally, and concisely. User: {message}"
    return ask_ai(prompt)


def generate_logo_prompt(data):
    # This now just returns a string prompt for the image generator
    prompt = f"A professional minimalist luxury logo for a brand named '{data['brand_name']}' in the {data['industry']} industry. Style: {data['keywords']}. Primary color: {data.get('color', 'gold')}. Elegant, high-end, vector style, white background, high resolution."
    return prompt

def generate_logo_image(data):
    brand_name = data.get('brand_name', 'Brand')
    industry = data.get('industry', 'Luxury')
    keywords = data.get('keywords', 'Minimalist')
    color = data.get('color', 'gold')
    style_preset = data.get('style', 'Minimalist')
    composition = data.get('composition', 'Icon + Text')

    # Enhanced prompt building
    style_descriptors = {
        "Art Deco Prestige": "Art Deco style, bold geometric shapes, clean lines, golden accents, 1920s luxury aesthetic",
        "Minimalist Modern": "Modern minimalist style, ultra-clean, simple shapes, ample whitespace, Swiss design influence",
        "Royal Heraldic": "Regal heraldic crest style, traditional emblem, authoritative, intricate details, classic royal aesthetic",
        "Futuristic Sleek": "Futuristic design, sleek curves, high-tech feel, subtle gradients, dynamic and innovative aesthetic"
    }
    
    selected_style = style_descriptors.get(style_preset, "clean professional minimalist style")
    
    composition_prompt = ""
    if composition == "Icon + Text":
        composition_prompt = f"combining a unique icon with the text '{brand_name}'"
    elif composition == "Icon Only":
        composition_prompt = "a standalone symbolic icon without any text"
    elif composition == "Typography Only":
        composition_prompt = f"focusing purely on exquisite custom typography for the name '{brand_name}'"

    prompt = (
        f"A professional high-end luxury logo for '{brand_name}' in the {industry} industry. "
        f"Style: {selected_style}. Composition: {composition_prompt}. "
        f"Primary color: {color}. Secondary elements: {keywords}. "
        f"Vector art style, flat design, sharp edges, isolated on a pure white background, "
        f"high contrast, premium quality, 8k resolution, trending on Behance."
    )
    
    print(f"Generating logo with prompt: {prompt}")

    API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

    max_retries = 3
    retry_delay = 20 # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=60)
            
            if response.status_code == 200:
                # Check if the response is actually an image
                content_type = response.headers.get('content-type', '')
                if 'image' not in content_type:
                    print(f"HF API Error: Expected image but got {content_type} - {response.text}")
                    raise Exception("HuggingFace API did not return an image.")

                image_bytes = response.content
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                print("Logo generated successfully.")
                return base64_image
            
            elif response.status_code == 503 or "loading" in response.text.lower():
                print(f"Model is loading (attempt {attempt+1}/{max_retries}). Waiting {retry_delay}s...")
                time.sleep(retry_delay)
                continue
            
            else:
                print(f"HF API Error: {response.status_code} - {response.text}")
                raise Exception(f"HuggingFace API returned error: {response.status_code}")

        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error in generate_logo_image after {max_retries} attempts: {str(e)}")
                raise e
            print(f"Attempt {attempt+1} failed: {str(e)}. Retrying...")
            time.sleep(5)
    
    raise Exception("Model failed to load within the retry period.")
