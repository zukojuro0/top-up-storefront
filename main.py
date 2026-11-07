from fastapi import FastAPI
import os

app = FastAPI()

# Get secret keys securely from Render environment variables
GAMESDROP_API_KEY = os.getenv("GAMESDROP_API_KEY")

@app.get("/")
def read_root():
    return {"status": "WildCore API is running live!"}

@app.post("/api/create-order")
def create_order(player_id: str, zone_id: str, product_code: str):
    print(f"Received order for {player_id}, Zone: {zone_id}, Product: {product_code}")
    return {
        "success": True,
        "message": f"Order processing for Player {player_id} initiated."
    }