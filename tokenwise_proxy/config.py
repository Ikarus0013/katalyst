# Placeholder for sensitive data - MUST be replaced with database lookup (WP 7.0)
# Maps Optimisation Key to (Target URL, Client's LLM API Key)
VALID_API_KEYS = {
    "optimiser_sk_xyz123": {
        "target_url": "https://api.openai.com/v1/chat/completions",
        "client_vendor_key": "sk-client-openai-testkey"
    },
    "optimiser_sk_abc456": {
        "target_url": "https://api.anthropic.com/v1/messages",
        "client_vendor_key": "sk-client-anthropic-testkey"
    }
}

# Classifier Threshold (WP 5.0)
REPETITION_THRESHOLD = 0.80  # 80% key repetition = suitable for TOON
NESTING_DEPTH_LIMIT = 3  # Max nesting allowed for TOON optimization

