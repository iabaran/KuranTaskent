#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vision API Test - API Key ile
"""

import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')

print(f"API Key: {api_key[:20]}...")

# Test Vision API erişimi
url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"

# Basit test isteği
test_request = {
    "requests": [{
        "image": {
            "content": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        },
        "features": [{"type": "TEXT_DETECTION"}]
    }]
}

print("\nVision API test ediliyor...")
response = requests.post(url, json=test_request)

print(f"Status Code: {response.status_code}")
print(f"\nResponse:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
