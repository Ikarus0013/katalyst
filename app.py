from fastapi import FastAPI
from tokenwise_proxy import api_gateway

app = FastAPI(title="TokenWise Optimization Proxy MVP")

# Include the main routing logic
app.include_router(api_gateway.router, prefix="/optimize")


@app.get("/")
def root():
    return {"status": "TokenWise Proxy is running. Use /optimize/v1/chat/completions"}

