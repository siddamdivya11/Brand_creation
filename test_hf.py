import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_hf():
    api_key = os.getenv("HF_API_KEY")
    print(f"Testing with API Key: {api_key[:5]}...{api_key[-5:]}")
    
    # Try multiple models to see which one is active for this key
    models = [
        "stabilityai/stable-diffusion-xl-base-1.0",
        "runwayml/stable-diffusion-v1-5",
        "black-forest-labs/FLUX.1-schnell"
    ]
    
    for model in models:
        print(f"\n--- Testing Model: {model} ---")
        API_URL = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {"inputs": "A simple red circle on a white background, minimalist logo"}
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"Success with {model}!")
                return model
            else:
                print(f"Failure with {model}: {response.text}")
        except Exception as e:
            print(f"Error with {model}: {e}")
    
    return None

if __name__ == "__main__":
    test_hf()
