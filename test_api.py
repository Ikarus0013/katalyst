#!/usr/bin/env python3
"""
Test script for TokenWise API
Run this while the server is running: uvicorn app:app --reload
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test the root endpoint"""
    print("1. Testing root endpoint (GET /):")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_chat_completions_valid():
    """Test chat completions with valid API key"""
    print("2. Testing chat completions with valid key:")
    url = f"{BASE_URL}/optimize/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "X-Tokenwise-Key": "optimiser_sk_xyz123"
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_chat_completions_invalid():
    """Test chat completions with invalid API key"""
    print("3. Testing chat completions with invalid key (should fail):")
    url = f"{BASE_URL}/optimize/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "X-Tokenwise-Key": "invalid_key"
    }
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "test"}]
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

if __name__ == "__main__":
    print("=" * 50)
    print("TokenWise API Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_root()
        test_chat_completions_valid()
        test_chat_completions_invalid()
        print("=" * 50)
        print("All tests completed!")
        print("=" * 50)
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server.")
        print("Make sure the server is running: uvicorn app:app --reload")
    except Exception as e:
        print(f"ERROR: {e}")


