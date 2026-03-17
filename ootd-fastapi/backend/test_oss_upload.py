#!/usr/bin/env python3
"""Test script for OSS upload functionality."""
import requests
import io
from PIL import Image
import json

# API base URL
BASE_URL = "http://localhost:8000"

def create_test_image():
    """Create a simple test image."""
    # Create a simple 200x200 red image
    img = Image.new('RGB', (200, 200), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def register_and_login():
    """Register a test user and get the token."""
    # Try to login first
    login_data = {
        "username": "testoss@example.com",
        "password": "test123456"
    }

    # Try login (using form data for OAuth2)
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)

    if response.status_code == 200:
        print("✓ Login successful")
        return response.json()["access_token"]
    else:
        # Try to register
        print("Login failed, trying to register...")
        register_data = {
            "username": "test_oss_user",
            "email": "testoss@example.com",
            "password": "test123456"
        }
        reg_response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)

        if reg_response.status_code == 201 or reg_response.status_code == 200:
            print("✓ Registration successful")
            # Try login again
            response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
            if response.status_code == 200:
                print("✓ Login successful")
                return response.json()["access_token"]

    print(f"✗ Authentication failed")
    print(f"Register response: {reg_response.status_code} - {reg_response.text}")
    return None

def test_oss_upload(token):
    """Test uploading an image to OSS."""
    # Create test image
    img_bytes = create_test_image()

    # Prepare the file
    files = {
        'file': ('test_image.png', img_bytes, 'image/png')
    }

    headers = {
        'Authorization': f'Bearer {token}'
    }

    print("\n" + "="*50)
    print("Testing OSS Upload...")
    print("="*50)

    # Test upload
    response = requests.post(
        f"{BASE_URL}/api/upload/image",
        files=files,
        headers=headers
    )

    print(f"\nStatus Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print("✓ Upload successful!")
        print(f"  URL: {result['url']}")
        print(f"  Size: {result['size']} bytes")
        print(f"  Type: {result['type']}")

        # Verify the URL is accessible
        try:
            verify_response = requests.head(result['url'], timeout=5)
            if verify_response.status_code == 200:
                print("✓ Image is publicly accessible")
            else:
                print(f"✗ Image verification failed: {verify_response.status_code}")
        except Exception as e:
            print(f"✗ Could not verify image accessibility: {e}")

        return result['url']
    else:
        print("✗ Upload failed!")
        print(f"  Error: {response.text}")
        return None

def test_oss_config():
    """Test OSS configuration by checking the service."""
    print("\n" + "="*50)
    print("Checking OSS Configuration...")
    print("="*50)

    from app.services.oss_service import oss_service, OSS2_AVAILABLE

    if not OSS2_AVAILABLE:
        print("✗ oss2 module is not installed")
        print("  Install with: pip install oss2")
        return False

    if oss_service is None:
        print("✗ OSS service is not initialized")
        print("  Check your .env configuration:")
        print("  - OSS_ACCESS_KEY_ID")
        print("  - OSS_ACCESS_KEY_SECRET")
        print("  - OSS_BUCKET")
        print("  - OSS_REGION")
        return False

    print("✓ oss2 module is installed")
    print("✓ OSS service is initialized")
    print(f"  Bucket: {oss_service.bucket_name}")
    print(f"  Region: {oss_service.region}")

    return True

if __name__ == "__main__":
    import sys
    import os

    # Add backend to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    print("\n" + "="*50)
    print("OSS Upload Test")
    print("="*50)

    # First test OSS configuration
    if not test_oss_config():
        print("\n✗ OSS configuration check failed. Exiting.")
        sys.exit(1)

    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        print("✓ Server is running")
    except requests.exceptions.RequestException:
        print("✗ Server is not running. Please start the server first:")
        print("  cd backend && python -m uvicorn main:app --reload")
        sys.exit(1)

    # Get auth token
    token = register_and_login()
    if not token:
        print("\n✗ Could not authenticate. Exiting.")
        sys.exit(1)

    # Test upload
    url = test_oss_upload(token)

    if url:
        print("\n" + "="*50)
        print("✓ All tests passed!")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("✗ Upload test failed")
        print("="*50)
        sys.exit(1)
