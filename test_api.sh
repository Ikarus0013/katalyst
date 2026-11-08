#!/bin/bash

# Test script for TokenWise API
# Make sure the server is running: uvicorn app:app --reload

echo "Testing TokenWise API..."
echo ""

# Test 1: Root endpoint
echo "1. Testing root endpoint (GET /):"
curl -X GET http://localhost:8000/
echo -e "\n\n"

# Test 2: Chat completions endpoint with valid key
echo "2. Testing chat completions endpoint (POST /optimize/v1/chat/completions):"
curl -X POST http://localhost:8000/optimize/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-Tokenwise-Key: optimiser_sk_xyz123" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7
  }'
echo -e "\n\n"

# Test 3: Test with invalid key (should return 401)
echo "3. Testing with invalid key (should fail):"
curl -X POST http://localhost:8000/optimize/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-Tokenwise-Key: invalid_key" \
  -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "test"}]}'
echo -e "\n\n"

echo "Testing complete!"


