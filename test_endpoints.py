import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_endpoint(name, url, data):
    print(f"\n--- Testing {name} ---")
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"✅ SUCCESS")
            print(f"Response: {json.dumps(response.json(), indent=2)[:200]}...") # Truncate for readability
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")

# 1. Generate Brand
test_endpoint(
    "Brand Generator",
    f"{BASE_URL}/generate-brand",
    {"industry": "Luxury Watches", "keywords": "Timeless, Gold", "tone": "Sophisticated"}
)

# 2. Generate Content
test_endpoint(
    "Content Generator",
    f"{BASE_URL}/generate-content",
    {"description": "A new gold watch release", "tone": "Persuasive", "content_type": "Social Media Caption"}
)

# 3. Analyze Sentiment
test_endpoint(
    "Sentiment Analysis",
    f"{BASE_URL}/analyze-sentiment",
    {"text": "I absolutely love this amazing product!"}
)

# 4. Chat
test_endpoint(
    "Chatbot",
    f"{BASE_URL}/chat",
    {"message": "Hello, who are you?"}
)

# 5. Generate Logo
test_endpoint(
    "Logo Generator",
    f"{BASE_URL}/generate-logo",
    {"brand_name": "LuxTime", "industry": "Watches", "keywords": "Minimalist, Crown"}
)
