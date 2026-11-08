# Katalyst (TokenWise Proxy)

Katalyst is a prototype of a proxy that counts the tokens of LLM requests and will convert JSON data to the TOON format.

## What it does

- The proxy gives an endpoint that has the same path as the OpenAI chat completions API.
- The proxy checks the `X-Tokenwise-Key` header of each request.
- The proxy counts the tokens of the original JSON request (`T_JSON`).
- The proxy counts the tokens of the optimized prompt (`T_ACTUAL`).
- The proxy returns a mock response with the number of saved tokens.

This version is an MVP. The proxy does not send requests to an LLM vendor. The classifier and the TOON converter are placeholders.

## Requirements

- macOS, Linux, or Windows.
- Python 3.10 or later.
- Internet access at the first start. The `tiktoken` package downloads its encoding file one time.
- You do not need an LLM API account for this version.
- Optional: PostgreSQL, if you want to make the database tables in `db_schema.sql`. The code does not use the database yet.

## Install

1. Get the code.

   ```bash
   git clone https://github.com/Ikarus0013/katalyst.git
   cd katalyst
   ```

2. Make a virtual environment.

   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment.

   ```bash
   source venv/bin/activate
   ```

4. Install the dependencies.

   ```bash
   pip install -r requirements.txt
   ```

## Configure

The code does not read environment variables. The configuration is in `tokenwise_proxy/config.py`.

| Setting | Description |
| --- | --- |
| `VALID_API_KEYS` | Maps each TokenWise key to a target URL and a vendor API key. The values in the file are test values. |
| `REPETITION_THRESHOLD` | Key repetition ratio (0 to 1) at which the classifier will select TOON. Not used yet. |
| `NESTING_DEPTH_LIMIT` | Maximum nesting depth for TOON conversion. Not used yet. |

**CAUTION:** Do not put real vendor API keys in `config.py`. A later version must get the keys from the database.

## Use

1. Start the server.

   ```bash
   uvicorn app:app --reload
   ```

2. Open a second terminal.
3. Send a test request.

   ```bash
   curl -X POST http://localhost:8000/optimize/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "X-Tokenwise-Key: optimiser_sk_xyz123" \
     -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Hello"}]}'
   ```

   Example response:

   ```json
   {"message": "Optimization Proxy Complete (MOCK)", "tokens_saved": 16, "payload_sent": "Placeholder JSON string"}
   ```

4. Run all test requests with the Python script.

   ```bash
   python test_api.py
   ```

5. Alternatively, run the test requests with the shell script.

   ```bash
   ./test_api.sh
   ```

A request with an incorrect key gets the status `401`.

The interactive API documentation is at `http://localhost:8000/docs`.

## How it works

1. FastAPI gets the request on `POST /optimize/v1/chat/completions`.
2. `api_gateway.py` finds the TokenWise key in `config.VALID_API_KEYS`.
3. `metering.py` counts the tokens of the compact JSON request with the `cl100k_base` encoding.
4. `classifier.py` decides if TOON is suitable and makes the final prompt. This step is a placeholder.
5. `metering.py` counts the tokens of the final prompt and writes the result to the console.
6. The gateway returns a mock response.

## Files

| File | Description |
| --- | --- |
| `app.py` | FastAPI application. Adds the router at the `/optimize` prefix. |
| `tokenwise_proxy/api_gateway.py` | Key check and the main route. |
| `tokenwise_proxy/metering.py` | Token count with `tiktoken`, and the usage log placeholder. |
| `tokenwise_proxy/classifier.py` | Placeholder for the JSON or TOON decision. |
| `tokenwise_proxy/converter.py` | Placeholder for TOON encoding and decoding. |
| `tokenwise_proxy/config.py` | Test keys and classifier thresholds. |
| `db_schema.sql` | PostgreSQL tables for users, API keys, and usage logs. |
| `test_api.py`, `test_api.sh` | Test requests for a server on `localhost:8000`. |
| `requirements.txt` | Python dependencies. |

## Limits

- The proxy does not send requests to OpenAI, Anthropic, or other vendors. It returns a mock response.
- The classifier always returns the same placeholder text. Thus, `tokens_saved` does not show a real saving.
- The TOON converter is a placeholder.
- The usage log goes to the console. The code does not write to the database.
- The API keys are in a Python file, not in a database.
- The token count uses one OpenAI encoding for all vendors.

## License

This project uses the MIT license. Refer to the `LICENSE` file.
