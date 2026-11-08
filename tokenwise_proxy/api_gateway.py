import json
from fastapi import APIRouter, Header, HTTPException, Depends, Request
from typing import Dict, Any
from . import config, metering, classifier  # Import local modules
import requests  # For forwarding the request

router = APIRouter()

# --- Authorization Dependency (WP 4.0 Step 2) ---
def get_client_credentials(x_tokenwise_key: str = Header(default=None, alias="X-Tokenwise-Key")) -> Dict[str, str]:
    """Validates the TokenWise Key and returns the client's LLM credentials."""
    if not x_tokenwise_key or x_tokenwise_key not in config.VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid X-Tokenwise-Key")
    return config.VALID_API_KEYS[x_tokenwise_key]


# --- Main Optimization Route (WP 4.0 Step 1) ---
@router.post("/v1/chat/completions")
async def optimize_chat_completions(
    request: Request,
    credentials: Dict[str, str] = Depends(get_client_credentials)
):
    client_payload = await request.json()
    optimisation_key_id = [k for k, v in config.VALID_API_KEYS.items() if v == credentials][0]  # Simple key ID lookup

    # --- Token Metering Step 1 (WP 6.0) ---
    t_json = metering.calculate_t_json(client_payload)
    print(f"[GATEWAY] Baseline T_JSON: {t_json}")

    # --- Classifier and Conversion Step (WP 5.0) ---
    # The classifier needs the original payload to analyze it
    final_prompt_string, conversion_applied = classifier.classify_and_optimize(client_payload)

    # --- Token Metering Step 2 (WP 6.0) ---
    t_actual = metering.calculate_t_actual(final_prompt_string)

    # --- Token Metering Step 3 (WP 6.0) ---
    await metering.log_usage_to_db({
        'T_JSON': t_json,
        'T_ACTUAL': t_actual,
        'optimisation_key_id': optimisation_key_id,
        'conversion_applied': conversion_applied
    })

    # --- Forwarding Logic Stub (WP 4.0 Step 4) ---
    # In the real app, we would craft the final request with final_prompt_string
    # and forward it. For now, we return a mock response.
    mock_response_data = {
        "message": "Optimization Proxy Complete (MOCK)",
        "tokens_saved": t_json - t_actual,
        "payload_sent": final_prompt_string
    }
    return mock_response_data

