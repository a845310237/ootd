#!/usr/bin/env python3
"""Test MiniMax API connection."""
import httpx
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_minimax_api():
    """Test MiniMax Image Generation API."""
    api_key = os.getenv("MINIMAX_API_KEY")
    print(f"API Key configured: {bool(api_key)}")
    if api_key:
        print(f"API Key (first 20 chars): {api_key[:20]}...")

    if not api_key:
        print("ERROR: MINIMAX_API_KEY not found in environment")
        return False

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "image-01",
        "prompt": "A simple test image of a red t-shirt",
        "aspect_ratio": "16:9",
        "response_format": "url",
        "n": 1,
        "prompt_optimizer": True
    }

    print("\nTesting MiniMax API...")
    print(f"Endpoint: https://api.minimaxi.com/v1/image_generation")
    print(f"Payload: {payload}")

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.minimaxi.com/v1/image_generation",
                headers=headers,
                json=payload
            )

            print(f"\nResponse Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")

            if response.status_code == 200:
                data = response.json()
                print(f"Response Data: {data}")
                if data.get("data"):
                    # Handle different response formats
                    if "image_urls" in data["data"]:
                        if len(data["data"]["image_urls"]) > 0:
                            print(f"✓ SUCCESS! Image URL: {data['data']['image_urls'][0]}")
                            return True
                    elif len(data["data"]) > 0:
                        print(f"✓ SUCCESS! Image URL: {data['data'][0].get('url')}")
                        return True
                print("✗ FAILED: No image data in response")
                return False
            else:
                print(f"✗ FAILED: {response.text}")
                return False

    except Exception as e:
        print(f"✗ EXCEPTION: {str(e)}")
        return False

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(test_minimax_api())
    exit(0 if result else 1)
